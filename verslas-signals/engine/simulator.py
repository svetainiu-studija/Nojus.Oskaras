"""Portfolio-level daily backtest simulator.

Execution semantics (matching the hypotheses and CHARTER §5):
- Decisions are made at bar close; fills happen at the NEXT bar's open,
  paying the cost model's one-way fraction each way.
- A hard stop is a CLOSE below the stop level -> exit at the next open
  (spot: no intrabar guarantees).
- The 2R partial is a resting limit sell: filled intrabar when the bar's
  high touches the target, at the target price.
- Zero-volume bars are non-tradable (D-019): fills scheduled onto one are
  postponed to the next tradable open; nothing is ever filled on them.
- D-015 caps: risk 1% of current equity per trade, max 6 concurrent
  positions, 6% portfolio heat (sum of open initial-risk fractions), and at
  most 2 held positions whose 30-day return correlation with the candidate
  exceeds 0.8.

The simulator is strategy-agnostic: a strategy object exposes
on_close(sim, pair, i) -> EntryIntent | None, called once per pair per bar
close; exits are governed by the per-strategy ExitPolicy.
"""
from dataclasses import dataclass

from .protocol import (RISK_PER_TRADE, MAX_POSITIONS, HEAT_CAP,
                       CORR_WINDOW, CORR_LIMIT, CORR_MAX_POSITIONS,
                       fold_of, regime_of)


@dataclass
class EntryIntent:
    pair: str
    stop_px: float          # initial hard stop (absolute price)
    signal_i: int           # pair-local index of the signal close
    partial_px: float = None  # optional absolute partial target; the fill
                              # price becomes min(policy 2R target, this)
                              # when it sits above the entry


@dataclass
class ExitPolicy:
    partial_frac: float = 0.5     # fraction sold at partial_r
    partial_r: float = 2.0        # R-multiple of the resting limit target
    trail_lookback: int = 10      # trail stop at N-day low (after partial fill)
    time_stop_bars: int = 10      # exit at market after N bars
    regime_exit: bool = True      # flatten when BTC closes below its SMA50
    stop_mode: str = "close_confirm"  # or "resting_stop" (fills at the level
                                      # when the bar's low touches it; at the
                                      # open if the bar gaps through)
    trail_mode: str = "after_partial"  # or "after_r": trail once max
                                       # unrealised R >= trail_after_r
    trail_after_r: float = 1.0
    time_stop_skip_if_r: float = None  # skip the time stop if the trade has
                                       # ever reached this unrealised R


class Position:
    def __init__(self, pair, units, entry_px, stop_px, risk_amount,
                 risk_frac, entry_ts, regime):
        self.pair = pair
        self.units = units                # remaining units
        self.units0 = units
        self.entry_px = entry_px
        self.stop = stop_px
        self.stop0 = stop_px
        self.risk_amount = risk_amount    # equity units at risk initially
        self.risk_frac = risk_frac        # fraction of equity at entry
        self.entry_ts = entry_ts
        self.regime = regime
        self.bars_held = 0
        self.half_taken = False
        self.max_r = 0.0                  # best unrealised R seen at a close
        self.cash_flow = 0.0              # net cash from fills (incl. entry)


