import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.hyp002 import Hyp002, policy

DAY = 86_400_000
T0 = 1_609_459_200_000


def make_pair(closes, volumes=None, lows=None):
    n = len(closes)
    volumes = volumes or [10.0] * n
    lows = lows or [c - 1 for c in closes]
    return {"ts": [T0 + i * DAY for i in range(n)],
            "open": list(closes), "high": [c + 1 for c in closes],
            "low": lows, "close": list(closes), "volume": volumes}


class FakeSim:
    def __init__(self, data):
        self.data = data


class Hyp002Test(unittest.TestCase):
    def _build(self):
        n = 80
        btc = make_pair([100.0] * n)                        # flat BTC
        x_closes = [100.0 + 0.1 * i for i in range(n)]      # steady leader
        x_closes[70] = x_closes[69] * 1.04                  # breakout at i=70
        x_vol = [10.0] * n
        x_vol[70] = 30.0                                    # 3x prior average
        x = make_pair(x_closes, x_vol, lows=[c - 2 for c in x_closes])
        y = make_pair([100.0 - 0.1 * i for i in range(n)])  # steady laggard
        data = {"BTC-USDT": btc, "X-USDT": x, "Y-USDT": y}
        universe = {(ts, p) for p in ("X-USDT", "Y-USDT") for ts in x["ts"]}
        return data, universe

    def test_rs_ranking(self):
        data, universe = self._build()
        strat = Hyp002(data, universe)
        ts = data["X-USDT"]["ts"][70]
        self.assertIn((ts, "X-USDT"), strat.top_n)
        # top half of 2 ranked pairs = 1 pair -> the laggard is out
        self.assertIn((ts, "X-USDT"), strat.top_half)
        self.assertNotIn((ts, "Y-USDT"), strat.top_half)

    def test_breakout_trigger_and_stop(self):
        data, universe = self._build()
        strat = Hyp002(data, universe)
        sim = FakeSim(data)
        intent = strat.on_close(sim, "X-USDT", 70, data["X-USDT"]["ts"][70])
        self.assertIsNotNone(intent)
        # stop = 10-day rolling low = close[61]-2 area
        self.assertAlmostEqual(intent.stop_px,
                               min(data["X-USDT"]["low"][61:71]))
        # no breakout the day before (no volume spike, no new high)
        self.assertIsNone(
            strat.on_close(sim, "X-USDT", 69, data["X-USDT"]["ts"][69]))

    def test_laggard_wants_exit(self):
        data, universe = self._build()
        strat = Hyp002(data, universe)
        sim = FakeSim(data)
        ts = data["Y-USDT"]["ts"][70]
        self.assertTrue(strat.wants_exit(sim, "Y-USDT", 70, ts))
        self.assertFalse(strat.wants_exit(sim, "X-USDT", 70, ts))

    def test_policy_matches_hypothesis(self):
        p = policy()
        self.assertEqual(p.stop_mode, "resting_stop")
        self.assertEqual(p.time_stop_bars, 15)
        self.assertEqual(p.time_stop_skip_if_r, 1.0)
        self.assertAlmostEqual(p.partial_frac, 1 / 3)
        self.assertEqual(p.partial_r, 3.0)
        self.assertEqual(p.trail_mode, "after_r")


if __name__ == "__main__":
    unittest.main()
