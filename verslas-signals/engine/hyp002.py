"""HYP-002: relative-strength leaders bought on a volume-confirmed
20-day-high breakout. Faithful translation of research/hypotheses/HYP-002.md;
interpretation choices I1–I3 are declared in NOTES-SPRINT-B.md.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone

from .indicators import sma, ema, rolling_min
from .simulator import EntryIntent

PARAMS = {
    "rs_lookback": 60, "rs_top_n": 5,
    "breakout_lookback": 20, "volume_mult": 1.5, "vol_sma": 20,
    "max_above_ema20": 0.15, "ema_fast": 20,
    "stop_lookback": 10, "max_stop_frac": 0.10,
    "rs_exit_fraction": 0.5,   # exit when rank falls out of the top half
}


def config_hash():
    return hashlib.sha256(
        json.dumps(PARAMS, sort_keys=True).encode()).hexdigest()[:12]


def _year(ts):
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).year


class Hyp002:
    max_stop_frac = PARAMS["max_stop_frac"]

    def __init__(self, data, universe):
        self.universe = universe
        self.funnel = Counter()
        self.ind = {}
        for pair, d in data.items():
            close, vol, low = d["close"], d["volume"], d["low"]
            self.ind[pair] = {
                "ema20": ema(close, PARAMS["ema_fast"]),
                "volsma": sma(vol, PARAMS["vol_sma"]),
                "low10": rolling_min(low, PARAMS["stop_lookback"]),
            }
        # relative strength vs BTC: 60-day return minus BTC's, ranked per day
        # among universe-eligible pairs (I3)
        btc = data["BTC-USDT"]
        btc_idx = {ts: i for i, ts in enumerate(btc["ts"])}
        n = PARAMS["rs_lookback"]

        def ret60(d_, i):
            if i < n or d_["close"][i - n] == 0:
                return None
            return d_["close"][i] / d_["close"][i - n] - 1.0

        per_day = {}
        for pair, d in data.items():
            for i, ts in enumerate(d["ts"]):
                if (ts, pair) not in universe:
                    continue
                bi = btc_idx.get(ts)
                r = ret60(d, i)
                rb = ret60(btc, bi) if bi is not None else None
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
        lb = PARAMS["breakout_lookback"]
        if i < lb or self.ind[pair]["ema20"][i] is None \
                or self.ind[pair]["volsma"][i - 1] is None:
            self.funnel[f"{year}:warmup"] += 1
            return None
        if (ts, pair) not in self.top_n:
            self.funnel[f"{year}:not_leader"] += 1
            return None
        close = d["close"][i]
        prior_max = max(d["close"][i - lb:i])
        if close <= prior_max:                                # I1
            self.funnel[f"{year}:no_breakout"] += 1
            return None
        if d["volume"][i] < PARAMS["volume_mult"] * self.ind[pair]["volsma"][i - 1]:  # I2
            self.funnel[f"{year}:volume_weak"] += 1
            return None
        if close >= self.ind[pair]["ema20"][i] * (1 + PARAMS["max_above_ema20"]):
            self.funnel[f"{year}:too_extended"] += 1
            return None
        self.funnel[f"{year}:triggered"] += 1
        stop = self.ind[pair]["low10"][i]
        return EntryIntent(pair=pair, stop_px=stop, signal_i=i)

    def wants_exit(self, sim, pair, i, ts):
        """RS exit: the coin has fallen out of the top half of the ranking."""
        return (ts, pair) not in self.top_half


def policy():
    from .simulator import ExitPolicy
    return ExitPolicy(partial_frac=1.0 / 3.0, partial_r=3.0,
                      trail_lookback=10, trail_mode="after_r",
                      trail_after_r=1.0, time_stop_bars=15,
                      time_stop_skip_if_r=1.0, regime_exit=True,
                      stop_mode="resting_stop")
