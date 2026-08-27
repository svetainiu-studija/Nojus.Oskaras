import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.indicators import atr
from engine.hyp004 import Hyp004, policy
from engine.sprint_d import expand_universe

DAY = 86_400_000
T0 = 1_609_459_200_000
H4 = 14_400_000


def make_pair(closes, volumes=None, spread=1.0, ts_step=DAY):
    n = len(closes)
    volumes = volumes or [10.0] * n
    return {"ts": [T0 + i * ts_step for i in range(n)],
            "open": list(closes),
            "high": [c + spread for c in closes],
            "low": [c - spread for c in closes],
            "close": list(closes), "volume": volumes}


class FakeSim:
    def __init__(self, data):
        self.data = data


class AtrTest(unittest.TestCase):
    def test_atr_hand_computed(self):
        # constant true range: high-low = 2 every bar, no gaps -> ATR = 2
        closes = [100.0] * 20
        highs = [101.0] * 20
        lows = [99.0] * 20
        a = atr(highs, lows, closes, 14)
        self.assertIsNone(a[13])
        self.assertAlmostEqual(a[14], 2.0)
        self.assertAlmostEqual(a[19], 2.0)

    def test_atr_gap_counts(self):
        # a gap day increases TR via |high - prev_close|
        closes = [100.0] * 15 + [120.0] * 5
        highs = [c + 1 for c in closes]
        lows = [c - 1 for c in closes]
        a = atr(highs, lows, closes, 14)
        self.assertGreater(a[15], a[14])  # the 21-point gap raised the ATR


class Hyp004Test(unittest.TestCase):
    def _build(self):
        n = 90
        btc = make_pair([100.0] * n)
        x_closes = [100.0 + 0.1 * i for i in range(n)]
        x_closes[80] = x_closes[79] * 1.04
        x_vol = [10.0] * n
        x_vol[80] = 30.0
        x = make_pair(x_closes, x_vol)
        data = {"BTC-USDT": btc, "X-USDT": x}
        universe = {(ts, "X-USDT") for ts in x["ts"]}
        return data, universe

    def test_atr_stop_and_trigger(self):
        data, universe = self._build()
        strat = Hyp004(data, universe)
        sim = FakeSim(data)
        i = 80
        intent = strat.on_close(sim, "X-USDT", i, data["X-USDT"]["ts"][i])
        self.assertIsNotNone(intent)
        expected_stop = data["X-USDT"]["close"][i] - 2.0 * strat.ind["X-USDT"]["atr"][i]
        self.assertAlmostEqual(intent.stop_px, expected_stop)
        # stop is volatility-scaled, not a structural low
        self.assertGreater(intent.stop_px, 0)

    def test_policy(self):
        p = policy()
        self.assertEqual(p.stop_mode, "resting_stop")
        self.assertEqual(p.time_stop_bars, 15)
        self.assertEqual(p.trail_mode, "after_r")


class UniverseExpansionTest(unittest.TestCase):
    def test_daily_membership_applies_to_4h_bars(self):
        bars_4h = make_pair([100.0] * 12, ts_step=H4)  # two UTC days
        data = {"A": bars_4h}
        daily_universe = {(T0, "A")}                   # only day 1 in-universe
        u = expand_universe(daily_universe, data)
        day1 = [ts for ts in bars_4h["ts"] if ts < T0 + DAY]
        day2 = [ts for ts in bars_4h["ts"] if ts >= T0 + DAY]
        for ts in day1:
            self.assertIn((ts, "A"), u)
        for ts in day2:
            self.assertNotIn((ts, "A"), u)


if __name__ == "__main__":
    unittest.main()
