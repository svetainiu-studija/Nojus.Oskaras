# Verification: payment rails and OKX EU programmes — 2026-08-27

Pre-verification for tasks 4 and 5 (STATUS), run against official policy pages. **Method:** stripe.com, paddle.com, whop.com and okx.com are all blocked by this environment's egress proxy, so every quote comes from search-result extracts of the *official* pages (cross-checked across multiple independent searches). Before anything contractual, re-verify the exact wording on the live pages — URLs are given. This narrows Nojus's work; it does not replace the in-writing confirmations D-007 requires.

## Verdicts at a glance

| Subject | Verdict | One line |
|---|---|---|
| **Paddle** | 🔴 effectively prohibited | Merchant of record with mandatory review; at least three AUP categories catch us. Drop it. |
| **Stripe** | 🟠 conditional | Restricted category — needs Stripe's prior written approval; realistic risk of decline or later account closure. Backup only. |
| **Whop** | 🟢 conditional (front-runner) | Purpose-built for trading communities; no policy language against non-personalised signals; conditions on marketing claims and onboarding. |
| **OKX Europe** | 🟢 conditional | Both programmes accessible from Lithuania — but the **spot profit share is 8–13%, not 30%** (charter corrected), and affiliate promo rules are strict. |

## 1. Paddle — treat as not viable

Three separate AUP categories apply (paddle.com/help "What am I not allowed to sell on Paddle"): (a) exchanges/dealers/trading platforms in financial instruments, currencies or cryptocurrencies; (b) anything "considered a regulated financial product or service **in any jurisdiction**" — a catch-all their compliance applies conservatively; (c) "human services that are not related to a software offering… including **access to a community of experts**" — a paid Telegram/Discord community fits. Paddle reviews every seller before onboarding (it resells your product as merchant of record), and its June 2025 FTC settlement ($5M) tightened screening further. Do not build on Paddle without written pre-clearance, which is unlikely.

## 2. Stripe — restricted, approval required, fragile

- Not named per-se, but sits inside restricted categories: "Investment and brokerage services" and the crypto-related list ("Virtual and cryptocurrencies…", "Cryptocurrency exchanges and wallets"). Restricted = usable **only with Stripe's explicit prior written approval** (Stripe Services Agreement), with extra due diligence ("proof of relevant licenses or more details about your business model"); Stripe states it "might not be able to grant approval".
- Flatly **prohibited** regardless of approval: "get rich quick" marketing — "investment opportunities or other services that promise high rewards to mislead consumers… fast and easy money", fake/deceptive testimonials. Our no-promises reporting standard (D-008) is also what keeps us out of this bucket.
- Stripe Billing is available to Lithuanian entities (Lithuania is a supported country; EU Billing GA) — so it's *technically* usable, if approved.
- Realistic posture: **backup rail only**; if pursued, disclose the exact model at onboarding and get the approval in writing.

## 3. Whop — the practical front-runner

- Whop actively courts trading communities (official guides "How to start a trading community on Whop", trading category pages, many live signal listings). The binding constraint is the Prohibited Products policy: "**Unregistered Financial Services** — investment products, asset management, or financial instruments offered without proper… registration and licensing" — a non-personalised, identical-to-all signal feed with no execution/custody/personal advice sits outside that as applied in practice, but sellers bear full legal-compliance responsibility, and some categories need Whop's prior approval → onboarding is the confirmation step.
- Compliance duties we'd sign up to (whop.com/guidelines, /ftc): earnings claims must be substantiated and account for expenses; testimonials must reflect typical results; endorsements disclosed; no guaranteed-profit claims; access period disclosed. All already our policy (D-008, TRIPWIRES T17-adjacent).
- **Fees:** 2.7% + $0.30 domestic cards, +1.5% international, +1% FX → model ~4.2–5.2% + $0.30 for EU traffic. Multiple 2026 third-party analyses report an **additional 3% platform fee on Discord/Telegram-gated products** (possibly no longer on the published schedule) → realistic worst case **~5.7–8% + $0.30**. Must be confirmed in the seller dashboard before pricing. Marketplace 30% discovery commission was removed May 2025.
- **Payouts for Lithuania:** local-currency international bank transfer documented as an option (country list unverified), else SWIFT wire $23 flat or USDC 5% + $1. EEA sellers contract under "Terms of Service (Rest of World)"; third-party sources say Whop handles EU VAT as MoR — confirm in writing.

## 4. OKX Europe — accessible, with corrected numbers

- **Copy trading (spot):** Lithuania is *not* on the unsupported-country list (curiously, Malta is, despite OKX Europe being Malta-licensed). Lead-trader requirements: Level-2 KYC, account balance > 500 USDT, ≥ 7 completed trades in the last 30 days, application reviewed in 3–5 business days.
- **⚠ Correction to our charter:** the "up to 30%" profit share applies to **futures** copy trading. **Spot lead-trading profit share is 8–13%** (tiered by 90-day average AUM), settled weekly (Mon 00:00 UTC+8 cycle), deferred while copies are open. Charter §3 updated (v1.2).
- **Discoverability constraint:** appearing on the public lead-trader list requires **100,000 USDT lead assets** (raised from 10k in late 2024). Below that you can lead trades (500 USDT minimum) but get no list placement — our followers must come from our own channel, which matches the distribution plan anyway.
- Spot lead trades: margin-free or single-currency margin mode; ≤ 500 new buy orders/day.
- **Affiliate (EEA):** dedicated EEA programme; KYC + EEA-registered account required. Default **30% of invitees' trading fees**, settled hourly in USDC; tier upgrades monthly; "up to 50%" was only found documented for Latin America — assume 30% for planning. Entry paths: refer 10 valid users, or the influencer/content-creator application.
- **Promotion rules (binding on us):** no bidding on OKX brand keywords in search engines; no false/misleading statements, click fraud, cookie stuffing; no impersonating OKX; clear-and-conspicuous relationship disclosure (#ad — our "Reklama" labels satisfy this); and affiliate content **must not constitute investment advice, an investment recommendation, or a solicitation** — one more reason the affiliate copy stays generic (TRIPWIRES T9).

## Consequences for the plan

1. **D-007 shortlist is now effectively Whop first, Stripe backup, Paddle out.** The final rail choice (a new D-number) waits for Whop onboarding + written fee confirmation.
2. **Copy-trading economics roughly halve** vs the charter's old example: €50k follower capital earning 3%/month = €1,500 profit → **€120–195/month** to us at 8–13% (was stated as €450 at 30%). Stream 2 is even more clearly a multiplier, not a starting income. Charter corrected.
3. The 100k-USDT list threshold means the lead account's followers will come from our channel, not OKX discovery — consistent with the existing distribution plan.
4. Nojus's remaining verification work: Kraken + Bitvavo affiliate terms; confirm OKX programmes from your own accounts; Whop onboarding questions in writing (3% platform fee? EUR payouts to Lithuania? VAT handling?).

## Open questions (carried into tasks)

- Whop: 3% Discord/Telegram platform fee current? EUR local payout for Lithuania? MoR/VAT in writing? Prior-approval category for trading products?
- Stripe: exact current restricted-list wording (post-Feb-2025); what "relevant licences" they'd ask a non-licensable publisher for.
- OKX: EEA affiliate tiers above 30%? Promotion rules inside a *paid closed* channel? Combining lead-trader profit share + affiliate commission on the same referred users — permitted?
- All quotes to be re-verified against live pages from an unblocked network (this file's method note).
