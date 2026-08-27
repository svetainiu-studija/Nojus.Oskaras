.PHONY: deps data check test

deps:
	pip install -r requirements.txt

data:
	python3 -m engine.data.download --config pairs.yaml --out data/raw
	python3 -m engine.data.manifest data/raw --config pairs.yaml

check:
	python3 -m engine.data.quality data/raw

audit:
	python3 -m engine.data.audit data/raw

universe:
	python3 -m engine.universe data/raw/okx/1d --out data/universe.csv

test:
	python3 -m unittest discover -s tests -v
