"""Point-in-time research universe (v1) from daily bars.

Usage:  python3 -m engine.universe data/raw/okx/1d --top 30 --out data/universe.csv

For each day: a pair is ELIGIBLE if its listing age is >= --min-age-days
(counted from its first bar) and it has accumulated >= --min-bars daily bars.
Its score is the trailing --window-bar sum of close*volume (approximate quote
volume). in_universe = the top --top eligible pairs by score that day.

Outputs a long CSV: date,symbol,rank,score,in_universe — the membership table
strategies must join against (never "the pair exists in the dataset").
Also prints the ALWAYS-IN-UNIVERSE subset (pairs in the top N on every day
they were eligible) — the mandatory sensitivity run from the hypotheses.

v1 limitation, stated loudly: the candidate set is the ~30 downloaded pairs,
which is a PRESENT-DAY snapshot — coins that died before today are absent, so
survivorship bias is reduced (listing-age + point-in-time ranking) but not
eliminated. v2 fix: widen the candidate set and add delisted pairs from an
external source.
"""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

DAY_MS = 86_400_000


def load_daily(path: Path):
    rows = []
    with path.open() as f:
        for r in csv.reader(f):
            if r and r[0] != "timestamp":
                rows.append((int(r[0]), float(r[4]), float(r[5])))  # ts, close, volume
    rows.sort(key=lambda x: x[0])
    return rows


def compute_universe(data, top, window_bars, min_age_days, min_bars):
    """data: {symbol: [(ts, close, volume), ...]} daily, sorted.

    Returns (rows, always_in) where rows = [(ts, symbol, rank, score, in_universe)],
    ranked per day, and always_in = sorted list of symbols in the top N on every
    day they were eligible.
    """
    per_symbol = {}
    for sym, rows in data.items():
        if not rows:
            continue
        first_ts = rows[0][0]
        scores = {}
        window = []
        running = 0.0
        for i, (ts, close, vol) in enumerate(rows):
            qv = close * vol
            window.append(qv)
            running += qv
            if len(window) > window_bars:
                running -= window.pop(0)
            age_ok = (ts - first_ts) >= min_age_days * DAY_MS
            bars_ok = (i + 1) >= min_bars
            if age_ok and bars_ok:
                scores[ts] = running
        per_symbol[sym] = scores

    all_days = sorted({ts for s in per_symbol.values() for ts in s})
    rows_out = []
    ever_eligible = set()
    dropped = set()  # eligible-but-not-in-universe at least once
    for ts in all_days:
        day_scores = [(sym, sc[ts]) for sym, sc in per_symbol.items() if ts in sc]
        day_scores.sort(key=lambda x: (-x[1], x[0]))
        for rank, (sym, score) in enumerate(day_scores, start=1):
            in_u = rank <= top
            rows_out.append((ts, sym, rank, score, in_u))
            ever_eligible.add(sym)
            if not in_u:
                dropped.add(sym)
    always_in = sorted(ever_eligible - dropped)
    return rows_out, always_in


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("daily_dir", help="directory of daily CSVs, e.g. data/raw/okx/1d")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--window-bars", type=int, default=90)
    ap.add_argument("--min-age-days", type=int, default=90)
    ap.add_argument("--min-bars", type=int, default=60)
    ap.add_argument("--out", default="data/universe.csv")
    args = ap.parse_args(argv)

    data = {p.stem: load_daily(p) for p in sorted(Path(args.daily_dir).glob("*.csv"))}
    rows, always_in = compute_universe(
        data, args.top, args.window_bars, args.min_age_days, args.min_bars)
    if not rows:
        raise SystemExit("no eligible pair-days — check the data directory")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "symbol", "rank", "score_quote_vol", "in_universe"])
        for ts, sym, rank, score, in_u in rows:
            d = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
            w.writerow([d, sym, rank, f"{score:.0f}", int(in_u)])

    days = len({r[0] for r in rows})
    syms = len({r[1] for r in rows})
    print(f"{days} days x {syms} ever-eligible pairs -> {out}")
    print(f"always-in-universe subset ({len(always_in)}): {', '.join(always_in)}")
    print("note: v1 candidate set is the downloaded pairs (present-day snapshot) — "
          "survivorship reduced, not eliminated; see module docstring")


if __name__ == "__main__":
    main()
