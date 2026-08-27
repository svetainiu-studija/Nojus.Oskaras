import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.hyp003 import Hyp003, policy
from engine.simulator import Simulator, ExitPolicy, EntryIntent

DAY = 86_400_000
T0 = 1_609_459_200_000


def make_pair(bars):
    cols = {"ts": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
    for i, (o, h, l, c, v) in enumerate(bars):
        cols["ts"].append(T0 + i * DAY)
        for k, val in zip(("open", "high", "low", "close", "volume"),
                          (o, h, l, c, v)):
            cols[k].append(float(val))
    return cols


class FakeSim:
    def __init__(self, data):
        self.data = data


class Hyp003PlumbingTest(unittest.TestCase):
    def _mk(self):
        bars = [(100, 101, 99, 100, 10)] * 12
        data = {"A": make_pair(bars)}
        universe = {(ts, "A") for ts in data["A"]["ts"]}
        strat = Hyp003(data, universe)
        strat.ind["A"]["ema20"] = [110.0] * 12  # partial target above price
        return data, universe, strat

    def test_arm_trigger_and_partial_target(self):
        data, universe, strat = self._mk()
        d = data["A"]
        # capitulation at i=3: cap_low 80, midpoint (96+80)/2 = 88
        strat._cap_ok = lambda pair, dd, i, year="": (80.0, 88.0) if i == 3 else None
        d["high"][4] = 89.0
        d["close"][4] = 87.0            # above cap_low, below midpoint: no trigger
        d["close"][5] = 90.0            # > prev high 89 and > midpoint 88 -> trigger
        sim = FakeSim(data)
        self.assertIsNone(strat.on_close(sim, "A", 3, d["ts"][3]))
        self.assertIn("A", strat.armed)
        self.assertIsNone(strat.on_close(sim, "A", 4, d["ts"][4]))
        intent = strat.on_close(sim, "A", 5, d["ts"][5])
        self.assertIsNotNone(intent)
        self.assertEqual(intent.stop_px, 80.0)
        self.assertEqual(intent.partial_px, 110.0)   # EMA20 at trigger (I3)

    def test_setup_broken_by_close_below_cap_low(self):
        data, universe, strat = self._mk()
        d = data["A"]
        strat._cap_ok = lambda pair, dd, i, year="": (80.0, 88.0) if i == 3 else None
        d["close"][4] = 79.0            # closes below the capitulation low
        sim = FakeSim(data)
        strat.on_close(sim, "A", 3, d["ts"][3])
        strat.on_close(sim, "A", 4, d["ts"][4])
        self.assertNotIn("A", strat.armed)

    def test_policy_matches_hypothesis(self):
        p = policy()
        self.assertEqual(p.stop_mode, "resting_stop")
        self.assertEqual(p.time_stop_bars, 7)
        self.assertEqual(p.trail_lookback, 5)
        self.assertEqual(p.trail_mode, "after_partial")
        self.assertEqual(p.partial_frac, 0.5)


class PartialTargetTest(unittest.TestCase):
    def test_partial_fills_at_ema20_when_below_2R(self):
        # entry 100, stop 90 -> 2R target 120; intent partial_px 105 -> use 105
        bars = [(100, 101, 99, 100, 10), (100, 101, 99, 100, 10),
                (104, 106, 103, 104, 10), (104, 105, 89, 90, 10),
                (90, 91, 89, 90, 10), (90, 91, 89, 90, 10)]
        data = {"A": make_pair(bars)}
        universe = {(ts, "A") for ts in data["A"]["ts"]}
        btc = {"ts_index": {T0 + i * DAY: i for i in range(6)},
               "close": [100.0] * 6, "sma50": [90.0] * 6, "sma200": [80.0] * 6}

        class OneShot:
            max_stop_frac = 0.5

            def on_close(self, sim, pair, i, ts):
                if i == 0:
                    return EntryIntent(pair=pair, stop_px=90.0, signal_i=0,
                                       partial_px=105.0)
                return None

        sim = Simulator(data, universe, btc, lambda p: 0.0, OneShot(),
                        ExitPolicy(stop_mode="resting_stop"))
        sim.run()
        self.assertEqual(len(sim.trades), 1)
        t = sim.trades[0]
        # units = 100/10 = 10; half out at 105 (+25), half stopped at 90 (-50)
        self.assertAlmostEqual(t["r"], -0.25, places=9)

    def test_max_positions_override(self):
        bars = [(100, 101, 99, 100, 10)] * 4
        data = {f"P{k}": make_pair(bars) for k in range(4)}
        universe = {(ts, p) for p, d in data.items() for ts in d["ts"]}
        btc = {"ts_index": {T0 + i * DAY: i for i in range(4)},
               "close": [100.0] * 4, "sma50": [90.0] * 4, "sma200": [80.0] * 4}

        class All:
            max_stop_frac = 0.5

            def on_close(self, sim, pair, i, ts):
                if i == 0:
                    return EntryIntent(pair=pair, stop_px=95.0, signal_i=0)
                return None

        sim = Simulator(data, universe, btc, lambda p: 0.0, All(),
                        ExitPolicy(), max_positions=2)
        sim.run()
        self.assertEqual(len(sim.positions), 2)


if __name__ == "__main__":
    unittest.main()
