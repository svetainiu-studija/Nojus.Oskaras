# EXP-001 / EXP-001b — post-run analysis and EXP-002 pre-registration

2026-08-28 · Analyst: build session (builder ≠ approver still applies to any G0 claim).

## What the two runs established

1. **The filters add value; the core loses money.** EXP-001 (filtered): 33 trades,
   −0.319 R, PF 0.67, maxDD 13.8%. EXP-001b (BTC gate, regime exit and trend
   filter off): 93 trades, −0.356 R, PF 0.64, maxDD 38.4%. The BTC/trend
   filters improved expectancy and cut drawdown to a third → the "edge = beta"
   falsifier did **not** fire against the filters. Both configs lose → the
   entry/exit core as implemented fails.
2. **Loss amplification at the stop.** Stop exits: 14 trades, mean **−1.97 R**
   (design: −1.0 R). Mechanism: hypothesis-specified execution ("exit at next
   open after a daily close below the stop") + tight stops (the ≤8% cap keeps
   the tightest ones; 48 of 81 triggers were rejected as too wide) + daily
   crypto gaps. The stop cap perversely *selects for* the stops that overshoot
   worst.
3. **Winner amputation at the time stop.** Time exits: 14 trades, mean
   **+1.13 R**, several still trending when force-closed (LINK 2023-10-16:
   +6.71 R at bar 10). The style's thesis (small losses, occasional runners)
   is structurally capped at both ends.
4. **Funnel is healthy.** 2022's zero trades = no uptrends in a bear year
   (trend_align 1,949 rejections) — correct behaviour. 2021's four trades =
   ~200-bar indicator warm-up eating seven months plus mania volume failing
   the "orderly pullback" rule. Biggest post-trigger killer: the 8% stop cap.

## EXP-002 pre-registration (declared BEFORE any EXP-002 result exists)

**Question:** do execution-fidelity corrections — not signal changes — flip the
economics? Signals, filters, sizing, universe, costs stay identical to EXP-001.

**Variant grid (2 × 2 = 4; total HYP-001 variants tried after this: 5):**

| variant | stop execution | time stop |
|---|---|---|
| A (= EXP-001 baseline) | close-confirm → next open | 10 bars |
| B | resting stop order (fills at the stop level when the daily low touches it; at the open if it gaps through) | 10 bars |
| C | close-confirm → next open | 20 bars |
| D | resting stop order | 20 bars |

Rationale: a live spot trader places an actual stop order on the exchange —
the resting-stop model is *more* faithful to real execution than the
close-confirm reading of the hypothesis text, not an optimisation. The 20-bar
time stop is a declared deviation from the hypothesis's 10 bars, motivated by
the observed +1.13 R mean on forced time exits.

**Decision rule (fixed now):**

- If **no** variant reaches expectancy > 0 → HYP-001 is **abandoned** under its
  own falsifier ("walk-forward net expectancy ≤ 0"), the obituary is written,
  and Sprint B (HYP-002) starts.
- If a variant reaches expectancy > 0 → it is *provisional only*: it must then
  survive the 2× cost stress (PF ≥ 1.1), the random-entry baseline (p < 0.05),
  a parameter-sensitivity table, the always-in-universe run, and independent
  reproduction — with holdout thresholds scaled to **5 variants tried**.
- No further HYP-001 variants beyond these four without a new pre-registration
  in this file.

**Known limitation regardless of outcome:** ~33–90 trades over 4.5 years
cannot reach G0's ≥200-trade requirement on daily bars × 30 pairs. If HYP-001
survives EXP-002, frequency must come from more pairs and/or the 4h timeframe
— each a new pre-registered experiment, never a silent widening.

---

## OUTCOME (2026-08-28): the rule fired — HYP-001 is ABANDONED

EXP-002 grid results: A −0.319 R (PF 0.67) · **B −0.036 R (PF 0.94, maxDD
8.9%)** · C −0.248 R (PF 0.75) · D −0.044 R (PF 0.93). No variant reached
expectancy > 0; every variant sat at 2/7 folds positive. Per the decision rule
above, HYP-001 is abandoned under its own falsifier. It is not to be revived
by further variants; a structurally different pullback idea would be a new
hypothesis file with its own pre-registration.

**What carries forward:**
1. The BTC/trend regime filters demonstrably add value (EXP-001b) — retained
   as a concept for future hypotheses.
2. **Execution finding:** close-confirm stop execution with tight stops loses
   ~0.28 R/trade to gap overshoot versus a resting stop order. → Declared
   *before any HYP-002 result exists*: **resting-stop is the primary
   execution model for all subsequent strategies**, with close-confirm
   reported once per strategy as an execution sensitivity. (See
   NOTES-SPRINT-B.md.)
3. Signal frequency on daily × 30 pairs is structurally low; any strategy
   reaching provisional G0 will need a pre-registered frequency extension.
