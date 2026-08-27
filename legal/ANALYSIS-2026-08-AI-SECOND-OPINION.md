# Second AI research pass — legal analysis (ChatGPT), 2026-08-27

**Provenance and status — read this first.**
This document was generated with ChatGPT and supplied by Oskaras on 2026-08-27 (identifiable from the text itself: it addresses "Claude Code" directly and its source links carry `utm_source=chatgpt.com` tags). It is **not** a lawyer's answer, **not** legal advice, and it does **not** satisfy task 0.4 (written answers from a lawyer to the 6 questions in `QUESTIONS-FOR-LAWYER.md`). AI analyses — this one, or Claude's own `RESEARCH-2026-08-legal-and-market.md` — are research inputs with no professional accountability attached. They inform the questions; only a qualified human lawyer's written answer closes them.

**How it compares to our first research pass (Claude, 2026-08-26).** Largely consistent, and sober. Three points worth acting on:

1. **Copy-trading flagged as the highest-risk stream (🟡/🔴).** It argues the fact that the exchange executes followers' trades does not by itself rule out the lead trader providing a regulated service (portfolio management / advice / order transmission), and that this must not launch on a disclaimer. This is stronger caution than our plan assumed → proposed decision **D-017**: written fintech-lawyer opinion on the copy-trading qualification required before followers are enabled.
2. **Concrete consumer-law mechanics** for the paid tier checkout: two separate, actively ticked (not pre-ticked) confirmations — (a) "start providing the digital content immediately" and (b) "I understand I thereby lose the 14-day withdrawal right" — technically logged as evidence. Goes into the G3 checklist.
3. **MB founder-agreement limits**: work/services cannot be an MB member contribution; a UAB-style 4-year share vesting doesn't map cleanly onto MB membership rights; IP assignment must be specific and documented, not "everything the founder ever creates". Feeds task 2 (founder agreement) and question 6 for the lawyer.

**One discrepancy for the lawyer to resolve:** this analysis reads ESMA Q&A 2882 as making the MiCA "advice" perimeter *broader* than MiFID II; our first pass read ESMA Q&A 2463 as aligning MiCA advice *with* MiFID II. Both cannot be fully right — this is exactly lawyer question 1.

The full text as received follows, unedited.

---

Taip. Supratau — tau reikia ne klausimų advokatui, o paruoštų atsakymų į visus 6 klausimus, kuriuos galėtum tiesiog nukopijuoti į Claude Code kaip teisinio tyrimo bazę.
Žemiau pateikiu versiją, kuri yra sąmoningai parašyta faktiškai, atsargiai ir su aiškia riba tarp to, kas nustatyta teisės aktuose, ir to, kas yra teisinė išvada. Šaltiniai yra oficialūs: EUR-Lex, ESMA, Lietuvos bankas, VMI, VVTAT, Sodra ir Lietuvos teisės aktai.

TEISINĖ ANALIZĖ — LIETUVA / ES / MiCA / CRYPTO SIGNALS BUSINESS
Data: 2026-08-27

Bendra išvada
Planuojamas verslo modelis gali būti vykdomas Lietuvoje be MiCA CASP licencijos tik tuo atveju, jei faktinė veikla išlieka informacinė ir neperžengia reguliuojamų crypto-asset services ribos.
Pagrindinė rizika nėra pats automatiškai generuojamų signalų egzistavimas. Pagrindinė rizika atsiranda tada, kai:

* rekomendacijos tampa personalizuotos;
* vartotojui rekomenduojama konkreti crypto-asset paslauga pagal jo individualias aplinkybes;
* įmonė perduoda ar vykdo klientų orderius;
* įmonė valdo klientų crypto-assets;
* įmonė teikia portfolio management;
* copy-trading veikloje įmonė faktiškai teikia reguliuojamą paslaugą;
* affiliate veikla faktiškai tampa individualizuota rekomendacija dėl konkretaus CASP.

MiCA apibrėžia „advice on crypto-assets" kaip personalizuotų rekomendacijų klientui teikimą, susijusį su viena ar keliomis crypto-assets operacijomis arba crypto-asset paslaugų naudojimu. ESMA 2026 m. Q&A 2882 aiškiai nurodo, kad MiCA advice apimtis yra platesnė nei MiFID II advice apimtis. (ESMA Q&A 2882)
Todėl verslo modelio teisinė konstrukcija turi remtis ne disclaimeriais, o faktine veikla ir technine produkto architektūra.

## 1. MiCA — ar automatiniai signalai yra „advice on crypto-assets"?

