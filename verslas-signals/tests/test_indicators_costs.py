import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.indicators import sma, ema, rsi, rolling_max, rolling_min, pct_return
from engine.costs import CostModel


class IndicatorTest(unittest.TestCase):
    def test_sma(self):
        self.assertEqual(sma([1, 2, 3, 4, 5], 3), [None, None, 2.0, 3.0, 4.0])

    def test_ema_seed_and_recursion(self):
        # n=3: seed = sma(1,2,3) = 2 at index 2; k = 0.5
        # idx3 = 4*0.5 + 2*0.5 = 3; idx4 = 5*0.5 + 3*0.5 = 4
        self.assertEqual(ema([1, 2, 3, 4, 5], 3), [None, None, 2.0, 3.0, 4.0])

    def test_rsi_extremes_and_flat(self):
        up = list(range(1, 20))
        self.assertEqual(rsi(up, 14)[14], 100.0)
        down = list(range(20, 1, -1))
        self.assertEqual(rsi(down, 14)[14], 0.0)
        flat = [5.0] * 20
        self.assertEqual(rsi(flat, 14)[14], 50.0)

    def test_rsi_mixed_hand_computed(self):
        # n=2 over [1, 2, 1.5, 3]: at i=2 avg_gain=0.5 avg_loss=0.25 -> RSI 66.67
        # at i=3: avg_gain=(0.5+1.5)/2=1.0, avg_loss=0.25/2=0.125 -> RSI 88.89
        r = rsi([1.0, 2.0, 1.5, 3.0], 2)
        self.assertAlmostEqual(r[2], 100 - 100 / (1 + 0.5 / 0.25), places=6)
        self.assertAlmostEqual(r[3], 100 - 100 / (1 + 1.0 / 0.125), places=6)

    def test_rolling_max_min(self):
        xs = [1, 3, 2, 5, 4]
        self.assertEqual(rolling_max(xs, 2), [None, 3, 3, 5, 5])
        self.assertEqual(rolling_min(xs, 2), [None, 1, 2, 2, 4])

    def test_no_lookahead(self):
        # value at index i must not change when future values are appended
        xs = [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0]
        for fn in (lambda v: sma(v, 3), lambda v: ema(v, 3), lambda v: rsi(v, 3),
                   lambda v: rolling_max(v, 3), lambda v: rolling_min(v, 3),
                   lambda v: pct_return(v, 3)):
            full = fn(xs)
            trunc = fn(xs[:5])
            self.assertEqual(full[:5], trunc)

    def test_pct_return(self):
        r = pct_return([100, 110, 121], 1)
        self.assertIsNone(r[0])
        self.assertAlmostEqual(r[1], 0.10)
        self.assertAlmostEqual(r[2], 0.10)


class CostModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cm = CostModel.from_yaml(Path(__file__).resolve().parents[1] / "costs.yaml")

    def test_tier_resolution(self):
        self.assertEqual(self.cm.tier("BTC/USDT"), "tier1")
        self.assertEqual(self.cm.tier("SOL/USDT"), "tier2")
        self.assertEqual(self.cm.tier("GRT/USDT"), "tier3")  # unlisted -> tier3

    def test_round_trip_okx_btc(self):
        # taker 0.10% + half-spread 1bp + slippage 2bp = 0.13% one-way -> 0.26% RT
        self.assertAlmostEqual(
            self.cm.round_trip_fraction("okx", "BTC/USDT"), 0.0026, places=10)
        self.assertAlmostEqual(
            self.cm.round_trip_fraction("okx", "BTC/USDT", stress=True), 0.0052, places=10)

    def test_round_trip_tier3(self):
        # taker 0.10% + half-spread 8bp + slippage 2bp = 0.20% one-way -> 0.40% RT
        self.assertAlmostEqual(
            self.cm.round_trip_fraction("okx", "GRT/USDT"), 0.0040, places=10)

    def test_large_orders_refused(self):
        with self.assertRaises(ValueError):
            self.cm.one_way_fraction("okx", "BTC/USDT", size="large")


if __name__ == "__main__":
    unittest.main()
