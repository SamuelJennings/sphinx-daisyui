# Contributing to sphinx-daisyui

Thank you for helping. This guide covers what the theme will and will not take, how to set up,
and what a pull request needs.

## Before you open an issue

`sphinx-daisyui` styles what Sphinx and the extensions it supports already write. It adds no
directives or roles of its own, and it doesn't restyle markup written for Bootstrap. A
configuration written for Furo or pydata-sphinx-theme should build unchanged: if one doesn't, that
is a bug worth reporting, with the `conf.py` that shows it. The README's *Scope & philosophy*
section says more.

## Setting up

You need [uv](https://docs.astral.sh/uv/) and [Node.js](https://nodejs.org/) 20 or later. Node
compiles the stylesheet.

```bash
git clone https://github.com/SamuelJennings/sphinx-daisyui.git
cd sphinx-daisyui
uv sync --group docs
uv run pre-commit install
```

## Making a change

1. Branch from `main`.
2. Write a test first, and watch it fail for the right reason. Tests build a small site with
   `sphinx.testing`, and test sites live under `tests/roots/`. See
   [docs/contributing/standards/testing.md](docs/contributing/standards/testing.md).
3. Make the change. Run `npm run watch` while you edit templates or `assets/`.
4. Run the checks:

   ```bash
   uv run pytest
   uv run pre-commit run --all-files
   uv run --group docs sphinx-build -b html -W --keep-going docs docs/_build/html
   ```

5. Add a line to `CHANGELOG.md` under `[Unreleased]` if the change is visible to a site author.
6. Open a pull request that says what changed and why.

## Standards

- [CONSTITUTION.md](CONSTITUTION.md): the rules every change follows.
- [CONTEXT.md](CONTEXT.md): the words this repository uses.
- [docs/contributing/standards/](docs/contributing/standards/): testing, documentation and
  docstrings.

## Licence

By contributing you agree that your contribution is licensed under the MIT License.