Atsakymas: Ne kiekvienas crypto signalas automatiškai yra MiCA „advice". Esminis MiCA kriterijus yra tai, ar teikiama personalizuota rekomendacija klientui.
MiCA Article 3(1)(24) „advice on crypto-assets" apibrėžia kaip personalizuotų rekomendacijų teikimą klientui jo prašymu arba paslaugų teikėjo iniciatyva, susijusių su viena ar daugiau crypto-assets operacijų arba crypto-asset paslaugų naudojimu. (EUR-Lex, Reg. (EU) 2023/1114)
ESMA 2026 m. Q&A 2882 papildomai pabrėžia, kad MiCA advice perimeter yra platesnis nei MiFID II. Todėl negalima remtis vien senesne MiFID II praktika.

Planuojamas modelis. Jeigu sistema:

* automatiškai generuoja signalus;
* visiems vartotojams pateikia identišką signalą;
* nerenka vartotojo finansinės padėties;
* nevertina jo rizikos tolerancijos;
* nevertina investavimo tikslų;
* nevertina portfelio;
* nekeičia signalo pagal konkretų vartotoją;
* neteikia individualių rekomendacijų DM;
* neatsako individualiai „ką tau pirkti?";

tada yra stiprus teisinis argumentas, kad tai yra nepersonalizuota rinkos informacija / signalų publikavimas, o ne MiCA Article 3(1)(24) advice.

Svarbus 2026 m. ESMA paaiškinimas: ESMA Q&A 2882 nurodo, jog MiCA advice analizėje reikia žiūrėti plačiau negu vien į tradicinį MiFID II „personal recommendation" supratimą. Todėl mokama uždara Telegram/Discord grupė nėra automatiškai saugi vien todėl, kad signalai yra vienodi. Tačiau uždarumas savaime taip pat nereiškia, kad veikla tampa advice. Reikia vertinti visą veiklos turinį ir jo pateikimo būdą.

Ką būtina uždrausti, kad būtų išlaikytas nepersonalizuotas modelis:

1. Individualių rekomendacijų per DM.
2. „Pagal tavo situaciją pirk X."
3. Portfolio review.
4. Individualaus position sizing.
5. Individualių stop-loss / take-profit pagal vartotojo riziką.
6. Vartotojų finansinės padėties vertinimo.
7. Klausimų apie vartotojo investavimo tikslus, jei atsakymai vėliau naudojami signalui individualizuoti.
8. „Tau tinka X" / „tau geriausia X" formuluočių.
9. Individualių signalų skirtingoms vartotojų grupėms pagal jų profilį.
10. Individualizuotų rekomendacijų dėl konkrečios crypto exchange.

Mokama grupė: mokama grupė, kurioje visi gauna identišką automatinį turinį, nėra vien dėl savo mokamumo automatiškai CASP advice. Tačiau negalima teigti, kad „uždara grupė yra vieša", kaip absoliučios teisinės taisyklės. Teisingesnė pozicija: grupės turinys nėra personalizuotas ir nėra grindžiamas konkretaus kliento individualiomis aplinkybėmis. Tai turi būti reali produkto savybė, o ne tik sutartinė deklaracija.

## 2. MAR ir perpetual futures

Čia būtina atskirti MiCA ir MAR/MiFID II režimus. MiCA netaikoma crypto-assets, kurie kvalifikuojami kaip finansinės priemonės; tokiems instrumentams gali būti taikoma MiFID II / MAR sistema. ESMA gairėse dėl crypto-assets kvalifikavimo kaip financial instruments pabrėžia, kad vertinimas turi būti atliekamas pagal ekonominę instrumento esmę, o ne vien jo technologinę formą. ESMA aiškiai aptaria crypto-native derivatives, įskaitant perpetual futures, ir nurodo, kad jų ekonominės funkcijos gali lemti kvalifikavimą kaip derivative instruments pagal MiFID II. 2026 m. ESMA toliau nagrinėja perpetual futures, įskaitant Bitcoin perpetual futures, kaip galimai patenkančius į finansinių išvestinių priemonių režimą.

Todėl planuojamas sprendimas neskelbti perpetual futures / CFD signalų yra teisingas. Tačiau teiginys „offshore perpetual futures niekada nepatenka į MAR" būtų per kategoriškas. Instrumento vieta už ES ribų savaime neišsprendžia jo teisinės kvalifikacijos klausimo. Reikia analizuoti konkretų instrumentą, jo savybes ir MAR Article 2 taikymo sąlygas.

