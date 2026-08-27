"""Cost model (WP2): loads costs.yaml and prices a round trip per pair.

Every simulated trade pays: taker fee + half-spread + slippage, on entry AND
exit (one_way * 2). Daily-strategy position sizes at our capital are far below
0.1% of bar volume, so the "small" slippage tier applies; the backtester must
assert order size stays under that bound. Stress runs multiply the whole
round trip by stress_multiplier (protocol step 4).
"""
from pathlib import Path

import yaml


class CostModel:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.stress_multiplier = float(cfg["stress_multiplier"])
        tiers = cfg.get("tiers", {})
        self._tier_of = {}
        for tier_name, pairs in tiers.items():
            for p in pairs:
                self._tier_of[p] = tier_name

    @classmethod
    def from_yaml(cls, path="costs.yaml"):
        return cls(yaml.safe_load(Path(path).read_text()))

    def tier(self, pair: str) -> str:
        return self._tier_of.get(pair, "tier3")

    def one_way_fraction(self, exchange: str, pair: str, size: str = "small") -> float:
        ex = self.cfg["exchanges"][exchange]
        fee = float(ex["taker_fee"])
        half_spread = float(self.cfg["spread_bps"][self.tier(pair)]) / 10_000
        slip_bps = self.cfg["slippage_bps"][size]
        if slip_bps is None:
            raise ValueError(f"slippage tier {size!r} is un-modelled by design — "
                             "orders that large must not be simulated")
        return fee + half_spread + float(slip_bps) / 10_000

    def round_trip_fraction(self, exchange: str, pair: str,
                            size: str = "small", stress: bool = False) -> float:
        rt = 2.0 * self.one_way_fraction(exchange, pair, size)
        return rt * self.stress_multiplier if stress else rt

    def min_order_usd(self, exchange: str) -> float:
        return float(self.cfg["exchanges"][exchange]["min_order_usd"])
