"""Dataset versioning: hash every CSV under a root into DATASET-<id>.json.

Usage:  python3 -m engine.data.manifest data/raw --config pairs.yaml

The dataset id is the first 12 hex chars of the sha256 of the manifest's
file-hash section, so the same data always yields the same id, and any
changed, added, or removed file yields a new one. Every experiment report
must cite the DATASET-<id> it ran on.
"""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def file_entry(path: Path) -> dict:
    h = hashlib.sha256()
    rows = 0
    first_ts = last_ts = None
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    with path.open() as f:
        for row in csv.reader(f):
            if not row or row[0] == "timestamp":
                continue
            rows += 1
            ts = int(row[0])
            first_ts = ts if first_ts is None else min(first_ts, ts)
            last_ts = ts if last_ts is None else max(last_ts, ts)
    return {"sha256": h.hexdigest(), "rows": rows, "first_ts": first_ts, "last_ts": last_ts}


def build_manifest(root: Path) -> dict:
    files = {}
    for path in sorted(root.rglob("*.csv")):
        # as_posix() keeps manifest keys (and thus dataset ids) identical
        # across Windows and Unix machines
        files[path.relative_to(root).as_posix()] = file_entry(path)
    return {"files": files}


def dataset_id(manifest: dict) -> str:
    canon = json.dumps(manifest["files"], sort_keys=True).encode()
    return hashlib.sha256(canon).hexdigest()[:12]


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", help="data root to hash, e.g. data/raw")
    ap.add_argument("--config", default=None, help="config file to embed for provenance")
    args = ap.parse_args(argv)

    root = Path(args.root)
    manifest = build_manifest(root)
    if not manifest["files"]:
        raise SystemExit(f"no CSV files under {root}")
    manifest["dataset_id"] = dataset_id(manifest)
    manifest["root"] = str(root)
    manifest["generated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if args.config:
        manifest["config"] = Path(args.config).read_text()

    out = root.parent / f"DATASET-{manifest['dataset_id']}.json"
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    print(f"{len(manifest['files'])} files -> {out}")


if __name__ == "__main__":
    main()
