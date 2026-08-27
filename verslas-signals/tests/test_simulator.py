import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.simulator import Simulator, ExitPolicy, EntryIntent
from engine.hyp001 import Hyp001
from engine.experiment import load_daily_dir

DAY = 86_400_000
T0 = 1_609_459_200_000  # 2021-01-01 UTC — inside the research window


def make_pair(bars):
    """bars: list of (o, h, l, c, v)."""
    cols = {"ts": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
    for i, (o, h, l, c, v) in enumerate(bars):
        cols["ts"].append(T0 + i * DAY)
        cols["open"].append(float(o))
        cols["high"].append(float(h))
        cols["low"].append(float(l))
        cols["close"].append(float(c))
        cols["volume"].append(float(v))
    return cols


def bull_btc(n):
    return {"ts_index": {T0 + i * DAY: i for i in range(n)},
            "close": [100.0] * n, "sma50": [90.0] * n, "sma200": [80.0] * n}


def full_universe(data):
    return {(ts, p) for p, d in data.items() for ts in d["ts"]}


class FakeStrategy:
    """Signals an entry for (pair -> (index, stop_px)) exactly once."""
    max_stop_frac = 0.5

    def __init__(self, plan):
        self.plan = dict(plan)

    def on_close(self, sim, pair, i, ts):
        if self.plan.get(pair) and self.plan[pair][0] == i:
            _, stop = self.plan.pop(pair)
            return EntryIntent(pair=pair, stop_px=stop, signal_i=i)
        return None


def zero_cost(pair):
    return 0.0


def run(data, plan, policy=None, cost=zero_cost):
    n = max(len(d["ts"]) for d in data.values())
    sim = Simulator(data, full_universe(data), bull_btc(n), cost,
                    FakeStrategy(plan), policy or ExitPolicy())
    return sim.run()


class SimulatorTest(unittest.TestCase):
    def test_entry_next_open_and_stop_exit(self):
        # signal at i=0 close 100 (stop 95); fill i=1 open 100;
        # i=1 closes 94 < stop -> exit at i=2 open 93
        a = make_pair([(100, 101, 99, 100, 10), (100, 101, 93, 94, 10),
                       (93, 94, 92, 93, 10), (93, 94, 92, 93, 10)])
        sim = run({"A": a}, {"A": (0, 95.0)})
        self.assertEqual(len(sim.trades), 1)
        t = sim.trades[0]
        # units = 1% * 10000 / (100-95) = 20; pnl = 20*(93-100) = -140; R = -1.4
        self.assertAlmostEqual(t["r"], -1.4, places=9)
        self.assertEqual(t["entry_ts"], T0 + DAY)
        self.assertEqual(t["exit_ts"], T0 + 2 * DAY)

    def test_partial_at_2R(self):
        # entry 100 stop 95 -> 2R target 110. i=2 high 111 fills half at 110;
        # i=3 closes 94 < stop -> remainder out at i=4 open 90.
        a = make_pair([(100, 101, 99, 100, 10), (100, 101, 99, 100, 10),
                       (105, 111, 104, 106, 10), (95, 96, 93, 94, 10),
                       (90, 91, 89, 90, 10), (90, 91, 89, 90, 10)])
        sim = run({"A": a}, {"A": (0, 95.0)})
        self.assertEqual(len(sim.trades), 1)
        # units 20: half out at 110 (+100), half out at 90 (-100) -> R = 0
        self.assertAlmostEqual(sim.trades[0]["r"], 0.0, places=9)

    def test_time_stop(self):
        bars = [(100, 101, 99, 100, 10)] * 6
        a = make_pair(bars)
        sim = run({"A": a}, {"A": (0, 95.0)},
                  policy=ExitPolicy(time_stop_bars=2))
        self.assertEqual(len(sim.trades), 1)
        t = sim.trades[0]
        self.assertEqual(t["bars_held"], 2)
        self.assertEqual(t["exit_ts"], T0 + 3 * DAY)  # exit at open after 2 bars
        self.assertAlmostEqual(t["r"], 0.0, places=9)

    def test_max_positions_cap(self):
        bars = [(100, 101, 99, 100, 10)] * 4
        data = {f"P{k}": make_pair(bars) for k in range(7)}
        plan = {f"P{k}": (0, 95.0) for k in range(7)}
        sim = run(data, plan)
        self.assertEqual(len(sim.positions), 6)
        self.assertGreaterEqual(sim.skips["slots"], 1)

    def test_correlation_cap_same_day_batch(self):
        # three identical wiggly series -> corr 1.0; only 2 may enter
        import math
        bars = [(100 + math.sin(i) * 5,) * 4 + (10,) for i in range(40)]
        bars = [(o, o + 1, o - 1, o, 10) for (o, _, _, _, _) in bars]
        data = {p: make_pair(bars) for p in ("A", "B", "C")}
        plan = {p: (38, bars[38][3] * 0.9) for p in ("A", "B", "C")}
        sim = run(data, plan)
        self.assertEqual(len(sim.positions), 2)
        self.assertEqual(sim.skips["corr"], 1)

    def test_zero_volume_entry_cancelled(self):
        a = make_pair([(100, 101, 99, 100, 10), (100, 101, 99, 100, 0),
                       (100, 101, 99, 100, 10)])
        sim = run({"A": a}, {"A": (0, 95.0)})
        self.assertEqual(len(sim.positions), 0)
        self.assertEqual(len(sim.trades), 0)
        self.assertEqual(sim.skips["zero_volume"], 1)

    def test_regime_exit(self):
        bars = [(100, 101, 99, 100, 10)] * 5
        a = make_pair(bars)
        btc = bull_btc(5)
        btc["close"] = [100.0, 100.0, 85.0, 85.0, 85.0]  # < sma50 from i=2
        sim = Simulator({"A": a}, full_universe({"A": a}), btc, zero_cost,
                        FakeStrategy({"A": (0, 95.0)}), ExitPolicy())
        sim.run()
        self.assertEqual(len(sim.trades), 1)
        self.assertEqual(sim.trades[0]["exit_ts"], T0 + 3 * DAY)

    def test_costs_are_paid_both_ways(self):
        a = make_pair([(100, 101, 99, 100, 10), (100, 101, 93, 94, 10),
                       (93, 94, 92, 93, 10), (93, 94, 92, 93, 10)])
        sim = run({"A": a}, {"A": (0, 95.0)}, cost=lambda p: 0.001)
        t = sim.trades[0]
        # pnl = 20*93*0.999 - 20*100*1.001 = 1858.14 - 2002.0 = -143.86
        self.assertAlmostEqual(t["r"], -1.4386, places=6)


class Hyp001PlumbingTest(unittest.TestCase):
    def _mk(self):
        bars = [(100, 101, 99, 100, 10)] * 12
        data = {"A": make_pair(bars)}
        strat = Hyp001(data, full_universe(data))
        # neutralise the rule internals; drive arming/trigger by hand
        strat._trend_ok = lambda pair, d, i, year="": i == 3
        strat._pullback_ok = lambda pair, d, i, year="": i == 3
        strat.ind["A"]["ema50"] = [0.0] * 12
        return data, strat

    def test_arm_then_trigger(self):
        data, strat = self._mk()
        d = data["A"]
        d["high"][4] = 101.0
        d["close"][5] = 102.0   # close above prev high
        d["low"][2], d["low"][3], d["low"][4] = 97.0, 96.0, 96.5
        strat.ind["A"]["rsi"] = [50.0] * 5 + [55.0] + [50.0] * 6  # rsi up at 5
        n = 12
        sim = Simulator(data, full_universe(data), bull_btc(n), zero_cost,
                        strat, ExitPolicy())
        # walk closes manually
        out3 = strat.on_close(sim, "A", 3, d["ts"][3])
        self.assertIsNone(out3)
        self.assertIn("A", strat.armed)
        out4 = strat.on_close(sim, "A", 4, d["ts"][4])
        self.assertIsNone(out4)   # close 100 not > prev high 101
        out5 = strat.on_close(sim, "A", 5, d["ts"][5])
        self.assertIsNotNone(out5)
        self.assertEqual(out5.stop_px, 96.0)  # min low of bars 2..4

    def test_arm_expiry(self):
        data, strat = self._mk()
        d = data["A"]
        strat.ind["A"]["rsi"] = [50.0] * 12  # rsi never turns up -> no trigger
        n = 12
        sim = Simulator(data, full_universe(data), bull_btc(n), zero_cost,
                        strat, ExitPolicy())
        strat.on_close(sim, "A", 3, d["ts"][3])
        self.assertIn("A", strat.armed)
        for i in range(4, 10):
            strat.on_close(sim, "A", i, d["ts"][i])
        self.assertNotIn("A", strat.armed)  # expired after 5 bars


class ExperimentSmokeTest(unittest.TestCase):
    def test_end_to_end_smoke(self):
        """The full runner executes on synthetic data and writes a report."""
        import csv as _csv
        import random as _random
        import tempfile
        from engine import experiment

        rng = _random.Random(7)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ddir = root / "derived" / "okx" / "1d"
            ddir.mkdir(parents=True)
            for pair in ("BTC-USDT", "AAA-USDT", "BBB-USDT"):
                px, rows = 100.0, []
                for i in range(400):
                    o = px
                    c = px * (1 + 0.001 + rng.uniform(-0.03, 0.03))
                    h = max(o, c) * (1 + rng.uniform(0, 0.01))
                    l = min(o, c) * (1 - rng.uniform(0, 0.01))
                    rows.append((T0 + i * DAY, o, h, l, c,
                                 1000 + rng.uniform(0, 100)))
                    px = c
                with (ddir / f"{pair}.csv").open("w", newline="") as f:
                    w = _csv.writer(f)
                    w.writerow(["timestamp", "open", "high", "low", "close",
                                "volume"])
                    for r in rows:
                        w.writerow(r)
            uni = root / "universe.csv"
            with uni.open("w", newline="") as f:
                w = _csv.writer(f)
                w.writerow(["date", "symbol", "rank", "score_quote_vol",
                            "in_universe"])
                for i in range(400):
                    for pair in ("BTC-USDT", "AAA-USDT", "BBB-USDT"):
                        w.writerow([experiment.day(T0 + i * DAY), pair, 1,
                                    1000, 1])
            out = root / "EXP-001.md"
            costs = Path(__file__).resolve().parents[1] / "costs.yaml"
            experiment.main(["--data", str(ddir), "--universe", str(uni),
                             "--costs", str(costs), "--out", str(out)])
            self.assertTrue(out.exists())
            text = out.read_text()
            self.assertIn("EXP-001", text)
            self.assertIn("holdout SEALED", text)

    def test_wrong_unlock_phrase_refused(self):
        from engine import experiment
        with self.assertRaises(SystemExit):
            experiment.main(["--unlock-holdout", "wrong-phrase"])


class HoldoutGuardTest(unittest.TestCase):
    def test_loader_drops_holdout_bars(self):
        import csv as _csv
        import tempfile
        from engine.protocol import HOLDOUT_START_MS
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "BTC-USDT.csv"
            with p.open("w", newline="") as f:
                w = _csv.writer(f)
                w.writerow(["timestamp", "open", "high", "low", "close", "volume"])
                w.writerow([HOLDOUT_START_MS - DAY, 1, 1, 1, 1, 1])
                w.writerow([HOLDOUT_START_MS, 2, 2, 2, 2, 2])       # sealed
                w.writerow([HOLDOUT_START_MS + DAY, 3, 3, 3, 3, 3])  # sealed
            data = load_daily_dir(Path(td), HOLDOUT_START_MS)
            self.assertEqual(len(data["BTC-USDT"]["ts"]), 1)


if __name__ == "__main__":
    unittest.main()
