# CHARTER — Verslas (Oskaras / Nojus)

Version 1.0 · 2026-08-26 · Status: **adopted — D-001…D-016 accepted by both founders on 2026-08-26** (see DECISIONS.md)
v0.2 incorporated an independent review (see STATUS.md log): timeline re-based, gates corrected, copy-trading account brought inside the validation framework, founder agreement and entity timing added.
v1.0: founders confirmed all decisions; agreed risk limits (D-015) written into §5; budget ceiling (D-016) confirmed.
v1.1 (2026-08-27): D-017 accepted and written into G2 — AI analyses never satisfy a written-legal-opinion requirement; a fintech lawyer's written opinion on the copy-trading qualification is required before followers are enabled.
v1.2 (2026-08-27): factual correction from programme verification (research/RAILS-AND-PROGRAMMES-2026-08.md) — OKX **spot** lead-trading profit share is 8–13% (the "up to 30%" figure is futures-only); §3 economics restated accordingly.

## 1. Objective

Build a pseudonymous crypto trading-intelligence brand that produces recurring, mostly automated income for two part-time founders by (1) proving a systematic strategy in public, then (2) monetising the proven track record through exchange affiliate commissions, an exchange copy-trading lead account, a paid spot-signal tier and, later, software.

Ambition: **€5,000+/month net**. This is a 36-month-plus destination, not a planning input. The plan is built around stage gates; the first gate that matters is a strategy with positive cost-adjusted expectancy that beats doing nothing. Nothing is sold before the gates pass.

"Passive" is the end state, not the starting point. The first 6–9 months are front-loaded work: strategy research, automation, audience. Passivity comes from automating signal generation, posting, performance reporting and billing.

"Pseudonymous" means: not on camera, no personal names in content. It does **not** mean unfindable: the company and its members are in the public register, the imprint shows the company and its registered address, exchanges and payment providers KYC the founders, and complaints reach real names.

## 2. Founders, roles, commitment

| Who | Owns | Notes |
|---|---|---|
| Oskaras | Systems: strategy research, backtest/validation pipeline, signal engine, automated posting, performance reporting, security, runbook | Builds with Claude as pair programmer; no prior codebase exists |
| Nojus | Brand & market: brand and channel operations, content, distribution, community, exchange programmes (affiliates, lead account), customer support, lawyer/accountant liaison, payment rails | Front of house, pseudonymous |
| Both | Strategy hypotheses from 3+ years of discretionary trading; weekly review; every material decision logged | Weekly 1-hour sync; hours actually spent are logged |

Commitment: 10–20 h/week each for the first 6 months, alongside studies (exam sessions in December/January and May/June are planned around: automated phases run through them, build phases do not). Risk budget: ≤ €5,000 total, confirmed (D-016); §7's €1,000 minimum scenario remains the fallback lever. Founders accept ≥ 9 months of zero revenue.

A written **founder agreement** (D-011) is a Phase 0 deliverable: equity split, vesting, IP assignment to the future company, ownership of handles/domain/accounts, shared credential vault, what happens if one founder leaves, and a runbook so that Nojus can operate the engine if Oskaras is unavailable.

## 3. Business model — revenue streams in launch order

