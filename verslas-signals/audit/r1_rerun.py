"""AUDIT-2026-08 R1 mechanical rerun of EXP-007 (LOCAL — needs bar data).

Reruns HYP-006 under the audited fixes and re-evaluates the SEVEN
UNCHANGED pre-registered checks (NOTES-SPRINT-E.md):

- Finding 1 fix: "reached +XR" counts the bar's high (intrabar), matching
  the resting partial's own fill basis.
- Finding 2 fix: spot cash floor (no leverage) + costs.yaml small-order
  bound, both as counted skips.
- F1 fix: the random baseline is random-entry / SAME-EXIT — random entries
  get the full exit stack (2xATR stop, 1/3 partial at 3R, 10-day-low trail
  after +1R intrabar, 15-bar time stop unless +1R reached, BTC regime
  flatten, RS top-half signal exit), per-trade, same costs. p uses the
  exact (r+1)/(N+1) estimator; the entry pool has no end-truncation
  (F2 fix) and the strategy's return convention (F4 fix).

Pre-declared interpretation choices (fixed before running):
- Baseline entries carry NO alpha filters (RS rank, breakout, volume,
  extension, BTC entry gate) — those are the strategy under test. Same as
  the original baseline's declared spec.
- A random trade still open at the window end is discarded and redrawn
  (both sides count completed trades only).

Writes research/experiments/EXP-007-AUDIT-R1.md (+ .trades.csv). The
original EXP-007.md is history and is NOT touched.

    python -m audit.r1_rerun                     (from verslas-signals/)
Optional (record-only EXP-005 variant on the historical 30-pair universe):
    git show 99e5f91:verslas-signals/data/universe.csv > data/universe-exp005.csv
    python -m audit.r1_rerun --universe data/universe-exp005.csv --tag EXP-005
"""
import argparse
import csv as _csv
import random
from pathlib import Path

from engine.costs import CostModel
from engine.hyp004 import PARAMS, config_hash
from engine.metrics import summarize
from engine.protocol import HOLDOUT_START_MS, RESEARCH_START_MS
from engine.sprint_d import run_sim
from engine.sprint_e import concentration, MIN_TRADES, MAX_TOP_PAIR_SHARE
from engine.experiment import (load_daily_dir, load_universe, btc_context,
                               dataset_ids, day)

SEED = 20260901
COMMITTED = Path(__file__).resolve().parents[2] / "research/experiments/EXP-007.trades.csv"


def btc_bearish_at(btc, ts):
    i = btc["ts_index"].get(ts)
    if i is None:
        return False
    s50 = btc["sma50"][i]
    return s50 is not None and btc["close"][i] < s50


def walk_random_trade(d, sig_i, pair, stop0, strat, btc, cost, policy_p):
    """One random entry through the same exit stack (fixed semantics).
    Returns net pct return (strategy convention) or None (discard/redraw)."""
    n = len(d["ts"])
    f = sig_i + 1
    if f >= n or d["volume"][f] <= 0:
        return None                       # entry cancelled (zero-volume/end)
    entry = d["open"][f]
    if entry <= stop0:
        return None                       # gapped through the stop: no trade
    risk_px = entry - stop0
    target = entry + policy_p["partial_r"] * risk_px
    units = 1.0                           # pct is size-invariant
    cash = -units * entry * (1.0 + cost)
    remaining = units
    stop = stop0
    half_taken = False
    max_r = 0.0
    bars_held = 0
    exit_pending = False
    lb = policy_p["trail_lookback"]
    j = f
    while j < n:
        ts = d["ts"][j]
        tradable = d["volume"][j] > 0
        if exit_pending and tradable:     # pending exits fill at the open
            cash += remaining * d["open"][j] * (1.0 - cost)
            return cash / (units * entry)
        if tradable:                      # intrabar: stop first, then partial
            if d["open"][j] <= stop:
                cash += remaining * d["open"][j] * (1.0 - cost)
                return cash / (units * entry)
            if d["low"][j] <= stop:
                cash += remaining * stop * (1.0 - cost)
                return cash / (units * entry)
            if not half_taken and policy_p["partial_frac"] > 0 \
                    and d["high"][j] >= target:
                qty = units * policy_p["partial_frac"]
                cash += qty * target * (1.0 - cost)
                remaining -= qty
                half_taken = True
        # close management (runs on zero-volume bars too, like the engine)
        bars_held += 1
        max_r = max(max_r, (d["high"][j] - entry) / risk_px)
        if max_r >= policy_p["trail_after_r"] and j >= lb:
            stop = max(stop, min(d["low"][j - lb + 1:j + 1]))
        if bars_held >= policy_p["time_stop_bars"] \
                and max_r < policy_p["time_stop_skip_if_r"]:
            exit_pending = True
        elif btc_bearish_at(btc, ts):
            exit_pending = True
        elif (ts, pair) not in strat.top_half:
            exit_pending = True           # same RS signal exit as the strategy
        j += 1
    return None                           # window ended with the trade open


