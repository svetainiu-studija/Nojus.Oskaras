"""Data-quality report: per-file bar gaps within each file's own date range.

Usage:  python3 -m engine.data.quality data/raw [--max-missing-pct 2.0]

Exit code 1 if any file misses more than --max-missing-pct of its expected bars
(computed from the file's first/last timestamp and its timeframe directory name).
Listing-date differences don't count as gaps because the range starts at each
file's own first bar.
"""
import argparse
import csv
import sys
from pathlib import Path

from .timeframes import TIMEFRAME_MS


def analyse(path: Path, tf_ms: int) -> dict:
    rows = 0
    first_ts = last_ts = None
    seen_dupes = 0
    prev = None
    with path.open() as f:
        for row in csv.reader(f):
            if not row or row[0] == "timestamp":
                continue
            ts = int(row[0])
            rows += 1
            if prev is not None and ts == prev:
                seen_dupes += 1
            prev = ts
            first_ts = ts if first_ts is None else min(first_ts, ts)
            last_ts = ts if last_ts is None else max(last_ts, ts)
    if rows == 0:
        return {"rows": 0, "expected": 0, "missing": 0, "missing_pct": 100.0, "dupes": 0}
    expected = (last_ts - first_ts) // tf_ms + 1
    missing = max(0, expected - (rows - seen_dupes))
    return {
        "rows": rows,
        "expected": expected,
        "missing": missing,
        "missing_pct": round(100.0 * missing / expected, 3) if expected else 0.0,
        "dupes": seen_dupes,
    }


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root")
    ap.add_argument("--max-missing-pct", type=float, default=2.0)
    args = ap.parse_args(argv)

    root = Path(args.root)
    failures = 0
    print(f"{'file':<50} {'rows':>8} {'missing':>8} {'miss%':>7} {'dupes':>6}")
    for path in sorted(root.rglob("*.csv")):
        tf = path.parent.name
        if tf not in TIMEFRAME_MS:
            print(f"{path}: skipped (unknown timeframe dir {tf!r})", file=sys.stderr)
            continue
        r = analyse(path, TIMEFRAME_MS[tf])
        flag = ""
        if r["missing_pct"] > args.max_missing_pct or r["dupes"]:
            failures += 1
            flag = "  <-- CHECK"
        rel = str(path.relative_to(root))
        print(f"{rel:<50} {r['rows']:>8} {r['missing']:>8} {r['missing_pct']:>7} {r['dupes']:>6}{flag}")
    if failures:
        print(f"\n{failures} file(s) over threshold", file=sys.stderr)
        sys.exit(1)
    print("\nall files within threshold")


if __name__ == "__main__":
    main()
