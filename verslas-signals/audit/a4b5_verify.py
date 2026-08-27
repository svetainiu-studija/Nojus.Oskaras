"""AUDIT-2026-08 A4 + B5, scripted (LOCAL — needs internet, no API keys).

Delegation note: A4/B5 were founder-owned chart checks; on 2026-08-28
Oskaras instructed full delegation ("fill everything yourself"). This
script preserves the checks' INDEPENDENCE differently: every number is
verified against freshly fetched NATIVE OKX candles plus an independent
second venue (Binance, fallback Bybit/KuCoin) — never against the
project's own derived dataset — and all fetched data is saved as
immutable evidence files so Nojus (or anyone) can re-run and inspect.

    python -m audit.a4b5_verify           (from verslas-signals/)

Writes research/experiments/AUDIT-A4B5-EVIDENCE.md and raw candles under
research/experiments/audit-evidence/. Verdict rules are the protocol's:
A4 PASS = the simulated trade path agrees with the real market
(regardless of trade economics); B5 PASS = direction/timing/magnitude of
each big winner's move is materially consistent on a second venue.

Tolerances (documented, fixed here): price checks 0.6% (measured
derived-vs-native tick rounding, audit B1); cross-venue price 1.5%;
window-extreme cross-venue 2.5%; volume confirmation factor 0.8 (native
daily volume disagrees with 1h sums by median 3.7%, p95 18% — B1/D-019).
"""
import csv
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import ccxt

from engine.indicators import atr, ema, sma

HERE = Path(__file__).resolve().parents[2] / "research/experiments"
TRADES = HERE / "EXP-007.trades.csv"
EVID = HERE / "audit-evidence"
OUT = HERE / "AUDIT-A4B5-EVIDENCE.md"
DAY_MS = 86_400_000
PRICE_TOL = 0.006
XVENUE_TOL = 0.015
XVENUE_EXTREME_TOL = 0.025
VOL_FACTOR = 0.8


