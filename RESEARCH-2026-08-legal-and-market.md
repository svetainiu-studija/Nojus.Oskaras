# RESEARCH — Legal position and market economics (as of 26 Aug 2026)

Two independent research passes run by Claude on 2026-08-26. Confidence levels are the researchers' own. Verify anything time-sensitive again before acting on it; check exchange registration in the ESMA register before signing anything. **None of this is legal advice — a Lithuanian lawyer must confirm the legal points before money changes hands.**

## Part A — Regulation

### A1. MiCA and non-personalised signals (confidence: medium)

- "Providing advice on crypto-assets" is a licensable crypto-asset service. MiCA Art. 3(1)(24): *"offering, giving or agreeing to give personalised recommendations to a client, either at the client's request or on the initiative of the crypto-asset service provider providing the advice, in respect of one or more transactions relating to crypto-assets, or the use of crypto-asset services."* Portfolio management (Art. 3(1)(25)) requires a discretionary mandate — signal-only is outside it.
- ESMA Q&A 2882 (18 June 2026) test for advice: a recommendation about transactions or use of crypto services, presented as suitable or based on the person's circumstances, **issued otherwise than exclusively to the public**, to a person as investor. A mere reference to a CASP that is equally accessible to all is not advice.
- ESMA Q&A 2463 (Apr 2025): MiCA advice is read consistently with MiFID II advice. ESMA's MiFID advice briefing (2023) warns that sending the same recommendation to multiple clients does not automatically make it non-personal, and social-media/app recommendations can be personal.
- **Open question:** whether a paid, closed group counts as "the public". Any DM Q&A, tiering, or "this fits you" language pushes toward advice. Lawyer needed before G3.

### A2. Derivatives, MiFID II and MAR (confidence: high on classification, medium on MAR scope)

- ESMA Guidelines on crypto-assets as financial instruments (19 Mar 2025): derivatives on crypto-assets are MiFID II financial instruments; perpetual futures should be treated as derivative contracts.
- Consequences: personalised advice on perps/CFDs = MiFID investment advice (licence from the Bank of Lithuania). Non-personalised recommendations = MAR "investment recommendations" (Art. 3(1)(35)); Art. 3(1)(34)(ii) captures non-professionals who repeatedly propose investment decisions and present themselves as having expertise ("experts").
- Delegated Regulation (EU) 2016/958 duties: identity and job title of every natural person producing the recommendation (Art. 2); facts vs opinions, sources, date and time (Art. 3); conflicts and interests (Art. 5). Experts additionally: valuation methodology, meaning of buy/sell/hold, time horizon and risk warning, update frequency, list of all recommendations in the preceding 12 months (Art. 4), proportions of buy/hold/sell and positions > 0.5% (Art. 6).
- ESMA statement (6 Feb 2024): "anyone" posting recommendations on social media is covered. ESMA finfluencer factsheet (Jan 2026, Lithuanian version exists): without a licence, do not give personal recommendations; disclaimers give no protection; CFDs/futures/crypto need clear risk warnings.
- **Open question:** MAR Art. 2(1)(d) scope for offshore perps (price "depends on or has an effect on" EU-venue instruments) is untested. Safe course: do not publish perps recommendations while pseudonymous (D-003).

### A3. Lithuania (confidence: medium-high)

- Law on Markets in Crypto-Assets (No. XIV-2879). Bank of Lithuania licenses CASPs; FNTT supervised the transition. National transitional period ended **31 Dec 2025**; from 1 Jan 2026 unlicensed crypto-asset *services* are illegal (Criminal Code Art. 202). EU-wide cut-off 1 July 2026.
- No Bank of Lithuania statement specifically on signal groups was found; warnings target fraudulent platforms. Lithuanian press frames signal-selling as largely fraudulent → reputational and consumer-complaint risk.
- An MB selling signals must observe: Law on Advertising and Law on Prohibition of Unfair Commercial Practices (VVTAT; influencer/affiliate posts labelled "Reklama"); distance-contract rules (Directive 2011/83: 14-day withdrawal unless the Art. 16(m) digital-content waiver is obtained; "order with obligation to pay" button); GDPR; MAR disclosures if derivatives are ever covered.

### A4. Affiliate marketing (confidence: medium-high)

- MiCA does not license affiliates. Promoting an **authorised** CASP with a plain referral link is lawful advertising. Promoting a **non-authorised** exchange to EU residents is the problem: ESMA reverse-solicitation guidelines (Dec 2024, applicable from ~Apr 2025) treat social media, influencers and sponsorships as solicitation, cover persons acting expressly or implicitly on the firm's behalf, and treat remuneration as a strong indication.
- Status (ESMA-register trackers, 21–26 Aug 2026). **Authorised:** Bybit EU (AT, May 2025), OKX Europe (MT), Kraken (IE), Coinbase (LU/IE — trackers disagree), Crypto.com (MT), Bitpanda (AT), Bitvavo (NL), KuCoin (AT, Nov 2025). **Not authorised:** Binance (withdrew Greek application 24 Jun 2026; halted new EU services 1 Jul 2026), MEXC (restricting EEA), Bitget (Austrian application filed 17 Jun 2026, pending).

