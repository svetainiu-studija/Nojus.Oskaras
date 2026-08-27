# AUDIT-2026-08 — findings ledger (running)

Protocol: `AUDIT-2026-08-PROTOCOL.md` (committed before any test ran).
Every test lands here, nulls included (R5). Verdicts per test: **NO ERROR**,
**VERIFIED ERROR** (→ fix, rerun affected experiments under unchanged
checks), or **DIAGNOSTIC** (R3: narrative only, never a verdict).

## Status board

| Test | Runs | Status |
|---|---|---|
| A1 code review — statistics/costs/baselines session | CLOUD | **DONE — 1 VERIFIED ERROR (F1)** + minors, below |
| A1 code review — simulator/strategy session | CLOUD | in progress |
| A2 clean-room reproduction | LOCAL | pending (script ships after A1) |
| A3 look-ahead property tests | CLOUD | **DONE — NO ERROR** |
| A4 manual chart verification | FOUNDERS | pending (sample below) |
| B1 audit battery on widened raw data | LOCAL | pending: `python -m engine.data.audit data/raw` |
| B2 gaps/duplicates | done 2026-08-27 | **NO ERROR** (run.py quality: 195 files, 0 missing, 0 dupes) |
| B3 independent universe recomputation | LOCAL | pending (script ships) |
| B4 availability-vs-strategy | CLOUD | **DONE — NO ERROR** |
| B5 cross-venue price check | FOUNDERS | pending (trade list below) |
| C1 costs.yaml vs reality | FOUNDERS | pending (Nojus) |
| C2 cost double-count walkthrough | CLOUD | **DONE — NO ERROR** (matched to 6 decimals, below) |
| C3 execution-semantics check | CLOUD | in progress (simulator session; partial notes below) |
| D1 SOL legitimacy | mixed | partially done (see D3; chart check in A4) |
| D2 restricted-universe recomputation | LOCAL | pending |
| D3 era analysis | CLOUD | **DONE — DIAGNOSTIC** (major, below) |
| E1 independent stats recomputation | CLOUD | **DONE — NO ERROR** (one episode, below) |
| E2 independent bootstrap | CLOUD | **DONE — NO ERROR** |
| E3 baseline reproduction | CLOUD+LOCAL | methodology review **DONE — VERIFIED ERROR F1**; compliant rerun = the R1 fix, pending |
| E4 multiple-testing accounting | CLOUD | **DONE** (can only strengthen the failure) |
| E5 concentration robustness | CLOUD | **DONE — DIAGNOSTIC** |

## Completed tests

### A3 — look-ahead property tests: NO ERROR

`tests/test_audit_lookahead.py` (new): every indicator (sma, ema, rsi,
rolling_max, rolling_min, pct_return, atr) is prefix-invariant when bars
after the decision index are mutated wildly; HYP-004's entry intent at the
decision close (trigger and stop price) is invariant across three
adversarial rewrites of the future. All pass; suite now 64 tests green.

### B4 — availability vs strategy: NO ERROR

`audit/b4_universe_availability.py` (stdlib-only, committed data only):
for all 63 pairs ever in-universe, first membership ≥ first derived bar +
90 days — the listing-age filter genuinely held; no pair entered early.
MINA and SEI have bars but were never members (never top-30 by volume /
holdout-only history). Nothing was treated specially by data availability.

### E1 — independent recomputation: NO ERROR (with one honest episode)

`audit/e1_stats.py` (stdlib-only, zero engine imports) recomputed every
headline number in EXP-007.md from the trades CSV: trades 48, expectancy
+0.3171, PF 1.593, win rate 29.17%, avg win +2.9205, avg loss −0.7549,
all seven folds (counts and expectancies), folds-positive 3, per-year
counts, top pair SOL, net-R share 148.06%, ex-top expectancy −0.1590.
**Episode:** the first run flagged `avg_loss_r` (−0.7549 vs printed −0.76)
and one fold (+0.5565 vs printed +0.556). Root cause in both: the report
prints rounded values (2 and 3 decimals) computed from full-precision
floats, while the recomputation uses the CSV's 3-decimal r values; the
checker's tolerances were tighter than the report's own printing
precision. Fixed the checker (tolerance = half a printed unit + CSV
rounding allowance), not the engine. All values MATCH.

### E2 — independent bootstrap: NO ERROR

Fresh resampler, 10,000 iterations, seed 20260828 (unrelated to any
engine seed): expectancy CI80 −0.240…+0.959 vs reported −0.244…+0.934;
PF CI80 0.58…2.97 vs reported 0.56…2.90. All within the pre-declared
tolerances — differences are resampling noise, not methodology.

### E4 — multiple-testing accounting: DONE

