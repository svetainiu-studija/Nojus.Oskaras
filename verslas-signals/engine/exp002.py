"""EXP-002: the pre-registered execution-fidelity grid for HYP-001.

Usage (from verslas-signals/):
    python3 -m engine.exp002

Runs the four variants declared in research/experiments/NOTES-EXP-001.md —
(stop execution: close-confirm vs resting stop) x (time stop: 10 vs 20 bars) —
with signals, filters, sizing, universe and costs identical to EXP-001.
All four results are reported side by side; the decision rule is fixed in the
pre-registration and repeated in the output. Total HYP-001 variants tried
after this run: 5.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path

from .costs import CostModel
from .hyp001 import Hyp001, config_hash
from .metrics import summarize
from .protocol import (HOLDOUT_START_MS, RESEARCH_START_MS,
                       FOLDS_REQUIRED_POSITIVE)
from .simulator import ExitPolicy, Simulator
from .experiment import load_daily_dir, load_universe, btc_context, dataset_ids, day

VARIANTS = [
    ("A", "close_confirm", 10),   # EXP-001 baseline, re-simulated
    ("B", "resting_stop", 10),
    ("C", "close_confirm", 20),
    ("D", "resting_stop", 20),
]


def run_variant(data, universe, btc, cost_model, stop_mode, time_stop):
    def cost_fn(pair):
        return cost_model.one_way_fraction("okx", pair.replace("-", "/"))
    strategy = Hyp001(data, universe)
    policy = ExitPolicy(stop_mode=stop_mode, time_stop_bars=time_stop)
    sim = Simulator(data, universe, btc, cost_fn, strategy, policy,
                    research_range=(RESEARCH_START_MS, HOLDOUT_START_MS))
    return sim.run()


def exit_reason_stats(trades):
    stats = {}
    for t in trades:
        n, s = stats.get(t["exit_reason"], (0, 0.0))
        stats[t["exit_reason"]] = (n + 1, s + t["r"])
    return {k: (n, s / n) for k, (n, s) in stats.items()}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="data/derived/okx/1d")
    ap.add_argument("--universe", default="data/universe.csv")
    ap.add_argument("--costs", default="costs.yaml")
    ap.add_argument("--out", default="../research/experiments/EXP-002.md")
    args = ap.parse_args(argv)

    data = load_daily_dir(Path(args.data), HOLDOUT_START_MS)  # holdout sealed
    universe = load_universe(Path(args.universe))
    btc = btc_context(data)
    cost_model = CostModel.from_yaml(args.costs)

    rows = []
    for name, stop_mode, time_stop in VARIANTS:
        print(f"variant {name}: stop={stop_mode}, time_stop={time_stop} ...")
        sim = run_variant(data, universe, btc, cost_model, stop_mode, time_stop)
        m = summarize(sim.trades, sim.equity_curve)
        er = exit_reason_stats(sim.trades)
        positive = sum(1 for f in m["folds"].values() if f["expectancy_r"] > 0)
        rows.append((name, stop_mode, time_stop, m, er, positive,
                     sim.equity_curve[-1] if sim.equity_curve else 0.0))
        print(f"  trades {m['trades']} | expectancy {m['expectancy_r']:+.3f} R "
              f"| PF {m['profit_factor']:.2f} | maxDD {m['max_drawdown']:.1%} "
              f"| folds+ {positive}/7")

    run_date = day(int(datetime.now(timezone.utc).timestamp() * 1000))
    lines = [
        "# EXP-002 — HYP-001 execution-fidelity grid (pre-registered)",
        "",
        f"Run: {run_date} · window {day(RESEARCH_START_MS)} .. "
        f"{day(HOLDOUT_START_MS)} (excl.) · holdout SEALED",
        f"Datasets: {dataset_ids(Path(args.data))} · signal config "
        f"`{config_hash()}` (unchanged from EXP-001)",
        "Pre-registration: research/experiments/NOTES-EXP-001.md "
        "(variants and decision rule declared before this run; "
        "HYP-001 variants tried incl. this grid: 5)",
        "",
        "| variant | stop exec | time stop | trades | expectancy (R) | CI80 | "
        "PF | maxDD | folds + | stop-exit mean R | time-exit mean R | "
        "final equity |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for name, stop_mode, time_stop, m, er, positive, eq in rows:
        s_n, s_r = er.get("stop", (0, 0.0))
        t_n, t_r = er.get("time", (0, 0.0))
        lines.append(
            f"| {name} | {stop_mode} | {time_stop} | {m['trades']} | "
            f"{m['expectancy_r']:+.3f} | {m['expectancy_ci80'][0]:+.2f}…"
            f"{m['expectancy_ci80'][1]:+.2f} | {m['profit_factor']:.2f} | "
            f"{m['max_drawdown']:.1%} | {positive}/7 | "
            f"{s_r:+.2f} ({s_n}) | {t_r:+.2f} ({t_n}) | {eq:,.0f} |")
    lines += [
        "",
        "## Decision rule (fixed in the pre-registration)",
        "",
        "- No variant with expectancy > 0 → HYP-001 abandoned under its own "
        "falsifier; Sprint B (HYP-002) starts.",
        "- A positive variant is provisional only: it must still pass the 2x "
        "cost stress, the random-entry baseline (p<0.05), parameter "
        "sensitivity, the always-in-universe run, and independent "
        f"reproduction, with fold threshold ≥{FOLDS_REQUIRED_POSITIVE}/7 and "
        "holdout thresholds scaled to 5 variants.",
        "- No further HYP-001 variants without a new pre-registration.",
        "",
        "*Generated by engine/exp002.py. No holdout data was accessible.*",
    ]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nreport -> {out}")


if __name__ == "__main__":
    main()
