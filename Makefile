SHELL = /bin/bash

default: help
.PHONY: help

.PHONY: sync
sync: ## Sync dependencies with uv
	uv sync --all-extras

test: ## Run tests
	uv run pytest

test-all-python: ## Run tests on all Python versions
	uv run --python 3.10 pytest
	uv run --python 3.11 pytest
	uv run --python 3.12 pytest
	uv run --python 3.13 pytest
	uv run --python 3.14 pytest

coverage: ## Test coverage report
	uv run pytest --cov=src/brunns --cov-report=term-missing --cov-report=html

lint: check-format ## Lint code

.PHONY: check-format
check-format:
	uv run ruff format . --check
	uv run ruff check .

mypy:
	uv run mypy src/

format: ## Format code
	uv run ruff format .
	uv run ruff check . --fix

.PHONY: docs
docs:  ## Generate documentation
	uv run sphinx-build docs build_docs --color -W -bhtml
	@ echo "Documentation available at file://$(PWD)/build_docs/index.html"

.PHONY: precommit
precommit: test lint coverage mypy docs ## Pre-commit targets
	@ python -m this

.PHONY: build
build: ## Build distribution packages
	uv build

.PHONY: publish
publish: build ## Publish to PyPI
	uv publish

clean: ## Clean generated files
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	rm -rf build/ dist/ *.egg-info/ .cache .coverage .pytest_cache htmlcov/ .venv/
	find . -name "__pycache__" -type d -print | xargs -t rm -r
	find . -name "test-output" -type d -print | xargs -t rm -r

.PHONY: repl
repl: ## Python REPL
	uv run python

outdated: ## List outdated dependencies
	uv pip list --outdated

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1,$$2}'