EXP-007's rule used a RAW p < 0.05. Nine configurations were tried across
the program; three in the momentum lineage. Any family-wise correction
(e.g. Bonferroni within-lineage → 0.0167) only lowers the bar EXP-007's
p = 0.1645 already failed. Recorded: the multiple-testing question cannot
rescue the result, only make its failure stricter. No correction error
exists because no correction was (or needed to be) applied.

### D3 — era analysis: DIAGNOSTIC, and it is the headline

**The "SOL era" is literally one trade.**

```
SOL-USDT  2021-07-31 -> 2021-08-08   +1.173 R  (2021, training year)
SOL-USDT  2023-10-17 -> 2024-01-03  +21.362 R  78 bars, exit: trailing stop
```

One entry on 2023-10-17 — the very start of SOL's Q4-2023 run from ~$24
toward ~$120 — rode +213% net of costs and produced **+21.36 R, more than
the entire book's net profit (+15.22 R over 48 trades)**. Remove that
single trade and the remaining 47 trades net **−6.14 R (expectancy
−0.131 R)**. Leave-one-out per pair confirms SOL is unique: removing any
other pair leaves expectancy between +0.17 and +0.41 R; only SOL's
removal flips the book negative. 9 of 31 traded pairs were profitable.

Under R3 this decides nothing by itself — but it sharpens what the audit
must now establish: **is that one trade real?** If implementation, data
and fills for it are clean (A4 chart check, A1 mechanics trace, B5
cross-venue), the honest reading of EXP-005/007 is "one great trade plus
noise", and the FAILED verdict stands on very solid ground. It also makes
the A1 deep-dive (how a 78-bar hold passes the 15-bar time stop via the
skip-if-in-profit rule; how the trail ratcheted; how the 2R partial blends
into +21.362 R) the most important code path in the audit.

### E5 — concentration robustness: DIAGNOSTIC

Pre-specified alternates only. Net-R share (the pre-registered check 6):
148.1%. Gross-positive-denominator share: 56.7% (SOL +22.54 R of
+39.77 R summed over profitable pairs) — still above the 50% line, so
check 6 fails under either denominator. The >100% net share is not a bug:
the non-SOL book nets a loss, shrinking the denominator below SOL's
contribution (the audit/e1 checker reproduces it independently).

## Founder tasks (paste results into chat; Claude logs them here)

**A4 — chart verification sample (fixed by the protocol):** trades
#1, 6, 11, 16, 21, 26, 31, 36, 41, 46 of EXP-007.trades.csv by entry
date, **plus both SOL trades** (the protocol says "3 largest SOL winners";
only 2 SOL trades exist — noted). For each: entry day really was a 20-day
high close by a volume-confirmed leader; fill = next day's open;
stop/exit path matches the chart. The one that matters most:
**SOL-USDT 2023-10-17 → 2024-01-03**.

**B5 — cross-venue price check, 5 largest winners:**

```
SOL-USDT   2023-10-17 -> 2024-01-03  +21.362 R
BTC-USDT   2023-10-17 -> 2023-11-12   +4.512 R
APE-USDT   2023-01-05 -> 2023-02-09   +3.579 R
SHIB-USDT  2024-11-07 -> 2024-11-26   +2.462 R
BTC-USDT   2021-07-27 -> 2021-08-16   +2.344 R
```

Check OKX daily closes on entry/exit days against Kraken or Binance on
TradingView; a divergence big enough to change a trade's outcome is a
verified-error candidate.

**C1 — costs.yaml vs reality (Nojus):** OKX spot taker fee for a regular
account from the live fee page, plus eyeballed spreads on 5 majors and 5
small pool pairs. Compare with costs.yaml's values.

## A1 (statistics/costs/baselines session) — findings

Independent review session (did not build the code); every claim verified
against actual lines and re-executed against the committed trades CSV and
a synthetic run through the real Simulator.

### F1 — VERIFIED ERROR (E3 criterion): the baseline is random-entry /
### same-HOLDING-PERIOD, not random-entry / same-EXIT

