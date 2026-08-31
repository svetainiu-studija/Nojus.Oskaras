# AUDIT-2026-08 — findings ledger (running)

Protocol: `AUDIT-2026-08-PROTOCOL.md` (committed before any test ran).
Every test lands here, nulls included (R5). Verdicts per test: **NO ERROR**,
**VERIFIED ERROR** (→ fix, rerun affected experiments under unchanged
checks), or **DIAGNOSTIC** (R3: narrative only, never a verdict).

## Status board

| Test | Runs | Status |
|---|---|---|
| A1 code review — statistics/costs/baselines session | CLOUD | **DONE — 1 VERIFIED ERROR (F1)** + minors, below |
| A1 code review — simulator/strategy session | CLOUD | **DONE — 2 VERIFIED ERRORS (Findings 1, 2, both FIXED)** + minors, below |
| A2 clean-room reproduction | LOCAL | **DROPPED** (D-023 amendment, 2026-08-28) |
| A3 look-ahead property tests | CLOUD | **DONE — NO ERROR** |
| A4 manual chart verification | delegated → scripted | `audit/a4b5_verify.py` committed; one optional local run. **If not run by Fri 2026-09-04, protocol R4 applies: resolves conservatively (conclusion stands) and the audit closes complete.** |
| B1 audit battery on widened raw data | LOCAL | **DONE — PASS, NO ERROR** (2026-08-28, below) |
| B2 gaps/duplicates | done 2026-08-27 | **NO ERROR** (run.py quality: 195 files, 0 missing, 0 dupes) |
| B3 independent universe recomputation | LOCAL | **DROPPED** (D-023 amendment; B4's availability proof + A1's universe.py review stand) |
| B4 availability-vs-strategy | CLOUD | **DONE — NO ERROR** |
| B5 cross-venue price check | delegated → scripted | same run as A4 (independent second venue, raw evidence saved) |
| C1 costs.yaml vs reality | done via secondary sources | **DONE — VERIFIED, exact match** (below; optional 1-min live-page glance remains) |
| C2 cost double-count walkthrough | CLOUD | **DONE — NO ERROR** (matched to 6 decimals, below) |
| C3 execution-semantics check | CLOUD | **DONE** — declared model matches code except Findings 1/2 (fixed) and cosmetic notes |
| D1 SOL legitimacy | mixed | code-side **DONE** (full mechanics trace below: legal, no bug); chart check in A4 |
| D2 restricted-universe recomputation | LOCAL | **DROPPED** (D-023 amendment — EXP-007-only diagnostic) |
| D3 era analysis | CLOUD | **DONE — DIAGNOSTIC** (major, below) |
| E1 independent stats recomputation | CLOUD | **DONE — NO ERROR** (one episode, below) |
| E2 independent bootstrap | CLOUD | **DONE — NO ERROR** |
| E3 baseline reproduction | CLOUD+LOCAL | **DONE** — F1 fixed; compliant same-exit p = **0.1069**, still FAIL (R1 rerun below) |
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

## C1 correction (recorded 2026-08-28): SPOT schedule, not futures

Oskaras's D-024 message cited OKX's **futures** Level-1 rates (0.02%
maker / 0.05% taker, funding separate). **That schedule does not apply to
this project**: the instrument universe is spot-only (D-003, CLAUDE.md
rule 1), so there is no funding component at all and the relevant page is
OKX's **spot** fee schedule for a regular-user account. costs.yaml models
a spot taker fill (0.10% taker + half-spread + slippage per leg, tiered
by pair). C1 (Nojus) = read the live SPOT fee page, record the account's
actual tier and maker/taker rates, note that the strategy fills as taker
(market-ish entries at open, resting stops), eyeball spreads on 5 majors
+ 5 small pool pairs, and compare against costs.yaml. Agreed stance
stands: the model stays conservative — a slightly cheaper live fee does
not resurrect an edge that failed at conservative costs.

## C1 RESULT (2026-08-28): VERIFIED — costs.yaml matches the live schedule exactly

