# Sprint D pre-registration — HYP-004 (daily) & HYP-005 (4h) / EXP-005 & EXP-006

2026-08-28 · Declared BEFORE any simulation of either hypothesis has run.
Founders' mandate: D-021 (Option A). This is round 2; at most one further
round may follow before the CHARTER §9 pivot discussion is mandatory.

## Configuration (fixed)

Exactly as `research/hypotheses/HYP-004.md` and `HYP-005.md`. Shared engine
code; the two differ only in the bar series (daily vs 4h) and the BTC/
universe contexts derived from it.

Interpretation choices (documented, not tuned):
- I1: ATR is Wilder's ATR(14); the stop is signal-close − 2×ATR, fixed at
  entry (the trail can only raise it).
- I2: the 25% stop-distance cap is a sizing-sanity guard, expected to bind
  rarely; its skip count is reported (if it rejects a material share of
  triggers, that is a finding, not a knob to turn).
- I3: HYP-005 windows are bar-parity (numbers keep their bar counts at 4h).
- I4: HYP-005 universe membership = the UTC day's daily membership applied
  to that day's six 4h bars.
- I5: 4h regime labels use the 4h series' own 50/200-bar SMAs (reporting
  only; the entry gate is the 50-bar SMA).

## Execution model

Resting-stop primary; close-confirm reported once per hypothesis as the
execution sensitivity. **Variants tried per hypothesis after this sprint: 2.**

## Decision rule (fixed now, per hypothesis, evaluated by the runner)

1. trades ≥ 30; 2. expectancy > 0; 3. ≥ 4/7 folds positive;
4. PF ≥ 1.1 under 2× cost stress; 5. p < 0.05 vs the random-entry baseline.

Pass all → that hypothesis proceeds to the full G0 battery (sensitivity
table, always-in-universe, independent reproduction, and for HYP-005 a
funding/latency review before any live use). Fail any → recorded as failed.
Both fail → the round is over; per D-021 the founders choose between one
final round and the §9 pivot discussion. No further variants of either
hypothesis without a new pre-registration here.

---

## OUTCOME (2026-08-28): both FAILED — but HYP-004 is the strongest signal yet

**EXP-006 / HYP-005 (4h): cleanly falsified.** 1,043 trades, +0.050 R, PF
1.11 → **PF 0.96 under the 2× cost stress** (costs eat the fast version, as
the pre-registration anticipated), 3/7 folds, and a 52.9% drawdown that
breaches D-015 regardless. Fast momentum on these pairs does not survive
costs. Closed.

**EXP-005 / HYP-004 (daily): failed ONE check of five — p = 0.068 vs the
0.05 requirement.** Everything else passed: 56 trades, expectancy +0.634 R
with an entirely-positive CI80 (+0.10…+1.20), PF 2.45 (CI80 lower bound
1.21), stress-robust (PF 2.32), execution-insensitive, 4/7 folds (the two
negatives are the 2022 bear halves on tiny samples). Post-hoc diagnostic
(analysis of the recorded trades, not a re-run): **SOL alone contributed
71% of total profit**; excluding it, 52 trades at +0.199 R, PF 1.43 —
still positive, much weaker. The p-fail and the concentration are the same
fact seen twice: the result leans on one coin's great runs.

**Status:** HYP-004 is recorded as FAILED per the rule. The honest
resolution of "promising, p=0.068, concentrated" is **a larger, more
diverse sample — not new parameters**. That would be the final round
(D-021 allows exactly one more): same frozen config, wider candidate
universe, stronger test, concentration criteria added. Founders decide.
