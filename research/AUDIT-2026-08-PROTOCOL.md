# Forensic audit protocol — AUDIT-2026-08 (pre-registered, D-023)

**AMENDED 2026-08-28 (D-023 amendment, Oskaras):** the audit closes **Fri
2026-09-04** (was 09-11). DROPPED: A2 clean-room reproduction, the
standalone fresh-seed E3 reproduction (superseded — the compliant
same-exit baseline ran inside the R1 rerun), B3, D2, and any EXP-007-only
diagnostic that cannot change the decision. Everything else ran to
completion; open at amendment time: A4, B5 (Oskaras) and C1 (Nojus).
R1–R6 unchanged.

Declared 2026-08-28, committed BEFORE any audit test below is run. Proposed
by Oskaras; scope agreed as: **verify the conclusion, do not reopen the
search.** The conclusion under audit: "signal research is over because
every tested strategy failed its pre-registered rule" — with the momentum
lineage (HYP-004/005/006, EXP-005/006/007) as the primary target since it
came closest.

## Rules (these preserve D-022)

- **R1 — Only verified errors change verdicts.** A verified error is a
  demonstrable implementation bug, data defect, cost mis-modelling, or
  statistics bug. When one is found: fix it, rerun ONLY the affected
  experiment(s), and re-evaluate their **unchanged** pre-registered checks
  mechanically. No parameter, rule, threshold, or universe change can
  rescue a hypothesis. "The strategy needs diversification / asset-neutral
  constraints" is a NEW strategy — out of audit scope; pursuing it would
  need both founders to explicitly supersede D-022's "no further rounds"
  in a new decision, and is not part of this audit.
- **R2 — Symmetry.** Errors that *inflated* results are fixed and rerun
  exactly the same as errors that deflated them. If a fix makes results
  worse, that stands too. We audit because the decision is large, not
  because the answer was negative — and the record must survive that
  criticism, so every finding is reported regardless of direction.
- **R3 — Diagnostics never decide.** Robustness/sensitivity computations
  (alternative universe subsets, leave-one-out concentration, era
  analysis) inform the post-mortem narrative only. Their interpretation
  rule is fixed now: they can change *what we write about* the result,
  never its PASS/FAIL.
- **R4 — Time box.** Two weeks: audit closes **2026-09-11**. Anything
  unresolved by then resolves conservatively (conclusion stands).
- **R5 — Findings ledger.** Every test's outcome goes in
  `research/AUDIT-2026-08-REPORT.md` (running document), including nulls.
- **R6 — Outcome mapping.** All tests pass → the EXP-007 verdict stands
  and the §9 pivot decision (a/b/c in PIVOT-DISCUSSION-2026-08.md)
  becomes D-024. Verified error found → fix → rerun affected experiments
  → verdicts re-evaluated; if a rerun then passes ALL its original
  checks, the hypothesis re-enters exactly where a pass would have put it
  (the full G0 battery), nothing more.

## Corrections to the audit request (recorded up front)

- The cost model in this repo is **OKX-based**: taker fee both ways +
  half-spread + slippage from `costs.yaml`; decisions at bar close, fills
  at next open; resting-stop intrabar fills; 2× stress rerun. There are
  **no MEXC fees and no 60-second-delay parameter anywhere in the repo**
  (MEXC is also excluded as a venue by D-004 — not MiCA-authorised for
  EEA). The audit verifies what is actually implemented (C-tests). If the
  founders intended a different venue's cost profile, that is a config
  decision to raise separately, not an audit finding.
- Multiple-testing (E4): EXP-007's rule used a RAW p < 0.05 with no
  family-wise correction across the 9 configurations tried. Any proper
  correction makes that bar *stricter*. This item can therefore only
  strengthen the failure, never rescue it — stated now so nobody is
  surprised later.
- Expectation-setting for the C-tests: the four checks EXP-007 failed
  (folds, p-value, both concentration checks) are structurally
  cost-insensitive, and EXP-007 already PASSED the 2× cost stress. Cost
  findings are unlikely to flip the verdict in either direction; they are
  audited anyway because G0 would need them right.

## Tests

Each test states its method and its **error criterion** (what counts as a
verified error). Runs marked LOCAL need the bar data, which exists only on
Oskaras's machine (data/raw and data/derived are gitignored); Claude ships
the scripts, Oskaras runs and pastes. Runs marked CLOUD run in Claude
sessions on committed files. FOUNDERS = by hand.

### A — Implementation

- **A1 (CLOUD) Adversarial code review** of `simulator.py`, `hyp004.py`,
  `indicators.py`, `metrics.py`, `costs.py`, `experiment.py`,
  `sprint_d.py`, `sprint_e.py` by independent review sessions that did not
  build the code, primed to find result-affecting bugs in either
  direction, look-ahead above all. Error criterion: a demonstrable
  behavioral divergence from the hypothesis file / pre-registration /
  declared execution model, or any read of data beyond the decision bar.
- **A2 (LOCAL) Clean-room reproduction.** A separate implementation of
  HYP-004's rules written from `research/hypotheses/HYP-004.md` and the
  NOTES pre-registrations alone — no reading of engine strategy/simulator
  code — run on the same derived daily data. Reconcile trade-by-trade
  with EXP-007.trades.csv. Error criterion: any trade-set or outcome
  divergence not attributable to a *documented* interpretation choice
  (I-notes); headline expectancy differing by more than ±0.02 R after
  reconciliation.
- **A3 (CLOUD) Look-ahead property tests.** Re-verify the pinned
  no-look-ahead tests and add adversarial cases (indicator values at bar t
  must be invariant to mutations of bars > t; entry decisions at close t
  invariant to bars > t). Error criterion: any failing case.
