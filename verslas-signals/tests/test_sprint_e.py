import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.hyp004 import config_hash
from engine.sprint_e import (concentration, BASELINE_SIMS, MAX_TOP_PAIR_SHARE,
                             MIN_TRADES)


def t(pair, r):
    return {"pair": pair, "r": r}


class FrozenConfigTest(unittest.TestCase):
    def test_hash_matches_exp005(self):
        # D-022: HYP-006 runs HYP-004 byte-frozen. Any PARAMS edit breaks
        # this and voids the round.
        self.assertEqual(config_hash(), "0e4dc9e0453a")

    def test_preregistered_constants(self):
        # NOTES-SPRINT-E.md decision rule, checks 1/5/6
        self.assertEqual(MIN_TRADES, 30)
        self.assertEqual(BASELINE_SIMS, 2000)
        self.assertEqual(MAX_TOP_PAIR_SHARE, 0.50)


class ConcentrationTest(unittest.TestCase):
    def test_top_share_and_ex_top_expectancy(self):
        trades = [t("SOL-USDT", 3.0), t("SOL-USDT", 1.0),
                  t("ETH-USDT", 0.5), t("BTC-USDT", -0.5),
                  t("LINK-USDT", 1.0)]
        top, share, ex = concentration(trades)
        self.assertEqual(top, "SOL-USDT")
        self.assertAlmostEqual(share, 4.0 / 5.0)   # 4 R of 5 R total
        self.assertAlmostEqual(ex, 1.0 / 3.0)      # (0.5 - 0.5 + 1.0) / 3

    def test_losing_pairs_do_not_dilute_top_r(self):
        # share is top-pair R over summed per-pair R; a deeply negative pair
        # shrinks the denominator and INCREASES the share (conservative)
        trades = [t("A", 1.0), t("B", -0.5)]
        _, share, _ = concentration(trades)
        self.assertAlmostEqual(share, 2.0)

    def test_nonpositive_total_gives_no_share(self):
        top, share, ex = concentration([t("A", 0.5), t("B", -1.0)])
        self.assertEqual(top, "A")
        self.assertIsNone(share)              # share undefined at a net loss
        self.assertAlmostEqual(ex, -1.0)

    def test_empty_and_single_pair(self):
        self.assertEqual(concentration([]), (None, None, None))
        top, share, ex = concentration([t("A", 1.0)])
        self.assertEqual(top, "A")
        self.assertAlmostEqual(share, 1.0)
        self.assertIsNone(ex)                 # no ex-top trades exist


if __name__ == "__main__":
    unittest.main()
