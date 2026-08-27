# STATUS — Verslas (Oskaras / Nojus)

Updated: 2026-08-26 · Phase: **0 — Set up** · Revenue: €0 (by design) · Next checkpoint: Week 2 (9 Sep 2026)

## Done

- Founders' constraints captured: €1–5k risk capital, 10–20 h/week each, 3+ years discretionary trading, no code, no strategy, no audience; want anonymity; ambition €5k+/month.
- Regulatory research (MiCA, MAR, Bank of Lithuania, affiliate rules, entity/tax) and market research (pricing, conversion, churn, affiliate economics, reselling, costs) completed with sources → RESEARCH-2026-08-legal-and-market.md.
- Recommendation delivered: pseudonymous trading-intelligence brand; spot-only public signals; perps never published, only via a validated lead account; affiliates to MiCA-authorised exchanges only; paid tier only after gates. Reselling rejected.
- CHARTER v0.2, DECISIONS (D-001…D-014 proposed), PLAN-90-DAYS v0.2 created.
- Independent review of v0.1 performed (verdict: "needs rework"); all ten major findings addressed in v0.2 (timeline re-based, G1 turned into an engineering gate, lead account brought inside validation, founder agreement, entity-before-income, payment-rail AUP check, GDPR/privacy, log anchoring and incident handling, baselines in G0, copy-trading economics stated).
- Workspace repo live: github.com/svetainiu-studija/Nojus.Oskaras — plan documents committed; both founders have access (Nojus added as collaborator, invite accepted).
- **Founders confirmed D-001…D-014** (2026-08-26). Risk limits agreed → D-015; budget ceiling €5k confirmed → D-016. CHARTER bumped to v1.0 (adopted).
- **D-017 accepted** (2026-08-27): AI analyses never satisfy a written-legal-opinion requirement; fintech-lawyer written opinion on copy-trading required before followers are enabled. Written into CHARTER G2 (v1.1). Founders also confirmed the 2026-08-27 review feedback was ChatGPT-written (provenance recorded; text kept as received).

## Open decisions (need founders)

- None blocking. D-015's position-count (6) and heat-cap (6%) numbers are Claude defaults — adjustable by a superseding decision until the holdout dates are locked (task 0.9).
- Lawyer consult skipped (D-018). Standing fact, kept visible without nagging: every legal input so far is AI-generated; the G2/G3 written-opinion gates are the points where that changes.
- Founder-agreement design constraint (from 2026-08-27 verification): transferring MB member rights within the first 3 years voids the 0% CIT relief — vesting must be contractual/economic, not staged transfers of membership. Include in lawyer Q6.
- Payout modelling constraint: from 2026-07-01 the VSD base on MB member withdrawals is 90% (was 50%) — accountant must model payouts on the new base.

