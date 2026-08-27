# Decision point — end of the first hypothesis round (2026-08-28)

For: Oskaras & Nojus · From: the build sessions · Status: **needs the
founders' decision** (log it as D-021 when made)

## Where we stand

All three interview hypotheses were implemented faithfully, pre-registered,
and tested against 4.5 years of clean data (2021-01 → 2025-06; the last 14
months stay sealed). All three closed in **week 1 of the 12-week research
window**:

| Sprint | Hypothesis | Result | Root cause |
|---|---|---|---|
| A | HYP-001 pullback-to-EMA20 | Abandoned (best −0.04 R after execution fix) | Economics ~breakeven net of costs; winners capped by design, losses amplified by tight stops |
| B | HYP-002 RS breakout | Failed — 4 trades, unfalsifiable | Its own stop rule rejects 95% of its entries (leader breakouts sit >10% above the 10-day low) |
| C | HYP-003 capitulation reclaim | Failed — 1 trade in 4.5y | The compound setup essentially never occurs; reversals dropped for good |

**Nothing was lost except a week — and the week bought a lot:** a validated
research machine (data pipeline, audited dataset, portfolio backtester,
baselines, pre-registration discipline — 50 unit tests), plus five
transferable findings:

1. Your **regime filters work** (BTC>SMA50 + trend structure cut drawdown to
   a third in the ablation).
2. **Resting-stop execution** is worth ~+0.28 R/trade vs waiting for daily
   closes — locked in as the standard.
3. **Fixed-percentage stop caps are geometrically wrong for crypto** — they
   rejected 58–95% of signals and selected for the worst stops. Stops must
   scale with volatility (ATR) if any future hypothesis uses them.
4. **Time stops amputate the winners** trend styles depend on (+1.13 R mean
   on forced exits in EXP-001).
5. **Daily bars × 30 pairs is a low-frequency regime** — any strategy needs
   either intraday bars (we already have clean 4h/1h data) or a wider
   universe to reach G0's ≥200 trades.

## The decision

**Option A — one more pre-registered hypothesis round (recommended).**
Two candidates designed from the findings, not from hope:
- **HYP-004: cross-sectional momentum with ATR-scaled stops** (daily). Fixes
  HYP-002's geometry. Its 4 permitted trades were profitable and
  stress-robust, and momentum is the best-documented effect in crypto — the
  one idea our data hinted at rather than rejected.
- **HYP-005: the same, or the pullback family, on 4h bars** — 6× the bars,
  aimed squarely at the frequency problem.

Cost: roughly one week. Honest prior: most hypotheses fail; two more rounds
maximum before Option B applies regardless (the week-12 hard stop already
enforces this). Needed from the founders: sign-off, plus answers to the
mini-interview below.

**Option B — CHARTER §9 pivot discussion now.** Stop signal research; pivot
toward the software/tooling business (backtesting-as-a-product, the
research machine itself is demonstrably real). Legitimate, but premature at
week 1 of 12 with an obvious evidence-backed candidate untested.

**Option C — pause.** Also legitimate; the repo keeps everything.

## Mini-interview for Option A (answer in a message, 5 minutes)

1. ATR stops: comfortable with stops defined as k × ATR(14) below entry
   (k fixed a priori, e.g. 2), meaning the *distance varies* per trade while
   the *risk stays 1%*? (This is the fix for finding 3.)
2. 4h bars mean signals can fire at 04:00 — fine for a future automated
   engine, but paper/live mirroring becomes bot-only. Any objection?
3. Anything from your discretionary years the interview missed that you'd
   bet on now, knowing what the machine has shown?

## Recommendation

Option A, both hypotheses, pre-registered together, decision rule identical
to Sprint C's (30-trade floor included). If both fail → Option B discussion
with clean consciences and a working machine to pivot around.
