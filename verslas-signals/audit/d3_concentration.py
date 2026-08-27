"""AUDIT-2026-08 D3 + E5: SOL era analysis and concentration robustness.

Diagnostics under protocol rule R3 — these numbers inform the narrative,
never a verdict. Stdlib only, no engine imports.

    python -m audit.d3_concentration      (from verslas-signals/)
"""
import csv
from collections import defaultdict
from pathlib import Path

TRADES = Path(__file__).resolve().parents[2] / "research/experiments/EXP-007.trades.csv"


def main():
    rows = list(csv.DictReader(TRADES.open()))
    rs = [float(t["r"]) for t in rows]
    n = len(rs)
    total = sum(rs)

    print("D3a — every SOL-USDT trade (contiguity check)")
    sol = [t for t in rows if t["pair"] == "SOL-USDT"]
    for t in sol:
        print(f"  {t['entry']} -> {t['exit']}  {float(t['r']):+7.3f} R  "
              f"{t['regime']:>5}  fold={t['fold'] or '2021/none'}  {t['exit_reason']}")
    sol_r = sum(float(t["r"]) for t in sol)
    print(f"  SOL: {len(sol)} trades, {sol_r:+.3f} R total "
          f"({sol_r / total:+.1%} of the book's net {total:+.3f} R)")

    print("\nD3b — leave-one-out expectancy per pair (is SOL unique?)")
    by_pair = defaultdict(list)
    for t in rows:
        by_pair[t["pair"]].append(float(t["r"]))
    loo = []
    for pair, prs in by_pair.items():
        rest = [r for t, r in zip(rows, rs) if t["pair"] != pair]
        loo.append((sum(rest) / len(rest), pair, len(prs), sum(prs)))
    loo.sort()
    print(f"  {'ex-pair expectancy':>19}  {'pair':<12} {'trades':>6} {'pair R':>8}")
    for e, pair, cnt, pr in loo:
        print(f"  {e:+19.3f}  {pair:<12} {cnt:>6} {pr:+8.3f}")

    print("\nE5 — top-pair share under the alternative (gross-positive) denominator")
    per_pair_r = {p: sum(v) for p, v in by_pair.items()}
    top_pair, top_r = max(per_pair_r.items(), key=lambda kv: kv[1])
    gross_pos = sum(v for v in per_pair_r.values() if v > 0)
    print(f"  net-R share (the pre-registered check 6): {top_r / total:.1%}")
    print(f"  gross-positive share: {top_r / gross_pos:.1%} "
          f"(top {top_pair} {top_r:+.3f} R of {gross_pos:+.3f} R summed over "
          f"profitable pairs)")
    print(f"  profitable pairs: {sum(1 for v in per_pair_r.values() if v > 0)}"
          f" of {len(per_pair_r)} traded")


if __name__ == "__main__":
    main()
