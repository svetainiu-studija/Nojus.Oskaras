# Sprint B pre-registration — HYP-002 (relative-strength breakout) / EXP-003

2026-08-28 · Declared BEFORE any HYP-002 simulation has been run.

## Configuration (fixed)

Signals exactly as `research/hypotheses/HYP-002.md`; all parameters as written
there (60-day relative strength vs BTC, top-5 leaders; new 20-day closing
high with volume ≥ 1.5× the prior 20-day average; not extended: close < 15%
above EMA20; BTC > SMA50 gate; stop = 10-day low, skip if > 10%; 1/3 off at
3R; trail at the 10-day low once the trade has been ≥ +1R; RS exit when the
coin leaves the top half of the ranking; 15-bar time stop only if never +1R;
regime exit). D-015 sizing and caps unchanged. Universe, costs, dataset and
D-020 windows identical to Sprint A.

Interpretation choices (documented, not tuned):
- I1: "new 20-day high" = today's close strictly above the max of the prior
  20 closes.
- I2: the breakout bar's volume is compared against the average of the PRIOR
  20 bars (excluding itself — a breakout bar inflating its own average would
  weaken the filter).
- I3: "top half of the relative-strength ranking" is evaluated among the
  universe-eligible pairs that day.

## Execution model (carried from the EXP-002 finding, declared a priori)

- **Primary run: resting-stop execution** (stop fills at the level when the
  bar's low touches it; at the open on a gap-through).
- One execution sensitivity: the same config under close-confirm, reported
  alongside. **Variants tried for HYP-002 after EXP-003: 2.**

## Decision rule (fixed now)

- Primary run must show **expectancy > 0 AND ≥ 4/7 folds positive AND PF ≥
  1.1 after the 2× cost stress AND p < 0.05 vs the random-entry baseline** to
  proceed to the full G0 battery (sensitivity table, always-in-universe,
  independent reproduction, frequency extension).
- Anything less → HYP-002 recorded as failed; Sprint C decision (HYP-003, or
  the CHARTER §9 pivot discussion) follows. No further HYP-002 variants
  without a new pre-registration in this file.

---

## OUTCOME (2026-08-28): FAILED — insufficient frequency, by its own geometry

EXP-003: **4 trades** in 4.5 years (+0.365 R, PF 2.95, stress-robust, but 2/7
folds and p=0.302 — unfalsifiable at n=4). Root cause, from the funnel: **82
triggers, 78 rejected by the ≤10% stop rule** — a momentum leader breaking
out to a 20-day high is structurally >10% above its own 10-day low, so the
hypothesis forbids almost every trade its setup generates. The four entries
that passed all sit in post-bear range compression.

Reading: cross-sectional momentum is **untested rather than disproven**; the
hypothesis's stop geometry contradicts its entry. A volatility-scaled-stop
momentum idea would be a NEW hypothesis (HYP-004+) with its own
pre-registration and founders' sign-off — not a variant of this one.
