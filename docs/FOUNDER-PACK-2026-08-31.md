# Founder decision pack — sync Monday 2026-08-31

For Oskaras & Nojus. Read time ~12 minutes. One decision is required
(§16). Nothing here is invented; every number traces to a committed file.
(The external reviewer's draft named this pack "2026-09-07" — the sync is
2026-08-31; the audit closes Friday 2026-09-04.)

## 1. The decision on the table (D-024, Proposed)

**Uphold D-022; research conclusion frozen: NO EDGE / DO NOT TRADE.**
Strategy mining stops. Reopening any research requires a new joint
decision with written scope, justification, new information source,
experiment cap and stopping rules. Business continues on the
product/infrastructure side. Oskaras's founder vote was recorded
2026-08-28 (chat + DECISIONS.md); Nojus confirms or contests Monday.

## 2. The NO-EDGE evidence, complete

Nine configurations, four hypothesis lineages, seven experiments, week 1
of a 12-week window. Every verdict fired by a rule committed to git
BEFORE the result existed (commit timestamps in AUDIT report, Finding 10).

| EXP | HYP | Trades | Exp. (R) | PF (CI80) | maxDD | Why it failed |
|---|---|---|---|---|---|---|
| 001 | 001 pullback | 33 | −0.319 | 0.67 (0.34–1.17) | 13.8% | negative; p=0.90 |
| 002 | 001 grid A–D | — | best −0.036 | 0.94 | 8.9% | all 4 variants negative → abandoned, not revivable |
| 003 | 002 RS breakout | 4 | +0.365 | 2.95 (0.23–17.1) | 2.4% | its stop rule rejects 95% of its own entries |
| 004 | 003 capitulation | 1 | +0.246 | inf | 0.1% | setup occurs once in 4.5y |
| 005 | 004 momentum 1d | 56 | +0.634 | 2.45 (1.21–4.01) | 12.9% | p=0.068 (Holm 0.136); SOL 71% of profit |
| 006 | 005 momentum 4h | 1043 | +0.050 | 1.11 (0.96–1.26) | 52.9% | stress PF 0.96; DD breaches D-015 |
| 007 | 006 frozen 004, 65 pairs | 48 | +0.317 | 1.59 (0.56–2.90) | 11.6% | folds 3/7; p=0.1645; SOL **148%** of profit; ex-SOL **−0.159 R** |

The decisive fact: EXP-007's entire net profit is smaller than ONE trade
(SOL 2023-10-17→2024-01-03, +21.36 R). Remove it: 47 trades, −6.14 R.
Remove any other pair instead: still positive. The concentration checks
exist precisely for this, and they fired.

## 3–5. Open founder checks (the ONLY unfinished audit items)

- **A4 (Oskaras, pending):** SOL 2023-10-17→2024-01-03 + 10 sampled
  trades vs real OKX/TradingView charts. Pass rule (fixed): chart agrees
  with the simulated path = PASS regardless of the trade's economics;
  disagreement = stop, investigate before closing.
- **B5 (Oskaras, pending):** five biggest winners vs a second venue —
  pre-filled table in AUDIT-2026-08-REPORT.md. Pass = direction/timing/
  magnitude materially consistent.
- **C1 (Nojus, pending):** OKX **SPOT** fee schedule (not futures — we
  are spot-only, no funding component exists) + eyeballed spreads vs
  costs.yaml. The model stays conservative regardless; cheaper live fees
  cannot resurrect an edge that failed at conservative costs.

## 6. Audit status, all items

DONE, no error: E1 independent stats recomputation · E2 independent
bootstrap · E4 Holm/multiple-testing ledger · B4 universe availability ·
B2 gaps/dupes · B1 full data battery on the widened set (PASS) · A3
look-ahead property tests (now permanent in the suite) · C2 cost
walkthrough (matched to 6 decimals) · C3 execution semantics · SOL
mechanics trace (fully explained by written rules — not a bug). DONE
with findings: both A1 adversarial reviews (3 verified errors, §8).
DROPPED by the accepted D-023 amendment: A2, B3, D2, standalone E3.
PENDING: A4, B5, C1 (§3–5). Audit closes Fri 2026-09-04.

## 7. Experiments completed

EXP-001…007 plus EXP-007-AUDIT-R1 (the mechanical rerun). One process
incident on record: an accidental EXP-003 regeneration on the wrong
dataset, reverted, original restored (report §Process incidents).

## 8. Bugs found and fixed (permanent record, all with regression tests)

1. **Monte-Carlo baseline** was random-entry/same-HOLDING-PERIOD, not
   the declared same-EXIT. Bias favored the strategy.
2. **"Reached +1R"** was measured on closes while the 3R partial filled
   intrabar — contradictory semantics. Fixed to intrabar.
3. **No spot cash floor** — simulated exposure could exceed equity
   (leverage a spot account cannot have). Never bound in EXP-007
   (verified by rerun counters); now enforced, with the costs.yaml
   small-order bound.

