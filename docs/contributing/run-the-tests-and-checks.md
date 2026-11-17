# Run the tests and checks

Each command below is the one CI runs.

## Run the tests

```bash
uv run pytest
```

Tests build small sites with `sphinx.testing`. Each site lives under `tests/roots/test-<name>/`.

## Run the linters and hooks

```bash
uv run pre-commit run --all-files
```

This runs ruff, mypy, deptry and pydoclint, and checks that `uv.lock` matches `pyproject.toml`.

## Build the documentation

```bash
uv run --group docs sphinx-build -b html -W --keep-going docs docs/_build/html
```

`-W` turns every warning into an error, so a page left out of the contents fails the build.

## Build the package

```bash
uv build
```

The build compiles the stylesheet if it isn't compiled yet, and puts it in both the wheel and the
sdist.
