"""Derive canonical UTC-aligned 4h and 1d bars from the 1h series (D-019).

Usage:  python3 -m engine.data.derive data/raw/okx/1h data/derived/okx

Rationale: the audit showed OKX's native daily candles disagree with the sum
of their own hourly candles on the volume field for ~5% of days. Rather than
trusting two independently fetched series, research uses ONE source of truth:
the 1h series, from which 4h and 1d bars are aggregated deterministically here
(open = first, high = max, low = min, close = last, volume = sum; buckets
anchored at 00:00 UTC). Only fully covered buckets are written — a partial
first listing day or a trailing partial day is dropped. The native 4h/1d
files stay in data/raw for QA (the audit's cross-check) and nothing else.

After deriving, fingerprint the result:
    python3 -m engine.data.manifest data/derived --config pairs.yaml
"""
import argparse
import csv
from pathlib import Path

from .audit import load, rebuild
from .timeframes import TIMEFRAME_MS

TARGETS = ("4h", "1d")


def derive_file(src: Path, out_root: Path) -> dict:
    rows = load(src)
    written = {}
    for tf in TARGETS:
        tf_ms = TIMEFRAME_MS[tf]
        need = tf_ms // TIMEFRAME_MS["1h"]
        buckets = rebuild(rows, tf_ms, 0)
        complete = sorted((ts, b) for ts, b in buckets.items() if b[7] == need)
        out_path = out_root / tf / src.name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "open", "high", "low", "close", "volume"])
            for ts, b in complete:
                w.writerow([ts, b[1], b[2], b[3], b[4], b[5]])
        written[tf] = len(complete)
    return written


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("hourly_dir", help="directory of 1h CSVs, e.g. data/raw/okx/1h")
    ap.add_argument("out_root", help="output root, e.g. data/derived/okx")
    args = ap.parse_args(argv)

    src_dir = Path(args.hourly_dir)
    out_root = Path(args.out_root)
    files = sorted(src_dir.glob("*.csv"))
    if not files:
        raise SystemExit(f"no CSV files in {src_dir}")
    totals = {tf: 0 for tf in TARGETS}
    for src in files:
        written = derive_file(src, out_root)
        for tf, n in written.items():
            totals[tf] += n
        print(f"{src.stem}: " + ", ".join(f"{n} {tf} bars" for tf, n in written.items()))
    print(f"done: {len(files)} pairs -> " +
          ", ".join(f"{totals[tf]} {tf} bars" for tf in TARGETS))
    print("now fingerprint it:  python3 -m engine.data.manifest "
          f"{out_root.parent} --config pairs.yaml")


if __name__ == "__main__":
    main()
