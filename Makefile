.PHONY: install dev install-deps clean build test lint format run docker-build docker-run docker-stop

install:
	pip install .

dev:
	pip install -e .

install-deps:
	pip install --upgrade pip
	pip install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .tox
	rm -rf dist

build:
	python -m build

test:
	pytest

lint:
	flake8 crystal_mind
	mypy crystal_mind

format:
	black crystal_mind
	isort crystal_mind

run:
	streamlit run crystal_mind/app.py

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down