## Next actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | ~~Confirm/override D-001…D-014; agree risk limits; choose budget scenario~~ **Done 2026-08-26** (D-015, D-016) | Both | ✔ |
| 2 | Founder agreement put in writing and signed. Founders affirm the mutual agreement holds and no one walks away — the written version exists to prevent misunderstanding, not to signal distrust: fix equity split, vesting, IP to the future MB, account/handle ownership, leaver terms (template; lawyer review if budget allows) | Both | 9 Sep |
| 3 | ~~Lawyer consult~~ **Skipped by founders' decision (D-018, 2026-08-27).** Questions stay on file in `legal/QUESTIONS-FOR-LAWYER.md`; G2 (D-017) and G3 legal gates unchanged | — | closed |
| 4 | ~~OKX pre-verified~~ (2026-08-27, `research/RAILS-AND-PROGRAMMES-2026-08.md`): Lithuania eligible for both programmes; **spot profit share 8–13% (not 30%)**; lead-list placement needs 100k USDT; affiliate default 30%, entry via 10 valid referrals or influencer route. **Remaining:** Kraken + Bitvavo affiliate terms; confirm OKX from own accounts | Nojus | 2 Sep |
| 5 | ~~Rails pre-verified~~ (2026-08-27, same doc): **Paddle out** (AUP prohibits); **Stripe backup only** (restricted, needs prior written approval); **Whop front-runner** (conditional). **Remaining:** Whop onboarding questions in writing — 3% Discord/Telegram platform fee? EUR payouts to Lithuania? VAT/MoR handling? | Nojus | 5 Sep |
| 6 | Brand name shortlist (5) with handle/domain availability; reserve handles | Nojus | 5 Sep |
| 7 | Fill the hypothesis template for 2–3 strategies from your discretionary trading | Both | 5 Sep |
| 8 | **Scaffolding built 2026-08-27** (`verslas-signals/`): OHLCV downloader (OKX public API, ~30 pairs, 1d/4h/1h since 2021), dataset versioning (DATASET-id manifests), gap-check, draft `costs.yaml`, project rules (CLAUDE.md); manifest/quality logic unit-tested. **Remaining (Oskaras, locally — exchange APIs unreachable from the cloud workspace):** run `make deps && make data && make check`, commit the first DATASET manifest; verify costs.yaml VERIFY values; lock holdout dates at the build session with the hypotheses | Oskaras | 9 Sep |
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
- 2026-08-26 — Workspace repo set up on GitHub; Nojus added as collaborator. Plan documents adopted into the repo. **Founders confirmed D-001…D-014; risk limits accepted (D-015); €5k budget ceiling confirmed (D-016). CHARTER v1.0 adopted.** Founders affirm mutual commitment; written founder agreement remains a week-2 deliverable (action 2). Documents merged to `main` via pull request.
- 2026-08-27 — Second AI legal analysis (ChatGPT) received from Oskaras and archived with provenance in `legal/`. Largely consistent with the first research pass; escalates copy-trading to highest-risk stream → D-017 proposed (AI ≠ legal opinion; written fintech-lawyer opinion required before followers enabled). One discrepancy flagged for the lawyer (MiCA advice scope vs MiFID II). Task 3 (cousin's written answers) remains open.
- 2026-08-27 — Review feedback (8 points) received and archived; all points dispositioned (`legal/REVIEW-2026-08-27-FEEDBACK.md`). TRIPWIRES.md created; lawyer question 7 (affiliate boundary) added. Verification pass completed (`legal/RESEARCH-2026-08-27-ADDENDUM.md`): ESMA Q&A 2882 discrepancy resolved (MiCA advice perimeter broader than MiFID II; generic equally-accessible CASP reference ≠ advice); 2026 tax rules verified — 0% CIT now first TWO periods but with a 3-year no-member-rights-transfer condition, and MB VSD withdrawal base rises 50%→90% from 1 Jul 2026. Awaiting: founders on D-017; cousin's written answers; feedback authorship confirmation.
- 2026-08-27 — **D-017 accepted** by founders; feedback confirmed ChatGPT-authored (provenance recorded, text unchanged); CHARTER v1.1 (G2 legal sub-gate). Rails/programmes verification run (`research/RAILS-AND-PROGRAMMES-2026-08.md`): Paddle out, Stripe backup-only, Whop front-runner; **OKX spot profit share corrected to 8–13%** → CHARTER v1.2 economics restated; 100k-USDT lead-list threshold noted. Founder-agreement template drafted (`legal/FOUNDER-AGREEMENT-TEMPLATE.md`) incorporating the 3-year no-transfer tax constraint; hypothesis starter files created (`research/hypotheses/`). Tasks 4–5 partially pre-done; remaining parts reassigned in the table above.
- 2026-08-27 — **Lawyer consult skipped on founders' instruction → D-018** (questions kept on file; G2/G3 gates unchanged). Build moved forward: `verslas-signals/` scaffolding created — data pipeline (downloader, dataset manifests, quality checks; 4 unit tests passing), draft cost model, strategy-work rules. First real data run is Oskaras's, locally.
