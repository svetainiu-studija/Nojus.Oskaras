# verslas-signals — strategy research & engine scaffolding

Scaffolding for tasks 0.9–0.10 (data pipeline, dataset versioning, cost model). Lives here temporarily; it will be split into the private strategy repo when that is created. **No secrets ever go in this folder** — public market data and code only.

## Quickstart (run locally — exchange APIs are not reachable from the Claude cloud workspace)

```bash
cd verslas-signals
make deps     # install python dependencies (ccxt, pyyaml)
make data     # download ~4.5 years of spot OHLCV for the pairs in pairs.yaml, then write a versioned dataset manifest
make check    # data-quality report (gaps per file); non-zero exit if any file misses >2% of bars
make test     # unit tests (no network needed)
```

`make data` is idempotent — rerunning refreshes files and produces a new manifest. Every backtest must record the `DATASET-<id>` it ran on (protocol step 2).

## Layout

```
pairs.yaml      # research universe (draft ~30 liquid OKX spot pairs — final list is set by the liquidity rule before holdout lock)
costs.yaml      # cost model per exchange: fees, spread, slippage, delay, missed-fill rule (task 0.10 — values marked VERIFY need checking against live fee pages)
engine/data/
  download.py   # paginated OHLCV downloader (ccxt, public endpoints, no API keys)
  manifest.py   # dataset versioning: sha256 per file -> DATASET-<id>.json
  quality.py    # gap report
tests/          # unit tests
data/           # downloaded data (git-ignored); manifests are committed
```

## Status

- [x] Downloader, manifest, quality check written; manifest logic unit-tested
- [ ] First real download run (Oskaras, locally) → commit the first `DATASET-*.json`
- [ ] `costs.yaml` VERIFY values checked against live OKX/Kraken fee pages (task 0.10, Nojus reviews)
- [ ] Backtester (task 1.1) — starts after hypotheses are filed (`../research/hypotheses/`)
