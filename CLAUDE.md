# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

brunns-row is a Python library that provides a convenience wrapper for DB API and csv.DictReader rows. It allows accessing row data via attributes instead of indices or dictionary keys, inspired by Greg Stein's dtuple module.

## Development Commands

### Testing
- Run tests: `tox -e py310,py314,pypy311` or `make test`
- Run single test: `pytest tests/unit/row/test_rowwrapper.py::test_identifiers_fixed_for_mapping_row`
- Run specific test file: `pytest tests/unit/row/test_rowwrapper.py`
- Run with coverage: `tox -e coverage` or `make coverage` (requires 100% coverage)
- Test environments: py310, py311, py312, py313, py314, pypy310, pypy311

### Code Quality
- Run all linting: `make lint` (runs check-format, bandit, safety, refurb)
- Format code: `tox -e format` or `make format` (ruff format + ruff check --fix)
- Check formatting: `tox -e check-format` (ruff format --check + ruff check)
- Type checking: `tox -e mypy` or `make mypy`
- Individual linters:
  - `tox -e bandit` (security)
  - `tox -e refurb` (modernization suggestions)

### Documentation
- Build docs: `tox -e docs` or `make docs`
- Docs built with Sphinx to `build_docs/` directory

### Pre-commit (Key Target)
- **`make precommit`** - Run all checks before committing
  - This is the main quality gate - runs: test, lint, coverage, mypy, docs
  - Must pass before code is ready to commit
  - Ends with "The Zen of Python" when successful

### Other
- Clean generated files: `make clean`
- Recreate tox environments: `make recreate`
- Python REPL: `make repl`

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
- **Coverage**: 100% required (omits */matcher.py)

## Release Process

Version is set in `setup.py`. The README documents a release process involving:
1. Create release branch
2. Run `make precommit`
3. Commit and push
4. Create GitHub release with `hub`
5. Build and upload to PyPI with `twine`
