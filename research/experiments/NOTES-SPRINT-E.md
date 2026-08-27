# Sprint E pre-registration — HYP-006 / EXP-007 (the final round, D-022)

2026-08-28 · Declared BEFORE the widened dataset exists and before any
simulation. If EXP-007 fails, signal research ends (§9 discussion mandatory).

## Configuration

Strategy: HYP-004, frozen (config hash must equal EXP-005's `0e4dc9e0453a`;
the runner prints it — any difference voids the run). Execution: resting-stop
primary, close-confirm sensitivity. D-015 caps, D-020 windows and holdout
unchanged. Universe: point-in-time top-30 by trailing 90-day quote volume,
listing age ≥ 90 days, selected from the widened ~60-pair candidate pool in
pairs.yaml; universe.csv rebuilt from the widened derived daily bars before
the run.

Interpretation choices:
- I1: pairs added to the pool are today's liquid OKX listings — survivorship
  is reduced by point-in-time selection but the pool itself remains a
  present-day snapshot (unchanged v1 limitation, stated).
- I2: the downloader skips pairs OKX does not list; the skip list is
  recorded in the run log and does not invalidate the round.

## Decision rule (fixed now — ALL seven must pass)

1. trades ≥ 30; 2. expectancy > 0; 3. ≥ 4/7 folds positive;
4. PF ≥ 1.1 under the 2× cost stress;
5. p < 0.05 vs the random-entry baseline at **2,000 simulations**;
6. **top-pair profit share < 50%**;
7. **ex-top-pair expectancy > 0**.

Pass all → HYP-006 proceeds to the full G0 battery (parameter-sensitivity
table, always-in-universe run, independent reproduction from raw data by a
separate session, then G0 judgment with variant counting: HYP-004 lineage =
3 tested configurations). Fail any → recorded as failed; **no further
rounds; the CHARTER §9 pivot discussion follows.**
