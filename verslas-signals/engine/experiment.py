"""EXP-001 runner: HYP-001 on the canonical derived daily bars.

Usage (from verslas-signals/, after `make derive` and `make universe`):
    python3 -m engine.experiment

Runs the full research-window backtest (2021-01-01 .. 2025-06-30 per D-020),
plus the 2x cost-stress rerun, the BTC buy-and-hold baseline and the
random-entry Monte-Carlo baseline, and writes the experiment report to
../research/experiments/EXP-001.md.

THE HOLDOUT IS SEALED: bars on/after 2025-07-01 are refused at load time
unless --unlock-holdout is given the exact phrase from engine/protocol.py —
which per D-020 happens exactly once, after all research is final.
"""
import argparse
import csv
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from .costs import CostModel
from .hyp001 import Hyp001, PARAMS, config_hash
from .indicators import sma
from .metrics import summarize
from .protocol import (HOLDOUT_START_MS, HOLDOUT_UNLOCK_PHRASE,
                       RESEARCH_START_MS, FOLDS_REQUIRED_POSITIVE)
from .simulator import ExitPolicy, Simulator


def day(ts):
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def load_daily_dir(dir_path: Path, max_ts: int):
    data = {}
    for p in sorted(dir_path.glob("*.csv")):
        cols = {"ts": [], "open": [], "high": [], "low": [], "close": [],
                "volume": []}
        with p.open() as f:
            for r in csv.reader(f):
                if not r or r[0] == "timestamp":
                    continue
                ts = int(r[0])
                if ts >= max_ts:
                    continue
                cols["ts"].append(ts)
                for k, v in zip(("open", "high", "low", "close", "volume"), r[1:6]):
                    cols[k].append(float(v))
        if cols["ts"]:
            data[p.stem] = cols
    return data


def load_universe(path: Path):
    members = set()
    with path.open() as f:
        for row in csv.DictReader(f):
            if row["in_universe"] == "1":
                dt = datetime.strptime(row["date"], "%Y-%m-%d").replace(
                    tzinfo=timezone.utc)
                members.add((int(dt.timestamp() * 1000), row["symbol"]))
    return members


def btc_context(data):
    d = data["BTC-USDT"]
    return {"ts_index": {ts: i for i, ts in enumerate(d["ts"])},
            "close": d["close"],
            "sma50": sma(d["close"], 50),
            "sma200": sma(d["close"], 200)}


def dataset_ids(data_dir: Path):
    ids = {}
    for m in sorted(data_dir.glob("DATASET-*.json")):
        try:
            j = json.loads(m.read_text())
            ids[j.get("root", m.stem)] = j.get("dataset_id", m.stem)
        except Exception:
            pass
    return ids


def run_sim(data, universe, btc, cost_model, stress, start_equity=10_000.0):
    def cost_fn(pair):
        return cost_model.one_way_fraction("okx", pair.replace("-", "/")) * \
            (cost_model.stress_multiplier if stress else 1.0)
    strategy = Hyp001(data, universe)
    sim = Simulator(data, universe, btc, cost_fn, strategy, ExitPolicy(),
                    start_equity=start_equity,
                    research_range=(RESEARCH_START_MS, HOLDOUT_START_MS))
    return sim.run()


def btc_buy_hold(data):
    d = data["BTC-USDT"]
    equity = [c / d["close"][0] for c in d["close"]]
    peak, mdd = 0.0, 0.0
    for e in equity:
        peak = max(peak, e)
        mdd = max(mdd, (peak - e) / peak)
    return {"return": d["close"][-1] / d["close"][0] - 1.0, "max_drawdown": mdd}


