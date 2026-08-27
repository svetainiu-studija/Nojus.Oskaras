# Project rules for Claude sessions (mirror of CHARTER §4 + research protocol)

Read `../CHARTER.md` (v1.2) and `../PLAN-90-DAYS.md` before any strategy work. These rules are binding in every session that touches this folder:

1. **Spot only.** The instrument universe contains no derivatives; never add perpetuals, margin, or CFDs to any config or backtest intended for publication.
2. **Chronological splits only.** Training → validation → walk-forward → final holdout. Holdout dates are written down before research starts and opened exactly once; reusing the holdout invalidates the candidate.
3. **Costs always.** Every result is net of the `costs.yaml` model (fees, spread, slippage, execution delay, missed fills, min order sizes); stress at 2× costs.
4. **Portfolio level.** Results measured across all pairs together under the D-015 limits: max drawdown 25%, per-trade risk ≤ 1% of equity, max 6 concurrent positions, heat cap ≤ 6%, no leverage.
5. **Baselines.** Every candidate is compared against BTC buy-and-hold (risk-adjusted) and a random-entry/same-exit Monte-Carlo baseline. Not beating both = market beta, not edge.
6. **Count every variant.** Every parameter set tried is recorded; holdout pass thresholds scale with the variant count.
7. **Builder ≠ approver.** The session that optimised a strategy never approves it; G0 review is an independent reproduction from raw data in a separate session.
8. **Dataset versioning.** Every experiment records its `DATASET-<id>`; `make data` must reproduce the dataset.
9. **No secrets.** No API keys, credentials, or personal data in this folder, ever. Public endpoints only.
10. **Experiment reports.** One page per experiment ID in `../research/experiments/` per the PLAN-90-DAYS template; nothing is called "working" without the report.
