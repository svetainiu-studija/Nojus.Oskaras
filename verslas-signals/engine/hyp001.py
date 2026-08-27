"""HYP-001: pullback-to-EMA20 in a confirmed uptrend, BTC-filtered.

Faithful translation of research/hypotheses/HYP-001.md. All parameters are
FIXED a priori (never optimised; reported only for sensitivity). Two
implementation choices the hypothesis text leaves open are documented here
and in the experiment report:
  I1. An armed setup expires after ARM_EXPIRY_BARS (5) bars without a
      trigger, or immediately when close < EMA50.
  I2. "New 20-day high within the last 15 bars" uses the bar HIGH against
      the rolling 20-bar high.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone

from .indicators import sma, ema, rsi, rolling_max
from .simulator import EntryIntent


def _year(ts):
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).year

PARAMS = {
    "ema_fast": 20, "ema_mid": 50, "ema_slow": 200,
    "recent_high_lookback": 20, "recent_high_within": 15,
    "min_down_closes": 2, "ema20_proximity": 0.02,
    "rsi_n": 14, "rsi_lo": 35, "rsi_hi": 55,
    "vol_sma": 20,
    "btc_sma": 50,
    "max_stop_frac": 0.08,
    "arm_expiry_bars": 5,
    "stop_lookback": 3,
}


def config_hash():
    return hashlib.sha256(
        json.dumps(PARAMS, sort_keys=True).encode()).hexdigest()[:12]


class Hyp001:
    max_stop_frac = PARAMS["max_stop_frac"]

    def __init__(self, data, universe, trend_filter=True):
        """data: same dict the Simulator gets. Precomputes indicators.

        trend_filter=False is the EXP-001b ablation: the uptrend/recent-high
        condition is skipped (together with the simulator-level BTC gate) to
        test whether the filters add anything over unfiltered EMA20 dips.
        """
        self.universe = universe
        self.trend_filter = trend_filter
        self.funnel = Counter()   # diagnostic: where do potential signals die
        self.ind = {}
        for pair, d in data.items():
            close, high, vol = d["close"], d["high"], d["volume"]
            ind = {
                "ema20": ema(close, PARAMS["ema_fast"]),
                "ema50": ema(close, PARAMS["ema_mid"]),
                "ema200": ema(close, PARAMS["ema_slow"]),
                "rsi": rsi(close, PARAMS["rsi_n"]),
                "volsma": sma(vol, PARAMS["vol_sma"]),
                "hh20": rolling_max(high, PARAMS["recent_high_lookback"]),
            }
            self.ind[pair] = ind
        self.armed = {}   # pair -> armed_at index

    # ----- rule pieces ---------------------------------------------------
    def _trend_ok(self, pair, d, i, year=""):
        ind = self.ind[pair]
        e20, e50, e200 = ind["ema20"][i], ind["ema50"][i], ind["ema200"][i]
        if e20 is None or e50 is None or e200 is None:
            self.funnel[f"{year}:warmup"] += 1
            return False
        c = d["close"][i]
        if not (c > e50 > e200):
            self.funnel[f"{year}:trend_align"] += 1
            return False
        # a new 20-day high occurred within the last `recent_high_within` bars
        lb = PARAMS["recent_high_within"]
        hh = ind["hh20"]
        for j in range(max(0, i - lb + 1), i + 1):
            if hh[j] is not None and d["high"][j] >= hh[j]:
                return True
        self.funnel[f"{year}:no_recent_high"] += 1
        return False

    def _pullback_ok(self, pair, d, i, year=""):
        ind = self.ind[pair]
        close, low, vol = d["close"], d["low"], d["volume"]
        # >= min_down_closes consecutive down-closes ending at i
        run = 0
        j = i
        while j >= 1 and close[j] < close[j - 1]:
            run += 1
            j -= 1
        if run < PARAMS["min_down_closes"]:
            self.funnel[f"{year}:no_pullback_run"] += 1
            return False
        e20, e50 = ind["ema20"][i], ind["ema50"][i]
        if e20 is None or e50 is None:
            return False
        if not (low[i] <= e20 * (1 + PARAMS["ema20_proximity"]) and close[i] > e50):
            self.funnel[f"{year}:not_at_ema20"] += 1
            return False
        # orderly: each pullback bar's volume below its 20-day average
        for k in range(i - run + 1, i + 1):
            vs = ind["volsma"][k]
            if vs is None or vol[k] >= vs:
                self.funnel[f"{year}:volume_not_orderly"] += 1
                return False
        r = ind["rsi"][i]
        if r is None or not (PARAMS["rsi_lo"] <= r <= PARAMS["rsi_hi"]):
            self.funnel[f"{year}:rsi_out_of_band"] += 1
            return False
        return True

    # ----- simulator hook ------------------------------------------------
    def on_close(self, sim, pair, i, ts):
        d = sim.data[pair]
        if (ts, pair) not in self.universe:
            self.armed.pop(pair, None)
            return None
        ind = self.ind[pair]
        year = _year(ts)

        armed_at = self.armed.get(pair)
        if armed_at is not None:
            e50 = ind["ema50"][i]
            if e50 is None or d["close"][i] < e50 \
                    or i - armed_at > PARAMS["arm_expiry_bars"]:
                self.funnel[f"{year}:arm_expired"] += 1
                self.armed.pop(pair, None)
            else:
                r_now, r_prev = ind["rsi"][i], ind["rsi"][i - 1]
                if (i >= 1 and d["close"][i] > d["high"][i - 1]
                        and r_now is not None and r_prev is not None
                        and r_now > r_prev):
                    self.armed.pop(pair, None)
                    self.funnel[f"{year}:triggered"] += 1
                    lb = PARAMS["stop_lookback"]
                    stop = min(d["low"][max(0, i - lb):i])
                    return EntryIntent(pair=pair, stop_px=stop, signal_i=i)

        if pair not in self.armed:
            trend = self._trend_ok(pair, d, i, year) if self.trend_filter else True
            if trend and self._pullback_ok(pair, d, i, year):
                self.funnel[f"{year}:armed"] += 1
                self.armed[pair] = i
        return None
