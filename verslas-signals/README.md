# verslas-signals — strategy research & engine scaffolding

Scaffolding for tasks 0.9–0.10 (data pipeline, dataset versioning, cost model). Lives here temporarily; it will be split into the private strategy repo when that is created. **No secrets ever go in this folder** — public market data and code only.

## Quickstart (run locally — exchange APIs are not reachable from the Claude cloud workspace)

Requires Python 3.10+ and Git.

**Windows (PowerShell)** — run the lines one at a time (older PowerShell doesn't accept `&&`):

```powershell
cd $HOME\Documents
git clone https://github.com/svetainiu-studija/Nojus.Oskaras.git   # first time only; later just: git pull
cd Nojus.Oskaras\verslas-signals
pip install -r requirements.txt
python run.py
```

**Mac/Linux:**

```bash
cd verslas-signals
make deps     # install python dependencies (ccxt, pyyaml)
make data     # download OHLCV + write a versioned dataset manifest (same as: python3 run.py)
make check    # data-quality report
make test     # unit tests (no network needed)
```

The first download takes a while (thousands of paginated requests, rate-limited). It is safe to interrupt and rerun — it resumes. When it finishes, commit the manifest:

```powershell
git add data
git commit -m "Add first dataset manifest"
git push
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
