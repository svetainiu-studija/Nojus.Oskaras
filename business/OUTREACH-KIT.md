# Outreach kit — discovery sprint (copy-paste ready)

Rules baked into every text below: no pitching before listening (the
interview guide leads), no performance claims, no signals, no advice.
You are two students who ran a rigorous test of their own trading and
are researching whether a verification tool/service is worth building.
That story is TRUE and it is the hook. Log every attempt in
`DISCOVERY-2026-09.md` (one line, even for silence).

## 1. Reddit post — r/algotrading (also fits r/Daytrading with the intro softened)

**Title:** We spent a week trying to prove our trading edge existed. It
didn't. AMA about the process.

**Body:**
My friend and I (students, ~3 years of discretionary crypto trading)
built a full research pipeline to test whether our "edge" was real
before risking our savings on it: pre-registered rules committed to git
before results, realistic costs + 2× stress, random-entry baselines,
walk-forward folds, a sealed holdout, and an adversarial audit of our
own code that found (and fixed) 3 real bugs.

Result: our best strategy's entire profit came from ONE trade on SOL.
Removing it, 4.5 years of "momentum edge" turned negative. We wrote NO
EDGE / DO NOT TRADE on our own work and didn't deploy a cent.

Two questions for people here, because we're deciding what to build
next:
1. Have you ever paid for (or built) a backtest/signal that looked
   great and then lost money live? What did checking it properly look
   like for you?
2. If a tool/service existed that stress-tested a strategy the way we
   just did ours — costs, baselines, look-ahead, concentration — would
   you use it before going live? What would that be worth to you?

Happy to share the methodology in the comments — everything is public
in our repo.

## 2. Reddit/forum comment version (for replying inside existing threads about backtests/signals)

We just went through exactly this — built the whole verification stack
(pre-registered rules, costs, random baselines, sealed holdout) for our
own strategies and they all failed honestly. Losing the illusion cost a
week; trading it would have cost our savings. Curious: when you tested
yours, what convinced you it was real? Asking because we're researching
whether people would actually use an independent "prove it first"
check.

## 3. X / fintwit reply (short)

We built the full "prove it before you trade it" battery for our own
strategies — pre-registered rules, real costs, random baselines, sealed
holdout. All of them failed. Best week we ever spent. Would you run
your strategy through something like that before going live?

## 4. Telegram/Discord DM (EN) — after someone posts about a strategy/signal

Hey — saw your post about [X]. Genuine question, not selling anything:
my friend and I just finished stress-testing our own strategies
(costs, random baselines, look-ahead checks) and every one failed,
which probably saved us our deposit. Before you went live with yours,
what did you check? We're trying to figure out if an independent
verification service would be worth anything to traders like you —
would love 10 minutes of your honest experience.

## 5. Lithuanian versions

**FB/Telegram grupės įrašas:**
Sveiki. Su draugu (studentai, ~3 m. prekybos patirtis) prieš
rizikuodami savo santaupomis pasidarėme rimtą savo strategijų
patikrinimą: taisyklės užfiksuotos prieš matant rezultatus, realūs
mokesčiai, atsitiktinės atrankos palyginimas, užantspauduotas testinis
periodas. Rezultatas — visas mūsų „pranašumas" buvo VIENAS sėkmingas
SOL sandoris. Be jo — minusas. Nusprendėme neprekiaut.

Klausimas grupei: ar esat pirkę signalų / kursų / strategijų, kurios
istorijoje atrodė puikiai, o realybėje prarado pinigus? Kaip
patikrinot, ar jos tikros? Galvojame, ar būtų naudinga nepriklausoma
strategijų patikra („įrodyk prieš rizikuodamas"), tad renkam nuomones —
jokio pardavinėjimo, tik pokalbis.

**Asmeninė žinutė (LT):**
Sveiki — mačiau jūsų įrašą apie [X]. Nuoširdus klausimas, nieko
neparduodu: mes ką tik patikrinome savo pačių strategijas su pilnu
statistiniu testu ir visos „sugriuvo" — tikriausiai išsaugojom savo
indėlį. O jūs kaip patikrinot savąją prieš prekiaujant? Renkame
patirtis, nes svarstome, ar verta kurti nepriklausomą strategijų
patikros įrankį. Skirtumėt 10 min pokalbiui?

## 6. The commitment ask (use ONLY after a positive conversation — this is criterion 3)

EN: That's really useful, thank you. We're deciding whether to build
this properly. If we do: a one-off independent audit of your strategy
(costs, baselines, look-ahead, the works) would be around €99–149, or
a self-serve tool at ~€19–29/month. Would you genuinely use either? If
yes — can I take your email for the first-access list? (First 10 get
the audit at half price.)

LT: Labai ačiū, tai naudinga. Sprendžiame, ar tai kurti rimtai. Jei
taip: vienkartinė nepriklausoma jūsų strategijos patikra kainuotų apie
99–149 €, arba įrankis už ~19–29 €/mėn. Ar realiai naudotumėtės? Jei
taip — ar galiu užrašyti jūsų el. paštą į pirmųjų sąrašą? (Pirmiems 10
— patikra už pusę kainos.)

## 7. Follow-up if they went quiet (48h later)

EN: No worries if this isn't interesting — one last question and I'll
leave you alone: what WOULD you pay for, if anything, in the "is my
strategy real" space? Even "nothing" is a useful answer for us.

## 8. Landing-page copy block (ready for the moment we have a brand + first commitment)

Headline: **Prove your strategy before the market does.**
Sub: Independent, statistics-grade verification for retail trading
strategies: real costs, random baselines, look-ahead checks,
concentration analysis. Built by people who ran it on themselves first
— and published the negative result.
CTA: Join the first-access list → [email link]
Footer must include: not investment advice; no signals; no performance
promises; imprint per legal/TRIPWIRES before going live.

## Logging reminder

Every conversation → one row in DISCOVERY-2026-09.md's OUTCOME LOG.
Every post → note where + response count. Hours → STATUS hours log.
