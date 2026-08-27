"""EXP-003: HYP-002 (relative-strength breakout), per the Sprint B
pre-registration in research/experiments/NOTES-SPRINT-B.md.

Usage (from verslas-signals/):
    python3 -m engine.exp003

Primary run: resting-stop execution. One declared sensitivity: close-confirm.
Plus the 2x cost stress and both baselines. The decision rule from the
pre-registration is evaluated and printed — the verdict is computed, not
chosen.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path

from .costs import CostModel
from .hyp002 import Hyp002, config_hash, policy as hyp002_policy
from .metrics import summarize
from .protocol import HOLDOUT_START_MS, RESEARCH_START_MS
from .simulator import Simulator
from .experiment import (load_daily_dir, load_universe, btc_context,
                         dataset_ids, day, btc_buy_hold, random_baseline)


def run(data, universe, btc, cost_model, stress=False,
        stop_mode="resting_stop"):
    def cost_fn(pair):
        return cost_model.one_way_fraction("okx", pair.replace("-", "/")) * \
            (cost_model.stress_multiplier if stress else 1.0)
    strategy = Hyp002(data, universe)
    pol = hyp002_policy()
    pol.stop_mode = stop_mode
    sim = Simulator(data, universe, btc, cost_fn, strategy, pol,
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
    ap.add_argument("--out", default="../research/experiments/EXP-003.md")
    args = ap.parse_args(argv)

    data = load_daily_dir(Path(args.data), HOLDOUT_START_MS)  # holdout sealed
    universe = load_universe(Path(args.universe))
    btc = btc_context(data)
    cost_model = CostModel.from_yaml(args.costs)

    print("primary run (resting stop) ...")
    sim = run(data, universe, btc, cost_model)
    m = summarize(sim.trades, sim.equity_curve)
    print(f"  trades {m['trades']} | expectancy {m['expectancy_r']:+.3f} R | "
          f"PF {m['profit_factor']:.2f} | maxDD {m['max_drawdown']:.1%}")
    print("2x cost stress ...")
    sim_s = run(data, universe, btc, cost_model, stress=True)
    m_s = summarize(sim_s.trades, sim_s.equity_curve)
    print("execution sensitivity (close-confirm) ...")
    sim_c = run(data, universe, btc, cost_model, stop_mode="close_confirm")
    m_c = summarize(sim_c.trades, sim_c.equity_curve)
    print("random-entry baseline ...")
    rb = random_baseline(data, universe, cost_model, sim.trades)
    bh = btc_buy_hold(data)
    strat_mean_pct = (sum(t["pct"] for t in sim.trades) / len(sim.trades)
                      if sim.trades else 0.0)
    p_val = (sum(1 for x in rb["dist"] if x >= strat_mean_pct) / len(rb["dist"])
             if rb else 1.0)

    folds_pos = sum(1 for f in m["folds"].values() if f["expectancy_r"] > 0)
    checks = {
        "expectancy > 0": m["expectancy_r"] > 0,
        "folds positive >= 4/7": folds_pos >= 4,
        "stress PF >= 1.1": m_s["profit_factor"] >= 1.1,
        "random baseline p < 0.05": p_val < 0.05,
    }
    verdict = ("PROCEED to full G0 battery" if all(checks.values())
               else "FAILED — per the pre-registered rule, HYP-002 is recorded "
                    "as failed; Sprint C decision follows")

    er = exit_reason_stats(sim.trades)
    per_year = {}
    for t in sim.trades:
        y = day(t["entry_ts"])[:4]
        per_year[y] = per_year.get(y, 0) + 1
    funnel = dict(sorted(sim.strategy.funnel.items(), key=lambda kv: -kv[1])[:40])

    run_date = day(int(datetime.now(timezone.utc).timestamp() * 1000))
    lines = [
        "# EXP-003 — HYP-002 relative-strength breakout (Sprint B)",
        "",
        f"Run: {run_date} · window {day(RESEARCH_START_MS)} .. "
        f"{day(HOLDOUT_START_MS)} (excl.) · holdout SEALED",
        f"Datasets: {dataset_ids(Path(args.data))} · config `{config_hash()}` "
        "· execution: resting stop (primary) · pre-registration: "
        "NOTES-SPRINT-B.md · HYP-002 variants tried: 2",
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
        f"- Max drawdown {m['max_drawdown']:.1%} · final equity "
        f"{sim.equity_curve[-1]:,.0f}" if sim.equity_curve else "- (no equity)",
        "",
        "## Folds",
        "",
        "| fold | trades | expectancy (R) |",
        "|---|---|---|",
    ]
    for name, f in m["folds"].items():
        lines.append(f"| {name} | {f['trades']} | {f['expectancy_r']:+.3f} |")
    lines += [
        f"\nPositive folds: **{folds_pos}/7**",
        "",
        "## Regimes",
        "",
        "| regime | trades | expectancy (R) |",
        "|---|---|---|",
    ]
    for name, f in m["regimes"].items():
        lines.append(f"| {name} | {f['trades']} | {f['expectancy_r']:+.3f} |")
    lines += [
        "",
        "## Stress and sensitivity",
        "",
        f"- 2x cost stress: {m_s['trades']} trades, "
        f"{m_s['expectancy_r']:+.3f} R, PF {m_s['profit_factor']:.2f}",
        f"- Close-confirm execution: {m_c['trades']} trades, "
        f"{m_c['expectancy_r']:+.3f} R, PF {m_c['profit_factor']:.2f}",
        "",
        "## Baselines",
        "",
        f"- BTC buy-and-hold: {bh['return']:+.1%}, maxDD {bh['max_drawdown']:.1%}",
        f"- Strategy mean per-trade net return: {strat_mean_pct:+.3%}",
    ]
    if rb:
        lines += [
            f"- Random-entry baseline: mean {rb['mean_of_means']:+.3%}, "
            f"p95 {rb['p95']:+.3%} · **p-value {p_val:.3f}**",
        ]
    lines += [
        "",
        "## Exit reasons",
        "",
        "| reason | trades | mean R |",
        "|---|---|---|",
    ]
    for reason, (n, mean_r) in sorted(er.items()):
        lines.append(f"| {reason} | {n} | {mean_r:+.3f} |")
    lines += [
        "",
        "## Trades per year",
        "",
        "| year | trades |",
        "|---|---|",
    ]
    for y, n in sorted(per_year.items()):
        lines.append(f"| {y} | {n} |")
    lines += [
        "",
        "## Signal funnel",
        "",
        "```",
    ]
    for key, n in sorted(funnel.items()):
        lines.append(f"{key:>24}: {n}")
    lines += [
        "```",
        "",
        f"`skips: {sim.skips}`",
        "",
        "## Decision rule (pre-registered) — evaluated",
        "",
    ]
    for check, ok in checks.items():
        lines.append(f"- {'PASS' if ok else 'FAIL'}: {check}")
    lines += ["", f"**Verdict: {verdict}**", "",
              "*Generated by engine/exp003.py. No holdout data was accessible.*"]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")

    trades_csv = out.with_suffix(".trades.csv")
    import csv as _csv
    with trades_csv.open("w", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["pair", "entry", "exit", "r", "pct", "bars_held",
                    "regime", "fold", "exit_reason"])
        for t in sorted(sim.trades, key=lambda t: t["entry_ts"]):
            w.writerow([t["pair"], day(t["entry_ts"]), day(t["exit_ts"]),
                        f"{t['r']:.3f}", f"{t['pct']:.4f}", t["bars_held"],
                        t["regime"], t["fold"], t["exit_reason"]])
    print(f"\nreport -> {out}\ntrades -> {trades_csv}")
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