def same_exit_baseline(data, universe, strat, btc, cost_fn, n_trades, sims, rng):
    atr_mult = PARAMS["atr_mult"]
    guard = PARAMS["max_stop_frac"]
    pol = {"partial_frac": 1.0 / 3.0, "partial_r": 3.0, "trail_lookback": 10,
           "trail_after_r": 1.0, "time_stop_bars": 15, "time_stop_skip_if_r": 1.0}
    pool = []
    for pair, d in data.items():
        a = strat.ind[pair]["atr"]
        for i in range(len(d["ts"]) - 1):
            if (d["ts"][i], pair) not in universe or a[i] is None:
                continue
            close = d["close"][i]
            stop = close - atr_mult * a[i]
            if stop <= 0 or (close - stop) / close > guard:
                continue
            pool.append((pair, i, stop))
    means = []
    for s in range(sims):
        got, total = 0, 0.0
        while got < n_trades:
            pair, i, stop = pool[rng.randrange(len(pool))]
            pct = walk_random_trade(data[pair], i, pair, stop, strat, btc,
                                    cost_fn(pair), pol)
            if pct is None:
                continue
            total += pct
            got += 1
        means.append(total / n_trades)
        if (s + 1) % 200 == 0:
            print(f"    {s + 1}/{sims} sims")
    return means


