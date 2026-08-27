"""EXP-007: HYP-006 — the frozen HYP-004 config on the widened universe.

Usage (from verslas-signals/, AFTER re-running the data pipeline on the
widened pairs.yaml):
    python run.py                                     # downloads new pairs
    python -m engine.data.derive data/raw/okx/1h data/derived/okx
    python -m engine.data.manifest data/derived --config pairs.yaml
    python -m engine.universe data/derived/okx/1d --out data/universe.csv
    python -m engine.sprint_e

Per NOTES-SPRINT-E.md: seven pre-registered checks, 2,000-sim baseline,
concentration criteria. If this fails, signal research ends (D-022).
"""
import argparse
import csv as _csv
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from .costs import CostModel
from .hyp004 import config_hash
from .metrics import summarize
from .protocol import HOLDOUT_START_MS, RESEARCH_START_MS
from .exp003 import exit_reason_stats
from .sprint_d import run_sim
from .experiment import (load_daily_dir, load_universe, btc_context,
                         dataset_ids, day, btc_buy_hold, random_baseline)

MIN_TRADES = 30
BASELINE_SIMS = 2000
MAX_TOP_PAIR_SHARE = 0.50


def concentration(trades):
    """(top_pair, top_share_of_total_R, ex_top_expectancy)."""
    if not trades:
        return None, None, None
    by_pair = defaultdict(float)
    for t in trades:
        by_pair[t["pair"]] += t["r"]
    total = sum(by_pair.values())
    top_pair, top_r = max(by_pair.items(), key=lambda kv: kv[1])
    share = (top_r / total) if total > 0 else None
    ex = [t["r"] for t in trades if t["pair"] != top_pair]
    ex_exp = sum(ex) / len(ex) if ex else None
    return top_pair, share, ex_exp


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="data/derived/okx/1d")
    ap.add_argument("--universe", default="data/universe.csv")
    ap.add_argument("--costs", default="costs.yaml")
    ap.add_argument("--out", default="../research/experiments/EXP-007.md")
    args = ap.parse_args(argv)

    data = load_daily_dir(Path(args.data), HOLDOUT_START_MS)  # holdout sealed
    universe = load_universe(Path(args.universe))
    btc = btc_context(data)
    cost_model = CostModel.from_yaml(args.costs)

    print(f"EXP-007 on {len(data)} pairs · frozen config {config_hash()} "
          "(must equal EXP-005's 0e4dc9e0453a)")
    print("primary run (resting stop) ...")
    sim = run_sim(data, universe, btc, cost_model)
    m = summarize(sim.trades, sim.equity_curve)
    print(f"  trades {m['trades']} | expectancy {m['expectancy_r']:+.3f} R | "
          f"PF {m['profit_factor']:.2f} | maxDD {m['max_drawdown']:.1%}")
    print("2x cost stress ...")
    m_s = summarize(*(lambda s: (s.trades, s.equity_curve))(
        run_sim(data, universe, btc, cost_model, stress=True)))
    print("close-confirm sensitivity ...")
    m_c = summarize(*(lambda s: (s.trades, s.equity_curve))(
        run_sim(data, universe, btc, cost_model, stop_mode="close_confirm")))
    print(f"random-entry baseline ({BASELINE_SIMS} sims, be patient) ...")
    rb = random_baseline(data, universe, cost_model, sim.trades,
                         sims=BASELINE_SIMS)
    bh = btc_buy_hold(data)
    strat_mean_pct = (sum(t["pct"] for t in sim.trades) / len(sim.trades)
                      if sim.trades else 0.0)
    p_val = (sum(1 for x in rb["dist"] if x >= strat_mean_pct) / len(rb["dist"])
             if rb else 1.0)

    top_pair, share, ex_exp = concentration(sim.trades)
    folds_pos = sum(1 for f in m["folds"].values() if f["expectancy_r"] > 0)
    checks = {
        f"trades >= {MIN_TRADES}": m["trades"] >= MIN_TRADES,
        "expectancy > 0": m["expectancy_r"] > 0,
        "folds positive >= 4/7": folds_pos >= 4,
        "stress PF >= 1.1": m_s["profit_factor"] >= 1.1,
        f"random baseline p < 0.05 ({BASELINE_SIMS} sims)": p_val < 0.05,
        f"top-pair profit share < {MAX_TOP_PAIR_SHARE:.0%}":
            share is not None and share < MAX_TOP_PAIR_SHARE,
        "ex-top-pair expectancy > 0": ex_exp is not None and ex_exp > 0,
    }
    verdict = ("PROCEED — HYP-006 advances to the full G0 battery"
               if all(checks.values())
               else "FAILED — signal research ends; the CHARTER §9 pivot "
                    "discussion is mandatory (D-022)")

    er = exit_reason_stats(sim.trades)
    per_year = {}
    for t in sim.trades:
        y = day(t["entry_ts"])[:4]
        per_year[y] = per_year.get(y, 0) + 1
    funnel = dict(sorted(sim.strategy.funnel.items(), key=lambda kv: -kv[1])[:40])

    run_date = day(int(datetime.now(timezone.utc).timestamp() * 1000))
    lines = [
        "# EXP-007 — HYP-006: frozen HYP-004 on the widened universe "
        "(Sprint E, the final round)",
        "",
        f"Run: {run_date} · window {day(RESEARCH_START_MS)} .. "
        f"{day(HOLDOUT_START_MS)} (excl.) · holdout SEALED",
        f"Pairs loaded: {len(data)} · Datasets: {dataset_ids(Path(args.data))} "
        f"· config `{config_hash()}` (frozen; EXP-005 parity required)",
        "Pre-registration: NOTES-SPRINT-E.md · HYP-004 lineage variants: 3",
        "",
        "## Primary run (net of costs)",
        "",
        f"- Trades: **{m['trades']}**",
        f"- Expectancy: **{m['expectancy_r']:+.3f} R** "
        f"(CI80 {m['expectancy_ci80'][0]:+.3f} … {m['expectancy_ci80'][1]:+.3f})",
        f"- Profit factor: **{m['profit_factor']:.2f}** "
        f"(CI80 {m['pf_ci80'][0]:.2f} … {m['pf_ci80'][1]:.2f})",
        f"- Win rate {m['win_rate']:.1%} · avg win {m['avg_win_r']:+.2f} R · "
        f"avg loss {m['avg_loss_r']:+.2f} R",
        f"- Max drawdown {m['max_drawdown']:.1%}",
        f"- Concentration: top pair **{top_pair}** at "
        f"{share:.1%} of profit · ex-top expectancy {ex_exp:+.3f} R"
        if share is not None else "- Concentration: n/a",
        "",
        "## Folds", "",
        "| fold | trades | expectancy (R) |", "|---|---|---|",
    ]
    for name, f in m["folds"].items():
        lines.append(f"| {name} | {f['trades']} | {f['expectancy_r']:+.3f} |")
    lines += [f"\nPositive folds: **{folds_pos}/7**", "",
              "## Regimes", "",
              "| regime | trades | expectancy (R) |", "|---|---|---|"]
    for name, f in m["regimes"].items():
        lines.append(f"| {name} | {f['trades']} | {f['expectancy_r']:+.3f} |")
    lines += [
        "",
        "## Stress and sensitivity", "",
        f"- 2x cost stress: {m_s['trades']} trades, "
        f"{m_s['expectancy_r']:+.3f} R, PF {m_s['profit_factor']:.2f}",
        f"- Close-confirm execution: {m_c['trades']} trades, "
        f"{m_c['expectancy_r']:+.3f} R, PF {m_c['profit_factor']:.2f}",
        "",
        "## Baselines", "",
        f"- BTC buy-and-hold: {bh['return']:+.1%}, maxDD {bh['max_drawdown']:.1%}",
        f"- Strategy mean per-trade net return: {strat_mean_pct:+.3%}",
    ]
    if rb:
        lines.append(f"- Random-entry baseline ({BASELINE_SIMS} sims): mean "
                     f"{rb['mean_of_means']:+.3%}, p95 {rb['p95']:+.3%} · "
                     f"**p-value {p_val:.4f}**")
    lines += ["", "## Exit reasons", "",
              "| reason | trades | mean R |", "|---|---|---|"]
    for reason, (n, mean_r) in sorted(er.items()):
        lines.append(f"| {reason} | {n} | {mean_r:+.3f} |")
    lines += ["", "## Trades per year", "", "| year | trades |", "|---|---|"]
    for y, n in sorted(per_year.items()):
        lines.append(f"| {y} | {n} |")
    lines += ["", "## Signal funnel", "", "```"]
    for key, n in sorted(funnel.items()):
        lines.append(f"{key:>24}: {n}")
    lines += ["```", "", f"`skips: {sim.skips}`", "",
              "## Decision rule (pre-registered, seven checks) — evaluated", ""]
    for check, ok in checks.items():
        lines.append(f"- {'PASS' if ok else 'FAIL'}: {check}")
    lines += ["", f"**Verdict: {verdict}**", "",
              "*Generated by engine/sprint_e.py. No holdout data was accessible.*"]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    with out.with_suffix(".trades.csv").open("w", newline="",
                                             encoding="utf-8") as f:
        w = _csv.writer(f)
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
