"""Protocol constants locked by D-020. DO NOT EDIT without a superseding
decision in DECISIONS.md — changing these voids the holdout.
"""
from datetime import datetime, timezone


def _ms(y, m, d):
    return int(datetime(y, m, d, tzinfo=timezone.utc).timestamp() * 1000)


RESEARCH_START_MS = _ms(2021, 1, 1)
HOLDOUT_START_MS = _ms(2025, 7, 1)   # everything from here on is sealed (D-020)

# Walk-forward out-of-sample folds (D-020). 2021 is training/warmup only.
FOLDS = [
    ("2022-H1", _ms(2022, 1, 1), _ms(2022, 7, 1)),
    ("2022-H2", _ms(2022, 7, 1), _ms(2023, 1, 1)),
    ("2023-H1", _ms(2023, 1, 1), _ms(2023, 7, 1)),
    ("2023-H2", _ms(2023, 7, 1), _ms(2024, 1, 1)),
    ("2024-H1", _ms(2024, 1, 1), _ms(2024, 7, 1)),
    ("2024-H2", _ms(2024, 7, 1), _ms(2025, 1, 1)),
    ("2025-H1", _ms(2025, 1, 1), _ms(2025, 7, 1)),
]
FOLDS_REQUIRED_POSITIVE = 5  # >=70% of 7

HOLDOUT_UNLOCK_PHRASE = "I-UNDERSTAND-THIS-OPENS-THE-HOLDOUT-ONCE"

# D-015 risk limits
RISK_PER_TRADE = 0.01
MAX_POSITIONS = 6
HEAT_CAP = 0.06
CORR_WINDOW = 30
CORR_LIMIT = 0.8
CORR_MAX_POSITIONS = 2


def fold_of(ts_ms: int):
    for name, start, end in FOLDS:
        if start <= ts_ms < end:
            return name
    return None


def regime_of(btc_close, btc_sma50, btc_sma200):
    """Pre-defined regime rule (protocol step 7): bull / bear / range."""
    if btc_sma200 is None or btc_sma50 is None:
        return "warmup"
    if btc_close < btc_sma200:
        return "bear"
    if btc_sma50 > btc_sma200:
        return "bull"
    return "range"