def trade_key(t):
    return (t["pair"], day(t["entry_ts"]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="data/derived/okx/1d")
    ap.add_argument("--universe", default="data/universe.csv")
    ap.add_argument("--costs", default="costs.yaml")
    ap.add_argument("--sims", type=int, default=2000)
    ap.add_argument("--tag", default="EXP-007")
    args = ap.parse_args(argv)
    out = Path(f"../research/experiments/{args.tag}-AUDIT-R1.md")

    data = load_daily_dir(Path(args.data), HOLDOUT_START_MS)  # holdout sealed
    universe = load_universe(Path(args.universe))
    btc = btc_context(data)
    cost_model = CostModel.from_yaml(args.costs)

    print(f"{args.tag}-AUDIT-R1 on {len(data)} pairs · frozen config "
          f"{config_hash()} (must equal 0e4dc9e0453a)")
    print("primary run (fixed engine) ...")
    sim = run_sim(data, universe, btc, cost_model)
    m = summarize(sim.trades, sim.equity_curve)
    print(f"  trades {m['trades']} | expectancy {m['expectancy_r']:+.3f} R | "
          f"PF {m['profit_factor']:.2f} | maxDD {m['max_drawdown']:.1%} | "
          f"skips {sim.skips}")
    print("2x cost stress ...")
    s_sim = run_sim(data, universe, btc, cost_model, stress=True)
    m_s = summarize(s_sim.trades, s_sim.equity_curve)

    # trade diff vs the committed EXP-007 record
    diff_note = ""
    if args.tag == "EXP-007" and COMMITTED.exists():
        old = {(t["pair"], t["entry"]) for t in _csv.DictReader(COMMITTED.open())}
        new = {trade_key(t) for t in sim.trades}
        diff_note = (f"Trade-set diff vs committed EXP-007: "
                     f"{len(new & old)} shared, {len(new - old)} added, "
                     f"{len(old - new)} removed")
        print(diff_note)

    print(f"same-exit baseline ({args.sims} sims, seed {SEED}) ...")
    def cost_fn(pair):
        return cost_model.one_way_fraction("okx", pair.replace("-", "/"))
    rng = random.Random(SEED)
    means = same_exit_baseline(data, universe, sim.strategy, btc, cost_fn,
                               max(1, len(sim.trades)), args.sims, rng)
    strat_mean = (sum(t["pct"] for t in sim.trades) / len(sim.trades)
                  if sim.trades else 0.0)
    ge = sum(1 for x in means if x >= strat_mean)
    p_val = (ge + 1) / (len(means) + 1)
    base_mean = sum(means) / len(means)

    top_pair, share, ex_exp = concentration(sim.trades)
    folds_pos = sum(1 for f in m["folds"].values() if f["expectancy_r"] > 0)
    checks = {
        f"trades >= {MIN_TRADES}": m["trades"] >= MIN_TRADES,
        "expectancy > 0": m["expectancy_r"] > 0,
        "folds positive >= 4/7": folds_pos >= 4,
        "stress PF >= 1.1": m_s["profit_factor"] >= 1.1,
        f"random baseline p < 0.05 ({args.sims} sims, same-exit)": p_val < 0.05,
        f"top-pair profit share < {MAX_TOP_PAIR_SHARE:.0%}":
            share is not None and share < MAX_TOP_PAIR_SHARE,
        "ex-top-pair expectancy > 0": ex_exp is not None and ex_exp > 0,
    }
    verdict = ("PASSED under the R1 rerun — per protocol R6 the hypothesis "
               "re-enters at the full G0 battery"
               if all(checks.values())
               else "STILL FAILED under the R1 rerun — the EXP-007 conclusion "
                    "stands (protocol R6)")

    ex21 = [t for t in sim.trades if day(t["entry_ts"])[:4] != "2021"]
    ex21_e = sum(t["r"] for t in ex21) / len(ex21) if ex21 else 0.0

    lines = [
        f"# {args.tag}-AUDIT-R1 — mechanical rerun under the audited fixes",
        "",
        "Per AUDIT-2026-08-PROTOCOL R1: fixes applied (Finding 1 intrabar "
        "max_r; Finding 2 cash floor + size bound; F1-F4 same-exit "
        "baseline), thresholds UNCHANGED. The original report is untouched "
        "history.",
        "",
        f"Window {day(RESEARCH_START_MS)} .. {day(HOLDOUT_START_MS)} (excl.) "
        f"· holdout SEALED · pairs {len(data)} · config `{config_hash()}` · "
        f"datasets {dataset_ids(Path(args.data))}",
        "",
        f"- Trades: **{m['trades']}** · expectancy **{m['expectancy_r']:+.3f} R** "
        f"(CI80 {m['expectancy_ci80'][0]:+.3f} … {m['expectancy_ci80'][1]:+.3f})",
        f"- PF **{m['profit_factor']:.2f}** · win rate {m['win_rate']:.1%} · "
        f"maxDD {m['max_drawdown']:.1%}",
        f"- Skips: `{sim.skips}` (cash/size_bound are the Finding 2 guards)",
        f"- Stress: {m_s['trades']} trades, {m_s['expectancy_r']:+.3f} R, "
        f"PF {m_s['profit_factor']:.2f}",
        f"- Same-exit baseline: mean of sim-means {base_mean:+.4%} vs strategy "
        f"{strat_mean:+.4%} → **p = {p_val:.4f}** ((r+1)/(N+1), seed {SEED})",
        ("- Concentration: top **%s** at %s · ex-top %s" % (
            top_pair,
            f"{share:.1%}" if share is not None else "n/a (net loss)",
            f"{ex_exp:+.3f} R" if ex_exp is not None else "n/a")
         if top_pair is not None else "- Concentration: n/a"),
        f"- Diagnostic (Finding 3, narrative only): ex-2021 trades "
        f"{len(ex21)}, expectancy {ex21_e:+.3f} R",
    ]
    if diff_note:
        lines.append(f"- {diff_note}")
    lines += ["", "## Folds", "", "| fold | trades | expectancy (R) |",
              "|---|---|---|"]
    for name, f in m["folds"].items():
        lines.append(f"| {name} | {f['trades']} | {f['expectancy_r']:+.3f} |")
    lines += [f"\nPositive folds: **{folds_pos}/7**", "",
              "## The seven checks (thresholds unchanged)", ""]
    for check, ok in checks.items():
        lines.append(f"- {'PASS' if ok else 'FAIL'}: {check}")
    lines += ["", f"**Verdict: {verdict}**", "",
              "*Generated by audit/r1_rerun.py. No holdout data was "
              "accessible.*"]
    out.write_text("\n".join(lines), encoding="utf-8")
    with out.with_suffix(".trades.csv").open("w", newline="",
                                             encoding="utf-8") as fh:
        w = _csv.writer(fh)
        w.writerow(["pair", "entry", "exit", "r", "pct", "bars_held",
                    "regime", "fold", "exit_reason"])
        for t in sorted(sim.trades, key=lambda t: t["entry_ts"]):
            w.writerow([t["pair"], day(t["entry_ts"]), day(t["exit_ts"]),
                        f"{t['r']:.3f}", f"{t['pct']:.4f}", t["bars_held"],
                        t["regime"], t["fold"], t["exit_reason"]])
    print(f"\nreport -> {out}")
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
