# Verslas — Nojus & Oskaras

The shared workspace for our business: a pseudonymous crypto trading-intelligence brand. We prove a systematic spot-trading strategy in public, then monetise the verified track record — exchange affiliate commissions, a copy-trading lead account, and (after the gates pass) a paid signal tier. Signal-only: no order execution for others, no custody, no managing anyone's money.

**Current phase: 0 — Set up** · Revenue: €0 (by design) · Next checkpoint: Week 2 (9 Sep 2026)

## Read in this order

| Document | What it is |
| --- | --- |
| [CHARTER.md](CHARTER.md) | The constitution: objective, roles, revenue streams, non-negotiables, stage gates G0–G4, budget, kill criteria |
| [DECISIONS.md](DECISIONS.md) | Every material decision (D-001…), its rationale and status. **D-001…D-016 accepted by both founders on 2026-08-26**; new decisions get new D-numbers |
| [PLAN-90-DAYS.md](PLAN-90-DAYS.md) | 27 Aug – 25 Nov 2026: tasks, owners, checkpoints, the strategy research protocol, hypothesis template |
| [STATUS.md](STATUS.md) | Live status: done / open decisions / next actions / risks / log. Updated at every weekly sync |
| [RESEARCH-2026-08-legal-and-market.md](RESEARCH-2026-08-legal-and-market.md) | Verified legal (MiCA, MAR, Lithuania, affiliates, tax) and market research with sources |
| [research/PROMPTS-2026-08.md](research/PROMPTS-2026-08.md) | The research prompts, kept for re-verification before time-sensitive decisions |
| [legal/](legal/) | Lawyer questions, review feedback, tripwires, research addenda — nothing in this repo is legal advice |

## The short version

1. **Track record before revenue.** Nothing is sold until the stage gates in CHARTER §5 pass. First ~9 months earn €0 by design.
2. **Spot-only public signals, pseudonymous brand.** No perpetual-futures recommendations published (MAR identity rules); perps exposure only ever via a validated copy-trading lead account.
3. **Only MiCA-authorised exchanges promoted** to EU residents. No Binance/MEXC/Bitget links.
4. **Everything is logged.** Decisions get D-numbers, experiments get EXP-numbers, signals get immutable timestamped IDs with daily hash anchoring.
5. **Weekly Monday sync** (1 hour): review STATUS.md, log decisions, assign tasks, compare hours spent with plan.

## Working rules for this repo

- STATUS.md is the single source of truth for "where are we" — update it at every sync.
- A decision isn't made until it's in DECISIONS.md with a status.
- Strategy-work scaffolding currently lives in [`verslas-signals/`](verslas-signals/) (data pipeline, dataset versioning, cost model) and will be split into a separate private repo when created (task 0.9). Nothing secret (keys, credentials, tuned strategy parameters) ever goes in *this* repo.
- None of the documents here are legal advice; the lawyer consult (task 0.4) validates the legal positions before money moves.
