.PHONY: all

all: check

.PHONY: check format lint mypy
check: lint format mypy

format:
	poetry run ruff format

lint:
	poetry run ruff check

mypy:
	poetry run mypy .