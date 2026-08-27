"""Performance metrics per D-008: computed from the trade list and equity
curve, never quoted selectively. Win rate is never reported alone.
"""
import random
from collections import defaultdict


def profit_factor(rs):
    wins = sum(r for r in rs if r > 0)
    losses = -sum(r for r in rs if r < 0)
    if losses == 0:
        return float("inf") if wins > 0 else 0.0
    return wins / losses


def expectancy(rs):
    return sum(rs) / len(rs) if rs else 0.0


def max_drawdown(equity):
    """Max peak-to-trough drawdown of an equity series, as a fraction."""
    peak = float("-inf")
    mdd = 0.0
    for e in equity:
        peak = max(peak, e)
        if peak > 0:
            mdd = max(mdd, (peak - e) / peak)
    return mdd


def bootstrap_ci(rs, stat_fn, iters=2000, lo=0.10, hi=0.90, seed=42):
    """Percentile bootstrap CI for a statistic of the R-multiple list."""
    if not rs:
        return (0.0, 0.0)
    rng = random.Random(seed)
    n = len(rs)
    stats = sorted(stat_fn([rs[rng.randrange(n)] for _ in range(n)])
                   for _ in range(iters))
    return (stats[int(iters * lo)], stats[int(iters * hi) - 1])


def summarize(trades, equity_curve):
    """trades: list of dicts with keys r, regime, fold, entry_ts, pair, bars_held.
    Returns the D-008 metrics dict."""
    rs = [t["r"] for t in trades]
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r <= 0]
    by_regime = defaultdict(list)
    by_fold = defaultdict(list)
    by_pair = defaultdict(list)
    for t in trades:
        by_regime[t["regime"]].append(t["r"])
        if t["fold"]:
            by_fold[t["fold"]].append(t["r"])
        by_pair[t["pair"]].append(t["r"])
    total_r = sum(rs)
    concentration = (max((sum(v) for v in by_pair.values()), default=0.0) / total_r
                     if total_r > 0 else None)
    return {
        "trades": len(rs),
        "expectancy_r": expectancy(rs),
        "expectancy_ci80": bootstrap_ci(rs, expectancy),
        "profit_factor": profit_factor(rs),
        "pf_ci80": bootstrap_ci(rs, profit_factor),
        "win_rate": len(wins) / len(rs) if rs else 0.0,
        "avg_win_r": expectancy(wins),
        "avg_loss_r": expectancy(losses),
        "max_drawdown": max_drawdown(equity_curve),
        "regimes": {k: {"trades": len(v), "expectancy_r": expectancy(v)}
                    for k, v in sorted(by_regime.items())},
        "folds": {k: {"trades": len(v), "expectancy_r": expectancy(v)}
                  for k, v in sorted(by_fold.items())},
        "top_pair_profit_share": concentration,
    }
