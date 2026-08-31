# Independent Strategy Audit — Example Report

**Subject:** "Momentum Leaders" — cross-sectional momentum with
volatility-scaled stops, daily bars, 65-pair crypto spot universe
**Client:** ourselves. This is the audit we ran on our own strategy
before deciding whether to trade our own savings on it. Every number
below is real and the full working record is public in our repository.

---

## VERDICT: FAILED — DO NOT TRADE

Three numbers decided it:
- **148%** of the strategy's total profit came from a single asset —
  more than all of it; the rest of the book nets a loss.
- **One trade** (+21.4 R, Oct 2023 – Jan 2024) exceeded the entire
  4.5-year net profit. Remove it: 47 trades, negative expectancy.
- **p = 0.11** against a random-entry baseline with identical exits —
  the results are statistically indistinguishable from luck.

The strategy was not "bad." It was *unproven* — and it looked good:
+0.32 R expectancy, profit factor 1.59, drawdown under 12%, robust to
2× costs. Every dashboard metric a signal seller would advertise,
passed. That is exactly why the deeper battery exists.

---

## What the audit checked (the same battery every client gets)

**1. Spec capture.** The rules restated as testable logic; every
ambiguity we had to interpret was documented and signed off before any
run (2 interpretation notes in this case).

**2. Data integrity.** 1.75M bars across 65 pairs; timestamp alignment
verified to the millisecond; gaps, duplicates, a documented
exchange-wide outage, and native-vs-rebuilt bar consistency all
audited. Result: clean — the verdict could not be blamed on data.

**3. Independent reproduction.** The strategy was re-run after an
adversarial review of the backtest engine itself. The review found
**three real implementation bugs** (a non-compliant statistical
baseline, an inconsistent intrabar rule, a missing no-leverage
constraint). All were fixed and regression-tested. The trade list was
byte-identical after the fixes — the verdict was not an artifact of the
bugs. Most retail backtests never survive this step.

**4. Costs.** Every trade net of the venue's real fee tier plus spread
and slippage, both ways; then the whole backtest re-run at 2× costs.
This strategy PASSED the cost stress — costs were not its problem.

**5. Baselines.** 2,000 Monte-Carlo simulations of random entries
managed by the strategy's own exit rules. The strategy's mean trade had
to beat what a coin-flip entry achieves with the same risk management.
It did not (p = 0.11; threshold 0.05).

**6. Temporal robustness.** Seven chronological half-year windows,
strictly out-of-sample. Positive in only 3 of 7.

**7. Concentration.** Profit share by asset, leave-one-out analysis,
single-trade dependence. This is the test that exposed the headline
result: an "edge" that is one coin's era is not an edge.

**8. Multiple-testing honesty.** Nine configurations were tried across
the research program — declared, counted, and the p-values corrected
for it (Holm). Nothing improved. If you tested 200 variants before
finding your winner, this section is where that truth surfaces.

**9. The verdict page.** Plain language, pre-agreed pass/fail criteria
declared *before* results existed, and the one paragraph that matters:

> *This strategy's apparent profitability rests on a single historical
> trade in a single asset. Deployed with real money, the expected
> outcome is the rest of the book: slow losses. Do not trade it.*

We followed our own advice. Not one euro was deployed.

---

## Why trust this process

- **We ran it on ourselves first** and published the negative result —
  the answer we did not want.
- **Rules before results:** every pass/fail criterion is committed to
  version control before the test runs; the verdict fires mechanically.
- **Adversarially reviewed:** independent review sessions are paid to
  find bugs in our own engine, in either direction. They have.
- **Reproducible:** datasets are fingerprinted, seeds fixed, and every
  claim traces to a committed file.

**What this is not:** investment advice, trading signals, or a
performance promise. We verify claims about strategies. We never tell
you what to trade.

---

*Independent Strategy Audit · turnaround 5 working days from signed
spec · founding price €99 (first 10), then €149–299 by complexity.*
