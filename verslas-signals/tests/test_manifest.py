import csv
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.data.manifest import build_manifest, dataset_id
from engine.data.quality import analyse
from engine.data.timeframes import TIMEFRAME_MS


def write_csv(path: Path, timestamps):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for ts in timestamps:
            w.writerow([ts, 1, 2, 0.5, 1.5, 100])


class ManifestTest(unittest.TestCase):
    def test_id_stable_and_sensitive(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "raw"
            day = TIMEFRAME_MS["1d"]
            write_csv(root / "okx" / "1d" / "BTC-USDT.csv", [0, day, 2 * day])
            m1 = build_manifest(root)
            id1 = dataset_id(m1)
            # rebuilding without changes gives the same id
            self.assertEqual(id1, dataset_id(build_manifest(root)))
            # any data change gives a different id
            write_csv(root / "okx" / "1d" / "BTC-USDT.csv", [0, day, 2 * day, 3 * day])
            self.assertNotEqual(id1, dataset_id(build_manifest(root)))

    def test_manifest_counts_rows_and_range(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "raw"
            day = TIMEFRAME_MS["1d"]
            write_csv(root / "okx" / "1d" / "ETH-USDT.csv", [day, 2 * day, 4 * day])
            m = build_manifest(root)
            entry = m["files"]["okx/1d/ETH-USDT.csv"]
            self.assertEqual(entry["rows"], 3)
            self.assertEqual(entry["first_ts"], day)
            self.assertEqual(entry["last_ts"], 4 * day)


class QualityTest(unittest.TestCase):
    def test_gap_detection(self):
        with tempfile.TemporaryDirectory() as d:
            day = TIMEFRAME_MS["1d"]
            p = Path(d) / "1d" / "BTC-USDT.csv"
            write_csv(p, [0, day, 3 * day])  # bar at 2*day missing
            r = analyse(p, day)
            self.assertEqual(r["expected"], 4)
            self.assertEqual(r["missing"], 1)

    def test_clean_file(self):
        with tempfile.TemporaryDirectory() as d:
            day = TIMEFRAME_MS["1d"]
            p = Path(d) / "1d" / "BTC-USDT.csv"
            write_csv(p, [0, day, 2 * day, 3 * day])
            r = analyse(p, day)
            self.assertEqual(r["missing"], 0)
            self.assertEqual(r["dupes"], 0)


if __name__ == "__main__":
    unittest.main()
