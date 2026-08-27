"""AUDIT-2026-08 A3: adversarial no-look-ahead property tests.

Every indicator value at bar i, and every entry decision at close i, must
be invariant to arbitrary mutation of bars > i. A failure here is a
verified error under the audit protocol.
"""
import random
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.indicators import sma, ema, rsi, rolling_max, rolling_min, atr, pct_return
from engine.hyp004 import Hyp004

DAY = 86_400_000
T0 = 1_609_459_200_000
CUT = 80  # decision bar; everything after it gets mutated


def mutate_tail(xs, rng, factor=50.0):
    out = list(xs)
    for i in range(CUT + 1, len(out)):
        out[i] = rng.uniform(0.001, factor) * out[i]
    return out


class IndicatorLookAheadTest(unittest.TestCase):
    def setUp(self):
        rng = random.Random(7)
        n = 120
        self.closes = [100.0]
        for _ in range(n - 1):
            self.closes.append(self.closes[-1] * rng.uniform(0.93, 1.08))
        self.highs = [c * 1.02 for c in self.closes]
        self.lows = [c * 0.98 for c in self.closes]
        self.mut = random.Random(11)

    def assert_prefix_invariant(self, fn_name, orig, mutated):
        for i in range(CUT + 1):
            a, b = orig[i], mutated[i]
            if a is None or b is None:
                self.assertEqual(a, b, f"{fn_name}[{i}] None-ness changed")
            else:
                self.assertAlmostEqual(a, b, places=9,
                                       msg=f"{fn_name}[{i}] depends on bars > {CUT}")

    def test_single_series_indicators(self):
        cases = [("sma", lambda xs: sma(xs, 20)), ("ema", lambda xs: ema(xs, 20)),
                 ("rsi", lambda xs: rsi(xs, 14)),
                 ("rolling_max", lambda xs: rolling_max(xs, 20)),
                 ("rolling_min", lambda xs: rolling_min(xs, 10)),
                 ("pct_return", lambda xs: pct_return(xs, 60))]
        mutated = mutate_tail(self.closes, self.mut)
        for name, fn in cases:
            self.assert_prefix_invariant(name, fn(self.closes), fn(mutated))

    def test_atr(self):
        mh = mutate_tail(self.highs, self.mut)
        ml = mutate_tail(self.lows, self.mut)
        mc = mutate_tail(self.closes, self.mut)
        self.assert_prefix_invariant("atr", atr(self.highs, self.lows, self.closes, 14),
                                     atr(mh, ml, mc, 14))


class Hyp004DecisionLookAheadTest(unittest.TestCase):
    """The entry intent produced at close CUT must not change when the
    future is rewritten (the strategy precomputes indicators at init, so a
    fresh instance is built over each dataset)."""

    def _pair(self, closes, volumes):
        n = len(closes)
        return {"ts": [T0 + i * DAY for i in range(n)], "open": list(closes),
                "high": [c * 1.01 for c in closes],
                "low": [c * 0.99 for c in closes],
                "close": list(closes), "volume": list(volumes)}

    def test_intent_invariant_to_future(self):
        n = 120
        closes = [100.0 + 0.1 * i for i in range(n)]
        closes[CUT] = closes[CUT - 1] * 1.05          # breakout at the cut
        volumes = [10.0] * n
        volumes[CUT] = 40.0
        btc = self._pair([100.0] * n, [10.0] * n)

        def build(mut_seed):
            x_c, x_v = list(closes), list(volumes)
            if mut_seed is not None:
                rng = random.Random(mut_seed)
                for i in range(CUT + 1, n):
                    x_c[i] = rng.uniform(0.5, 200.0)
                    x_v[i] = rng.uniform(0.0, 500.0)
            data = {"BTC-USDT": btc, "X-USDT": self._pair(x_c, x_v)}
            universe = {(ts, "X-USDT") for ts in data["X-USDT"]["ts"]}
            return data, Hyp004(data, universe)

        class FakeSim:
            def __init__(self, data):
                self.data = data

        data0, strat0 = build(None)
        base = strat0.on_close(FakeSim(data0), "X-USDT", CUT,
                               data0["X-USDT"]["ts"][CUT])
        self.assertIsNotNone(base, "test setup must trigger an entry at CUT")
        for seed in (1, 2, 3):
            data1, strat1 = build(seed)
            got = strat1.on_close(FakeSim(data1), "X-USDT", CUT,
                                  data1["X-USDT"]["ts"][CUT])
            self.assertIsNotNone(got, f"future mutation (seed {seed}) killed the entry")
            self.assertAlmostEqual(got.stop_px, base.stop_px, places=9,
                                   msg=f"stop depends on the future (seed {seed})")


if __name__ == "__main__":
    unittest.main()