class Simulator:
    """data: {pair: {"ts": [...], "open": [...], "high": [...], "low": [...],
                     "close": [...], "volume": [...]}} — daily, chronological.
    universe: set of (ts_ms, pair) that are in-universe that day.
    btc_ctx: {"ts_index": {ts: i}, "close": [...], "sma50": [...], "sma200": [...]}
    cost_fn: pair -> one-way cost fraction.
    """

    def __init__(self, data, universe, btc_ctx, cost_fn, strategy, policy,
                 start_equity=10_000.0, research_range=None, btc_entry_gate=True,
                 max_positions=MAX_POSITIONS):
        self.btc_entry_gate = btc_entry_gate
        self.max_positions = min(max_positions, MAX_POSITIONS)
        self.data = data
        self.universe = universe
        self.btc = btc_ctx
        self.cost_fn = cost_fn
        self.strategy = strategy
        self.policy = policy
        self.cash = start_equity
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.skips = {"slots": 0, "heat": 0, "corr": 0, "zero_volume": 0,
                      "stop_wide": 0}
        self.pending_entries = []   # (intent, sized at schedule time close)
        self.pending_exits = []     # (pair, reason)
        self.ts_index = {p: {ts: i for i, ts in enumerate(d["ts"])}
                         for p, d in data.items()}
        all_ts = sorted({ts for d in data.values() for ts in d["ts"]})
        if research_range:
            lo, hi = research_range
            all_ts = [t for t in all_ts if lo <= t < hi]
        self.calendar = all_ts
        # daily simple returns per pair, for the correlation cap
        self.returns = {}
        for p, d in data.items():
            rs = [None]
            for i in range(1, len(d["close"])):
                prev = d["close"][i - 1]
                rs.append(d["close"][i] / prev - 1.0 if prev else None)
            self.returns[p] = rs

    # ----- helpers -------------------------------------------------------
    def bar(self, pair, ts):
        i = self.ts_index[pair].get(ts)
        if i is None:
            return None, None
        return i, self.data[pair]

    def mark_equity(self, ts):
        total = self.cash
        for p, pos in self.positions.items():
            i, d = self.bar(p, ts)
            px = d["close"][i] if i is not None else pos.entry_px
            total += pos.units * px
        return total

    def heat(self):
        return sum(p.risk_frac for p in self.positions.values())

    def corr30(self, pair_a, pair_b, ts):
        ia = self.ts_index[pair_a].get(ts)
        ib = self.ts_index[pair_b].get(ts)
        if ia is None or ib is None:
            return 0.0
        ra = [x for x in self.returns[pair_a][max(1, ia - CORR_WINDOW + 1):ia + 1]
              if x is not None]
        rb = [x for x in self.returns[pair_b][max(1, ib - CORR_WINDOW + 1):ib + 1]
              if x is not None]
        n = min(len(ra), len(rb))
        if n < 10:
            return 0.0
        ra, rb = ra[-n:], rb[-n:]
        ma, mb = sum(ra) / n, sum(rb) / n
        cov = sum((a - ma) * (b - mb) for a, b in zip(ra, rb))
        va = sum((a - ma) ** 2 for a in ra)
        vb = sum((b - mb) ** 2 for b in rb)
        if va == 0 or vb == 0:
            return 0.0
        return cov / (va ** 0.5 * vb ** 0.5)

    def btc_at(self, ts):
        i = self.btc["ts_index"].get(ts)
        if i is None:
            return None
        return i

    # ----- fills ---------------------------------------------------------
    def _fill_exit(self, pair, px, ts, units=None, reason=None):
        pos = self.positions[pair]
        qty = pos.units if units is None else units
        cost = self.cost_fn(pair)
        self.cash += qty * px * (1.0 - cost)
        pos.cash_flow += qty * px * (1.0 - cost)
        pos.units -= qty
        if pos.units <= 1e-12:
            r = pos.cash_flow / pos.risk_amount
            self.trades.append({
                "pair": pair, "entry_ts": pos.entry_ts, "exit_ts": ts,
                "r": r, "bars_held": pos.bars_held, "regime": pos.regime,
                "fold": fold_of(pos.entry_ts),
                "pct": pos.cash_flow / (pos.units0 * pos.entry_px),
                "exit_reason": reason or "unknown",
                "took_partial": pos.half_taken,
            })
            del self.positions[pair]

    # ----- main loop -----------------------------------------------------
    def run(self):
        for ts in self.calendar:
            self._process_opens(ts)
            self._process_intrabar(ts)
            self._process_close(ts)
            self.equity_curve.append(self.mark_equity(ts))
        return self

    def _tradable(self, pair, ts):
        i, d = self.bar(pair, ts)
        return i is not None and d["volume"][i] > 0

    def _process_opens(self, ts):
        # exits first: they free slots and heat
        still_pending = []
        for pair, reason in self.pending_exits:
            if pair not in self.positions:
                continue
            if not self._tradable(pair, ts):
                still_pending.append((pair, reason))  # postpone (D-019)
                continue
            i, d = self.bar(pair, ts)
            self._fill_exit(pair, d["open"][i], ts, reason=reason)
        self.pending_exits = still_pending

        still_entries = []
        for intent, units, risk_amount, risk_frac, regime in self.pending_entries:
            pair = intent.pair
            if pair in self.positions:
                continue
            if not self._tradable(pair, ts):
                self.skips["zero_volume"] += 1
                continue  # cancel: the setup's price basis is stale
            # re-verify caps at fill time (exits above may have freed room)
            if len(self.positions) >= self.max_positions:
                self.skips["slots"] += 1
                continue
            if self.heat() + risk_frac > HEAT_CAP + 1e-12:
                self.skips["heat"] += 1
                continue
            i, d = self.bar(pair, ts)
            px = d["open"][i]
            if px <= intent.stop_px:
                continue  # gapped through the stop before entry: no trade
            cost = self.cost_fn(pair)
            self.cash -= units * px * (1.0 + cost)
            pos = Position(pair, units, px, intent.stop_px, risk_amount,
                           risk_frac, ts, regime)
            pos.cash_flow = -units * px * (1.0 + cost)
            target_2r = px + self.policy.partial_r * (px - intent.stop_px)
            if intent.partial_px is not None and intent.partial_px > px:
                pos.partial_px = min(target_2r, intent.partial_px)
            else:
                pos.partial_px = target_2r
            self.positions[pair] = pos
        self.pending_entries = still_entries

    def _process_intrabar(self, ts):
        for pair, pos in list(self.positions.items()):
            i, d = self.bar(pair, ts)
            if i is None or d["volume"][i] <= 0:
                continue
            # resting stop order: conservative ordering — if both the stop and
            # the partial target sit inside one bar, the stop is assumed first
            if self.policy.stop_mode == "resting_stop":
                if d["open"][i] <= pos.stop:
                    self._fill_exit(pair, d["open"][i], ts, reason="stop")
                    continue
                if d["low"][i] <= pos.stop:
                    self._fill_exit(pair, pos.stop, ts, reason="stop")
                    continue
            if self.policy.partial_frac <= 0 or pos.half_taken:
                continue
            target = getattr(pos, "partial_px", None)
            if target is None:
                target = pos.entry_px + self.policy.partial_r * (pos.entry_px - pos.stop0)
            if d["high"][i] >= target:
                qty = pos.units0 * self.policy.partial_frac
                self._fill_exit(pair, target, ts, units=min(qty, pos.units),
                                reason="partial")
                if pair in self.positions:
                    self.positions[pair].half_taken = True

    def _process_close(self, ts):
        bi = self.btc_at(ts)
        btc_bearish = False
        regime = "warmup"
        if bi is not None:
            c = self.btc["close"][bi]
            s50 = self.btc["sma50"][bi]
            s200 = self.btc["sma200"][bi]
            regime = regime_of(c, s50, s200)
            btc_bearish = s50 is not None and c < s50

        # manage open positions
        for pair, pos in list(self.positions.items()):
            i, d = self.bar(pair, ts)
            if i is None:
                continue
            pos.bars_held += 1
            close = d["close"][i]
            risk_px = pos.entry_px - pos.stop0
            if risk_px > 0:
                pos.max_r = max(pos.max_r, (close - pos.entry_px) / risk_px)
            trail_on = (pos.half_taken if self.policy.trail_mode == "after_partial"
                        else pos.max_r >= self.policy.trail_after_r)
            if trail_on and i >= self.policy.trail_lookback:
                trail = min(d["low"][i - self.policy.trail_lookback + 1:i + 1])
                pos.stop = max(pos.stop, trail)
            time_due = (pos.bars_held >= self.policy.time_stop_bars
                        and (self.policy.time_stop_skip_if_r is None
                             or pos.max_r < self.policy.time_stop_skip_if_r))
            if self.policy.stop_mode == "close_confirm" and close < pos.stop:
                self.pending_exits.append((pair, "stop"))
            elif time_due:
                self.pending_exits.append((pair, "time"))
            elif self.policy.regime_exit and btc_bearish:
                self.pending_exits.append((pair, "regime"))
            else:
                wants = getattr(self.strategy, "wants_exit", None)
                if wants is not None and wants(self, pair, i, ts):
                    self.pending_exits.append((pair, "signal"))

        # new entries (blocked while BTC is below its SMA50, unless ablated)
        if btc_bearish and self.btc_entry_gate:
            return
        exiting = {p for p, _ in self.pending_exits}
        for pair in self.data:
            if pair in self.positions or pair in exiting:
                continue
            i = self.ts_index[pair].get(ts)
            if i is None:
                continue
            intent = self.strategy.on_close(self, pair, i, ts)
            if intent is None:
                continue
            equity = self.mark_equity(ts)
            close = self.data[pair]["close"][i]
            stop_frac = (close - intent.stop_px) / close
            if stop_frac <= 0 or stop_frac > self.strategy.max_stop_frac:
                self.skips["stop_wide"] += 1
                continue
            if len(self.positions) + sum(1 for e in self.pending_entries
                                         if e[0].pair != pair) >= self.max_positions:
                self.skips["slots"] += 1
                continue
            risk_frac = RISK_PER_TRADE
            if self.heat() + risk_frac > HEAT_CAP + 1e-12:
                self.skips["heat"] += 1
                continue
            held_pairs = list(self.positions) + \
                [e[0].pair for e in self.pending_entries]
            correlated = sum(1 for held in held_pairs
                             if self.corr30(pair, held, ts) > CORR_LIMIT)
            if correlated >= CORR_MAX_POSITIONS:
                self.skips["corr"] += 1
                continue
            risk_amount = equity * RISK_PER_TRADE
            units = risk_amount / (close - intent.stop_px)
            self.pending_entries.append((intent, units, risk_amount, risk_frac,
                                         regime))
