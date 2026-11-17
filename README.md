# sphinx-daisyui

[![Tests](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/tests.yml/badge.svg)](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/tests.yml)
[![Build](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/build.yml/badge.svg)](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/build.yml)
[![Publish](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/publish.yml/badge.svg)](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/publish.yml)
[![Docs](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/docs.yml/badge.svg)](https://samueljennings.github.io/sphinx-daisyui/)
[![Coverage](https://codecov.io/gh/SamuelJennings/sphinx-daisyui/branch/main/graph/badge.svg)](https://codecov.io/gh/SamuelJennings/sphinx-daisyui)
[![PyPI](https://img.shields.io/pypi/v/sphinx-daisyui)](https://pypi.org/project/sphinx-daisyui/)
[![Development status](https://img.shields.io/pypi/status/sphinx-daisyui)](https://pypi.org/project/sphinx-daisyui/)
[![Python](https://img.shields.io/pypi/pyversions/sphinx-daisyui)](https://pypi.org/project/sphinx-daisyui/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Licence](https://img.shields.io/github/license/SamuelJennings/sphinx-daisyui)](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/LICENSE)

A [Sphinx](https://www.sphinx-doc.org/) theme drawn with [daisyUI](https://daisyui.com/) 5 and
Tailwind CSS 4. It has its own `html_theme_options`, named and shaped after those of
[pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io/) where it has the same setting.
A site coming from [Furo](https://pradyunsg.me/furo/) or pydata-sphinx-theme reconfigures, and
the layout option can give it a page arranged like either.

**Documentation:** https://samueljennings.github.io/sphinx-daisyui/ (the site is built with the theme).

## Why

Most Sphinx themes are drawn with Bootstrap or with a stylesheet of their own. daisyUI gives a
component library and 35 ready-made colour themes on Tailwind's tokens, each with a light and a
dark variant. A theme built on it gets every one of those themes for free, and a site that
already uses daisyUI elsewhere gets documentation that looks like the rest of it.

## Status

Pre-alpha. v0.1.0 is the first release, and options may still change before 1.0. It has:

- the page layout, rearranged with the `layout` option and filled from component lists
- site navigation, breadcrumbs, header links and the On this page list
- a search dialog, a version switcher, and a light, dark and named-theme picker
- icon links, and edit and view buttons for GitHub, GitLab and Bitbucket
- styles for Sphinx's page body and the sphinx-design and sphinx-copybutton markup

The [changelog](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CHANGELOG.md) lists
each change.

## Usage

```bash
pip install sphinx-daisyui
```

```python
# conf.py
html_theme = "daisyui"
```

- [Installation](https://samueljennings.github.io/sphinx-daisyui/developer/installation.html)
- [Moving from Furo or pydata-sphinx-theme](https://samueljennings.github.io/sphinx-daisyui/developer/move-from-furo-or-pydata-sphinx-theme.html)
- [Options reference](https://samueljennings.github.io/sphinx-daisyui/reference/options.html)

## Scope & philosophy

**What it is**

- A Sphinx HTML theme drawn with daisyUI 5.
- A theme with its own options, which follow pydata-sphinx-theme's names and shapes where it has
  the same setting. A site coming from Furo or pydata-sphinx-theme reconfigures.
- Every colour comes from a daisyUI token, so any daisyUI theme works, in light and dark.
- The page layout can be rearranged with one option, and each part of the page is filled from a
  list of components.

**What it is not**

- A collection of new directives or roles. It styles what Sphinx and common extensions such as
  sphinx-design already write.
- A Bootstrap compatibility layer. Markup written for Bootstrap is not restyled.
- Something that needs Node to use. The compiled stylesheet ships in the package. A site
  changes the look with daisyUI's CSS variables in its own static files.

**When two goals conflict**, one name and one shape for each option wins over resemblance to
another theme.

### Prior art

- [Furo](https://github.com/pradyunsg/furo) and
  [pydata-sphinx-theme](https://github.com/pydata/pydata-sphinx-theme) are the themes most
  modern Sphinx sites use. pydata-sphinx-theme is drawn with Bootstrap 5. Furo has a stylesheet of
  its own. This theme borrows their page layout and the names of
  pydata-sphinx-theme's options, and has options of its own.
- [Shibuya](https://github.com/lepture/shibuya) and
  [sphinxawesome-theme](https://github.com/kai687/sphinxawesome-theme) are modern themes with their
  own options. sphinxawesome-theme is built on Tailwind.
- None of them uses daisyUI.

## Contributing

See [CONTRIBUTING.md](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CONTRIBUTING.md).

## License

MIT. See [LICENSE](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/LICENSE).
