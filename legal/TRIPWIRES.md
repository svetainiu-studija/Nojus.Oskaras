# Tripwires — facts that would change the legal conclusion

2026-08-27 · Research document, not legal advice. Requested in the 2026-08-27 review (`REVIEW-2026-08-27-FEEDBACK.md`, point 8).

The business's legal position rests on **facts about the product**, not on disclaimers or wording. This document lists the facts that, if they change, change the legal conclusion — and what each change would trigger. Product and content decisions must be checked against this list *before* they ship. The engine and channels should make the forbidden facts **technically impossible**, not merely against policy (review point 5).

## The three regimes, in one map

| Regime | Governs | Applies to us when |
|---|---|---|
| **MiCA** (Reg. (EU) 2023/1114) | Crypto-assets that are *not* financial instruments; crypto-asset *services* (advice, custody, execution, portfolio management…) require CASP authorisation | Our spot-signal content and any exchange-related promotion. We stay outside it only while nothing we do is a "crypto-asset service" — above all, while nothing is a *personalised recommendation* (Art. 3(1)(24)) |
| **MiFID II** | Financial instruments — which, per ESMA guidance, include crypto **derivatives** (perpetual futures, CFDs) | The moment any content recommends a derivative, that content falls under the financial-instruments regime, not MiCA |
| **MAR** (Reg. 596/2014) + Del. Reg. 2016/958 | *Investment recommendations* about MiFID II instruments — even by non-professionals who repeatedly recommend and claim expertise; requires producer identity, objective presentation, conflicts, 12-month recommendation history | Only if we publish derivative recommendations — which is why we never do while pseudonymous |

A signal about **spot BTC/ETH** lives in the MiCA world. A signal about a **BTC perpetual future** lives in the MiFID II/MAR world. Same chart, entirely different law.

## Tripwire table

| # | If this fact changes… | …the legal conclusion becomes | Severity |
|---|---|---|---|
| T1 | We collect any user's financial situation, goals, risk tolerance, or portfolio — and anything we send varies because of it | The content is a **personalised recommendation** → MiCA "advice on crypto-assets" → CASP authorisation required; unlicensed = criminal exposure in LT (CC Art. 202) | 🔴 fatal |
| T2 | We answer an individual "what should I buy / is X good for me?" in DM or private reply | Same as T1 — a single personalised recommendation is enough; "educational and general" is the only permitted Q&A register | 🔴 fatal |
| T3 | Different members receive different signals (tiers by profile, "VIP picks chosen for you") | Same as T1. Price tiers that differ only in *timing or extras around identical signals* are a separate, lawyer-gated question | 🔴 fatal |
| T4 | We publish individual position sizing / stop-loss "for your account size" | Same as T1 (suitability language). Published *rule-based* sizing formulas identical for everyone are the permitted form | 🔴 |
| T5 | Any published recommendation concerns a **derivative** (perp, CFD, option) | Content leaves MiCA, enters MiFID II/MAR: producer identity disclosure (Del. Reg. 2016/958 Art. 2) → incompatible with pseudonymity; full recommendation-history duties | 🔴 while pseudonymous |
| T6 | We execute, transmit, or relay orders for anyone else; or automate order placement on any account that is not our own | MiCA "execution/reception-transmission of orders" → CASP authorisation | 🔴 fatal |
| T7 | We hold anyone's funds, keys, or wallet access | MiCA custody service → CASP authorisation | 🔴 fatal |
| T8 | Copy-trading structure changes from "exchange executes under its licence, we are a listed lead trader" to anything with a **direct contract with followers, discretionary decisions for them, or fees collected from them directly** | Potential portfolio management / advice / order transmission → the D-017 specialist opinion is void; re-analysis required before continuing | 🔴 |
| T9 | Our promotion names a specific exchange as right *for an individual* ("for your situation, use X") rather than generic disclosed advertising | Advice on the *use of a crypto-asset service* (also MiCA Art. 3(1)(24)) — the affiliate boundary, lawyer question 7 | 🟠 |
| T10 | We link or promote a **non-MiCA-authorised** exchange to EU residents | Solicitation on behalf of an unauthorised firm (ESMA reverse-solicitation guidelines treat paid affiliates as acting for the firm) | 🟠 severe |
| T11 | The paid group adds any interactive feature that individualises content (per-member Q&A threads, portfolio reviews, "ask about your trades") | The "not personalised" defence of the paid tier collapses; G3 legal opinion void | 🔴 for stream 3 |
| T12 | Consent flow for the paid tier uses pre-ticked boxes, or content starts before the explicit withdrawal-right waiver is captured and logged | Consumer-law breach (Directive 2011/83 Art. 16(m); VVTAT practice) — fines, refund exposure | 🟠 |
| T13 | Marketing emails sent without a separate lawful basis from service emails | GDPR / e-communications breach (VDAI practice) | 🟠 |
| T14 | Rolling 12-month revenue approaches **€45,000** | VAT registration obligation; pricing must be re-planned VAT-inclusive | 🟡 planned |
| T15 | Any payout received by a founder personally before the MB exists | Individual-activity income (GPM/VSD/PSD), source-of-funds friction at banks — the exact mess D-006 exists to prevent | 🟠 |
| T16 | Company composition changes: a non-natural-person member, or founders' stakes in other companies triggering PMĮ 5 str. 3 d. conditions, or period income above the small-company threshold | Loss of the 0%/7% CIT relief (exact conditions: `RESEARCH-2026-08-27-ADDENDUM.md`) | 🟡 |
| T17 | We start describing ourselves as "advisors", "consultants", "wealth managers" — in any language, any channel, any contract | Self-declared regulated activity; converts every grey question into a presumption against us | 🔴 never |

## Engineering consequences (build these in, don't police them)

1. **The bot has no DM capability.** Signals post to channels only; the bot cannot reply to individuals. Q&A happens in public threads with a pinned "educational and general only" rule.
2. **One content stream.** The engine produces exactly one signal record per event; there is no code path that varies output per recipient. Membership status gates *access timing*, never *content*.
3. **No user profiling fields anywhere** — no onboarding questions about finances, goals, risk, or portfolio. Not collected = cannot personalise = T1 impossible.
4. **Sizing is a published formula** (% of equity per D-015), identical for all, stated as the strategy's rule — never computed for a specific person.
5. **Universe filter is spot-only** at the engine level: the instrument list physically contains no derivatives, so T5 cannot happen by accident.
6. **Affiliate copy is templated**: generic, "Reklama"-labelled, never generated in reply to an individual's question. The bot never answers "which exchange should I use?" — pinned answer points to a static comparison page listing all partners identically.
7. **Consent flow logs**: double active checkbox at checkout (start now + waiver acknowledgement), timestamped and stored.
8. **Payout addresses are company-controlled** (once the MB exists); the engine and dashboards never touch member funds or keys.

## Standing rule

Any change that touches a 🔴 row is **blocked** unless a written opinion from a qualified lawyer says otherwise *in advance* — the same standard as D-017. Any 🟠 row needs a founders' decision logged in DECISIONS.md before shipping. This file is reviewed at every weekly sync alongside STATUS.md.
