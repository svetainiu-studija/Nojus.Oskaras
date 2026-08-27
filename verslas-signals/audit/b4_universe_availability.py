"""AUDIT-2026-08 B4: availability-vs-strategy check, from committed files only.

Verifies from data/universe.csv and the derived dataset manifest that no
pair is ever in-universe before (its first bar + 90 days) — i.e. the
listing-age filter genuinely held and no pair was treated specially by
data availability. Stdlib only, no engine imports.

    python -m audit.b4_universe_availability      (from verslas-signals/)
"""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
UNIVERSE = HERE / "data/universe.csv"
MANIFEST = HERE / "data/DATASET-8b092d267524.json"   # derived (canonical)
DAY_MS = 86_400_000
LISTING_AGE_DAYS = 90


def day(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def main():
    manifest = json.loads(MANIFEST.read_text())
    first_bar = {}
    for key, info in manifest["files"].items():
        parts = key.replace("\\", "/").split("/")
        if len(parts) == 3 and parts[1] == "1d":
            first_bar[parts[2].removesuffix(".csv")] = info["first_ts"]

    first_member = {}
    with UNIVERSE.open() as f:
        for row in csv.DictReader(f):
            if row["in_universe"] == "1":
                sym = row["symbol"]
                if sym not in first_member or row["date"] < first_member[sym]:
                    first_member[sym] = row["date"]

    violations = []
    print(f"{'pair':<14} {'first bar':>10} {'eligible from':>13} {'first member':>13}")
    for sym in sorted(first_member):
        if sym not in first_bar:
            violations.append((sym, "in universe.csv but not in the derived manifest"))
            continue
        eligible = day(first_bar[sym] + LISTING_AGE_DAYS * DAY_MS)
        fm = first_member[sym]
        flag = ""
        if fm < eligible:
            flag = "  <-- VIOLATION"
            violations.append((sym, f"member {fm} before eligible {eligible}"))
        print(f"{sym:<14} {day(first_bar[sym]):>10} {eligible:>13} {fm:>13}{flag}")

    never = sorted(set(first_bar) - set(first_member))
    if never:
        print(f"\npairs with bars but never in-universe ({len(never)}): "
              f"{', '.join(never)}")
    if violations:
        print(f"\nB4 verdict: {len(violations)} VIOLATION(S) — verified-error candidate:")
        for sym, why in violations:
            print(f"  {sym}: {why}")
        return 1
    print("\nB4 verdict: PASS — no pair was in-universe before first bar + "
          f"{LISTING_AGE_DAYS} days")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