### A5. Entity and tax (confidence: high)

- Two founders: **MB** (1–10 natural-person members, limited liability, no minimum capital) or UAB. *Individuali veikla* is single-person with unlimited liability.
- Corporate income tax from 1 Jan 2026: 17% standard; **7%** for small companies (< 10 employees, income < €300k), with a 0% start-up rate for the first two years subject to conditions (confirm with VMI).
- VAT registration threshold **€45,000** per calendar year (rule since 1 May 2025); standard rate 21%; EU consumer subscriptions fall under OSS rules (or use a merchant of record such as Paddle).
- Individual-activity reference (if ever used): GPM 5–15%, VSD 12.52%, PSD 6.98%, optional 30% deemed expenses.

### Questions a lawyer must answer before launch

Paid closed group vs "the public" (A1); MAR scope for offshore perps and confirmation that a copy-trading lead account carries no producer obligations (A2); any BoL/FNTT notification for information-only businesses (A3); consumer-law wording (A3); MB member payout structuring and 0% CIT conditions (A5).

## Part B — Market economics

Legend: [V] verified on a primary/official page; [S] secondary source; [E] estimate.

### B1. Paid signal / trading communities

- Price points [V/S]: Telegram crypto-signal channels $70–290/month; Whop crypto communities $47–225/month; Skool trading/finance niche median $69/month (2,629 groups, May 2026); Whop's most common band $25–50.
- Outcome distribution [S]: Whop (191,654 products, Feb 2026): 87.8% earn $0, median earner $74/month, 2% above $1k/month; trading products median $333/month (mean $4,647, heavily skewed). Gumroad: 44% at $0, median $72/month, 5% above $1k/month.
- Free → paid conversion: no trading-specific benchmark. Substack median ~3%; only ~1 in 5 clear 5%; cold social traffic ~1% [S].
- Churn: no verified trading benchmark; general subscriptions 3.2–5.0%/month (Recurly, Jul 2026) [V]; expect signal groups to churn faster in drawdowns [E].
- Trust builders [S]: independent trackers are thin (SmartOptions tracks some Telegram channels — e.g. a channel claiming 93% win rate tracked at 86%; Cornix Marketplace publishes channel stats but a 2026 review flags it as high-risk). Credible providers post public P&L sheets. The most verifiable option is an exchange copy-trading lead account (Bybit Master Trader 10–15% profit share [V]; Binance lead trader 10% + fee commission [V] but closed to new EU users; **OKX Europe lead trading: spot, futures and bots, profit share up to 30%, weekly settlement, available to EEA users** [V, OKX EU help page, "may not apply to all customers"]).
- Payment rails [V]: Whop 2.7% + $0.30 (+1.5% intl, +1% FX; payouts extra). Telegram Stars: creators cash out at ~$0.013/Star vs ~$0.02 paid → ~35% haircut, 21-day hold [S]. Discord Server Subscriptions 90/10 but **US-only**. Patreon 10% + 3.4% + €0.35 + 2.5% FX. Stripe (LT) 1.5% + €0.25 EEA cards, 3.15% intl, +2% FX, +0.7% Billing. Paddle 5% + $0.50 (merchant of record, handles EU VAT). InviteMember bot $19–39/month. Tribute flat 10%.

### B2. Exchange referral / affiliate programmes (EU, 2026)

- OKX Europe affiliate [V]: default 30% of invitees' fees, up to 50% by level, settled hourly in USDC; zero-fee trades excluded.
- Bybit EU [V]: fee-commission referral **discontinued 19 Mar 2026**; now €25 in BTC per qualified referee (≥ 100 USDC deposit within 7 days), max 20 per 30 days. Affiliate "up to 50%" unverified.
- Kraken [V]: affiliate up to 50% revenue share, negotiated per partner, monthly USDC; consumer referral $5–50 random BTC, capped.
- Bitvavo [V]: 15% of referred users' fees. Bitpanda [V]: up to 20% "for a limited time", via Impact; no PPC.
- Non-EU only: Binance affiliate (5,000+ followers, up to 50%); MEXC cut 60% → 40% (Jan 2025).
- Revenue per active referred trader [E from verified fee schedules]: spot retail at €10k/month volume → ~€3/month at 30%; active perps trader at €100k/month → ~€15/month; only €500k+/month derivatives traders yield ~€75+/month. **Realistic €2–20/month per active referral**, decaying as users go inactive. Exchange "average affiliate earnings" figures are marketing, not data.

