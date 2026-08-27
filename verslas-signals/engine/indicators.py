"""Indicator library for daily-bar strategies (pure Python, no dependencies).

Every function takes a list of floats and returns a list of the SAME length,
with None where the indicator is not yet defined — index i of the output uses
ONLY inputs [0..i], never anything later. That property (no look-ahead) is
what the unit tests pin down; keep it when adding indicators.

Conventions: EMA seeds with the SMA of the first n values (classic); RSI is
Wilder's smoothing; a perfectly flat window has RSI 50 by convention.
"""
from collections import deque


def sma(xs, n):
    out = [None] * len(xs)
    s = 0.0
    for i, x in enumerate(xs):
        s += x
        if i >= n:
            s -= xs[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def ema(xs, n):
    out = [None] * len(xs)
    if len(xs) < n:
        return out
    out[n - 1] = sum(xs[:n]) / n
    k = 2.0 / (n + 1)
    for i in range(n, len(xs)):
        out[i] = xs[i] * k + out[i - 1] * (1.0 - k)
    return out


def rsi(xs, n=14):
    out = [None] * len(xs)
    if len(xs) <= n:
        return out

    def value(avg_gain, avg_loss):
        if avg_gain == 0.0 and avg_loss == 0.0:
            return 50.0
        if avg_loss == 0.0:
            return 100.0
        if avg_gain == 0.0:
            return 0.0
        return 100.0 - 100.0 / (1.0 + avg_gain / avg_loss)

    gains = losses = 0.0
    for i in range(1, n + 1):
        d = xs[i] - xs[i - 1]
        gains += max(d, 0.0)
        losses += max(-d, 0.0)
    avg_gain, avg_loss = gains / n, losses / n
    out[n] = value(avg_gain, avg_loss)
    for i in range(n + 1, len(xs)):
        d = xs[i] - xs[i - 1]
        avg_gain = (avg_gain * (n - 1) + max(d, 0.0)) / n
        avg_loss = (avg_loss * (n - 1) + max(-d, 0.0)) / n
        out[i] = value(avg_gain, avg_loss)
    return out


def rolling_max(xs, n):
    out = [None] * len(xs)
    dq = deque()  # indices, values decreasing
    for i, x in enumerate(xs):
        while dq and xs[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - n:
            dq.popleft()
        if i >= n - 1:
            out[i] = xs[dq[0]]
    return out


def rolling_min(xs, n):
    out = [None] * len(xs)
    dq = deque()  # indices, values increasing
    for i, x in enumerate(xs):
        while dq and xs[dq[-1]] >= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - n:
            dq.popleft()
        if i >= n - 1:
            out[i] = xs[dq[0]]
    return out


def pct_return(xs, n):
    """n-bar percentage return: xs[i] / xs[i-n] - 1."""
    out = [None] * len(xs)
    for i in range(n, len(xs)):
        if xs[i - n] != 0:
            out[i] = xs[i] / xs[i - n] - 1.0
    return out
