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

---

## OUTCOME (2026-08-28): FAILED — 4 of 7 checks. Signal research ends.

Run by Oskaras on the widened dataset (`DATASET-ff106e72bc5e` raw /
`DATASET-8b092d267524` derived; 65 pairs — MKR and EOS unlisted on OKX,
skipped per I2; SEI's whole history falls inside the sealed holdout so 64
pairs load). Frozen-config parity held: `0e4dc9e0453a`. Report: EXP-007.md.

The widened universe answered EXP-005's open question, and the answer is
the bad one: **the HYP-004 result was one coin's era, not a thin real
edge.**

- p-value **worsened** with more data: 0.068 → **0.1645**. A real edge
  sharpens as the sample grows; this diluted.
- **SOL-USDT = 148% of total profit** (the rest of the book nets a loss);
  ex-SOL expectancy **−0.159 R**. Both concentration checks failed.
- Folds 3/7 (was 4/7). All profit sits in the "range" regime — 6 trades,
  +4.09 R each on average: a handful of SOL runs. Bear and bull regimes
  are both negative.
- What still passed — trade count, raw expectancy, cost stress — shows the
  strategy is robust to *costs* but not to *reality*: with real competition
  for the leadership slots, the entries don't select winners.

Per the pre-registered rule and D-022: HYP-006 is FAILED and closed, no
further rounds, and the CHARTER §9 pivot discussion is mandatory →
`research/PIVOT-DISCUSSION-2026-08.md`. Variant accounting at close:
HYP-001 lineage 4 configs, HYP-002 1, HYP-003 1, HYP-004 lineage 3
(EXP-005, EXP-006, EXP-007) — 9 configurations total, every one recorded,
every verdict fired by a rule written before the result existed.