- **A4 (FOUNDERS) Manual chart verification.** Sample rule (fixed now):
  every 5th trade of EXP-007.trades.csv by entry date — trades #1, 6, 11,
  16, 21, 26, 31, 36, 41, 46 — plus the 3 largest SOL winners if not
  already sampled. For each, on OKX/TradingView charts: entry day was a
  genuine 20-day-high close by a top-RS leader with the volume condition;
  the fill equals the next day's open; the stop/exit path matches the
  bars. Error criterion: any sampled trade not reproducible on the public
  chart beyond tick/rounding tolerance.

### B — Data

- **B1 (LOCAL) Full audit battery on the widened dataset.**
  `python -m engine.data.audit data/raw` never ran on the 35 new pairs
  (an honest gap in the Sprint E flow — the run went download → quality →
  derive without it). Error criterion: audit FAIL by its existing v3
  thresholds on any pair that produced EXP-007 trades.
- **B2 (DONE, attach) Gaps/duplicates.** run.py's quality report printed
  clean on 2026-08-27 (0 missing, 0 dupes, 195 files); attach to the
  report. Error criterion: any nonzero on a traded pair.
- **B3 (LOCAL) Independent universe recomputation.** A standalone script
  (no engine imports) recomputes point-in-time top-30 by trailing 90-day
  quote volume with the ≥90-day listing-age filter for 20 dates fixed
  now: the 1st of each month 2022-01 … 2023-08. Error criterion: any
  membership mismatch vs `data/universe.csv`.
- **B4 (CLOUD) Availability-vs-strategy check.** From universe.csv alone:
  no pair is a member before (first bar + 90 days); each new pair's first
  membership date is consistent with its bar count. Error criterion: any
  violation.
- **B5 (FOUNDERS) Cross-venue price check.** For the 5 largest EXP-007
  winners (by R): check OKX daily closes on entry and exit days against a
  second venue's chart (Kraken/Binance on TradingView). Error criterion:
  a divergence large enough to change that trade's outcome.

### C — Costs & execution

- **C1 (FOUNDERS/NOJUS) Verify costs.yaml against reality** — the VERIFY
  task open since WP2, now blocking: OKX spot taker fee for a regular
  account, and eyeballed spreads on 5 majors + 5 small pairs from the
  pool. Error criterion: a real-world value materially worse than
  costs.yaml stress already covers, or materially better in a way that
  changes any EXP-007 check (see expectation note above).
- **C2 (CLOUD) Cost double-count walkthrough.** Trace one winning and one
  losing trade end-to-end through entry/exit cost application; document
  the arithmetic in the report. Error criterion: any cost applied twice,
  with the wrong sign, or to the wrong notional.
- **C3 (CLOUD) Execution-semantics check.** Confirm the declared model
  (close-decision → next-open fill; resting-stop intrabar fills at the
  level, gap-through at open, stop-before-target ordering; 4h parity
  windows in EXP-006) matches the simulator, and that EXP-007's
  close-confirm sensitivity row used the same trades pipeline. Error
  criterion: divergence between declaration and code behavior.

### D — HYP-004 / SOL forensics (diagnostics under R3)

- **D1 (CLOUD+FOUNDERS)** List every SOL trade with dates and R; verify
  each was a legitimate top-RS member at entry (cross-check with B3
  dates; A4 sample includes the 3 biggest SOL winners).
- **D2 (LOCAL)** Recompute EXP-007's headline numbers restricted to (a)
  the always-in-universe subset and (b) the original 30-pair universe on
  the same widened build. Fixed interpretation: narrative only.
- **D3 (CLOUD)** Era analysis from the trades CSV: are SOL's profits one
  contiguous period? Leave-one-out concentration for every pair — is SOL
  unique, or is the book generally lumpy? Narrative only.

### E — Statistics

- **E1 (CLOUD) Independent recomputation** of every headline number in
  EXP-007.md from EXP-007.trades.csv using a standalone stdlib-only
  script (`verslas-signals/audit/`, no engine imports): trade count,
  expectancy, PF, win rate, avg win/loss, folds, per-year, concentration,
  ex-top expectancy. Error criterion: any number beyond rounding.
- **E2 (CLOUD) Bootstrap reimplementation.** Independent resampler for
  the CI80s; methodology review of `metrics.py`. Error criterion: CI
  bounds shifted by > 0.05 R / 0.1 PF, indicating a bug rather than seed
  noise.
- **E3 (LOCAL) Baseline reproduction.** Review `random_baseline` for
  spec-compliance (uniform draws over tradable in-universe bar-pair
  space, same exits, same costs), then reproduce the p-value with an
  independent implementation and a different seed. Error criterion:
  spec divergence, or a reproduced p < 0.05 where the original reported
  ≥ 0.05 (either triggers root-cause before any conclusion).
- **E4 (CLOUD) Multiple-testing accounting.** Report raw p-values next to
  the variant count (9 configs; 3 in the momentum lineage) and what a
  family-wise correction would imply. Per the correction note: this can
  only strengthen the conclusion.
- **E5 (CLOUD) Concentration robustness.** Pre-specified alternates only:
  leave-one-out per pair (D3), share computed on gross-positive R
  (sum of winners) as an alternative denominator to net R. Narrative
  only.

## Sequencing

1. This protocol commits first (this file). 2. CLOUD tests run in Claude
sessions; A1 reviewers are sessions that did not write the code. 3. LOCAL
scripts ship in `verslas-signals/audit/`; Oskaras runs them after the
CLOUD code-review findings are in (so any fixes land first). 4. FOUNDERS
items run in parallel; A4/B5/C1 results pasted into chat, Claude logs
them. 5. Report closes by 2026-09-11 with a single verdict per R6, then
the founders make D-024.
