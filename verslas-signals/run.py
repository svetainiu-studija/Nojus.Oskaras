"""One-command data pipeline, cross-platform (Windows PowerShell included).

    pip install -r requirements.txt   # once
    python run.py                     # download -> manifest -> quality report

Safe to interrupt and rerun: the download resumes where it stopped.
Requires Python 3.10+.
"""
import sys

if sys.version_info < (3, 10):
    raise SystemExit(f"Python 3.10+ required, you have {sys.version.split()[0]} — "
                     "install from https://python.org and reopen the terminal.")

from engine.data import download, manifest, quality

if __name__ == "__main__":
    print("=== 1/3 downloading OHLCV (this can take a while on the first run) ===")
    download.main(["--config", "pairs.yaml", "--out", "data/raw"])
    print("\n=== 2/3 writing dataset manifest ===")
    manifest.main(["data/raw", "--config", "pairs.yaml"])
    print("\n=== 3/3 data-quality report ===")
    quality.main(["data/raw"])
