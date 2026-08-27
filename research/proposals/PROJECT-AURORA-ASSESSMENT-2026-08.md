# "Project Aurora" — received 2026-08-28, assessment for the founders

Received from Oskaras in chat: a ~90-part "30-day institutional research
mandate" (ChatGPT-authored; provenance noted as with all external AI
inputs). It directs a new research program over perpetual futures with
microstructure/cross-exchange/ML branches, execution engines and staged
live deployment. Oskaras's own transmittal corrections: venue is OKX (not
MEXC), and he executes manually with **no API keys on any exchange**.

**Status: NOT started.** It conflicts with recorded decisions and with
its own transmittal constraints; per D-024's reopening rule it can only
proceed as a new joint founder decision (D-025-class). This file exists
so Monday's sync decides on facts.

## Premise corrections (the mandate was written for a different project)

| Mandate premise | This project's reality |
|---|---|
| MEXC futures venue | MEXC excluded (D-004, not MiCA-authorised EEA); venue OKX |
| USDT-margined perpetual futures | **Spot-only** for anything the business touches (D-003; CLAUDE.md rule 1: never add perps to any config); no leverage year 1 (D-015) |
| ~$15,000 account | Recorded risk capital €1–5k (D-016). No $15k exists in any project document |
| API bot execution, order reconciliation, shadow mode | Oskaras executes **manually, no API keys** (his own transmittal) — which by itself invalidates the mandate's Priority 1/2/7 (microstructure, cross-exchange latency, execution alpha at 1s–1min horizons) |
| "R1/R2" prior research | Actual record: HYP-001…006, EXP-001…007 + AUDIT-2026-08, conclusion NO EDGE / DO NOT TRADE (D-024 proposed, Oskaras's vote recorded) |
| "MEXC API fee re-audit" | Already audit item C1: OKX **spot** schedule vs costs.yaml (Nojus) |

## Feasibility, honestly

- **Not feasible here:** Tier-3 microstructure (needs L2 book/tick
  history — not retroactively obtainable free; needs automated
  execution to monetize); execution alpha; shadow-execution latency
  measurement; anything at sub-hour horizons under manual execution.
- **Partly feasible:** derivatives-state research (funding/OI/basis at
  4h–1d horizons from OKX public endpoints — new data acquisition, real
  but bounded history) and daily cross-exchange lead/lag on OHLCV
  (weak at that horizon). Both concern PERPS — outside the business's
  spot-only charter; relevant only to a personal-account question.
- **Already done by this project:** the mandate's Days 1–6 (repository
  forensic audit, lineage, data forensics, cost audit, statistical
  audit, reproduction) = AUDIT-2026-08, completed, three bugs found and
  fixed, conclusion unchanged.

## Adopted regardless of the decision (governance upgrades)

Multiplicity ledger with corrected p-values (Holm — in place); PBO and
Deflated Sharpe as mandatory reporting IF research ever reopens; the
hypothesis-registry field set (superset of ours); placebo and ablation
tests as standard; the no-trade-zone principle; "negative evidence is
permanent" (already CLAUDE.md-adjacent practice).

## What starting Aurora would actually require (per D-024's own rule)

A new joint founder decision stating: exactly what reopens; why D-022/
D-024's stopping rules are overridden; what NEW information justifies it
(a longer prompt is not new information); instrument scope vs the
spot-only charter; a data-acquisition budget vs the €5k ceiling;
maximum experiments; exact stopping criteria; no retroactive changes.
As pasted, Aurora satisfies none of these.

## Recommendation

Do not adopt. Confirm D-024 at the sync and move to the business side.
If the founders genuinely want one more research program, commission a
scoped D-025 on the feasible subset only — knowing it concerns perps
(personal-account territory, not the business) and that the recorded
evidence says the founders currently hold no demonstrated edge even in
unleveraged spot. Counsel: the pattern of same-day pivots driven by
external prompts is itself the biggest current risk to this project's
one proven asset — that its decisions, once made, bind.
