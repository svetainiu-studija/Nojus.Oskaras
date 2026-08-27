"""Download spot OHLCV history via ccxt public endpoints (no API keys).

Usage:  python3 -m engine.data.download --config pairs.yaml --out data/raw

Writes one CSV per pair/timeframe: data/raw/<exchange>/<timeframe>/<PAIR>.csv
with header timestamp,open,high,low,close,volume (timestamp = ms since epoch, UTC).
Idempotent: an existing file is resumed from its last timestamp; pass --force
to refetch a file from scratch.
"""
import argparse
import csv
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .timeframes import TIMEFRAME_MS

BATCH_LIMIT = 300          # bars per request; ccxt clamps to each exchange's max
MAX_RETRIES = 5


def parse_since(s: str) -> int:
    dt = datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def last_timestamp(path: Path) -> int | None:
    if not path.exists():
        return None
    last = None
    with path.open() as f:
        for row in csv.reader(f):
            if row and row[0] != "timestamp":
                last = int(row[0])
    return last


def fetch_pair(exchange, symbol: str, timeframe: str, since_ms: int, out_path: Path) -> int:
    """Append bars from since_ms onward; returns number of bars written."""
    tf_ms = TIMEFRAME_MS[timeframe]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not out_path.exists()
    written = 0
    cursor = since_ms
    now_ms = int(time.time() * 1000)

    with out_path.open("a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        while cursor < now_ms:
            batch = None
            for attempt in range(MAX_RETRIES):
                try:
                    batch = exchange.fetch_ohlcv(symbol, timeframe, since=cursor, limit=BATCH_LIMIT)
                    break
                except Exception as e:  # network hiccups, rate limits
                    wait = 2 ** attempt
                    print(f"    retry {attempt + 1}/{MAX_RETRIES} in {wait}s ({e})", file=sys.stderr)
                    time.sleep(wait)
            if batch is None:
                raise RuntimeError(f"{symbol} {timeframe}: giving up after {MAX_RETRIES} retries")
            # keep only complete, strictly-forward bars
            rows = [b for b in batch if b[0] >= cursor and b[0] + tf_ms <= now_ms]
            if not rows:
                break
            for ts, o, h, l, c, v in rows:
                writer.writerow([ts, o, h, l, c, v])
                written += 1
            cursor = rows[-1][0] + tf_ms
            if len(batch) < 2:  # exchange returned a final sliver
                break
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="pairs.yaml")
    ap.add_argument("--out", default="data/raw")
    ap.add_argument("--force", action="store_true", help="refetch files from scratch")
    args = ap.parse_args()

    import ccxt  # imported here so `make test` needs no network deps

    cfg = yaml.safe_load(Path(args.config).read_text())
    ex_name = cfg["exchange"]
    exchange = getattr(ccxt, ex_name)({"enableRateLimit": True})
    since_default = parse_since(cfg["since"])
    out_root = Path(args.out) / ex_name

    total = 0
    for timeframe in cfg["timeframes"]:
        if timeframe not in TIMEFRAME_MS:
            raise SystemExit(f"unknown timeframe {timeframe!r}")
        for symbol in cfg["pairs"]:
            fname = symbol.replace("/", "-") + ".csv"
            path = out_root / timeframe / fname
            if args.force and path.exists():
                path.unlink()
            resume = last_timestamp(path)
            since = since_default if resume is None else resume + TIMEFRAME_MS[timeframe]
            print(f"{ex_name} {symbol} {timeframe}: fetching from "
                  f"{datetime.fromtimestamp(since / 1000, tz=timezone.utc):%Y-%m-%d} ...", flush=True)
            n = fetch_pair(exchange, symbol, timeframe, since, path)
            total += n
            print(f"    +{n} bars -> {path}")
    print(f"done: {total} new bars")


if __name__ == "__main__":
    main()
