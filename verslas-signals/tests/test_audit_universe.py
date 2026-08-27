import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.data.audit import rebuild, compare, zero_volume_runs, offsets
from engine.data.timeframes import TIMEFRAME_MS
from engine.universe import compute_universe

H = TIMEFRAME_MS["1h"]
D = TIMEFRAME_MS["1d"]


def hour_bars(n, start=0):
    """n synthetic 1h bars: price walks up 1 per bar, volume 10 each."""
    rows = []
    for i in range(n):
        o = 100.0 + i
        rows.append((start + i * H, o, o + 2, o - 1, o + 1, 10.0))
    return rows


class AuditTest(unittest.TestCase):
    def test_rebuild_and_compare_clean(self):
        base = hour_bars(48)  # exactly 2 UTC days
        rebuilt = rebuild(base, D, 0)
        self.assertEqual(len(rebuilt), 2)
        b0 = rebuilt[0]
        self.assertEqual(b0[1], 100.0)            # first open
        self.assertEqual(b0[2], 100.0 + 23 + 2)   # max high
        self.assertEqual(b0[3], 99.0)             # min low
        self.assertEqual(b0[4], 100.0 + 23 + 1)   # last close
        self.assertEqual(b0[5], 240.0)            # summed volume
        self.assertEqual(b0[7], 24)               # fully covered
        stored = [(0, 100.0, 125.0, 99.0, 124.0, 240.0),
                  (D, 124.0, 149.0, 123.0, 148.0, 240.0)]
        r = compare(stored, rebuilt, 24)
        self.assertEqual((r["checked"], r["price_bad"], r["vol_bad"]), (2, 0, 0))

    def test_compare_separates_price_and_volume(self):
        base = hour_bars(24)
        rebuilt = rebuild(base, D, 0)
        stored = [(0, 100.0, 125.0, 99.0, 124.0, 300.0)]  # wrong volume only
        r = compare(stored, rebuilt, 24)
        self.assertEqual((r["checked"], r["price_bad"], r["vol_bad"]), (1, 0, 1))
        self.assertAlmostEqual(r["vol_diffs"][0], 60.0 / 300.0)
        stored = [(0, 100.0, 130.0, 99.0, 124.0, 240.0)]  # wrong high only
        r = compare(stored, rebuilt, 24)
        self.assertEqual((r["price_bad"], r["vol_bad"]), (1, 0))
        self.assertIn("high", r["price_examples"][0][1])

    def test_partial_buckets_skipped(self):
        base = hour_bars(30)  # 1 full day + 6 hours
        rebuilt = rebuild(base, D, 0)
        stored = [(0, 100.0, 125.0, 99.0, 124.0, 240.0),
                  (D, 124.0, 131.0, 123.0, 130.0, 60.0)]
        r = compare(stored, rebuilt, 24)
        self.assertEqual(r["checked"], 1)  # partial second day not compared

    def test_offset_detection(self):
        utc8 = [(57_600_000 + i * D, 1, 1, 1, 1, 1) for i in range(5)]
        offs = offsets(utc8, D)
        self.assertEqual(offs.most_common(1)[0][0], 57_600_000)

    def test_zero_volume_runs(self):
        rows = [(i * H, 1, 1, 1, 1, 0.0 if 3 <= i <= 6 else 5.0) for i in range(10)]
        runs = zero_volume_runs(rows)
        self.assertEqual(runs, [(3 * H, 4)])


class DeriveTest(unittest.TestCase):
    def test_derive_writes_complete_buckets_only(self):
        import csv as _csv
        import tempfile
        from engine.data.derive import derive_file

        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "1h" / "BTC-USDT.csv"
            src.parent.mkdir(parents=True)
            with src.open("w", newline="") as f:
                w = _csv.writer(f)
                w.writerow(["timestamp", "open", "high", "low", "close", "volume"])
                for ts, o, h, l, c, v in hour_bars(30):  # 1 full day + 6h
                    w.writerow([ts, o, h, l, c, v])
            out_root = Path(d) / "derived"
            written = derive_file(src, out_root)
            self.assertEqual(written["1d"], 1)   # partial day dropped
            self.assertEqual(written["4h"], 7)   # 30h -> 7 full 4h buckets
            with (out_root / "1d" / "BTC-USDT.csv").open() as f:
                rows = [r for r in _csv.reader(f)][1:]
            self.assertEqual(len(rows), 1)
            self.assertEqual(float(rows[0][5]), 240.0)  # summed volume


class UniverseTest(unittest.TestCase):
    def test_age_filter_and_ranking(self):
        def daily(n_days, start_day, close, vol):
            return [((start_day + i) * D, close, vol) for i in range(n_days)]

        data = {
            "BIG": daily(200, 0, 100.0, 1000.0),   # highest quote volume
            "MID": daily(200, 0, 10.0, 1000.0),
            "NEW": daily(80, 120, 1000.0, 1000.0),  # listed late, huge volume
        }
        rows, always_in = compute_universe(
            data, top=2, window_bars=10, min_age_days=30, min_bars=10)
        by_day = {}
        for ts, sym, rank, score, in_u in rows:
            by_day.setdefault(ts, {})[sym] = (rank, in_u)
        # before NEW is old enough, BIG and MID fill the universe
        early = by_day[50 * D]
        self.assertTrue(early["BIG"][1] and early["MID"][1])
        self.assertNotIn("NEW", early)
        # once NEW is eligible (age >= 30d and >= 10 bars), it outranks MID
        late = by_day[199 * D]
        self.assertEqual(late["NEW"][0], 1)
        self.assertTrue(late["NEW"][1])
        self.assertFalse(late["MID"][1])       # pushed out of top 2
        self.assertIn("BIG", always_in)
        self.assertNotIn("MID", always_in)     # dropped at least once


if __name__ == "__main__":
    unittest.main()
