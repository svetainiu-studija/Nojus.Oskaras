# Research addendum — 2026-08-27

Verification pass requested by the 2026-08-27 review (`REVIEW-2026-08-27-FEEDBACK.md`, points 1, 2, 7). Research, not legal advice.

**Method note:** this environment's network policy blocks direct fetches of esma.europa.eu and vmi.lt, so findings below were assembled from search-result extracts of the official pages (URLs listed). Marks: **[V]** wording corroborated by extracts of the official page/document itself; **[S]** secondary source only. Anything load-bearing should be re-confirmed by the lawyer/accountant from the primary page — the URLs are exact.

## 1. ESMA on the MiCA "advice" perimeter (review points 1–2)

**The discrepancy between our two research passes is resolved — both were partly right:**

- **[V]** ESMA Q&A 2882 (published June/July 2026): *"The perimeter of advice on crypto-assets under MiCA should be regarded as broader than the perimeter of advice under MiFID II"* — because MiCA's definition covers personalised recommendations on **(i) transactions in crypto-assets AND (ii) the use of crypto-asset services**. So the ChatGPT pass was right that the perimeter is broader; our first pass was right that the *personalisation* analysis still leans on MiFID II guidance — Q&A 2882 itself points to ESMA's MiFID II advice supervisory briefing (ESMA35-43-3861) as the reference for when a recommendation is personal.
  https://www.esma.europa.eu/publications-data/questions-answers/2882
- **[V]** The same Q&A: *"providing solely a reference to a CASP (without further indications) equally accessible to all potential investors should not constitute a recommendation"* — but **introductory services that recommend a specific CASP or service to a person can be advice under MiCA even without recommending any transaction**. This is the exact affiliate boundary (lawyer question 7, tripwire T9): a generic, equally-accessible link = advertising; steering an individual to an exchange = potentially advice.
- **[V]** Briefing ESMA35-43-3861 (2023): ESMA dropped the old comfort that a recommendation "issued exclusively through distribution channels or to the public" cannot be personal, and states that recommendations via apps and social media (including influencers) *"could, in certain instances, be regarded as a personal recommendation and not as issued exclusively to the public."*
  https://www.esma.europa.eu/sites/default/files/2023-07/ESMA35-43-3861_Supervisory_briefing_on_understanding_the_definition_of_advice_under_MiFID_II.pdf

**Consequences for us:** (a) the free public channel's safety rests on *zero personalisation in substance*, not on being "public" — which our product architecture already enforces (TRIPWIRES engineering rules); (b) the paid closed group question is genuinely open, exactly as the review says — lawyer question 1 stands, G3 stays gated on a written opinion; (c) affiliate copy must stay generic and equally accessible — never a reply to an individual.

## 2. Lithuania 2026 tax rules verified (review point 7)

- **[V]** CIT rates from 2026: standard **17%**, reduced small-unit rate **7%**, and **0% for newly registered units in the first AND second tax periods** (extended from one period by the 2025 amendments; the employee-count limit was removed).
  https://www.vmi.lt/evmi/5724 · https://www.vmi.lt/evmi/5676 · https://www.vmi.lt/evmi/0proc-tarifas
- **[V]** 0% conditions: income in **each** of the first two periods ≤ **€300,000**; **all participants are natural persons**; the PMĮ 5 str. 3 d. conditions must not be met; and — **the catch our docs didn't have** — during a **three-year consecutive period** covering the first two tax periods the unit's activity must not be suspended, the unit not liquidated or reorganised, and **its shares/member rights not transferred to new members**. A member-rights transfer in the first three years voids the relief.
- **[V/S]** PMĮ 5 str. 3 d. (anti-splitting): the reliefs do not apply where the same participant (or the same participants together) holding **> 50%** of the unit on the last day of the tax period also hold(s) > 50% in other units — founders' majority stakes in other companies can disqualify the MB. Exact statutory wording to be confirmed by the accountant.
  https://www.vmi.lt/evmi/documents/20142/737112/RM-17740.pdf
- **[V]** MB member social contributions — **material change**: the VSD base for amounts an MB member withdraws for personal needs is **50% of the withdrawal until 2026-06-30 and 90% from 2026-07-01** (aligned with individual activity). Withdrawal economics after July 2026 are therefore meaningfully worse than older guides suggest — the payout model must be built on the 90% base.
  https://sodra.lt/imokos/esu-mazosios-bendrijos-narys
- **[V]** 2026 reference figures: MMA **€1,153** (https://socmin.lrv.lt/lt/naujienos/patvirtinta-mma-nuo-2026-m-1153-eurai-mNK/); PSD 6.98% × MMA = **€80.48/month** (consistent with the earlier research); VDU **€2,312.15**; annual Sodra ceiling for the self-employed 43 VDU (~€99.4k) **[S]**.

**Consequences for us:**
1. **Founder agreement / vesting design (D-011, lawyer Q6):** any mechanism that transfers MB member rights during the first three years after registration can retroactively kill the 0% relief. Vesting must be structured contractually (economic rights, buy-out formulas) rather than as actual staged transfers of membership — one more reason the agreement needs the lawyer's eye.
2. **Payout model:** from July 2026 the effective tax+Sodra burden on MB member withdrawals is higher than most 2025-era guides state; the accountant must model member payouts on the 90% VSD base before we promise ourselves any "net" number.
3. **Entity timing (D-006) unchanged** — but when the MB is registered, both founders' other shareholdings (if any ever exist) matter for keeping the 0%/7% rates.

## Still open

- Exact statutory text of PMĮ 5 str. 3 d. (accountant to confirm scope of the >50% rule).
- VMI virtual-currency accounting guidance (RM-21969) — from the first research pass, not re-verified today.
- The cousin's written answers to the 7 questions (task 3) — this addendum narrows, but does not replace, them.
