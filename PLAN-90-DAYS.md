# 90-DAY PLAN — Verslas (Oskaras / Nojus)

Version 0.2 · 2026-08-26 · Covers 27 Aug – 25 Nov 2026 · Read CHARTER.md first.

Purpose of the 90 days: find out, with evidence, whether you have a strategy worth publishing, and get the machine that publishes it running unattended. Revenue in this window: **€0 by design.**

**Day-90 deliverable (D-014):** at least one strategy has passed G0, the signal engine has run unattended for ≥ 7 days, and the private paper-forward test has started. G1 follows in January 2027; public launch February 2027.

Scope discipline: Oskaras is building everything from zero at 10–20 h/week. Anything not needed for the day-90 deliverable is out (no CI, no polished performance page, no landing page yet). Expect the build to take 1.5–2× the estimate; the week-4 checkpoint exists to catch that early.

## Phase 0 — Set up (Weeks 1–2, 27 Aug – 9 Sep)

| # | Task | Owner | Done when |
|---|---|---|---|
| 0.1 | Confirm or override D-001…D-014 in DECISIONS.md | Both | Statuses changed from Proposed |
| 0.2 | Agree risk limits: max portfolio drawdown (proposal 25%), per-trade risk (proposal ≤ 1% of equity), max concurrent positions, portfolio-heat cap, max leverage for any future perps variant (proposal: none in year 1) | Both | Written into CHARTER §5 (G0 row) |
| 0.3 | Founder agreement (D-011): equity, vesting, IP, account ownership, credential vault, leaver terms, runbook commitment | Both | Signed; template reviewed by the lawyer in 0.4 if budget allows |
| 0.4 | Book a 1-hour consult with a Lithuanian fintech/crypto lawyer; send the 6 questions in DECISIONS.md | Nojus | Appointment booked; answers logged as D-017+ |
| 0.5 | Verify on your own accounts: OKX Europe lead-trader eligibility (spot) and requirements; OKX EU, Kraken and Bitvavo affiliate access from Lithuania and their promotion rules | Nojus | Findings in STATUS.md |
| 0.6 | Verify payment-rail acceptable-use policies for a paid trading-signal community: Stripe, Paddle, Whop (D-007) | Nojus | Which rails permit it, in writing (support ticket or policy quote) |
| 0.7 | Brand: shortlist 5 names; check domain, Telegram handle, X and YouTube handle availability; pick one; reserve handles | Nojus | Name chosen, handles reserved |
| 0.8 | Write down 2–3 strategy hypotheses from your discretionary trading using the template below | Both | Filled templates in repo `research/hypotheses/` |
| 0.9 | Create the private strategy repo (layout below) with `CLAUDE.md` mirroring CHARTER §4 and the protocol; Python env; pick the data sources (OKX history candles, Kraken downloadable history, and a public historical dataset for research — Kraken's live OHLC endpoint only returns recent candles); download ≥ 4 years of daily/4h/1h spot data for the top ~30 liquid pairs; record dataset version IDs | Oskaras (with Claude) | `make data` reproduces the dataset; README documents sources and versions |
| 0.10 | Cost model per exchange: taker/maker fees, typical spread by pair, slippage assumption by order size, execution delay (bar close → fill), missed-fill rule, min order sizes | Oskaras | `costs.yaml` reviewed by Nojus |
| 0.11 | Budget split, expense log, and the €1k-vs-€5k scenario decision | Both | Sheet exists |
| 0.12 | Decide the shared credential vault and 2FA setup for all accounts | Both | Vault in use |

## Phase 1 — Strategy research + engine skeleton (Weeks 3–8, 10 Sep – 21 Oct)

Two-week sprints. Each candidate goes through the protocol below and ends with a one-page report. The backtester and the live engine share the same strategy and cost code from day one, so the engine skeleton is built alongside the research, not after it.

| # | Task | Owner | Done when |
|---|---|---|---|
| 1.1 | Backtester: chronological walk-forward, cost model, portfolio-level accounting across pairs with heat cap, holdout lock (holdout dates written down before research starts), bootstrap CIs, BTC buy-and-hold and random-entry baselines. Use an existing library if it fits (e.g. vectorbt / backtesting.py) rather than writing one; keep custom code to strategy + costs + reporting | Oskaras (with Claude) | Toy strategy runs end-to-end; unit tests for costs and gates pass |
| 1.2 | Sprint A (weeks 3–4): codify hypothesis 1 → backtest → walk-forward → report `EXP-001…` | Oskaras | Report filed |
| 1.3 | **Week 4 checkpoint (23 Sep):** hours actually spent vs plan; if < 70%, re-scope before continuing | Both | Decision logged |
| 1.4 | Sprint B (weeks 5–6): hypothesis 2 | Oskaras | Report filed |
| 1.5 | Sprint C (weeks 7–8): hypothesis 3 or the strongest candidate's robustness pass (parameter sensitivity, regime breakdown, variant count) | Oskaras | Report filed |
| 1.6 | Engine skeleton: one scheduled script (cron on a €5 VPS) that pulls latest bars, runs the frozen strategy config, applies the deterministic gates, writes a signal record with immutable ID and timestamp; dry-run mode | Oskaras (with Claude) | Runs on schedule for 3 days in dry-run |
| 1.7 | Independent G0 review of any candidate that looks like passing: reproduction from raw data in a separate Claude session (read-only reviewer prompt), plus a human with quant skills if one can be found | Oskaras arranges | Review notes attached to the report; builder ≠ approver |
| 1.8 | Distribution plan: where the first 500 members come from without paid ads and without a face (X/Twitter, Reddit, YouTube faceless explainers, Lithuanian and English communities, cross-posting rules); weekly content cadence; what the channel promises and does not | Nojus | 2-page plan with weekly targets |
| 1.9 | Content system: post types (signal, weekly recap, "why this call", market-structure note, drawdown post), templates, tone; 15 evergreen educational drafts | Nojus | Templates + 15 drafts |
| 1.10 | Study 10 established signal/analysis channels: pricing, what they show, how they build trust, what they get wrong; 1-page positioning note | Nojus | Note in `brand/` |
| 1.11 | Apply to affiliate programmes (OKX EU, Kraken, Bitvavo); do not publish links yet | Nojus | Approvals logged |

**Week 8 checkpoint (21 Oct): G0 review.** Pass → Phase 2. No pass → sprints continue to the hard stop at week 12 (18 Nov); then the pivot criteria in CHARTER §9 apply.

## Phase 2 — Harden the machine, start the paper forward (Weeks 9–13, 22 Oct – 25 Nov)

| # | Task | Owner | Done when |
|---|---|---|---|
| 2.1 | Freeze the passing strategy: version-pinned config, hash recorded, no further edits (edits = new version = new validation) | Oskaras | Config hash in DECISIONS.md |
| 2.2 | Poster: Telegram bot posts each signal to a **private** channel at emit time (pair, side, entry, invalidation, size rule, timestamp, strategy version, signal ID); closes posted with result net of modelled costs; late-signal cut-off enforced | Oskaras | 7 days of automated posts |
| 2.3 | Integrity: daily hash of the signal log committed to a public git repo (or OpenTimestamps); "engine offline" auto-post on missed runs; structured logs; failure alert to both phones | Oskaras | Simulated outage produces the post and the alert |
| 2.4 | Data-quality checks: gaps, symbol renames, delistings, stale feeds; weekly QA report generated automatically | Oskaras | First weekly report produced |
| 2.5 | Minimal report generator: markdown/HTML summary of D-008 metrics from the signal log (this becomes the public performance page later) | Oskaras | Report regenerates on each close |
| 2.6 | Runbook: how to restart, how to flatten, how to pause, where the logs are — written so Nojus can execute it | Oskaras | Nojus performs a restart from the runbook alone |
| 2.7 | **Unattended run ≥ 7 consecutive days** with zero manual intervention | Oskaras | Achieved and logged |
| 2.8 | **Paper forward starts** (target: by week 11, 4 Nov); weekly 30-minute reviews comparing realised paper results with the backtest distribution; no strategy edits during the run | Both | Start date logged; reviews logged weekly |
| 2.9 | Launch content bank: 30 posts; channel description; pinned "how to read our signals" and risk-warning posts; landing-page copy (page built after day 90) | Nojus | Ready in `brand/` |
| 2.10 | Legal follow-through: draft terms, imprint, privacy policy, risk wording from the consult (lawyer review before G3, not now); decide virtual office | Nojus | Drafts in `legal/` |
| 2.11 | Lead-account prep: open/verify the OKX Europe account under the brand pseudonym; document what followers see, settlement, limits. No capital yet. | Nojus | Notes in STATUS.md |
| 2.12 | Exam-season plan: on-call rota for Dec–Jan, what is allowed to be paused, what is not | Both | Rota in STATUS.md |

**Day 90 (25 Nov): deliverable check** — G0 passed, engine unattended ≥ 7 days, paper forward running. Then the paper forward runs through the exam session with 30-minute weekly reviews; **G1 review in weeks 18–20 (mid/late January 2027)**.

## After day 90 (orientation only)

Jan 2027: G1. Feb 2027 (month 6): entity registered before any payout; public launch of the free channel; distribution plan live; affiliate links with "Reklama" labels; lead account seeded €200–300 without followers; performance page public. May 2027 (month 9): first affiliate revenue expected. Aug–Nov 2027 (months 12–15): G2 (≥ 6 months public, ≥ 60 closed signals) → followers enabled on the lead account; G3 → paid tier. €500/month net target: months 12–18. Re-plan with real data at month 12.

## Strategy research protocol (mandatory for every candidate)

1. **Hypothesis first.** Write the economic reason the edge exists (who is on the other side and why they lose) before touching data. No reason → no sprint.
2. **Data.** Versioned OHLCV; record dataset ID, source, pairs, timeframe, date range, gaps handled. Test period ≥ 4 years where data exists, including the 2022 bear. Survivorship: include delisted pairs where possible, or define the universe by liquidity rules that could have been applied at the time.
3. **Splits.** Chronological only. Training → validation → walk-forward folds → final holdout (fixed dates written down before research starts, opened exactly once, after everything else is final). Reusing the holdout invalidates the candidate.
4. **Costs.** Fees, spread, slippage, execution delay, missed fills, tick/lot/min-order sizes; funding and liquidation for any perps variant. Stress at 2× costs.
5. **Portfolio level.** Results are measured across all pairs together with the heat cap and max-concurrent-positions rule, not per pair in isolation.
6. **Baselines.** BTC buy-and-hold (risk-adjusted) and a random-entry / same-exit Monte-Carlo baseline. A strategy that does not beat both is market beta, not edge.
7. **Metrics.** Trade count, expectancy net of costs, profit factor, max drawdown and its duration, average win/loss, per-regime breakdown (bull/bear/range by a rule defined in advance), symbol concentration, bootstrap 80% confidence intervals for expectancy and PF.
8. **Overfitting controls.** Few parameters; report sensitivity to each; no parameter chosen by looking at out-of-sample results; count every variant tried and report it; holdout pass threshold scaled to that count.
9. **Report.** One page per experiment ID: hypothesis, config version, dataset version, results, baselines, what would falsify it, reviewer notes.
10. **Approval.** Independent reproduction from raw data before G0. Builder ≠ approver.

## Repo layout (proposal)

```
verslas-signals/
  README.md            # how to reproduce everything
  CLAUDE.md            # project rules for Claude sessions (mirror CHARTER §4 + protocol)
  data/                # raw + processed, versioned, git-ignored
  research/
    hypotheses/        # HYP-001.md … (template below)
    experiments/       # EXP-001.md … one page each
  strategy/            # frozen strategy configs, version-pinned, hashed
  engine/              # signal engine, gates, cost model (shared with backtester)
  poster/              # Telegram bot
  report/              # D-008 metrics generator
  tests/
  runbook/             # restart / flatten / pause / on-call
  legal/               # drafts only; nothing secret
  brand/               # positioning, distribution plan, templates, content bank
```

## Hypothesis template

```
ID: HYP-00X
Name:
Setup (what you look for, in rules a computer can check):
Entry rule:
Exit rules (target / invalidation / time stop):
Position sizing rule:
Universe (pairs, timeframe):
Why it should work (who is on the other side and why they lose):
What would make you abandon it:
Your discretionary experience with it (years, rough hit rate, worst period):
```

## Weekly rhythm

Monday 1-hour sync: review STATUS.md, log decisions, assign the week's tasks, compare hours spent with plan. Every experiment, dataset and config gets an ID. Nothing is claimed as "working" without the report.