After all three fixes: **trade set byte-identical, same four checks
fail** (EXP-007-AUDIT-R1: p=0.1069 under the compliant baseline, SOL
148.8%, ex-SOL −0.161 R, folds 3/7). One honest correction on record:
the pre-rerun expectation that p would worsen was wrong — it improved,
and still fails by 2×.

## 9. Statistical validation performed

Pre-registered decision rules (committed before results, git-provable) ·
7 chronological OOS folds · bootstrap CI80s (reproduced independently) ·
random-entry baselines (original + compliant same-exit rebuild, exact
(r+1)/(N+1) estimator, fresh seed) · 2× cost stress · execution
sensitivity (resting vs close-confirm) · concentration checks ·
Holm-corrected p-values across the 9-config ledger (nothing improves) ·
sealed holdout never opened (loader-enforced; verified airtight) ·
adversarial reviews by two independent sessions · look-ahead property
tests · full data-integrity battery.

## 10. Strongest findings

- No look-ahead anywhere (reviewed + property-tested).
- The verdict is bug-invariant: three real bugs fixed, zero trades
  changed.
- The "edge" is one trade on one coin; every diagnostic agrees.
- p fails under BOTH baseline constructions; Holm only strengthens this.
- The dataset itself is clean (B1 PASS).

## 11. What remains uncertain

- A4/B5: the simulator has not yet been checked against real charts —
  the one untested link to reality (yours, Oskaras).
- 48 trades is a small sample: this evidence cannot distinguish "no
  edge" from "weak edge undetectable at this frequency" — but either
  fails the pre-registered bar, and G0's ≥200-trade requirement is
  structurally unreachable for this strategy family.
- The candidate pool is a present-day snapshot (I1, disclosed):
  survivorship reduced by point-in-time membership, not eliminated —
  the residual bias direction would INFLATE results, not rescue them.
- costs.yaml values await C1 — stress already covered 2×.

## 12–14. Project Aurora

A ChatGPT-authored 30-day perps/microstructure mandate, received AFTER
Oskaras's D-024 vote. **Not started.** Full assessment:
`research/proposals/PROJECT-AURORA-ASSESSMENT-2026-08.md`. Its premises
(MEXC, $15k, API-bot execution, "R1/R2" history) do not match this
project (OKX, spot-only charter, €1–5k, manual execution, no API keys).
**Adopted without reopening research:** PBO + Deflated Sharpe as
mandatory reporting in any future experiment, the multiplicity ledger
(Holm in place), hypothesis-registry fields, placebo + ablation testing
standards, the no-trade-zone principle. **Rejected:** everything
requiring perps (charter D-003), leverage (D-015), API execution
(Oskaras's own constraint), L2/tick data (unobtainable at budget), or
reopening strategy mining (D-024).

## 15. Does the current evidence justify reopening research?

No. Nothing new has arrived: no new information source, no error that
changed a verdict, no mechanism the tested families missed that our
data could test. A longer prompt is not new information. Reopening now
would be searching because the answer is disliked — the exact failure
mode the founders' own rules prohibit. (If genuinely new information
ever appears — e.g., a data class we don't have plus a mechanism —
D-024's reopening rule says exactly what a D-025 must contain.)

## 16. The exact Monday decision (choose ONE, record in DECISIONS.md)

- **D-024 CONFIRMED** — research closed; NO EDGE / DO NOT TRADE frozen;
  audit closes Friday after A4/B5/C1; effort moves to the business side.
- **D-025 COMMISSIONED** — research reopened, ONLY via a written joint
  decision: exact scope, why the stopping rule is overridden, the new
  information source, experiment cap, stopping criteria, no retroactive
  changes. "Maybe a little more research" is not an option.

## 17. Business-side priorities if D-024 is confirmed

Honest premise: the original streams 1–3 (signals → affiliates →
copy-trading → paid tier) die with the signal — they were all gated on a
verified track record that does not exist. What survives is real:
1. **Weeks 1–2 — discovery sprint (€0, go/no-go pre-committed):** what
   exactly would we sell, and who pays? Candidates to test with real
   people: honest backtesting/strategy-audit tooling ("prove your edge
   before you risk money"), research-verification as a service, and
   education/content on honest testing (no signals → no MiCA advice
   perimeter). Deliverable: 1-page market note + go/no-go.
2. **Week 2 in parallel — the standing founder tasks that survive any
   direction:** founder agreement signed (due 9 Sep), brand shortlist +
   handles, credential vault + 2FA, hours log.
3. **Weeks 3–4 — build only what discovery validated;** CHARTER v2.0 +
   new 90-day plan; the repo (pipeline, backtester, audit framework, 68
   tests, this whole documented process) becomes the demo asset.
If discovery returns no-go: PIVOT-DISCUSSION option b (archive with a
post-mortem, full dignity) — decided then, not now.