### B3. Reselling models with €1–5k from Lithuania

- Amazon.de FBA arbitrage [V/S]: Pro plan €39/month; referral fees 8–15%; survey (n≈2,000): 57% of sellers > 10% margin, 28% > 20%, 13% unprofitable; arbitrage guides cite 15–30% net margins; #1 pitfall brand gating / dead stock; capital cycles 30–90 days [E]. Sourcing is labour. Not passive.
- eBay.de [V]: flat commercial fees 7–14% from 1 Jul 2026. Vinted: 0% seller fees; Vinted Pro not offered in Lithuania [S]. Low ticket, high labour.
- Dropshipping [S]: survivors net 15–25%; typical capital $5–10k plus $200–1,000+ test ad spend. Poor fit for €1–5k. Not passive.
- Print-on-demand [V]: 20–40% "good" margin; near-zero capital; revenue scales only with an audience.
- Reseller hosting [S]: $30–50/month plan resold at $20–25/client; 15 clients ≈ $150–350/month profit. Closest to passive but requires sales and support.

### B4. Income timelines

No credible dataset measures "months to €500 / €2,000". Proxies: Stan (80k creators, 2025): average monthly sales $89 with < 1k followers, $273 at 1–10k, $666 at 10–100k [S]. Whop median $74/month. At ~3% conversion and €49/month, €2,000/month needs ~41 subscribers ≈ ~1,400 engaged free members [E]. Sober view: €500/month in 6–12 months is plausible only with consistent public content; €2,000/month typically 12–24+ months [E, low confidence].

### B5. Lean cost stack (monthly)

VPS (Hetzner CX-class) ~€4.50 [S]; exchange public APIs free; CoinGecko Demo free → Basic $35 [V]; CoinMarketCap free → $29 [V]; TradingView Essential $12.95 / Plus $29.95 / Premium $59.95 [V]; Carrd Pro $19/year [V]; domain ~€12/year [E]; membership bot $19–39 or Whop 2.7% + $0.30. **Fixed ~€20–60/month lean; ~€100–200/month with paid data and premium charting; plus 3–10% of revenue in payment fees.**

## Sources

### Regulation
- https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mica/article-3-definitions
- https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R1114
- https://www.esma.europa.eu/publications-data/questions-answers/2882
- https://www.esma.europa.eu/publications-data/questions-answers/2463
- https://www.esma.europa.eu/sites/default/files/2023-07/ESMA35-43-3861_Supervisory_briefing_on_understanding_the_definition_of_advice_under_MiFID_II.pdf
- https://www.esma.europa.eu/sites/default/files/2025-03/ESMA75453128700-1323_Guidelines_on_the_conditions_and_criteria_for_the_qualification_of_CAs_as_FIs.pdf
- https://www.legislation.gov.uk/eur/2014/596/article/2/adopted/data.html (MAR Arts. 2, 3, 20)
- https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0958
- https://www.esma.europa.eu/press-news/esma-news/requirements-when-posting-investments-recommendations-social-media
- https://www.esma.europa.eu/sites/default/files/2024-02/ESMA74-1103241886-912_Warnings_on_Social_Media_and_Investment_Recommendations.pdf
- https://www.esma.europa.eu/sites/default/files/2026-01/LT_Lithuania_lt_-_Finfluencers_factsheet.pdf
- https://www.esma.europa.eu/sites/default/files/2025-10/Updated_Joint_ESAs_revised_warning_on_crypto-assets_LT.pdf
- https://www.esma.europa.eu/sites/default/files/2026-04/ESMA75-113276571-1679_Statement_on_the_end_of_transitional_periods_under_MiCA.pdf
- https://www.esma.europa.eu/sites/default/files/2024-12/ESMA35-1872330276-1899_-_Final_report_on_GLs_on_reverse_solicitation_under_MiCA.pdf
- https://www.lb.lt/en/markets-in-crypto-assets
- https://www.lb.lt/lt/naujienos/lietuvos-bankas-primena-reikalavimus-del-kriptoturto-paslaugu-teikimo
- https://www.lb.lt/lt/naujienos/lietuvos-bankas-kriptoturto-paslaugu-teikejai-turi-atsakingai-apsispresti-del-veiklos-ir-informuoti-klientus
- https://fntt.lrv.lt/lt/naujienos/baigiasi-pereinamasis-laikotarpis-vasp-nuo-2026-m-sausio-1-d-privaloma-kriptoturto-paslaugu-teikejo-licencija-uww/
- https://glimstedt.lt/naujienos/kripto-mica-aml-reguliavimas-2026-2027/
- https://ve.lt/verslas/nauja-aukso-gysla-ar-lengvatikiu-pinigu-isviliojimas-kas-yra-kriptosignalai-ir-kodel-jie
- https://vvtat.lrv.lt/lt/naujienos-ir-pranesimai-ziniasklaidai-377/vvtat-primena-kaip-influenceriai-turi-zymeti-reklama-socialiniuose-tinkluose-1692/
- https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32011L0083
- https://casptracker.eu/ · https://www.outrun.at/micar-dashboard
- https://www.coindesk.com/policy/2026/06/24/binance-withdraws-greek-mica-bid-but-vows-to-remain-in-europe
- https://www.amlintelligence.com/2026/07/binance-mexc-and-htx-accessible-eu-users-mica-licences/
- https://taxsummaries.pwc.com/lithuania/corporate/taxes-on-corporate-income · https://taxsummaries.pwc.com/lithuania/corporate/other-taxes
- https://www.vmi.lt/evmi/kaip-skaiciuojama-45-000-euru-riba-del-prievoles-tapti-pvm-moketoju-
- https://lamigra.lt/mb-ar-individuali-veikla/
- https://www.jdsupra.com/legalnews/what-s-up-2026-esma-says-finfluencers-2748094/

