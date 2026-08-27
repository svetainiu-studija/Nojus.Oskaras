"""HYP-003: capitulation reclaim inside an intact uptrend (with-trend
reversal). Faithful translation of research/hypotheses/HYP-003.md;
interpretation choices I1–I4 are declared in NOTES-SPRINT-C.md.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone

from .indicators import sma, ema, rsi, rolling_min
from .simulator import EntryIntent

PARAMS = {
    "ema_trend": 200, "ema_target": 20,
    "drop_pct": 0.15, "drop_window": 5, "low_lookback": 30,
    "volume_mult": 2.0, "vol_sma": 20, "rsi_n": 14, "rsi_max": 30,
    "trigger_window": 5, "max_stop_frac": 0.10,
}


def config_hash():
    return hashlib.sha256(
        json.dumps(PARAMS, sort_keys=True).encode()).hexdigest()[:12]


def _year(ts):
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).year


class Hyp003:
    max_stop_frac = PARAMS["max_stop_frac"]

    def __init__(self, data, universe):
        self.universe = universe
        self.funnel = Counter()
        self.ind = {}
        for pair, d in data.items():
            close, vol, low = d["close"], d["volume"], d["low"]
            self.ind[pair] = {
                "ema20": ema(close, PARAMS["ema_target"]),
                "ema200": ema(close, PARAMS["ema_trend"]),
                "rsi": rsi(close, PARAMS["rsi_n"]),
                "volsma": sma(vol, PARAMS["vol_sma"]),
                "low30": rolling_min(low, PARAMS["low_lookback"]),
            }
        self.armed = {}  # pair -> (armed_at_i, cap_low, cap_mid)

    def _cap_ok(self, pair, d, i, year=""):
        """Is bar i a capitulation bar? Returns (cap_low, cap_mid) or None."""
        ind = self.ind[pair]
        if ind["ema200"][i] is None or ind["volsma"][i - 1] is None \
                or ind["rsi"][i] is None or ind["low30"][i] is None:
            self.funnel[f"{year}:warmup"] += 1
            return None
        if d["close"][i] <= ind["ema200"][i]:
            self.funnel[f"{year}:below_ema200"] += 1
            return None
        w = PARAMS["drop_window"]
        high_ref = max(d["high"][max(0, i - w):i])          # I1
        if high_ref <= 0 or (high_ref - d["low"][i]) / high_ref < PARAMS["drop_pct"]:
            self.funnel[f"{year}:no_flush"] += 1
            return None
        if d["low"][i] > ind["low30"][i]:                    # must BE the 30d low
            self.funnel[f"{year}:not_30d_low"] += 1
            return None
        if d["volume"][i] < PARAMS["volume_mult"] * ind["volsma"][i - 1]:  # I2
            self.funnel[f"{year}:volume_weak"] += 1
            return None
        if self.ind[pair]["rsi"][i] >= PARAMS["rsi_max"]:
            self.funnel[f"{year}:rsi_not_oversold"] += 1
            return None
        self.funnel[f"{year}:capitulation"] += 1
        return d["low"][i], (d["high"][i] + d["low"][i]) / 2.0

    def on_close(self, sim, pair, i, ts):
        d = sim.data[pair]
        if (ts, pair) not in self.universe:
            self.armed.pop(pair, None)
            return None
        year = _year(ts)

        armed = self.armed.get(pair)
        if armed is not None:
            armed_at, cap_low, cap_mid = armed
            if d["close"][i] < cap_low:                      # I4: setup broken
                self.funnel[f"{year}:setup_broken"] += 1
                self.armed.pop(pair, None)
            elif i - armed_at > PARAMS["trigger_window"]:
                self.funnel[f"{year}:arm_expired"] += 1
                self.armed.pop(pair, None)
            elif (i >= 1 and d["close"][i] > d["high"][i - 1]
                  and d["close"][i] > cap_mid):
                self.armed.pop(pair, None)
                self.funnel[f"{year}:triggered"] += 1
                ema20 = self.ind[pair]["ema20"][i]           # I3
                return EntryIntent(pair=pair, stop_px=cap_low, signal_i=i,
                                   partial_px=ema20)
            return None

        cap = self._cap_ok(pair, d, i, year) if i >= 1 else None
        if cap is not None:
            self.armed[pair] = (i, cap[0], cap[1])
        return None


def policy():
    from .simulator import ExitPolicy
    return ExitPolicy(partial_frac=0.5, partial_r=2.0,
                      trail_mode="after_partial", trail_lookback=5,
                      time_stop_bars=7, regime_exit=True,
                      stop_mode="resting_stop")