Ar copy-trading lead trader automatiškai tampa „investment recommendation producer" pagal MAR? Neįmanoma to patvirtinti vien dėl to, kad paskyra yra lead trader. MAR ir Delegated Regulation 2016/958 reglamentuoja investment recommendations ir interesų konfliktų atskleidimą tais atvejais, kai MAR apskritai taikomas atitinkamam finansiniam instrumentui. Todėl pirmiausia reikia nustatyti:

1. Ar konkretus copy-trading instrumentas yra financial instrument pagal MiFID II?
2. Ar jam taikomas MAR?
3. Ar lead trader veiksmai teisiškai yra investment recommendation?
4. Ar platforma pati vykdo followerių orderius savo vardu / pagal savo licencijuotą paslaugą?
5. Ar lead trader turi sutartinius santykius su followeriais?
6. Ar lead trader priima individualius sprendimus followerių naudai?
7. Ar compensation priklauso nuo followerių prekybos rezultatų?

Konflikto atskleidimas: net jeigu MAR techniškai netaikomas, interesų konflikto atskleidimas turėtų būti privalomas kaip geros praktikos minimumas. Pavyzdžiui: „Our company receives a performance-based share of the results generated through this lead-trader account. This creates a financial interest that may influence the promotion of the account."

Išvada: copy-trading klausimas turi būti laikomas G3 fintech/crypto teisininko klausimu, nes vien faktas, kad birža pati techniškai vykdo followerių sandorius, dar nėra pakankamas pagrindas teigti, kad lead trader neteikia jokios reguliuojamos paslaugos.

## 3. Lietuvos bankas / FNTT

Jeigu įmonė tik publikuoja nepersonalizuotą informaciją apie crypto-assets ir neteikia MiCA Article 3(1)(16) crypto-asset services, vien informacijos publikavimas savaime neturėtų sukurti CASP licencijos pareigos. MiCA autorizavimo režimas taikomas crypto-asset service providers, teikiantiems MiCA reguliuojamas crypto-asset services. Lietuvos bankas nurodo, kad crypto-asset services Lietuvoje po pereinamojo laikotarpio turi būti teikiamos pagal MiCA autorizavimo režimą.

Todėl planuojama įmonė neturėtų: saugoti klientų crypto-assets; valdyti klientų wallet; vykdyti orderių klientų vardu; priimti ir perduoti klientų orderių; teikti portfolio management; teikti personalizuoto advice; keisti vartotojo signalų pagal jo profilį.

Affiliate: vien affiliate nuorodos naudojimas nėra automatiškai tas pats, kas CASP paslaugos teikimas. Tačiau jeigu affiliate veikla tampa „Mes išanalizavome jūsų situaciją ir rekomenduojame jums naudoti Exchange X", situacija pasikeičia, nes gali atsirasti MiCA advice dėl crypto-asset paslaugos naudojimo.

FNTT: jeigu įmonė pati neteikia virtualiosios valiutos keitimo, custody, transfer ar kitų reguliuojamų paslaugų, vien informacinė veikla savaime neturėtų paversti jos VASP/CASP. Tačiau įmonė vis tiek turi laikytis bendrų apskaitos, mokesčių, vartotojų teisių, jai taikomų AML/KYC taisyklių, reklamos ir GDPR reikalavimų.

## 4. Vartotojų teisė ir privatumas

14 dienų atsisakymo teisė: pagal Lietuvos vartotojų teisę vartotojas paprastai turi 14 dienų teisę atsisakyti nuotolinės sutarties, tačiau skaitmeniniam turiniui yra speciali išimtis. VVTAT paaiškinime nurodo, kad ši išimtis taikoma, kai skaitmeninio turinio teikimas pradėtas: (1) gavus vartotojo išankstinį aiškų sutikimą; ir (2) vartotojui pripažinus, kad dėl to jis praras teisę atsisakyti sutarties.

Todėl checkout sistemoje turėtų būti aktyvus vartotojo pasirinkimas, o ne iš anksto pažymėtas checkbox. Rekomenduojama struktūra:
☐ Prašau pradėti teikti skaitmeninį turinį nedelsiant.
ir atskirai:
☐ Patvirtinu, kad suprantu, jog pradėjus teikti skaitmeninį turinį nedelsiant, prarasiu teisę atsisakyti sutarties per 14 dienų.
Tai turi būti įrodyta ir techniškai užfiksuota.

Svetainės rekvizitai: juridinis pavadinimas; teisinė forma; juridinio asmens kodas; buveinės adresas; el. paštas; kiti privalomi kontaktiniai duomenys; PVM kodas, jei taikoma; Terms & Conditions; Privacy Policy; informacija apie atsisakymo teisę; prenumeratos nutraukimo tvarka.

