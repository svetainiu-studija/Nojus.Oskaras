# Sprint C pre-registration — HYP-003 (capitulation reclaim) / EXP-004

2026-08-28 · Declared BEFORE any HYP-003 simulation has been run.

## Configuration (fixed)

Signals exactly as `research/hypotheses/HYP-003.md`: coin above EMA200; a
capitulation bar (≥15% drop from the recent high within ≤5 bars, making a
30-day low, volume ≥2× the prior 20-day average, RSI(14) < 30); BTC > SMA50;
trigger within 5 bars = first close above the previous bar's high AND above
the capitulation bar's midpoint; entry next open; skip if stop (the
capitulation low) is >10% away. Exits: 50% at 2R **or at EMA20, whichever is
nearer**; trail the rest at the 5-day low; 7-bar time stop; regime exit.
**Max 2 concurrent positions** (flushes cluster) on top of D-015.

Interpretation choices (documented, not tuned):
- I1: "drop from the 10-day high within ≤5 bars" = today's low is ≥15% below
  the highest high of the previous 5 bars, and today's low is a 30-day low.
- I2: the volume spike is measured against the prior 20-bar average
  (excluding the capitulation bar itself).
- I3: the EMA20 partial target is fixed at trigger time (EMA20 of the trigger
  bar); the partial fills at min(2R target, that EMA20) when that EMA20 is
  above the entry, else at 2R.
- I4: an armed setup dies if any close falls below the capitulation low
  before the trigger.

## Execution model

Resting-stop primary (standing declaration from Sprint A), close-confirm as
the one sensitivity. **HYP-003 variants tried after EXP-004: 2.**

## Decision rule (fixed now)

Primary run must satisfy ALL of:
1. trades ≥ 30 (falsifiability floor — below it the verdict is
   "insufficient frequency", as HYP-002's was);
2. expectancy > 0;
3. ≥ 4/7 folds positive;
4. PF ≥ 1.1 under the 2× cost stress;
5. p < 0.05 vs the random-entry baseline.

Pass all → proceed to the full G0 battery. Fail any → HYP-003 recorded as
failed, reversals dropped for good (per the hypothesis's own intent), and the
**founders' decision point** follows: Sprint C is the last interview
hypothesis, so the options are (a) a new hypothesis round — e.g. 4h
timeframe, wider universe, volatility-scaled stops — each needing a fresh
interview/pre-registration, or (b) the CHARTER §9 pivot discussion. We are in
week 1 of 12; the hard stop is nowhere near.

---

## OUTCOME (2026-08-28): FAILED — the setup essentially does not exist

EXP-004: **1 trade** in 4.5 years (TRX 2024-03-25, +0.246 R, time exit).
The funnel shows the compound condition co-occurred exactly once across 30
pairs — coin-specific capitulations of this depth, inside intact uptrends,
while BTC is bullish, are a null set on daily bars. Nothing to validate or
refute economically. **Reversals are dropped for good**, per the
hypothesis's own intent. Decision memo: `research/DECISION-POINT-2026-08.md`.
