"""Pre-backtest dataset audit — the three checks required by the WP1 review.

Usage:  python3 -m engine.data.audit data/raw

A. Timestamp alignment per timeframe: the modal value of ts % timeframe.
   Daily bars aligned to 00:00 UTC have offset 0; a consistent 57,600,000 ms
   offset means the exchange rolls its daily candle at 16:00 UTC (midnight
   UTC+8) — flagged, because indicator calendars and cross-pair joins assume
   UTC midnights. Mixed offsets inside one file are a structural failure.
B. Aggregation consistency: rebuild 4h and 1d bars from the stored 1h series
   (using each stored timeframe's own observed offset) and compare
   open/high/low/close/volume against the stored files.
C. Zero-volume runs of >= 3 consecutive bars (dead feeds, halted pairs).
D. Single-bar close-to-close moves > 40% on daily bars (possible bad prints).
E. Volume-semantics sanity: BTC-USDT median implied daily quote volume
   (close * volume) printed for eyeballing — base-vs-quote confusion shows up
   as an absurd magnitude.

Exit code 1 on structural failures: mixed alignment within a file, or > 0.5%
of comparable rebuilt bars mismatching beyond tolerance (price rel 1e-6,
volume rel 0.5%).
"""
import argparse
import csv
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .timeframes import TIMEFRAME_MS

PRICE_RTOL = 1e-6
VOLUME_RTOL = 0.005
MISMATCH_BUDGET = 0.005  # fraction of compared bars allowed to mismatch


def load(path: Path):
    rows = []
    with path.open() as f:
        for r in csv.reader(f):
            if r and r[0] != "timestamp":
                rows.append((int(r[0]), float(r[1]), float(r[2]),
                             float(r[3]), float(r[4]), float(r[5])))
    rows.sort(key=lambda x: x[0])
    return rows


def day(ts: int) -> str:
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def offsets(rows, tf_ms: int) -> Counter:
    return Counter(ts % tf_ms for ts, *_ in rows)