def random_baseline(data, universe, cost_model, trades, sims=500, seed=123):
    """Random-entry, cost-paying baseline with the strategy's holding periods."""
    if not trades:
        return None
    holds = [max(1, t["bars_held"]) for t in trades]
    pool = []
    for pair, d in data.items():
        for i, ts in enumerate(d["ts"]):
            if (ts, pair) in universe and i + max(holds) + 2 < len(d["ts"]) \
                    and d["volume"][i] > 0:
                pool.append((pair, i))
    if not pool:
        return None
    rng = random.Random(seed)
    means = []
    for _ in range(sims):
        total = 0.0
        n = 0
        while n < len(trades):
            pair, i = pool[rng.randrange(len(pool))]
            h = holds[rng.randrange(len(holds))]
            d = data[pair]
            if d["volume"][i + 1] <= 0 or d["volume"][i + 1 + h] <= 0:
                continue
            cost = cost_model.one_way_fraction("okx", pair.replace("-", "/"))
            entry = d["open"][i + 1] * (1 + cost)
            exit_ = d["open"][i + 1 + h] * (1 - cost)
            total += exit_ / entry - 1.0
            n += 1
        means.append(total / len(trades))
    means.sort()
    return {"mean_of_means": sum(means) / len(means),
            "p95": means[int(len(means) * 0.95)], "dist": means}


def fmt_pct(x):
    return "n/a" if x is None else f"{x:+.2%}"


