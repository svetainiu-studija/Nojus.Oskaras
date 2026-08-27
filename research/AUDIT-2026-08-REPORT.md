# AUDIT-2026-08 — findings ledger (running)

Protocol: `AUDIT-2026-08-PROTOCOL.md` (committed before any test ran).
Every test lands here, nulls included (R5). Verdicts per test: **NO ERROR**,
**VERIFIED ERROR** (→ fix, rerun affected experiments under unchanged
checks), or **DIAGNOSTIC** (R3: narrative only, never a verdict).

## Status board

| Test | Runs | Status |
|---|---|---|
| A1 code review (2 independent sessions) | CLOUD | in progress |
| A2 clean-room reproduction | LOCAL | pending (script ships after A1) |
| A3 look-ahead property tests | CLOUD | **DONE — NO ERROR** |
| A4 manual chart verification | FOUNDERS | pending (sample below) |
| B1 audit battery on widened raw data | LOCAL | pending: `python -m engine.data.audit data/raw` |
| B2 gaps/duplicates | done 2026-08-27 | **NO ERROR** (run.py quality: 195 files, 0 missing, 0 dupes) |
| B3 independent universe recomputation | LOCAL | pending (script ships) |
| B4 availability-vs-strategy | CLOUD | **DONE — NO ERROR** |
| B5 cross-venue price check | FOUNDERS | pending (trade list below) |
| C1 costs.yaml vs reality | FOUNDERS | pending (Nojus) |
| C2 cost double-count walkthrough | CLOUD | in progress (review session) |
| C3 execution-semantics check | CLOUD | in progress (review session) |
| D1 SOL legitimacy | mixed | partially done (see D3; chart check in A4) |
| D2 restricted-universe recomputation | LOCAL | pending |
| D3 era analysis | CLOUD | **DONE — DIAGNOSTIC** (major, below) |
| E1 independent stats recomputation | CLOUD | **DONE — NO ERROR** (one episode, below) |
| E2 independent bootstrap | CLOUD | **DONE — NO ERROR** |
| E3 baseline reproduction | CLOUD+LOCAL | methodology review in progress; local rerun pending |
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

## Pending local runs (scripts ship after the A1 review lands)

B1 (`python -m engine.data.audit data/raw`), A2 clean-room rerun, B3
universe recomputation, D2 restricted-universe reruns, E3 fresh-seed
baseline reproduction. Sequenced after A1 so any code fixes land first
(protocol §Sequencing).