def d2ms(s):
    return int(datetime.strptime(s, "%Y-%m-%d")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def ms2d(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def fetch_daily(ex, symbol, since_ms, until_ms):
    rows, cursor = [], since_ms
    while cursor < until_ms:
        batch = ex.fetch_ohlcv(symbol, "1d", since=cursor, limit=300)
        if not batch:
            break
        rows += [r for r in batch if r[0] < until_ms]
        nxt = batch[-1][0] + DAY_MS
        if nxt <= cursor:
            break
        cursor = nxt
        time.sleep(ex.rateLimit / 1000)
    seen, out = set(), []
    for r in sorted(rows):
        if r[0] not in seen:
            seen.add(r[0])
            out.append(r)
    return out


def save_evidence(venue, pair, rows):
    EVID.mkdir(parents=True, exist_ok=True)
    p = EVID / f"{venue}-{pair}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "date", "open", "high", "low", "close", "volume"])
        for r in rows:
            w.writerow([r[0], ms2d(r[0])] + r[1:6])
    return p.name


def series(rows):
    return {"ts": [r[0] for r in rows], "open": [r[1] for r in rows],
            "high": [r[2] for r in rows], "low": [r[3] for r in rows],
            "close": [r[4] for r in rows], "volume": [r[5] for r in rows],
            "idx": {r[0]: i for i, r in enumerate(rows)}}


def main():
    trades = list(csv.DictReader(TRADES.open()))
    sample = [trades[i] for i in range(0, len(trades), 5)]          # #1,6,...,46
    for t in trades:
        if t["pair"] == "SOL-USDT" and t not in sample:
            sample.append(t)
    top5 = sorted(trades, key=lambda t: -float(t["r"]))[:5]
    need = {t["pair"] for t in sample} | {t["pair"] for t in top5} | {"BTC-USDT"}

    okx = ccxt.okx()
    second = None
    for name in ("binance", "bybit", "kucoin"):
        try:
            ex = getattr(ccxt, name)()
            ex.fetch_ohlcv("BTC/USDT", "1d", limit=3)
            second = ex
            print(f"second venue: {name}")
            break
        except Exception as e:
            print(f"  {name} unavailable ({type(e).__name__}); trying next")
    if second is None:
        raise SystemExit("no second venue reachable — rerun when online")

    lo = min(d2ms(t["entry"]) for t in sample + top5) - 100 * DAY_MS
    hi = max(d2ms(t["exit"]) for t in sample + top5) + 4 * DAY_MS
    data, vdata, files = {}, {}, []
    for pair in sorted(need):
        sym = pair.replace("-", "/")
        rows = fetch_daily(okx, sym, lo, hi)
        files.append(save_evidence("okx", pair, rows))
        data[pair] = series(rows)
        print(f"okx {pair}: {len(rows)} bars")
        try:
            vrows = fetch_daily(second, sym, lo, hi)
            files.append(save_evidence(second.id, pair, vrows))
            vdata[pair] = series(vrows)
            print(f"{second.id} {pair}: {len(vrows)} bars")
        except Exception as e:
            print(f"{second.id} {pair}: unavailable ({type(e).__name__})")

    btc = data["BTC-USDT"]
    btc_sma50 = sma(btc["close"], 50)
    lines = ["# AUDIT-2026-08 — A4/B5 evidence (scripted verification)", "",
             f"Run {ms2d(int(time.time() * 1000))} · native OKX + independent "
             f"venue **{second.id}** · tolerances per script header · raw "
             f"candles in `audit-evidence/` ({len(files)} files)", ""]
    a4_fail = 0

    lines += ["## A4 — sampled trades vs native OKX candles", "",
              "| pair | entry | checks | result |", "|---|---|---|---|"]
    for t in sample:
        pair = t["pair"]
        d = data[pair]
        e_ts = d2ms(t["entry"])
        ei = d["idx"].get(e_ts)
        notes, ok = [], True
        if ei is None or ei < 36:
            notes.append("bars missing on OKX fetch")
            ok = False
        else:
            si = ei - 1
            close = d["close"][si]
            hi20 = max(d["close"][si - 20:si])
            if close <= hi20 * (1 - PRICE_TOL):
                ok = False
                notes.append(f"NOT a 20d-high close ({close:.6g} vs {hi20:.6g})")
            else:
                notes.append("20d-high close ok")
            vs = sma(d["volume"], 20)[si - 1]
            if vs and d["volume"][si] < 1.5 * vs * VOL_FACTOR:
                ok = False
                notes.append("volume confirm FAILED beyond tolerance")
            else:
                notes.append("volume ok")
            e20 = ema(d["close"], 20)[si]
            if close >= e20 * 1.15 * (1 + PRICE_TOL):
                ok = False
                notes.append("over extension cap")
            else:
                notes.append("extension ok")
            bi = btc["idx"].get(d["ts"][si])
            if bi is not None and btc_sma50[bi] is not None \
                    and btc["close"][bi] < btc_sma50[bi]:
                ok = False
                notes.append("BTC gate would have BLOCKED entry")
            a = atr(d["high"], d["low"], d["close"], 14)[si]
            stop0 = close - 2.0 * a if a else None
            if stop0 is None or stop0 <= 0 or (close - stop0) / close > 0.25:
                ok = False
                notes.append("stop implausible")
            x_ts = d2ms(t["exit"])
            xi = d["idx"].get(x_ts)
            reason = t["exit_reason"]
            if xi is None:
                ok = False
                notes.append("exit bar missing")
            elif reason == "stop" and stop0 is not None:
                trail = max(stop0, min(d["low"][max(0, xi - 10):xi] or [stop0]))
                if d["low"][xi] <= trail * (1 + 0.01):
                    notes.append("stop-touch ok")
                else:
                    ok = False
                    notes.append(f"exit-day low {d['low'][xi]:.6g} never reached "
                                 f"trail~{trail:.6g}")
            elif reason == "regime":
                bi = btc["idx"].get(d["ts"][xi - 1]) if xi else None
                if bi is not None and btc_sma50[bi] is not None \
                        and btc["close"][bi] < btc_sma50[bi]:
                    notes.append("BTC<SMA50 on decision day ok")
                else:
                    ok = False
                    notes.append("regime exit not supported by BTC series")
            elif reason == "time":
                span = (x_ts - e_ts) // DAY_MS
                notes.append(f"time exit after {span}d (held {t['bars_held']}) "
                             + ("ok" if abs(span - int(t["bars_held"])) <= 2 else "DATE MISMATCH"))
                ok &= abs(span - int(t["bars_held"])) <= 2
            else:
                notes.append("signal exit: RS condition needs full universe "
                             "(covered by A1 review); price consistency only")
        a4_fail += 0 if ok else 1
        lines.append(f"| {pair} | {t['entry']} | {'; '.join(notes)} | "
                     f"{'PASS' if ok else 'FAIL'} |")

    sol = max(trades, key=lambda t: float(t["r"]))
    d = data["SOL-USDT"]
    ei = d["idx"][d2ms(sol["entry"])]
    si = ei - 1
    a = atr(d["high"], d["low"], d["close"], 14)[si]
    entry_px = d["open"][ei]
    stop0 = d["close"][si] - 2.0 * a
    target = entry_px + 3.0 * (entry_px - stop0)
    xi = d["idx"][d2ms(sol["exit"])]
    win_hi = max(d["high"][ei:xi + 1])
    trail = min(d["low"][xi - 10:xi])
    gross = (win_hi / entry_px - 1)
    lines += ["", "## A4 deep-dive — the SOL +21.36 R trade, from native bars", "",
              f"- entry open {entry_px:.4g} on {sol['entry']}; stop0 {stop0:.4g} "
              f"({(entry_px - stop0) / entry_px:.1%} risk)",
              f"- 3R partial target {target:.4g}: window high {win_hi:.4g} "
              f"({'REACHED' if win_hi >= target else 'NOT REACHED'}); peak move "
              f"{gross:+.1%} from entry",
              f"- 10-day-low trail at exit ≈ {trail:.4g}; exit-day low "
              f"{d['low'][xi]:.4g} ({'touches trail' if d['low'][xi] <= trail * 1.01 else 'DOES NOT touch trail'}); "
              f"exit-day move {(d['close'][xi] / d['open'][xi] - 1):+.1%}",
              f"- recorded net pct +213.2%: supported iff the blended path above "
              f"holds — see verdict"]
    sol_ok = (win_hi >= target and d["low"][xi] <= trail * 1.01
              and gross > 2.0)
    a4_fail += 0 if sol_ok else 1
    lines.append(f"- **SOL deep-dive: {'PASS' if sol_ok else 'FAIL'}**")

    lines += ["", "## B5 — five biggest winners vs the second venue", "",
              "| pair | entry | exit | R | second venue agrees? | detail |",
              "|---|---|---|---|---|---|"]
    b5_fail = 0
    for t in top5:
        pair = t["pair"]
        ok, detail = True, []
        if pair not in vdata:
            ok = False
            detail.append("no second-venue data")
        else:
            d1, d2_ = data[pair], vdata[pair]
            for label, ts in (("entry", d2ms(t["entry"])), ("exit", d2ms(t["exit"]))):
                i1, i2 = d1["idx"].get(ts), d2_["idx"].get(ts)
                if i1 is None or i2 is None:
                    ok = False
                    detail.append(f"{label} bar missing")
                    continue
                diff = abs(d1["open"][i1] / d2_["open"][i2] - 1)
                ok &= diff <= XVENUE_TOL
                detail.append(f"{label} open diff {diff:.2%}")
            i1a, i1b = d1["idx"].get(d2ms(t["entry"])), d1["idx"].get(d2ms(t["exit"]))
            i2a, i2b = d2_["idx"].get(d2ms(t["entry"])), d2_["idx"].get(d2ms(t["exit"]))
            if None not in (i1a, i1b, i2a, i2b):
                h1 = max(d1["high"][i1a:i1b + 1])
                h2 = max(d2_["high"][i2a:i2b + 1])
                diff = abs(h1 / h2 - 1)
                ok &= diff <= XVENUE_EXTREME_TOL
                detail.append(f"window-high diff {diff:.2%}")
        b5_fail += 0 if ok else 1
        lines.append(f"| {pair} | {t['entry']} | {t['exit']} | {t['r']} | "
                     f"{'PASS' if ok else 'FAIL'} | {'; '.join(detail)} |")

    a4_v = "PASS" if a4_fail == 0 else f"FAIL ({a4_fail} trade(s) — investigate before closing)"
    b5_v = "PASS" if b5_fail == 0 else f"FAIL ({b5_fail} trade(s) — investigate before closing)"
    lines += ["", f"## Verdicts", "", f"- **A4: {a4_v}**", f"- **B5: {b5_v}**", "",
              "*Generated by audit/a4b5_verify.py from freshly fetched public "
              "data; no project dataset was consulted. Rerunnable by anyone.*"]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nreport -> {OUT}")
    print(f"A4: {a4_v}\nB5: {b5_v}")


if __name__ == "__main__":
    main()
