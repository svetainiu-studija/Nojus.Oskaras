# CHARTER §9 pivot discussion (2026-08-28)

For: Oskaras & Nojus · From: the build sessions · Status: **deferred —
audit first (D-023, 2026-08-28).** The founders chose to verify the
conclusion before acting on it: a pre-registered forensic audit
(`AUDIT-2026-08-PROTOCOL.md`, closes 2026-09-11) checks implementation,
data, costs and statistics for verified errors. If the conclusion
survives, the a/b/c choice below is made as **D-024**; if a verified
error changes an experiment's verdict under its unchanged rules, the
affected hypothesis re-enters where a pass would have put it. This
discussion was mandatory under D-022: EXP-007 failed.

## What happened, in one paragraph

In one week, every strategy idea was implemented faithfully, tested against
4.5 years of clean audited data, and judged by rules written down before
each result existed. Nine configurations across four hypothesis lineages —
the three from your trading interview, plus the momentum family the data
itself suggested — and every one failed its own pre-registered rule. The
last and strongest, HYP-004, looked genuinely promising at p=0.068 until
the widened universe revealed the truth: **SOL's great runs were 148% of
the profit** (everything else combined nets a loss), ex-SOL expectancy is
negative, and the p-value got *worse* with more data. That is the
signature of an era, not an edge.

| Lineage | Configs | Verdict | Root cause |
|---|---|---|---|
| HYP-001 pullback | 4 | Abandoned | ~Breakeven net of costs; the filters worked, the core lost |
| HYP-002 RS breakout | 1 | Failed | Its own stop rule rejected 95% of its entries |
| HYP-003 capitulation | 1 | Failed | The setup occurs once in 4.5 years |
| HYP-004/005/006 momentum | 3 | Failed | Costs kill 4h; daily was SOL's era, not an edge |

This is the base-rate outcome (CHARTER §8.1 warned of exactly this), reached
honestly, at week 1 of 12 instead of week 12 — the machine is fast enough
that no idea died of neglect. Nothing about the process failed; the *ideas*
failed, which is what a working process is for.

## What it means for the business

Be clear-eyed: streams 1–3 of the CHARTER (affiliates on the back of a
public track record, copy-trading lead account, paid tier) all sit behind a
verified systematic track record. There is no track record to verify. The
tempting third path — "just try more hypotheses" — is closed by D-022, and
reopening it would repudiate the one thing this week *proved*: that your
rules mean what they say. That proof is worth more than any strategy.
(Trading your own money discretionarily as a hobby remains your private
business — but the data says don't build a company on selling it.)

## What survives (real assets, all pushed)

1. **The research machine.** Data pipeline with fingerprinted datasets and
   audits, canonical derived bars, point-in-time universe construction, a
   portfolio backtester with honest execution and cost modelling, bootstrap
   statistics, Monte-Carlo baselines, pre-registration harness — 61 unit
   tests, cross-platform, built in a week and validated on 1.75M bars.
2. **The demonstrated discipline.** Two students who ran a genuinely
   rigorous research program and published every failure. Rare, and visible
   in the git history to anyone you show it to.
3. **The knowledge corpus.** MiCA/MAR/affiliate/payment-rail research,
   tripwires, founder-agreement template — reusable for any future venture
   near this space.
4. **The budget.** Effectively €0 spent. The €1–5k risk capital is intact.
5. **The negative result itself.** You now know first-hand that the thing
   most signal sellers sell does not survive honest testing. That insight
   is a positioning weapon for Option A.

## The §9 menu

**Option A — software/tooling pivot (the path §9 names).** Build around
what is provably real: the machine and the discipline, not predictions.
First step is NOT code — it is a **time-boxed discovery sprint (2 weeks,
€0)**: talk to retail traders and small communities; find out who would pay
for honest backtesting/verification tooling ("prove your edge before you
risk money on it"), strategy-audit reports, or the data-pipeline itself as
a service. Also list the non-product routes: freelance/contract work on the
back of this repo. Deliverable: a 1-page market note and a go/no-go. If go
→ CHARTER v2.0 + a new 90-day plan. If no-go → Option B with clean
consciences.

**Option B — stop.** Archive the repo read-only, write a 1-page
post-mortem, keep it as a portfolio piece for both of you. Zero further
cost, full dignity: the record shows a disciplined build and an honest
negative result — most people cannot show either.

**Option C — pause until a named date** (e.g., after the exam session).
Not listed in §9, but legitimate; the repo keeps everything. The risk is
that "paused" quietly becomes "abandoned" without the honesty of B.

## Recommendation

**A, as a 2-week discovery sprint with a pre-committed go/no-go.** It risks
nothing but a fortnight, uses the same discipline that just worked (declare
the pass criteria for "go" before talking to anyone), and its failure mode
*is* Option B. Choosing B outright is also entirely respectable. C only
with a date attached.

Reply with **a**, **b**, or **c** (plus a date if c) — logged as D-023
either way.
