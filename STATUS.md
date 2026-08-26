# STATUS — Verslas (Oskaras / Nojus)

Updated: 2026-08-26 · Phase: **0 — Set up** · Revenue: €0 (by design) · Next checkpoint: Week 2 (9 Sep 2026)

## Done

- Founders' constraints captured: €1–5k risk capital, 10–20 h/week each, 3+ years discretionary trading, no code, no strategy, no audience; want anonymity; ambition €5k+/month.
- Regulatory research (MiCA, MAR, Bank of Lithuania, affiliate rules, entity/tax) and market research (pricing, conversion, churn, affiliate economics, reselling, costs) completed with sources → RESEARCH-2026-08-legal-and-market.md.
- Recommendation delivered: pseudonymous trading-intelligence brand; spot-only public signals; perps never published, only via a validated lead account; affiliates to MiCA-authorised exchanges only; paid tier only after gates. Reselling rejected.
- CHARTER v0.2, DECISIONS (D-001…D-014 proposed), PLAN-90-DAYS v0.2 created.
- Independent review of v0.1 performed (verdict: "needs rework"); all ten major findings addressed in v0.2 (timeline re-based, G1 turned into an engineering gate, lead account brought inside validation, founder agreement, entity-before-income, payment-rail AUP check, GDPR/privacy, log anchoring and incident handling, baselines in G0, copy-trading economics stated).

## Open decisions (need founders)

- D-003: pseudonymous + spot-only public signals + perps only via a validated lead account — confirm, or choose the named-person alternative.
- D-005: planning target €500/month by month 12–18 with €5k as a 36-month-plus destination — confirm.
- D-011: founder agreement terms (equity split, vesting, IP, leaver terms).
- D-012: lead-account execution policy (manual mirroring; automation only as an explicitly approved execution project).
- D-001, D-002, D-004, D-006…D-010, D-013, D-014 — confirm or comment.
- Risk limits (task 0.2): max portfolio drawdown, per-trade risk, max concurrent positions, heat cap.
- Budget scenario: €1k minimum vs up to €5k (task 0.11).

## Next actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Confirm/override D-001…D-014; agree risk limits; choose budget scenario | Both | 2 Sep |
| 2 | Founder agreement drafted and signed (template; lawyer review if budget allows) | Both | 9 Sep |
| 3 | Book lawyer consult; send the 6 questions from DECISIONS.md | Nojus | 2 Sep |
| 4 | Check OKX Europe lead-trader (spot) eligibility and affiliate access; Kraken and Bitvavo affiliate access and promotion rules | Nojus | 2 Sep |
| 5 | Verify Stripe / Paddle / Whop acceptable-use policies for a paid signal community | Nojus | 5 Sep |
| 6 | Brand name shortlist (5) with handle/domain availability; reserve handles | Nojus | 5 Sep |
| 7 | Fill the hypothesis template for 2–3 strategies from your discretionary trading | Both | 5 Sep |
| 8 | Create the private strategy repo; data sources chosen; ≥ 4 years of spot history for ~30 pairs downloaded with dataset versioning; cost model; holdout dates locked (next Claude session: bring the hypotheses and we build this together) | Oskaras | 9 Sep |
| 9 | Credential vault + 2FA on every account | Both | 5 Sep |

## Blockers

None yet. Legal opinion is a soft blocker for G3 only (months away). Payment-rail AUP approval is a risk for stream 3 (check in Phase 0).

## Risks being tracked

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| No strategy passes G0 (discretionary edge does not codify, or the edge is market beta) | High | Fatal for streams 1–3 | Protocol with baselines + 12-week hard stop; software pivot pre-defined |
| Build takes 1.5–2× longer than planned (no existing code, part-time) | High | Timeline slips | Scope cut to the day-90 deliverable; week-4 hours checkpoint; existing libraries |
| Anonymity limits trust, conversion and distribution (no crypto ads to a faceless brand) | Medium–high | Slower audience growth | Exchange-verified lead-account stats; anchored public log; distribution plan without paid ads |
| Paid closed group deemed "advice" under MiCA | Medium | Paid tier blocked | Lawyer opinion before G3; fallback = free channel + affiliates + copy trading |
| Payment rails reject trading-signal products | Medium | Paid tier delayed | AUP verification in Phase 0; Whop fallback |
| Copy-trading revenue is zero during drawdowns; follower capital small at first | Certain at times | Income volatility | Multiple streams; economics stated honestly in CHARTER §3 |
| Founder dispute / one founder leaves / key-person risk on the engine | Medium | Project ends | Founder agreement (D-011); runbook; credential vault |
| Founders' hours fall during exam sessions | Certain | Slippage | Automated phases scheduled over exams; on-call rota; re-scope trigger |
| Platform dependency (Telegram, exchange programme terms — Bybit EU cut fee-share in Mar 2026) | Medium | Revenue loss | Own the member list (email, with GDPR basis); spread across exchanges |
| Reputational damage from one bad public period | Medium | Slow recovery | Never promise; publish drawdowns as loudly as wins; sizing public |
| Payouts received before the entity exists | Medium | Tax/AML mess | Entity + accountant before first payout (D-006) |

## Log

- 2026-08-26 — Kick-off session. Research, recommendation, workspace v0.1 created; independent review returned "needs rework"; v0.2 issued addressing all major findings. Awaiting founders' confirmations.
