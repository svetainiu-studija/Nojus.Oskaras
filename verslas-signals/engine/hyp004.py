"""HYP-004 / HYP-005: momentum leaders with ATR-scaled stops.

One strategy class for both — HYP-004 runs it on daily bars, HYP-005 on 4h
bars with bar-parity windows (NOTES-SPRINT-D.md, I3). Entry/RS logic follows
HYP-002; the stop is signal-close − 2×ATR(14), fixing round 1's finding 3.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone

from .indicators import sma, ema, atr
from .simulator import EntryIntent

PARAMS = {
    "rs_lookback": 60, "rs_top_n": 5,
    "breakout_lookback": 20, "volume_mult": 1.5, "vol_sma": 20,
    "max_above_ema20": 0.15, "ema_fast": 20,
    "atr_n": 14, "atr_mult": 2.0,
    "max_stop_frac": 0.25,     # sanity guard only (I2), skip count reported
    "rs_exit_fraction": 0.5,
}


def config_hash():
    return hashlib.sha256(
        json.dumps(PARAMS, sort_keys=True).encode()).hexdigest()[:12]


def _year(ts):
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).year


class Hyp004:
    max_stop_frac = PARAMS["max_stop_frac"]

    def __init__(self, data, universe):
        self.universe = universe
        self.funnel = Counter()
        self.ind = {}
        for pair, d in data.items():
            self.ind[pair] = {
                "ema20": ema(d["close"], PARAMS["ema_fast"]),
                "volsma": sma(d["volume"], PARAMS["vol_sma"]),
                "atr": atr(d["high"], d["low"], d["close"], PARAMS["atr_n"]),
            }
        btc = data["BTC-USDT"]
        btc_idx = {ts: i for i, ts in enumerate(btc["ts"])}
        n = PARAMS["rs_lookback"]

        def retn(d_, i):
            if i is None or i < n or d_["close"][i - n] == 0:
                return None
            return d_["close"][i] / d_["close"][i - n] - 1.0

        per_day = {}
        for pair, d in data.items():
            for i, ts in enumerate(d["ts"]):
                if (ts, pair) not in universe:
                    continue
                r = retn(d, i)
                rb = retn(btc, btc_idx.get(ts))
                if r is None or rb is None:
                    continue
                per_day.setdefault(ts, []).append((r - rb, pair))
        self.top_n = set()
        self.top_half = set()
        for ts, lst in per_day.items():
            lst.sort(reverse=True)
            for rank, (_, pair) in enumerate(lst, start=1):
                if rank <= PARAMS["rs_top_n"]:
                    self.top_n.add((ts, pair))
                if rank <= max(1, int(len(lst) * PARAMS["rs_exit_fraction"])):
                    self.top_half.add((ts, pair))

    def on_close(self, sim, pair, i, ts):
        d = sim.data[pair]
        if (ts, pair) not in self.universe:
            return None
        year = _year(ts)
        ind = self.ind[pair]
        lb = PARAMS["breakout_lookback"]
        if i < lb or ind["ema20"][i] is None or ind["volsma"][i - 1] is None \
                or ind["atr"][i] is None:
            self.funnel[f"{year}:warmup"] += 1
            return None
        if (ts, pair) not in self.top_n:
            self.funnel[f"{year}:not_leader"] += 1
            return None
        close = d["close"][i]
        if close <= max(d["close"][i - lb:i]):
            self.funnel[f"{year}:no_breakout"] += 1
            return None
        if d["volume"][i] < PARAMS["volume_mult"] * ind["volsma"][i - 1]:
            self.funnel[f"{year}:volume_weak"] += 1
            return None
        if close >= ind["ema20"][i] * (1 + PARAMS["max_above_ema20"]):
            self.funnel[f"{year}:too_extended"] += 1
            return None
        self.funnel[f"{year}:triggered"] += 1
        stop = close - PARAMS["atr_mult"] * ind["atr"][i]     # I1
        if stop <= 0:
            return None
        return EntryIntent(pair=pair, stop_px=stop, signal_i=i)

    def wants_exit(self, sim, pair, i, ts):
        return (ts, pair) not in self.top_half


def policy():
    from .simulator import ExitPolicy
    return ExitPolicy(partial_frac=1.0 / 3.0, partial_r=3.0,
                      trail_lookback=10, trail_mode="after_r",
                      trail_after_r=1.0, time_stop_bars=15,
                      time_stop_skip_if_r=1.0, regime_exit=True,
                      stop_mode="resting_stop")