`engine/experiment.py:110-142`: `random_baseline` draws a holding period
from the strategy's realized `bars_held` distribution and exits
unconditionally at `open[i+1+h]`. No stop, no partial, no trail, no time
stop, no regime flatten are applied to the random entries — but the spec
(CLAUDE.md rule 5, protocol E3) says "random-entry / **same-exit**".
Direction of bias: **favors the strategy** (the real exit stack applied to
random entries would cut bear-regime holds and harvest drift
asymmetrically, pushing the null's mean up → true p ≥ reported p).
Severity: protocol-grade — E3's error criterion ("spec divergence") is
met. Affects the whole family (EXP-001/003/005/006/007 share the
function). **R1 consequence: fix and rerun the p-value check for the
affected experiments** — materially EXP-007 (the verdict under audit) and
EXP-005 (the only experiment whose verdict hinged solely on p). Honest
expectation, stated before the rerun: since the bug favored the strategy
and check 5 failed anyway (p = 0.1645), a compliant baseline most
plausibly *worsens* p. The rule is the rule; we rerun regardless (R2).

Minor findings in the same area (recorded; none verdict-capable): **F2**
baseline entry pool truncated by `max(holds)+2`, structurally excluding
the last ~80 bars per pair (~Q2-2025) from the null; **F3** p computed as
r/N instead of the exact (r+1)/(N+1) — bias ≤ 0.0005 toward
significance; **F4** return-denominator convention differs strategy vs
baseline (≈ ×0.9985, negligible); **F5** zero-bar intraday holds clamped
to 1 in the holds distribution (one trade affected); **F12**
(methodology, spec-compliant): iid-uniform entries ignore the strategy's
temporal clustering → the null is too narrow → reported p is if anything
an underestimate — strengthens, never rescues, the failure. The fix
implementation addresses F1-F4 together.

### C2 — cost walkthrough: NO ERROR

One winning trade (entry, 1/3 partial at target, final exit) and one
losing trade (resting-stop fill, plus the gap-through variant) traced
end-to-end through the real Simulator against hand arithmetic: matched to
6 decimals. Each leg pays exactly one one-way cost (taker + half-spread +
slippage) on its own notional — nothing double-counted, nothing
wrong-signed. Stress applies the 2× multiplier exactly once per leg.
Real-trade cross-check: stop-outs cluster at r ≈ −1.02…−1.09, matching
−1 − 2c/stop_frac per cost tier. Conservative-direction modelling notes
(consistent with declarations, no action): partial legs pay taker though
a resting limit would earn maker (F7); gap-above-target partials fill at
target, not the better open (F8).

### Also verified clean by this session

- **Holdout truncation airtight:** no bar ≥ 2025-07-01 can reach any
  simulation or the baseline pool (loader skips at `HOLDOUT_START_MS`;
  the simulator calendar is bounded independently).
- **Seven-check wiring:** every check computed on the right quantity;
  per-sim n = 48 exactly; same costs both sides of the baseline
  comparison.
- **Metrics reproduce exactly** (expectancy, PF, folds, regimes,
  concentration 148.1% / −0.159 R); bootstrap is a standard percentile
  bootstrap; fold threshold 4/7 matches the pre-registration.
- **exit_reason_stats** table reproduces exactly (SOL's +21.36 R exits
  via trailing stop — why "stop" averages +0.134).
- Neutral notes on record: declared order-size assertion missing in the
  simulator (positions here are far inside bounds — latent only, F6);
  entries onto zero-volume bars canceled rather than postponed (docstring
  divergence; zero occurrences in EXP-007 — F9); entry skipped when next
  open gaps through the stop (defensible, rare — F10); concentration
  share can exceed 100% when the ex-top book nets a loss (correct
  ordering for check 6; robust under the E5 alternate denominator — F11).

## Process incidents

- 2026-08-28 — Oskaras ran `python -m engine.exp003` (not an audit task);
  the runner regenerated EXP-003.md / EXP-003.trades.csv on the *widened*
  dataset, overwriting the historical Sprint B record (original: 4 trades
  on DATASET-7a161580a8b6; rerun: 5 trades on 8b092d267524, verdict still
  FAILED). Originals restored from git history; the accidental rerun's
  content remains permanently readable at commit `0a63964`. Incidentally
  informative (not a pre-registered test): HYP-002 stays failed on the
  widened universe too. Rule going forward, audit window included: only
  the commands listed in this report / chat get run; experiment reports
  are history, not scratch output.

## F1 fix plan (R1), fixed before implementation

The compliant baseline is built **clean-room**: a self-contained
`audit/` implementation written from the pre-registration text (stop =
2×ATR(14) at entry; 1/3 partial at its R target; trail per policy after
its R threshold; 15-bar time stop with skip-if-in-profit; BTC-SMA50
regime flatten; same per-pair cost tiers), NOT by importing the engine's
simulator — so an engine bug cannot hide in its own baseline. Entries
drawn uniformly over the tradable in-universe (ts, pair) space with no
end-truncation beyond what the strategy itself faces (fixes F2);
p computed as (r+1)/(N+1) (fixes F3); strategy's return convention
(fixes F4); 2,000 sims; fresh seed. Reruns the p check for **EXP-007**
and **EXP-005** under their unchanged thresholds; results go to
`research/experiments/EXP-007-AUDIT-E3.md` (and -005) — the original
reports are history and stay untouched. This same clean-room module is
then reused for A2 (reproducing the strategy's own 48 trades from the
hypothesis text). Ships after the second A1 session lands.

## Pending local runs (scripts ship after the A1 review lands)

B1 (`python -m engine.data.audit data/raw`), A2 clean-room rerun, B3
universe recomputation, D2 restricted-universe reruns, E3 compliant
fresh-seed baseline (the F1 fix above). Sequenced after A1 so any code
fixes land first (protocol §Sequencing).
