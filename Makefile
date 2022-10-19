SHELL = /bin/bash

default: help
.PHONY: help

test: ## Run tests
	tox -e py37,py311

coverage: ## Test coverage report
	tox -e coverage

lint: check-format flake8 bandit safety refurb ## Lint code

flake8:
	tox -e flake8

bandit:
	tox -e bandit

safety:
	tox -e safety

extra-lint: pylint mypy  ## Extra, optional linting.

pylint:
	tox -e pylint

.PHONY: refurb
refurb:
	tox -e refurb

mypy:
	tox -e mypy

check-format:
	tox -e check-format

format: ## Format code
	tox -e format

piprot: ## Check for outdated dependencies
	tox -e piprot

.PHONY: docs
docs:  ## Generate documentation
	tox -e docs

.PHONY: precommit
precommit: test lint coverage mypy docs ## Pre-commit targets
	@ python -m this

.PHONY: recreate
recreate: clean ## Recreate tox environments
	tox --recreate --notest -p -s
	tox --recreate --notest -e coverage,format,check-format,flake8,pylint,bandit,safety,piprot,mypy,docs,refurb -p

clean: ## Clean generated files
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	rm -rf build/ dist/ *.egg-info/ .cache .coverage .pytest_cache
	find . -name "__pycache__" -type d -print | xargs -t rm -r
	find . -name "test-output" -type d -print | xargs -t rm -r

repl: ## Python REPL
	tox -e py311 -- python

outdated: ## List outdated dependancies
	tox -e py311 -- pip list --outdated

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1,$$2}'