### Market
- https://docs.whop.com/fees · https://whoptrends.com/blog/whop-creator-earnings-data-2026 · https://whop.com/blog/crypto-trading-whops/
- https://nftevening.com/best-crypto-signals/ · https://smartoptions.io/crypto-signals-discord/
- https://help.cornix.io/en/articles/5814936-marketplace · https://coinspot.io/en/telegram-trading-bots/cornix/
- https://codingoblin.com/blog/most-profitable-skool-community-niches
- https://www.yana-g-y.com/p/substack-free-to-paid-conversion-rate · https://recurly.com/research/churn-rate-benchmarks/
- https://creator-support.discord.com/hc/en-us/articles/10424143128343-Creator-Revenue-FAQ
- https://support.patreon.com/hc/en-us/articles/36426991446797-A-standard-platform-fee-for-new-creators-effective-after-August-4-2025
- https://telegram.org/blog/superchannels-star-reactions-subscriptions · https://core.telegram.org/api/subscriptions
- https://blog.invitemember.com/telegram-stars-to-ton-how-to-withdraw-and-convert-2025/ · https://invitemember.com/pricing · https://tribute.top/blog/telegram-stars-creators-guide
- https://stripe.com/en-lt/pricing · https://www.paddle.com/pricing
- https://www.bybit.com/en/help-center/article/Copy-Trading-Profit-Sharing-Explained
- https://www.binance.com/en/support/faq/binance-futures-copy-trading-lead-trader-growth-plan-3160c961b2734d1cbb5342d1e86c6cdb
- https://www.okx.com/en-eu/help/lead-traders-faq · https://www.okx.com/en-eu/help/copy-trading-frequently-asked-questions
- https://www.okx.com/en-eu/help/whats-okx-affiliate-program-in-eea · https://www.okx.com/en-eu/help/okx-affiliate-and-referral-program-faq
- https://www.bybit.eu/en-EU/help-center/article/Bybit-Referral-Program-General-FAQ · https://www.bybit.eu/en-EU/help-center/article/Trading-Fee-Structure
- https://www.kraken.com/affiliate · https://www.kraken.com/referrals-dyn-lat-50
- https://bitvavo.com/en/affiliates · https://www.bitpanda.com/en/affiliate-programme
- https://www.bitget.com/support/articles/12560603824255 · https://www.mexc.com/support/articles/17827791521024
- https://www.coindesk.com/policy/2026/06/26/binance-tells-eu-users-it-will-no-longer-provide-services-after-failing-to-secure-mica-license
- https://sell.amazon.de/en/preisgestaltung · https://www.aboutamazon.eu/news/empowering-small-business/update-to-european-referral-and-fulfilment-by-amazon-fees-for-2026
- https://www.junglescout.com/resources/articles/how-much-do-amazon-sellers-make/ · https://goaura.com/blog/retail-arbitrage-on-amazon
- https://ohn.haendlerbund.de/themen/marktplaetze/ebay-aendert-gebuehren-teurer-guenstiger · https://margeoapp.com/en/blog/vinted-pro-account-guide/
- https://trueprofit.io/blog/dropshipping-success-rate · https://www.printful.com/blog/what-is-a-good-profit-margin-for-print-on-demand
- https://www.inmotionhosting.com/blog/is-reseller-hosting-profitable/
- https://invoicetrack.lt/en/individual-activity-tax-calculator/
- https://stan.store/blog/state-of-the-creator-economy/ · https://insightraider.com/en/state-of-gumroad-2026 · https://communipass.com/blog/creator-monetization-timeline-2026/
- https://www.coingecko.com/en/api/pricing · https://coinmarketcap.com/api/pricing/ · https://www.tradingview.com/pricing/
- https://www.bitdoze.com/hetzner-cloud-cost-optimized-plans/ · https://carrd.com/pro