def rebuild(base_rows, tf_ms: int, offset: int) -> dict:
    """Aggregate base bars into tf_ms buckets anchored at `offset`.

    Returns {bucket_start_ts: [first_ts, o, h, l, c, v, last_ts, count]}.
    """
    buckets = {}
    for ts, o, h, l, c, v in base_rows:
        b = ((ts - offset) // tf_ms) * tf_ms + offset
        cur = buckets.get(b)
        if cur is None:
            buckets[b] = [ts, o, h, l, c, v, ts, 1]
        else:
            cur[2] = max(cur[2], h)
            cur[3] = min(cur[3], l)
            if ts > cur[6]:
                cur[4], cur[6] = c, ts
            if ts < cur[0]:
                cur[1], cur[0] = o, ts
            cur[5] += v
            cur[7] += 1
    return buckets


def compare(stored_rows, rebuilt: dict, bars_per_bucket: int):
    """Compare stored bars with rebuilt buckets that are fully covered."""
    checked = mismatched = 0
    examples = []
    for ts, o, h, l, c, v in stored_rows:
        b = rebuilt.get(ts)
        if b is None or b[7] != bars_per_bucket:
            continue
        checked += 1
        bad = [name for name, sv, rv in
               (("open", o, b[1]), ("high", h, b[2]), ("low", l, b[3]), ("close", c, b[4]))
               if abs(sv - rv) > PRICE_RTOL * max(abs(sv), 1e-12)]
        if abs(v - b[5]) > VOLUME_RTOL * max(v, 1e-12):
            bad.append("volume")
        if bad:
            mismatched += 1
            if len(examples) < 3:
                examples.append((day(ts), bad))
    return checked, mismatched, examples


def zero_volume_runs(rows, min_len: int = 3):
    runs, start, n = [], None, 0
    for ts, _o, _h, _l, _c, v in rows:
        if v == 0:
            if start is None:
                start = ts
            n += 1
        else:
            if n >= min_len:
                runs.append((start, n))
            start, n = None, 0
    if n >= min_len:
        runs.append((start, n))
    return runs


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", help="data root, e.g. data/raw")
    args = ap.parse_args(argv)
    root = Path(args.root)
    fail = False

    for ex_dir in sorted(d for d in root.iterdir() if d.is_dir()):
        tf_dirs = {d.name: d for d in ex_dir.iterdir()
                   if d.is_dir() and d.name in TIMEFRAME_MS}
        data = {tf: {p.stem: load(p) for p in sorted(d.glob("*.csv"))}
                for tf, d in tf_dirs.items()}

        print(f"\n=== {ex_dir.name}: A. timestamp alignment ===")
        tf_offset = {}
        for tf, files in sorted(data.items()):
            tf_ms = TIMEFRAME_MS[tf]
            modal_all = Counter()
            mixed = []
            for name, rows in files.items():
                offs = offsets(rows, tf_ms)
                if len(offs) > 1:
                    mixed.append((name, dict(offs.most_common(3))))
                modal_all.update(offs)
            modal = modal_all.most_common(1)[0][0] if modal_all else 0
            tf_offset[tf] = modal
            note = ""
            if tf == "1d" and modal == 57_600_000:
                note = "  <-- daily candle rolls at 16:00 UTC (midnight UTC+8), NOT UTC midnight"
            elif modal != 0:
                note = f"  <-- non-zero offset ({modal} ms)"
            print(f"  {tf}: modal offset {modal} ms across {len(files)} files{note}")
            for name, offs in mixed:
                print(f"    STRUCTURAL: {name} has mixed offsets {offs}")
                fail = True

        if "1h" in data:
            print(f"\n=== {ex_dir.name}: B. aggregation consistency (rebuilt from 1h) ===")
            for target in ("4h", "1d"):
                if target not in data:
                    continue
                tf_ms = TIMEFRAME_MS[target]
                bars_per_bucket = tf_ms // TIMEFRAME_MS["1h"]
                tot_checked = tot_mismatched = 0
                worst = []
                for name, stored in sorted(data[target].items()):
                    base_rows = data["1h"].get(name)
                    if not base_rows:
                        continue
                    rebuilt = rebuild(base_rows, tf_ms, tf_offset[target])
                    ch, mi, ex = compare(stored, rebuilt, bars_per_bucket)
                    tot_checked += ch
                    tot_mismatched += mi
                    if mi and len(worst) < 5:
                        worst.append((name, mi, ch, ex))
                rate = (tot_mismatched / tot_checked) if tot_checked else 0.0
                status = "OK" if rate <= MISMATCH_BUDGET else "FAIL"
                if rate > MISMATCH_BUDGET:
                    fail = True
                print(f"  {target}: {tot_checked} bars compared, {tot_mismatched} mismatched "
                      f"({rate:.4%}) -> {status}")
                for name, mi, ch, ex in worst:
                    print(f"    {name}: {mi}/{ch} mismatched, e.g. {ex}")

        print(f"\n=== {ex_dir.name}: C. zero-volume runs (>=3 bars) ===")
        any_run = False
        for tf, files in sorted(data.items()):
            for name, rows in sorted(files.items()):
                for start, n in zero_volume_runs(rows):
                    print(f"  {tf}/{name}: {n} zero-volume bars from {day(start)}")
                    any_run = True
        if not any_run:
            print("  none")

        if "1d" in data:
            print(f"\n=== {ex_dir.name}: D. daily close-to-close moves > 40% ===")
            spikes = []
            for name, rows in data["1d"].items():
                for (pts, *_p, pc, _pv), (ts, *_c2, c, _v) in zip(
                        [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows[:-1]],
                        [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows[1:]]):
                    if pc > 0 and abs(c / pc - 1) > 0.40:
                        spikes.append((abs(c / pc - 1), name, day(ts)))
            for pct, name, d in sorted(spikes, reverse=True)[:10]:
                print(f"  {name} {d}: {pct:+.1%}")
            if not spikes:
                print("  none")

            btc = data["1d"].get("BTC-USDT")
            if btc:
                qv = statistics.median(r[4] * r[5] for r in btc)
                print(f"\n=== {ex_dir.name}: E. volume semantics ===")
                print(f"  BTC-USDT median implied daily quote volume: {qv:,.0f} USDT")
                print("  (hundreds of millions to billions = volume field is base units, as assumed;"
                      " absurdly large = it was quote units all along)")

    print(f"\naudit: {'FAIL (structural issues above)' if fail else 'PASS'}")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