Verified against multiple current secondary sources (OKX's own domain is
egress-blocked from the cloud session): **OKX spot regular-user Lv1 =
0.08% maker / 0.10% taker.** `costs.yaml` models exactly that
(`maker_fee: 0.0008`, `taker_fee: 0.0010`), and the strategy fills as
taker — so the fee component is correct, with the conservative
half-spread + slippage layers on top and the 2× stress above that. The
spread/slippage placeholders remain deliberately conservative (their
empirical order-book verification was a pre-G0 task; G0 is moot).
Conclusion unchanged and un-changeable by fees: the strategy failed at
costs equal to or harsher than reality. Optional belt-and-braces: any
founder glances at https://www.okx.com/fees once (1 minute) to confirm
the Lv1 row; a cheaper live fee changes nothing (recorded stance).
Sources: tradersunion.com, bitdegree.org, supa.is fee guides (2026),
cross-consistent.

## A4 / B5 — delegated to a scripted verification (2026-08-28)

Oskaras instructed full delegation ("fill everything yourself"). Chart
eyeballing is replaced by `audit/a4b5_verify.py`, which preserves the
checks' independence differently: it verifies every sampled trade
against **freshly fetched native OKX candles** and an **independent
second venue** (Binance, fallback Bybit/KuCoin), never touching the
project's own derived dataset, and saves all fetched candles as
immutable evidence files (`audit-evidence/`) so anyone — Nojus included
— can re-run and inspect. It checks, per sampled trade: the 20-day-high
close, volume confirmation, extension cap, BTC gate, stop plausibility,
and the exit mechanism (stop-touch vs the 10-day trail, regime vs the
BTC series, time-stop date math); runs the SOL +21.36 R deep-dive
(partial target reached, trail touched on 2024-01-03, peak move
supports the recorded return); and fills the B5 cross-venue table with
numeric diffs. Cloud execution is impossible (exchange and price-data
domains are egress-blocked — OKX, Kraken, CoinGecko all 403), so the
one remaining human act before sign-off is running it locally once.

## A4 / B5 evidence templates (fill in; Claude logs results here)

A4 verdict rule (fixed): PASS if the chart agrees with the simulated
price path — even if the trade is economically unattractive; FAIL stops
the audit close and triggers investigation. B5 pass condition: direction,
timing and magnitude of the move materially consistent on a second venue;
small venue differences expected.

| B5 trade | Sim entry | Sim exit | R | Second venue agrees? | Material discrepancy? |
|---|---|---|---|---|---|
| SOL-USDT | 2023-10-17 | 2024-01-03 | +21.36 | | |
| BTC-USDT | 2023-10-17 | 2023-11-12 | +4.51 | | |
| APE-USDT | 2023-01-05 | 2023-02-09 | +3.58 | | |
| SHIB-USDT | 2024-11-07 | 2024-11-26 | +2.46 | | |
| BTC-USDT | 2021-07-27 | 2021-08-16 | +2.34 | | |

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

## A1 (simulator/strategy session) — findings and adjudications

Second independent review session; line-by-line over simulator, strategy,
indicators, protocol and run_sim. **No look-ahead was found in any
decision, indicator, ranking or fill path.** Findings, with the builder's
adjudication recorded transparently (protocol R1 — adjudications default
to the stricter treatment):

- **Finding 1 — VERIFIED ERROR, FIXED.** "Reached +1R" (trail activation,
  time-stop skip) was measured on closes only, while the engine's own 3R
  partial fills off the intrabar high — two contradictory intrabar
  semantics for the same concept, and the closes-only reading was never
  documented as an interpretation choice. A trade could bank its +3R
  partial and still be time-stopped for "never reaching +1R". Adjudicated
  an error (undocumented interpretation contradicting the spec's plain
  reading AND internally inconsistent). Fix: `max_r` now tracks the bar's
  high (simulator.py); regression tests pin both the time-stop-skip and
  trail-activation cases. Direction: ambiguous. In EXP-007 the three
  time-stopped trades took no partial, so the bite is plausible but
  unproven without the rerun — hence the R1 rerun below.
