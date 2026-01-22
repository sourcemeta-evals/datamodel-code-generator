.PHONY: all install test type clean

all: install test type

install:
	uv sync --all-extras

test:
	uv run pytest -p no:benchmark -n auto -m "not perf" --cov=datamodel_code_generator --cov-fail-under=95 tests

type:
	uv run pyright src

clean:
	rm -rf .tox .pytest_cache .coverage coverage.xml htmlcov dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
