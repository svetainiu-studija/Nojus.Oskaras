# O1 — Independent Strategy Audit (service spec, ready to sell)

Status: demand being tested in the discovery sprint. This file makes the
service deliverable the day the first customer commits — the engine
behind it already exists and audited itself in public.

## The offer (one paragraph, customer-facing)

You send us your strategy's exact rules (or your backtest + trade
list). We rebuild it independently and put it through the same battery
we ran on our own strategies before refusing to trade them: realistic
costs with a 2× stress pass, a random-entry baseline with a proper
p-value, walk-forward folds, look-ahead and data-integrity checks,
concentration and leave-one-out analysis, and a multiplicity-corrected
read of your results. You get a written verdict you can trust —
including, if that's the truth, "this would have lost you money." We
publish our methodology and we ran it on ourselves first: our own
result was NO EDGE, and we shipped it.

**What this is not:** investment advice, signals, portfolio management,
or a performance promise. We verify claims; we never tell you what to
trade. (Legal basis: verification/education sits outside the MiCA
advice perimeter — see legal/ research; wording above must be kept.)

## Deliverable: the audit report (template)

1. **Spec capture** — the strategy restated as testable rules; every
   ambiguity we had to interpret, listed. (Customer signs off before we
   run — the same pre-registration discipline we use ourselves.)
2. **Data integrity** — the venues/bars used, gap/duplicate/outage
   scan, survivorship notes.
3. **Reproduction** — our independent implementation's results vs the
   customer's claims; every divergence explained.
4. **Costs** — results net of fees/spread/slippage for their actual
   venue tier; the 2× stress pass.
5. **Baselines** — random-entry/same-exit Monte-Carlo p-value; buy-and-
   hold comparison.
6. **Robustness** — walk-forward folds; parameter neighbourhood (did
   they pick a spike or a plateau?); regime split.
7. **Concentration** — top-asset share, leave-one-out, biggest-trade
   dependence (the check that killed our own strategy).
8. **Multiplicity** — how many variants they tried (we ask; we also
   estimate), Holm-corrected significance.
9. **Verdict page** — PASS/FAIL per pre-agreed criteria + the three
   sentences that matter, in plain language.

Turnaround: 5 working days from signed spec. One revision round
included (spec corrections only — no re-running until it passes).

## Intake questionnaire (send on first commitment)

1. The rules, exactly: entry, exit, stop, sizing, universe, timeframe.
   Code welcome but not required.
2. Venue + account tier (for real fees).
3. Your backtest results if any (trade list ideal).
4. How many versions/parameter sets you tried before this one (honest
   answer makes the audit stronger, not weaker).
5. What result would change your mind? (We put this on the verdict
   page.)

## Pricing hypotheses (test in discovery; do not undercut below floor)

- Launch: **€99** first 10 customers ("founding audits", public
  waitlist) → then **€149–299** by complexity (single-pair simple rules
  vs multi-asset portfolio logic).
- Floor: never below €99 — the work is 4–8 real hours even with the
  engine.
- Tool tier (O2, later, if demand shows): €19–29/month self-serve
  subset.

## Proof assets (already public in this repo)

- Our own audit: `research/AUDIT-2026-08-*` — three bugs found in our
  own code by our own adversarial process, verdict unchanged, published.
- The full research arc EXP-001…007 with pre-registered rules and a
  negative final verdict we acted on.
- 68 automated tests incl. look-ahead property tests.
The sales line is one sentence: *"We did this to ourselves first, and
we published the answer we didn't want."*

## Operations (when first customer lands)

Payment: rails per `research/RAILS-AND-PROGRAMMES-2026-08.md` (Whop
front-runner; no rail promises until AUP confirmed). Entity: D-006 —
register the MB before the first payout is RECEIVED; a first invoice
can wait days, not weeks, so start registration at first commitment.
Founder agreement must be signed before first revenue (D-011).
