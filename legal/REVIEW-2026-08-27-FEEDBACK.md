# Review feedback on the legal analysis — received 2026-08-27

**Provenance:** supplied by Oskaras on 2026-08-27 as review feedback on `ANALYSIS-2026-08-AI-SECOND-OPINION.md`. Authorship not yet stated — **if this is the cousin's (a lawyer's) written reply, record their name and the date here**; that is what makes it citable as a lawyer's written view. Until then it is treated as founder-relayed feedback.

**Disposition of the eight points:**

| # | Point (summary) | Action taken |
|---|---|---|
| 1 | Automation/identical signals do not *automatically* exclude MiCA advice; the definition and ESMA Q&A 2882 govern; analyse the paid model separately from the free model | Already the workspace position (free = launch path; paid = gated on written opinion at G3). Re-verified against the ESMA source → `RESEARCH-2026-08-27-ADDENDUM.md` |
| 2 | Analyse "issued otherwise than exclusively to the public" for a paid closed group specifically | Verified the ESMA text → addendum; remains lawyer question 1 (open) |
| 3 | Separate affiliate analysis: when does promoting a specific exchange stop being ordinary marketing | **Question 7 added** to `QUESTIONS-FOR-LAWYER.md`; boundary rules in `TRIPWIRES.md` |
| 4 | Copy-trading needs separate specialist analysis; exchange execution ≠ no obligations for us | Matches proposed **D-017** (written fintech-lawyer opinion before followers enabled) — awaiting founders' confirmation |
| 5 | Rely on product architecture, not disclaimers: no profiling, no personalised signals, no portfolio analysis, no personalised DMs | Already CHARTER §4.2; now also expressed as engineering requirements in `TRIPWIRES.md` (the product must make these *impossible*, not just forbidden) |
| 6 | Distinguish MiCA vs MiFID II vs MAR clearly | Regime map included in `TRIPWIRES.md` |
| 7 | Verify the exact 2026 0% CIT rules (eligibility, related-party rules, threshold, loss of relief) against current VMI guidance | Verified → `RESEARCH-2026-08-27-ADDENDUM.md` |
| 8 | Add a "facts that would change the legal conclusion" section | Written → `legal/TRIPWIRES.md` |

## The feedback as received (verbatim)

I broadly agree with the statements and the overall legal approach. I would, however, add a few important points.

First, I would not treat the fact that signals are automatically generated or identical for everyone as automatically excluding MiCA advice. The key issue is the actual legal definition and ESMA's interpretation of "advice on crypto-assets", especially ESMA Q&A 2882. The paid private-group model therefore needs to be analysed separately from the free public-information model.

Second, I would specifically analyse whether a paid closed Telegram/Discord group can still constitute information provided to the public, and exactly what ESMA means by information being issued "otherwise than exclusively to the public". This is one of the most important uncertainties for our business model.

Third, I would add a separate analysis of affiliate marketing. We need to know when simply linking to a MiCA-authorised exchange is ordinary advertising/marketing and when promoting a particular exchange could become a personalised recommendation or another regulated activity.

Fourth, the copy-trading lead-trader model deserves separate specialist analysis. We should not assume that because the exchange executes the followers' trades, we automatically have no regulatory obligations. The exact contractual relationship, copy-trading mechanism, performance fee and communications with followers should all be considered.

Fifth, I agree that disclaimers should not be treated as our legal protection. The business model itself must remain outside regulated activities. We should therefore design technical restrictions into the product from the beginning: no user profiling, no personalised signals, no portfolio analysis, no personalised DMs and no individual recommendations.

Sixth, I would like the research to distinguish clearly between MiCA, MiFID II and MAR, because crypto-assets and crypto derivatives can fall under different regulatory frameworks depending on their legal classification.

Seventh, for the tax section, I want the exact 2026 rules verified rather than relying on general statements about the 0% corporate tax rate. The conditions for eligibility, related-party rules, revenue threshold and circumstances that cause the exemption to be lost should all be checked against the current VMI guidance and legislation.

Finally, I would add a practical "facts that would change the legal conclusion" section. For example, if we later introduce personalised recommendations, portfolio analysis, different signals based on user profiles, individual DMs, derivatives, or a different copy-trading structure, I want the document to explain exactly which legal conclusions would change.

Other than those points, I agree with the general direction of the analysis. The main principle should be that we do not try to rely on disclaimers or wording to avoid regulation; instead, we structure the actual product and business activities so that they remain outside regulated services.