Virtualus biuras: gali būti naudojamas, jeigu jis teisėtai yra juridinio asmens buveinė ir įmonė faktiškai gali gauti ten siunčiamus teisinius dokumentus. Nerekomenduojama naudoti neegzistuojančio ar tik fiktyvaus adreso.

Affiliate reklama: affiliate santykiai turi būti aiškiai atskleidžiami. Rekomenduojama naudoti „REKLAMA / AFFILIATE" ir: „Jeigu registruositės arba atliksite veiksmus per šią nuorodą, galime gauti komisinį mokestį." Vartotojas turi suprasti, kad egzistuoja komercinis interesas.

GDPR: email duomenų naudojimas turi turėti teisėtą pagrindą. Reikia atskirti paslaugos administravimą (invoice; password reset; subscription renewal; account security) ir tiesioginę rinkodarą (nauji signalai; naujas premium planas; affiliate pasiūlymai; produkto reklama). Antrajai kategorijai turi būti atskirai įvertintas sutikimo / teisėto intereso pagrindas ir Elektroninių ryšių įstatymo reikalavimai. VDAI turi atskirą praktiką dėl elektroninių ryšių naudojimo tiesioginei rinkodarai.

## 5. Įmonė, USDT/USDC ir mokesčiai

USDT/USDC gavimas nepanaikina mokesčių: pajamų apskaitos; pelno mokesčio; PVM, jeigu taikoma; apskaitos dokumentų; source-of-funds klausimų. VMI yra išaiškinusi virtualiųjų valiutų apskaitos principus ir nurodo, kad dėl didelio kurso svyravimo įmonė turi savo apskaitos politikoje nustatyti naudojamą kurso šaltinį ir momentą, kuriuo kursas fiksuojamas apskaitai ir mokestinėms prievolėms.

Praktinis modelis — jeigu įmonė gauna 10,000 USDC, apskaitoje reikia nustatyti: gavimo datą; USDC kiekį; EUR rinkos vertę tuo momentu; naudojamą kurso šaltinį; blockchain transaction hash; wallet address; mokėtoją; sutartį/invoice/partner statement; pajamų ekonominį pagrindą. Tada pajamos registruojamos eurais pagal įmonės apskaitos politiką.

Rekomenduojama: Company → corporate crypto account → corporate wallet → company bank account; nelaikyti verslo pajamų founderio asmeninėje Binance/Bybit wallet.

MB ar UAB? MB tinka dviem fiziniams steigėjams ir yra paprastesnė mažam verslui. MB įstatymas nustato, kad MB nariai yra fiziniai asmenys, o MB nario įnašu negali būti darbai ir paslaugos. UAB yra geresnė, jeigu planuojama: investuotojai; akcijų perleidimas; equity vesting; ESOP; fundraising; ateityje parduoti įmonę. Jeigu tikslas yra 90 dienų testas ir maža įmonė → MB yra racionalus. Jeigu tikslas yra kurti rimtą startupą su equity struktūra → UAB techniškai patogesnė.

0 % pelno mokestis nuo 2026 m.: VMI nurodo, kad nuo 2026 m. naujai įregistruoti maži vienetai gali taikyti 0 % pelno mokesčio tarifą pirmąjį ir antrąjį mokestinius laikotarpius, jeigu tenkinamos PMĮ 5 straipsnio sąlygos. Svarbiausios sąlygos: pajamos kiekvienu iš pirmųjų dviejų mokestinių laikotarpių neviršija 300 000 EUR; dalyviai yra fiziniai asmenys; netenkinamos PMĮ 5 str. 3 d. sąlygos; tenkinamos kitos PMĮ sąlygos. Nuo 2026 m. taip pat taikomas 7 % tarifas atitinkantiems mažiems vienetams. 0 % PM nereiškia, kad visa įmonės ekonomika neapmokestinama — vis tiek gali būti GPM, VSD, PSD, PVM, kiti mokesčiai.

MB narių išmokos: MB narių socialinio draudimo sistema 2026 m. keičiasi. Prieš pasirenkant „mes abu pasiimsime pinigus kaip MB nariai", reikia apskaičiuoti konkrečią išmokų struktūrą. Sodra pateikia atskiras taisykles MB nariams; 2026 m. PSD mėnesinė įmoka tam tikrais atvejais yra 80,48 EUR, tačiau konkreti prievolė priklauso nuo asmens statuso. Išmokų modelį turi patikrinti buhalteris pagal: ar nariai dirba kitur; ar studijuoja; ar turi kitą draudimą; išmokų rūšį; sumą; laikotarpį.

## 6. Founder agreement

