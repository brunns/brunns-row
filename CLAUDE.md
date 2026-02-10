# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

brunns-row is a Python library that provides a convenience wrapper for DB API and csv.DictReader rows. It allows accessing row data via attributes instead of indices or dictionary keys, inspired by Greg Stein's dtuple module.

## Package Management

This project uses **uv** for dependency management and packaging. All configuration is in `pyproject.toml`.

### First Time Setup
```bash
uv sync --all-extras  # Install all dependencies and create .venv
```

## Development Commands

### Testing
- Run tests: `uv run pytest` or `make test`
- Run single test: `uv run pytest tests/unit/row/test_rowwrapper.py::test_identifiers_fixed_for_mapping_row`
- Run specific test file: `uv run pytest tests/unit/row/test_rowwrapper.py`
- Run with coverage: `uv run pytest --cov=src/brunns --cov-report=term-missing --cov-report=html` or `make coverage`
- Test all Python versions: `make test-all-python` (tests 3.10, 3.11, 3.12, 3.13, 3.14)

### Code Quality
- Run all linting: `make lint` (runs check-format, bandit, refurb)
- Format code: `uv run ruff format .` or `make format`
- Check formatting: `uv run ruff format . --check && uv run ruff check .` or `make check-format`
- Type checking: `uv run mypy src/` or `make mypy`
- Individual linters:
  - `uv run bandit -r src/` (security)
  - `uv run refurb src/` (modernization suggestions)

### Documentation
- Build docs: `uv run sphinx-build docs build_docs --color -W -bhtml` or `make docs`
- Docs built with Sphinx to `build_docs/` directory

### Pre-commit (Key Target)
- **`make precommit`** - Run all checks before committing
  - This is the main quality gate - runs: test, lint, coverage, mypy, docs
  - Must pass before code is ready to commit
  - Ends with "The Zen of Python" when successful

### Building and Publishing
- Build distribution: `uv build` or `make build`
- Publish to PyPI: `uv publish` or `make publish`

### Other
- Sync dependencies: `uv sync --all-extras` or `make sync`
- Clean generated files: `make clean`
- Python REPL: `uv run python` or `make repl`
- Check outdated deps: `uv pip list --outdated` or `make outdated`

## Architecture

### Core Structure
- **Source**: `src/brunns/row/`
  - Uses namespace package structure (`brunns.row`)
  - Main module: `rowwrapper.py` contains the `RowWrapper` class
- **Tests**: `tests/`
  - `unit/row/` - Unit tests for RowWrapper functionality
  - `integration/row/` - Integration tests with actual SQLite DB and CSV files
  - `integration/conftest.py` - Shared pytest fixtures (db, csv_file)

### Main Component: RowWrapper

The `RowWrapper` class is the heart of the library:

1. **Initialization**: Takes a sequence of column descriptions (column names or DB API cursor.description tuples)
2. **Identifier normalization**: Converts column names to valid Python identifiers by:
   - Replacing invalid characters (spaces, hyphens, special chars) with underscores
   - Prefixing numeric-leading names with `a_`
   - De-duplicating conflicting names by adding numeric suffixes
   - Optional lowercase conversion via `force_lower_case_ids` parameter
3. **Dynamic dataclass creation**: Uses `dataclasses.make_dataclass()` to create a row class with the normalized identifiers
4. **Row wrapping**: The `wrap()` method accepts either:
   - Mapping (dict-like) rows - e.g., from csv.DictReader
   - Sequence (tuple-like) rows - e.g., from DB API cursor.fetchall()
5. **Callable interface**: RowWrapper instances are callable, invoking `wrap()`

### Testing Patterns

- Uses pytest with hamcrest matchers (`assert_that`, `has_properties`, `contains`)
- Integration tests use fixtures:
  - `db` fixture: In-memory SQLite database with sample "sausages" table
  - `csv_file` fixture: StringIO with sample CSV data
- Test naming: `test_<behavior>_for_<context>` pattern

## Code Style

- **Formatting**: Ruff (format + linting)
- **Line length**: 120 characters (configured in pyproject.toml)
- **Target version**: Python 3.10+
- **Complexity**: Max McCabe complexity of 5
- **Linting**: Ruff with extensive rules enabled (see pyproject.toml for full config)
- **Coverage**: 100% required

## Dependency Management

- **Lock file**: `uv.lock` is committed to the repository and should be kept up to date
- **Adding dependencies**: Edit `pyproject.toml` [project.dependencies] or [project.optional-dependencies], then run `uv sync`
- **Updating dependencies**: `uv sync --upgrade`
- **Automated updates**: Dependabot runs weekly (Mondays at 9am) to check for:
  - Python dependency updates (grouped: production deps and dev deps)
  - GitHub Actions updates
  - Creates PRs with labels and conventional commit messages

## Release Process

1. Update version in `pyproject.toml`
2. Run `make precommit` to ensure all checks pass
3. Commit changes
4. Create git tag: `git tag v<version>`
5. Push with tags: `git push --tags`
6. Build and publish: `make publish` (runs `uv build && uv publish`)