| # | Stream | Mechanism | Earliest | Depends on | Evidence (RESEARCH doc) |
|---|---|---|---|---|---|
| 1 | Exchange affiliate | Referral links to MiCA-authorised exchanges only: OKX Europe 30% of referred fees (up to 50%), Kraken (negotiated, up to 50%), Bitvavo 15%. Posts labelled "Reklama". | Public launch (month 6) | Audience; entity registered before first payout | Official programme pages; realistic €2–20/month per *active* referred trader |
| 2 | Copy-trading lead account | Pseudonymous lead-trader account on OKX Europe running **the same frozen, validated strategy the channel publishes** (spot lead-trading first). Exchange executes followers' copies under its licence and pays profit share (**spot lead-trading: 8–13%**, tiered by 90-day average AUM, settled weekly; the "up to 30%" often quoted is futures-only). | Followers enabled after G2 (month 12+); account itself seeded after G1 with €200–300 | G1 (small own capital), G2 (followers, incl. D-017 legal sub-gate); D-012 execution policy | OKX EU help pages, verified 2026-08-27 (research/RAILS-AND-PROGRAMMES-2026-08.md); public lead-trader list placement requires 100k USDT lead assets — our followers come from our own channel |
| 3 | Paid spot-signal tier | €29–49/month (VAT-inclusive pricing), same non-personalised content to all members | After G3 (month 12–18) | G2 + legal opinion + entity + payment rail AUP-approved | Whop/Skool price data; ~3% free→paid benchmark |
| 4 | Software | Dashboard, journal, backtester or signal API as SaaS | Month 12+ or as pivot | Demand signal from members, or streams 1–3 stalling | — |

Copy-trading economics, so nobody fools themselves (corrected 2026-08-27): the spot profit share is **8–13%** of *followers' realised profit*. €50,000 of follower capital earning 3%/month net is €1,500 profit → **€120–195/month** to us; in a drawdown month it is €0. A new lead trader typically attracts far less than €50k, and without 100k USDT of lead assets the account gets no placement on OKX's public list — followers must come from our own channel. Stream 2 is a multiplier on a proven record, not a starting income.

Explicitly rejected: reselling / retail arbitrage; publishing perps recommendations while pseudonymous; Binance / MEXC / Bitget affiliate links; discretionary trading of the lead account; trading own capital as "the business".

## 4. Non-negotiables (legal, ethical, risk)

1. **Signal-only, for others.** No order execution for anyone else, no custody, no managing anyone's money, no wallet access, no withdrawals. Copy trading is executed by the exchange under its own licence; we are a lead trader only. Any automation that places orders on *our own* lead account is a separate execution project that needs Oskaras's explicit approval (D-012); until then, orders on the lead account are placed by hand, mirroring the engine's posted signals exactly, with a reconciliation log.
2. **Non-personalised only.** No DMs advising individuals, no "this suits you", no tiered advice. Identical content to everyone. Q&A is educational and general.
3. **Public signals are spot-only while pseudonymous.** No published perpetual-futures or derivatives recommendations unless a named person and MAR-compliant disclosures are in place (D-003). A perps variant of the strategy for the lead account needs its own G0 with funding and liquidation modelled, and is never published as a signal.
4. **Never promise returns.** Win rate is never a selling point. Publish trade count, expectancy, profit factor, maximum drawdown, average win/loss, fees included, with confidence intervals. A/A+ labels are rule-based quality classes, never guarantees.
5. **Immutable, anchored track record.** Every signal is timestamped at posting with an immutable ID; a daily hash of the full signal log is published to a second, independent venue (e.g. a public git commit or an OpenTimestamps anchor); the performance page is computed from the log; no deletions, no retroactive edits; mistakes are corrected by a new, timestamped post. Signals not posted within N minutes of bar close are discarded and the gap is posted.
6. **Deterministic risk gates** before any signal goes out. No martingale, no averaging down, no automatic stop widening, no leverage beyond the strategy's defined limit, position-sizing and portfolio-heat rules stated publicly. Production strategies are frozen; challengers are validated separately and promoted only after independent review. Manual intervention on the lead account is **flatten-only** and publicly logged.
7. **Conflicts of interest.** Founders trade the published signals only at or after the post timestamp, never before. This, and the lead-account profit share and affiliate income, are disclosed on the channel and the site.
8. **Only MiCA-authorised exchanges are promoted** to EU residents. Verify the legal entity in the ESMA register before signing any affiliate agreement; read each programme's promotion rules (no paid search, no misleading claims).
9. **Consumer law and privacy.** Legal entity disclosed in terms and imprint (virtual office if the founders do not want a home address public); distance-contract rules (14-day withdrawal or explicit digital-content waiver; "order with obligation to pay" wording); clear risk warnings on every channel; "Reklama" labelling; privacy policy, lawful basis for the email list, data-processing agreement with any membership bot or payment provider (GDPR).
10. **Security.** No secrets in repos, docs or chats; 2FA everywhere; separate exchange sub-accounts; API keys read-only wherever possible and never withdrawal-enabled; shared credential vault; no passwords, keys, seed phrases or tokens ever pasted into Claude or messages.
11. **Capital.** Never risk more than the agreed budget. Lead-account capital goes in only after G1, starts at €200–300, and is treated as expendable.
12. **Entity before income.** The company (or registered individual activity) exists, with an accountant, before the first affiliate or profit-share payout is received (D-006).

