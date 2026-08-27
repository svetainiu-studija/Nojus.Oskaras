"""AUDIT-2026-08 E1 + E2: independent recomputation of EXP-007's headline
numbers from the trades CSV alone.

Deliberately imports NOTHING from engine/ — stdlib only — so a bug in
engine/metrics.py cannot hide here. Expected values are hardcoded from the
committed research/experiments/EXP-007.md; every line prints MATCH or
MISMATCH.

    python -m audit.e1_stats          (from verslas-signals/)
"""
import csv
import random
from collections import defaultdict
from pathlib import Path

TRADES = Path(__file__).resolve().parents[2] / "research/experiments/EXP-007.trades.csv"

# Hardcoded from EXP-007.md (the report under audit).
EXPECTED = {
    "trades": 48,
    "expectancy_r": 0.317,
    "profit_factor": 1.59,
    "win_rate": 0.292,
    "avg_win_r": 2.92,
    "avg_loss_r": -0.76,
    "folds": {"2022-H1": (3, -0.734), "2022-H2": (7, -0.526),
              "2023-H1": (6, 0.556), "2023-H2": (12, 1.478),
              "2024-H1": (6, -0.804), "2024-H2": (5, 0.846),
              "2025-H1": (6, -0.310)},
    "folds_positive": 3,
    "top_pair": "SOL-USDT",
    "top_share": 1.481,
    "ex_top_expectancy": -0.159,
    "exp_ci80": (-0.244, 0.934),
    "pf_ci80": (0.56, 2.90),
    "per_year": {"2021": 3, "2022": 10, "2023": 18, "2024": 11, "2025": 6},
}
BOOT_ITERS = 10_000
BOOT_SEED = 20260828   # deliberately different from any engine seed
CI_TOL_R = 0.05        # error criterion from the protocol (E2)
CI_TOL_PF = 0.10

# Comparison tolerances = half a unit of the report's printed precision
# plus an allowance for the CSV's per-trade 3-decimal rounding of r.
# (First run used tighter ones and flagged avg_loss_r and one fold; both
# root-caused to display rounding — see AUDIT-2026-08-REPORT.md E1.)
TOL_3DP = 0.0007       # values the report prints to 3 decimals
TOL_2DP = 0.006        # values the report prints to 2 decimals


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'MATCH   ' if ok else 'MISMATCH'} {name}: recomputed {got:+.4f} "
          f"vs report {want:+.4f}")
    return ok


def main():
    rows = list(csv.DictReader(TRADES.open()))
    rs = [float(t["r"]) for t in rows]
    n = len(rs)
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r <= 0]
    ok = True

    print(f"E1 — independent recomputation from {TRADES.name} ({n} rows)")
    ok &= check("trades", n, EXPECTED["trades"], 0)
    ok &= check("expectancy_r", sum(rs) / n, EXPECTED["expectancy_r"], TOL_3DP)
    pf = sum(wins) / abs(sum(losses))
    ok &= check("profit_factor", pf, EXPECTED["profit_factor"], TOL_2DP)
    ok &= check("win_rate", len(wins) / n, EXPECTED["win_rate"], 0.0005)
    ok &= check("avg_win_r", sum(wins) / len(wins), EXPECTED["avg_win_r"], TOL_2DP)
    ok &= check("avg_loss_r", sum(losses) / len(losses), EXPECTED["avg_loss_r"], TOL_2DP)

    by_fold = defaultdict(list)
    for t in rows:
        if t["fold"]:
            by_fold[t["fold"]].append(float(t["r"]))
    pos = 0
    for fold, (want_n, want_e) in EXPECTED["folds"].items():
        got = by_fold.get(fold, [])
        e = sum(got) / len(got) if got else 0.0
        pos += e > 0
        ok &= check(f"fold {fold} trades", len(got), want_n, 0)
        ok &= check(f"fold {fold} expectancy", e, want_e, TOL_3DP)
    extra = set(by_fold) - set(EXPECTED["folds"])
    if extra:
        ok = False
        print(f"  MISMATCH unexpected folds in CSV: {sorted(extra)}")
    ok &= check("folds_positive", pos, EXPECTED["folds_positive"], 0)
    unfolded = [t for t in rows if not t["fold"]]
    print(f"  note: {len(unfolded)} trades carry no fold "
          f"(2021 = training-only per D-020): "
          f"{[t['entry'][:4] for t in unfolded]}")

    by_year = defaultdict(int)
    for t in rows:
        by_year[t["entry"][:4]] += 1
    for y, want_n in EXPECTED["per_year"].items():
        ok &= check(f"year {y} trades", by_year.get(y, 0), want_n, 0)

    by_pair = defaultdict(float)
    for t in rows:
        by_pair[t["pair"]] += float(t["r"])
    top_pair, top_r = max(by_pair.items(), key=lambda kv: kv[1])
    print(f"  {'MATCH   ' if top_pair == EXPECTED['top_pair'] else 'MISMATCH'} "
          f"top pair: {top_pair}")
    ok &= top_pair == EXPECTED["top_pair"]
    ok &= check("top_share (net-R denominator)", top_r / sum(by_pair.values()),
                EXPECTED["top_share"], 0.005)
    ex = [float(t["r"]) for t in rows if t["pair"] != top_pair]
    ok &= check("ex_top_expectancy", sum(ex) / len(ex),
                EXPECTED["ex_top_expectancy"], TOL_3DP)
    print("  note: max drawdown is equity-curve-based and cannot be recomputed "
          "from the trades CSV; it is covered by A2 (clean-room rerun).")

    print(f"\nE2 — independent bootstrap ({BOOT_ITERS} iters, seed {BOOT_SEED})")
    rng = random.Random(BOOT_SEED)
    means, pfs = [], []
    for _ in range(BOOT_ITERS):
        sample = [rs[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
        w = sum(r for r in sample if r > 0)
        l = abs(sum(r for r in sample if r <= 0))
        pfs.append(w / l if l else float("inf"))
    means.sort()
    pfs.sort()

    def pct(xs, p):
        return xs[min(len(xs) - 1, int(p * len(xs)))]

    ok &= check("expectancy CI80 low", pct(means, 0.10), EXPECTED["exp_ci80"][0], CI_TOL_R)
    ok &= check("expectancy CI80 high", pct(means, 0.90), EXPECTED["exp_ci80"][1], CI_TOL_R)
    ok &= check("PF CI80 low", pct(pfs, 0.10), EXPECTED["pf_ci80"][0], CI_TOL_PF)
    ok &= check("PF CI80 high", pct(pfs, 0.90), EXPECTED["pf_ci80"][1], CI_TOL_PF)

    print(f"\nE1/E2 verdict: {'ALL MATCH — no error found' if ok else 'DISCREPANCY — root-cause required'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