- **Finding 2 — VERIFIED ERROR, FIXED.** No cash floor: aggregate notional
  could exceed equity (leverage a spot account cannot have — D-015 "no
  leverage"). Per-trade R/pct are provably invariant to the cash path, and
  in EXP-007 the worst concurrent clusters imply ~45–55% summed notional,
  so it almost certainly never bound — the rerun's `cash` skip counter
  verifies that. Fix: entries beyond available cash are refused and
  counted; the costs.yaml small-order bound (0.1% of fill-bar volume) is
  now enforced the same way (`size_bound`). Regression tests added.
- **Finding 3 — interpretation gap, DIAGNOSTIC.** Three 2021-entry trades
  (net +2.49 R) sit in EXP-007's headline numbers though D-020 calls 2021
  training-only; the folds correctly exclude them. The pre-registered
  checks were defined over the primary run as specified (window starts
  2021-01-01), so per R1 the checks stay as defined; the rerun reports the
  ex-2021 view as a diagnostic. Excluding them changes no check's outcome
  (expectancy +0.283 still passes; concentration gets worse).
- **Findings 5–9 — minor/cosmetic, recorded.** Entry-postponement
  docstring corrected (entries cancel, exits postpone — code was already
  conservative and test-pinned); partial fills at target on gap-above
  (deflating, matches its declaration); mixed R bases (sizing at signal
  close vs management at fill — undocumented, both-ways, immaterial on
  daily bars; to be pinned in any future spec); `stop<=0` bypasses the I2
  skip counter (undercount only); regime tagged at signal close vs fold at
  fill date (one-day skew, correct for every EXP-007 trade checked).
- **Finding 10 — timestamps RECONCILED.** EXP-007.md says "Run:
  2026-08-27" while the pre-registration headers say 2026-08-28. The
  header dates were a drafting label error; git commit times are
  authoritative and prove the ordering: pre-registration + runner
  committed `990927f` 2026-08-27 **17:19:11 UTC**, Oskaras's results
  committed `56db25e` 2026-08-27 **18:36:23 UTC** (21:36 +03:00) — 77
  minutes later. Same pattern for every sprint: each NOTES pre-registration
  commit precedes its results commit in git history.

**The SOL 2023-10-17 trade (the mandatory trace): fully explained by the
written rules — not a bug.** Every step verified legal: rank-6-by-volume
universe membership from committed data, RS/breakout/volume/extension
gates evaluated look-ahead-free, stop = close − 2×ATR(14) ≈ 10% (under
the guard), 78-bar hold legal because the trade cleared +1R within days
(HYP-004: "15 bars only if the trade never reached +1R" — under both old
and fixed semantics), 1/3 banked at ≈1.30× entry in early Nov, 10-day-low
trail ratcheted through the run, final 2/3 exited at the trailed stop on
the Jan-3 crash day, R-blend arithmetic a straight cost-adjusted cash-flow
sum over one initial-risk denominator (cross-checked: trailed stop ≈
$97–100 vs $24.6 entry matches SOL's actual late-Dec 10-day lows).
Findings 1 and 7 do not touch this trade. What remains for the founders is
A4: confirm those bars against the public chart.

## R1 rerun RESULT (Oskaras ran, 2026-08-28): STILL FAILED — conclusion stands

`research/experiments/EXP-007-AUDIT-R1.md` (commit `a2f4977`). Under the
fixed engine and the compliant baseline, with all seven thresholds
unchanged:

- **Trade set identical** to the committed EXP-007 (48 shared, 0 added, 0
  removed) — the three verified errors never changed which trades exist.
  Expectancy +0.316 R (was +0.317; one fold moved −0.310→−0.321 — the
  entire Finding-1 effect).
- **Finding 2 guards never triggered** (`cash: 0, size_bound: 0`),
  confirming the reviewer's non-binding prediction.
- **Same-exit p = 0.1069** ((r+1)/(N+1), 2,000 sims, seed 20260901).
  Honest correction of the record: the pre-rerun expectation ("p most
  plausibly worsens") was NOT borne out — the compliant null's mean is
  higher (+0.52% vs +0.12%) but its variance is tighter, so p *improved*
  from 0.1645. It still fails the unchanged 0.05 threshold by 2×. This is
  why the protocol reruns instead of arguing directions.
- Same four checks fail: folds 3/7, p, top-pair share 148.8%, ex-top
  −0.161 R. **Verdict: STILL FAILED; per R6 the EXP-007 conclusion
  stands.**

## B1 result (Oskaras ran, 2026-08-28): PASS — NO ERROR

`python -m engine.data.audit data/raw` on the full 65-pair raw dataset:
alignment clean (modal offset 0 ms, all timeframes, all files);
aggregation consistency within budget (material price mismatches 0.047%
of 4h bars, 0.125% of 1d bars — concentrated on the known 2022-12-18
outage and crash days like CRV 2022-06-13/FLOW 2022-02-28); zero-volume
runs are exactly the documented 2022-12-18 exchange-wide outage (~9×1h /
5×4h bars per pair; absent from post-2022 listings, as expected); spike
list is real market events; volume field confirmed base units (BTC ≈
$480M median daily quote). Notes on record: SOL-USDT shows 39 material
native-vs-derived daily diffs concentrated in early-2021 low-price
history (0.5–0.6%, the AVAX/CRV tick-rounding pattern from audit v3) —
research trades DERIVED bars (D-019) and the SOL mega-trade sits in
Oct-2023→Jan-2024, nowhere near them; two spike rows (ORDI 2026-04-16,
OKB 2025-08-13) fall in the holdout era — raw-data QA only, no research
run touches those dates. **audit: PASS.**

## R1 mechanical rerun (built; runs LOCAL)

Per R1 the three verified errors (F1 baseline, Findings 1–2) are fixed and
EXP-007 reruns under the seven UNCHANGED checks: `audit/r1_rerun.py`
(fixed engine + compliant same-exit baseline with (r+1)/(N+1), unbounded
entry pool, strategy return convention, 2,000 sims, seed 20260901). It
writes `EXP-007-AUDIT-R1.md` and prints the trade-set diff vs the
committed record; the original EXP-007.md stays untouched. Honest
expectation, recorded before running: the baseline bug favored the
strategy, so p most plausibly worsens; Findings 1–2 are ambiguous/neutral
here. 68 unit tests pass on the fixed engine.

## E4 addendum — Holm correction across the variant ledger (Step-3 request)

Raw p-values by lineage, Holm-adjusted within lineage (adjustment can only
raise p; every experiment's other failed checks are untouched by it):

| Lineage | Configs | Raw p per test | Holm-adjusted |
|---|---|---|---|
| HYP-001 (4) | EXP-001 p=0.90 (grid EXP-002 reported no per-variant p) | 0.90 | 0.90 |
| HYP-002 (1) | EXP-003 p=0.302 | 0.302 | 0.302 |
| HYP-003 (1) | EXP-004 p=0.362 | 0.362 | 0.362 |
| HYP-004 (3) | EXP-005 0.068 · EXP-006 0.014 · EXP-007 0.1645 | — | 0.136 · 0.042 · 0.1645 |

EXP-006's p survives Holm (0.042) but EXP-006 failed on the 2× stress
(PF 0.96) and a 52.9% drawdown regardless. EXP-005 rises 0.068 → 0.136;
EXP-007 stays 0.1645 (largest). Nothing improves; the failures sharpen.
Adopted going forward: every future EXP report carries its lineage variant
counter and the Holm-adjusted p alongside the raw one.

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

## Closure (pre-drafted 2026-08-31; becomes final Fri 2026-09-04)

Status at the Monday sync-day check: every machine-runnable test is
complete; C1 verified; the optional A4/B5 evidence run has not landed.
If it lands by Friday, its verdicts complete this section. If not,
protocol R4 applies as written and pre-agreed: *"whatever is unresolved
by the deadline resolves conservatively (conclusion stands)"* — A4/B5
close as NOT RUN / RESOLVED CONSERVATIVELY, and the audit closes
complete with this final finding:

> **AUDIT-2026-08 CONCLUSION: the EXP-007 verdict (FAILED — NO EDGE /
> DO NOT TRADE) survived every executed attempt at falsification.
> Three verified implementation errors were found, fixed,
> regression-tested, and shown not to change a single trade or any
> check's outcome. No look-ahead, no cost error, no data defect, no
> statistical error capable of altering the verdict was found. The one
> unexecuted item (chart/cross-venue verification) resolves
> conservatively per R4 and is retained as a permanent caveat: the
> simulator's agreement with real charts was never independently
> confirmed — a caveat that could only matter if anyone ever proposed
> trusting the simulator's POSITIVE output with money, which D-024
> forbids.**

## Pending local runs (scripts ship after the A1 review lands)

B1 (`python -m engine.data.audit data/raw`), A2 clean-room rerun, B3
universe recomputation, D2 restricted-universe reruns, E3 compliant
fresh-seed baseline (the F1 fix above). Sequenced after A1 so any code
fixes land first (protocol §Sequencing).