def write_report(out_path: Path, ctx):
    m, ms = ctx["metrics"], ctx["metrics_stress"]
    lines = [
        "# EXP-001 — HYP-001 pullback-to-EMA20 (Sprint A)",
        "",
        f"Run: {ctx['run_date']} · research window {ctx['window']} · "
        f"holdout SEALED (opens once, per D-020)",
        f"Datasets: {ctx['datasets']} · config `{ctx['config_hash']}` · "
        f"start equity {ctx['start_equity']:,.0f}",
        "",
        "## Headline (net of costs)",
        "",
        f"- Trades: **{m['trades']}** (G0 needs ≥200)",
        f"- Expectancy: **{m['expectancy_r']:+.3f} R** "
        f"(bootstrap 80% CI {m['expectancy_ci80'][0]:+.3f} … "
        f"{m['expectancy_ci80'][1]:+.3f})",
        f"- Profit factor: **{m['profit_factor']:.2f}** "
        f"(CI80 {m['pf_ci80'][0]:.2f} … {m['pf_ci80'][1]:.2f}; "
        f"G0 needs ≥1.3 with CI lower bound >1.0)",
        f"- Win rate {m['win_rate']:.1%} · avg win {m['avg_win_r']:+.2f} R · "
        f"avg loss {m['avg_loss_r']:+.2f} R (never quote win rate alone)",
        f"- Max portfolio drawdown: {m['max_drawdown']:.1%} (limit 25%)",
        f"- Top-pair share of profit: "
        f"{fmt_pct(m['top_pair_profit_share'])}",
        f"- Final equity: {ctx['final_equity']:,.0f} "
        f"({ctx['total_return']:+.1%} over the window)",
        "",
        "## Walk-forward folds (D-020; entries bucketed by entry date)",
        "",
        "| fold | trades | expectancy (R) |",
        "|---|---|---|",
    ]
    positive = 0
    for name, f in m["folds"].items():
        positive += 1 if f["expectancy_r"] > 0 else 0
        lines.append(f"| {name} | {f['trades']} | {f['expectancy_r']:+.3f} |")
    lines += [
        f"\nPositive folds: **{positive}/7** "
        f"(G0 needs ≥{FOLDS_REQUIRED_POSITIVE})",
        "",
        "## Regimes (rule fixed a priori in engine/protocol.py)",
        "",
        "| regime | trades | expectancy (R) |",
        "|---|---|---|",
    ]
    for name, f in m["regimes"].items():
        lines.append(f"| {name} | {f['trades']} | {f['expectancy_r']:+.3f} |")
    lines += [
        "",
        "## 2x cost stress (protocol step 4)",
        "",
        f"- Trades {ms['trades']} · expectancy {ms['expectancy_r']:+.3f} R · "
        f"PF {ms['profit_factor']:.2f} (abandon if PF < 1.1)",
        "",
        "## Baselines",
        "",
        f"- BTC buy-and-hold over the window: {ctx['bh']['return']:+.1%}, "
        f"max drawdown {ctx['bh']['max_drawdown']:.1%}",
        f"- Strategy per-trade net return: {ctx['strat_mean_pct']:+.3%} mean",
    ]
    rb = ctx["rb"]
    if rb:
        p_val = sum(1 for x in rb["dist"] if x >= ctx["strat_mean_pct"]) / len(rb["dist"])
        lines += [
            f"- Random-entry baseline ({len(rb['dist'])} sims, same holding "
            f"periods, costs paid): mean {rb['mean_of_means']:+.3%}, "
            f"p95 {rb['p95']:+.3%}",
            f"- **p-value (random ≥ strategy): {p_val:.3f}** (G0 needs <0.05)",
        ]
    lines += [
        "",
        "## Skip counters (cap behaviour)",
        "",
        f"`{ctx['skips']}`",
        "",
        "## Implementation choices (variants tried: 1 — this config only)",
        "",
        "- I1: armed setup expires after 5 bars or on close < EMA50",
        "- I2: '20-day high' measured on bar highs",
        "- Zero-volume bars non-tradable; fills postponed/cancelled (D-019)",
        "",
        "## Not yet run (required before G0)",
        "",
        "- Ablation EXP-001b: BTC-filter and trend-filter off (edge-vs-beta test)",
        "- Always-in-universe sensitivity (v1 universe makes it near-identical)",
        "- Parameter sensitivity table for the fixed params",
        "- Independent reproduction from raw data by a separate session "
        "(builder ≠ approver)",
        "",
        "*Generated by engine/experiment.py. No holdout data was accessible "
        "to this run.*",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="data/derived/okx/1d")
    ap.add_argument("--universe", default="data/universe.csv")
    ap.add_argument("--costs", default="costs.yaml")
    ap.add_argument("--start-equity", type=float, default=10_000.0)
    ap.add_argument("--unlock-holdout", default=None)
    ap.add_argument("--out", default="../research/experiments/EXP-001.md")
    args = ap.parse_args(argv)

    if args.unlock_holdout is None:
        max_ts = HOLDOUT_START_MS
    elif args.unlock_holdout == HOLDOUT_UNLOCK_PHRASE:
        max_ts = 2 ** 62
        print("!!! HOLDOUT UNLOCKED — this is only valid once, after all "
              "research is final (D-020) !!!")
    else:
        raise SystemExit("wrong holdout phrase; the holdout stays sealed")

    data = load_daily_dir(Path(args.data), max_ts)
    if "BTC-USDT" not in data:
        raise SystemExit("BTC-USDT missing — run `make derive` first")
    universe = load_universe(Path(args.universe))
    btc = btc_context(data)
    cost_model = CostModel.from_yaml(args.costs)

    print("running main simulation ...")
    sim = run_sim(data, universe, btc, cost_model, stress=False,
                  start_equity=args.start_equity)
    print(f"  {len(sim.trades)} trades, skips {sim.skips}")
    print("running 2x cost-stress simulation ...")
    sim_s = run_sim(data, universe, btc, cost_model, stress=True,
                    start_equity=args.start_equity)

    metrics = summarize(sim.trades, sim.equity_curve)
    metrics_s = summarize(sim_s.trades, sim_s.equity_curve)
    bh = btc_buy_hold(data)
    strat_mean_pct = (sum(t["pct"] for t in sim.trades) / len(sim.trades)
                      if sim.trades else 0.0)
    print("running random-entry baseline ...")
    rb = random_baseline(data, universe, cost_model, sim.trades)

    ctx = {
        "run_date": day(int(datetime.now(timezone.utc).timestamp() * 1000)),
        "window": f"{day(RESEARCH_START_MS)} .. {day(HOLDOUT_START_MS)} (excl.)",
        "datasets": dataset_ids(Path(args.data).parents[1]),
        "config_hash": config_hash(),
        "start_equity": args.start_equity,
        "final_equity": sim.equity_curve[-1] if sim.equity_curve else 0.0,
        "total_return": (sim.equity_curve[-1] / args.start_equity - 1.0
                         if sim.equity_curve else 0.0),
        "metrics": metrics, "metrics_stress": metrics_s,
        "bh": bh, "rb": rb, "strat_mean_pct": strat_mean_pct,
        "skips": sim.skips,
    }
    out = Path(args.out)
    write_report(out, ctx)
    print(f"\nreport -> {out}")
    print(f"trades {metrics['trades']} | expectancy {metrics['expectancy_r']:+.3f} R "
          f"| PF {metrics['profit_factor']:.2f} | maxDD {metrics['max_drawdown']:.1%}")


if __name__ == "__main__":
    main()