MB narių susitarimas gali reguliuoti tarpusavio santykius, tačiau negali panaikinti imperatyvių MB įstatymo taisyklių. MB įstatymas reguliuoja nario teisių perleidimą ir nustato, kad įnašu negali būti darbai ar paslaugos. Todėl „Founder A gauna 50 %, nes ateityje dirbs 2 metus" ir „Founder A įneša darbą kaip MB įnašą" yra du skirtingi dalykai — antrasis nėra tinkamas MB įnašo mechanizmas.

Vesting: founder agreement gali nustatyti sutartinį ekonominį mechanizmą, tačiau MB atveju reikia suderinti su MB nario teisių perleidimo taisyklėmis, MB nuostatais, Civiliniu kodeksu ir faktine narystės struktūra. MB nėra taip patogu naudoti kaip UAB akcijų 4 metų vesting modelį.

IP: visas verslui sukurtas IP turi būti aiškiai perduotas įmonei: source code; trading algorithms; signal-generation code; strategy documentation; datasets; website; graphics; brand; trademarks; domain; Telegram; Discord; social media; GitHub repositories; documentation; proprietary research. Autorių teisių turtinių teisių perdavimas turi būti tinkamai įformintas; negalima remtis vien abstrakčiu teiginiu „viskas, ką founderis kada nors sukurs, priklauso įmonei". IP assignment turi būti konkretus ir dokumentuotas.

Account ownership: verslo paskyros neturi būti kontroliuojamos tik vieno founderio asmeniniu el. paštu. Rekomenduojama: company-owned email → domain → Google Workspace → GitHub organization → Telegram/Discord administration → exchange corporate account → corporate wallet → 2FA recovery → password manager. Ypač svarbu copy-trading versle — kitaip gali kilti ginčas, kam priklauso trading account, API keys, strategy, followers, performance fees.

## Galutinis teisinis verdiktas

🟢 Gana saugus modelis: nemokamas turinys → automatiškai generuojami signalai → spot only → identiški visiems → jokio personalizavimo → jokio klientų turto → jokio order execution → jokio individual advice.

🟡 Sąlyginai saugus: paid Telegram/Discord → identiški signalai visiems → nėra suitability → nėra portfolio analysis → nėra individualių DM rekomendacijų. Šiam modeliui prieš paleidimą rekomenduojama gauti rašytinę MiCA specialisto išvadą, nes ESMA Q&A 2882 2026 m. išplėtė praktinę advice analizę.

🟡/🔴 Didžiausia rizika: copy-trading lead trader — reikia nustatyti, ar faktinis modelis nėra portfolio management, advice, order transmission ar kita MiCA/MiFID reguliuojama veikla. Šito nereikėtų paleisti vien remiantis bendru disclaimeriu.

🔴 Nerekomenduojama: personalizuoti signalai; portfolio management; individualūs DM signalai; klientų lėšų custody; orderių vykdymas klientams; perpetual futures / CFD recommendations; individualus exchange parinkimas.

## Šaltiniai (kaip pateikta)

1. MiCA — Regulation (EU) 2023/1114 — EUR-Lex — https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng
2. ESMA Q&A 2882 — https://www.esma.europa.eu/publications-data/questions-answers/2882
3. ESMA MiCA Q&A database — https://www.esma.europa.eu/publications-and-data/questions-answers
4. ESMA guidelines on classification of crypto-assets as financial instruments — https://www.esma.europa.eu/sites/default/files/2024-12/ESMA75453128700-1323_Final_Report_Guidelines_on_the_conditions_and_criteria_for_the_qualification_of_CAs_as_FIs.pdf
5. Delegated Regulation (EU) 2016/958 — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0958
6. Lietuvos bankas — https://www.lb.lt/en/news/lithuanian-authorities-requirements-for-crypto-asset-companies-must-be-tightened-immediately
7. VMI — 0 % pelno mokestis nuo 2026 m. — https://www.vmi.lt/evmi/tarifai-5-str.-
8. VMI — virtualiosios valiutos apskaita — https://www.vmi.lt/evmi/documents/20142/391185/ (RM-21969)
9. VVTAT — 14 dienų teisė ir digital content exception — https://vvtat.lrv.lt/lt/informacija-lietuviu-gestu-kalba/dazniausiai-uzduodami-klausimai-2-dalis/
10. Sodra — MB narių socialinis draudimas — https://sodra.lt/informacija/susipazinkite-su-svarbiausiais-klausimais-ir-atsakymais-apie-mazaja-bendrija
11. Mažųjų bendrijų įstatymas — https://e-seimas.lrs.lt/portal/legalActPrint/lt?documentId=TAIS.429530