## 5. Stage gates

| Gate | Name | Pass criteria (all required) |
|---|---|---|
| G0 | Backtest | Rules fully written down and reproducible from raw data. Test period ≥ 4 years where data exists, including the 2022 bear market. ≥ 200 closed trades. Costs modelled: taker/maker fees, spread, slippage, execution delay, missed fills, tick/lot/min-order sizes (funding and liquidation too for any perps variant). Portfolio-level results across all pairs respecting the agreed risk limits (D-015): per-trade risk ≤ 1% of equity, max 6 concurrent positions, portfolio heat cap ≤ 6% of equity, no leverage in year 1. Cost-adjusted expectancy > 0; profit factor ≥ 1.3 with bootstrap 80% CI lower bound > 1.0; max portfolio drawdown ≤ 25% (D-015). **Beats two baselines:** BTC buy-and-hold on a risk-adjusted basis over the same period, and a random-entry / same-exit Monte-Carlo baseline (p < 0.05). Chronological walk-forward: out-of-sample expectancy positive in ≥ 70% of folds. Final untouched holdout passes at a threshold scaled to the number of variants tried (all variants counted and reported). Independent review found no leakage or look-ahead and reproduced the headline numbers from raw data. |
| G1 | Private paper forward (engineering gate) | ≥ 6 weeks of unattended engine operation. Engine output reconciles 100% with a backtester replay over the same period. Realised paper fills within the modelled cost bounds. Zero manual interventions. Signal count ≥ 70% of the backtest-expected count for the period. Realised results inside the backtest's bootstrap 80% band for that sample size (this is a consistency check, not a profitability proof — 8–16 signals cannot prove expectancy). Data-quality report clean (gaps, renames, delistings handled). |
| G2 | Public forward | **Track-record sub-gate:** ≥ 6 months public and ≥ 60 closed public signals (≥ 100 if the strategy's frequency allows); net PF ≥ 1.3 with bootstrap 80% CI lower bound > 1.0; portfolio drawdown within limit; zero rewrites; hash anchors unbroken. **Audience sub-gate:** ≥ 500 real members via the distribution plan. **Legal sub-gate (D-017):** written opinion from a qualified fintech/crypto lawyer that the copy-trading lead-account setup, as contractually structured, is not a regulated service for us. All three must pass before followers are enabled on the lead account and before G3. |
| G3 | Monetisation | G2 plus: written legal opinion on the paid closed group; entity and accountant in place (already required for stream 1); terms, imprint, privacy policy and risk warnings live; payment rail whose acceptable-use policy explicitly permits the product (verified, not assumed); support and refund process defined. |
| G4 | Scale | ≥ €500/month net for 3 consecutive months → second strategy and/or software. |

## 6. Milestones (conditional on gates; dates assume a 27 Aug 2026 start)

| When | Milestone | Condition |
|---|---|---|
| Week 2 (9 Sep) | Decisions confirmed, founder agreement signed, lawyer consult booked, payment-rail AUPs checked, brand shortlist, hypotheses written, data pipeline started | — |
| Week 4 (23 Sep) | Hours-actually-spent checkpoint; re-scope if < 70% of plan | — |
| Week 8 (21 Oct) | G0 review of candidates | Hard stop for G0 at week 12 (18 Nov) → pivot decision |
| Day 90 (25 Nov) | **G0 passed + engine unattended ≥ 7 days + paper forward started** | This is the 90-day deliverable |
| Weeks 14–20 (Dec – Jan) | Paper forward runs through the exam session (automated; 30-min weekly review) | — |
| Week 18–20 (mid/late Jan 2027) | G1 review | — |
| Month 6 (Feb 2027) | Public launch: free channel, distribution plan live, affiliate links; entity registered before first payout; lead account seeded €200–300 (no followers) | G1 passed |
| Month 9 (May 2027) | First revenue (affiliates) | Audience growing |
| Month 12–15 (Aug–Nov 2027) | G2 → followers enabled on lead account; G3 → paid tier | Track record holds in public |
| Month 12–18 | €500/month net | — |
| Month 24+ | €2,000/month net | ~1,400+ engaged members or equivalent copy-trading following |
| Month 36+ | €5,000/month net (destination) | Multiple streams or software on top |

## 7. Budget

| Item | Estimate | When | In the €1,000 minimum scenario? |
|---|---|---|---|
| Lawyer: 1-hour consult | €150–300 | Week 1–2 | Yes |
| Lawyer: terms, imprint, privacy policy, written opinion on paid group | €500–1,500 | Before G3 | No (deferred until revenue) |
| Founder agreement (template + 1 h lawyer review) | €0–200 | Week 2 | Template only |
| Entity registration, accountant setup, virtual office | €100–300 setup; accountant €50–100/month once revenue; virtual office €10–30/month | Before first payout (month 6) | Registration only, when needed |
| Infrastructure: VPS €5–10/month, domain ~€12/year, data APIs €0–35/month | ~€20–60/month | From week 2 | Yes (free data tiers) |
| Lead-account capital (real money at risk) | €200–300 seed after G1; scale only after G2 | Month 6+ | No |
| Content tooling | €0–30/month | From month 5 | Free tools |
| Reserve | Remainder | — | — |

## 8. Assumptions (stated, to be verified)

1. The discretionary edge from 3+ years of trading can be codified into rules. If it cannot, research starts from standard systematic hypotheses (trend/momentum, volatility breakout, mean reversion on liquid spot pairs) — with the base-rate warning that most such hypotheses fail G0 after costs.
2. OKX Europe lead-trading (spot) and affiliate programmes are accessible for the founders' own accounts from Lithuania (verify week 1).
3. Lithuanian counsel confirms non-personalised spot signals are outside MiCA "advice"; the paid closed group is confirmed in writing before G3.
4. A payment rail exists whose acceptable-use policy permits a paid trading-signal community (Stripe and Paddle restrict or reject some trading/crypto-advice products — verify week 1; Whop is the fallback at 2.7% + $0.30).
5. Multi-year spot history is obtainable: Kraken's OHLC endpoint returns only recent candles, so use Kraken's downloadable history, OKX history endpoints and/or public historical datasets for research, while trading on OKX/Kraken live.
6. Both founders continue their studies; 10–20 h/week is real. Zero revenue for ≥ 9 months is acceptable to both.

## 9. Kill / pivot criteria

- No strategy passes G0 by week 12 → stop signal work; decide between software/tooling pivot or stopping.
- Public forward fails the G2 track-record sub-gate twice → do not monetise signals; pivot.
- Legal opinion negative on the paid group → free channel + affiliates + copy trading only.
- Either founder drops below ~8 h/week for a month outside exam sessions → re-scope to one stream.
- Hours checkpoint at week 4 shows < 70% of planned hours → re-scope the 90-day plan before continuing.

## 10. Operating rhythm

Weekly 1-hour sync (Monday): review STATUS.md, log decisions, assign the week's tasks, compare hours spent with plan. Every material decision gets a D-number. Experiment IDs, config versions and dataset versions are recorded in the strategy repo. Incident rule: if the engine is down, an automated "engine offline since HH:MM UTC" post goes out and the on-call founder (rotating weekly, exam weeks pre-assigned) acknowledges within 12 hours.
