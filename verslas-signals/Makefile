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

derive:
	python3 -m engine.data.derive data/raw/okx/1h data/derived/okx
	python3 -m engine.data.manifest data/derived --config pairs.yaml

universe:
	python3 -m engine.universe data/derived/okx/1d --out data/universe.csv

exp001:
	python3 -m engine.experiment

exp003:
	python3 -m engine.exp003

exp004:
	python3 -m engine.exp004

test:
	python3 -m unittest discover -s tests -v
