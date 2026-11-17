# sphinx-daisyui

[![Tests](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/tests.yml/badge.svg)](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/tests.yml)
[![Build](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/build.yml/badge.svg)](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/build.yml)
[![Publish](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/publish.yml/badge.svg)](https://github.com/SamuelJennings/sphinx-daisyui/actions/workflows/publish.yml)
[![Coverage](https://codecov.io/gh/SamuelJennings/sphinx-daisyui/branch/main/graph/badge.svg)](https://codecov.io/gh/SamuelJennings/sphinx-daisyui)
[![PyPI](https://img.shields.io/pypi/v/sphinx-daisyui)](https://pypi.org/project/sphinx-daisyui/)
[![Development status](https://img.shields.io/pypi/status/sphinx-daisyui)](https://pypi.org/project/sphinx-daisyui/)
[![Python](https://img.shields.io/pypi/pyversions/sphinx-daisyui)](https://pypi.org/project/sphinx-daisyui/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Licence](https://img.shields.io/github/license/SamuelJennings/sphinx-daisyui)](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/LICENSE)

A [Sphinx](https://www.sphinx-doc.org/) theme drawn with [daisyUI](https://daisyui.com/) 5 and
Tailwind CSS 4. It reads the `html_theme_options` of
[Furo](https://pradyunsg.me/furo/) and [pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io/),
so a site using either can switch by changing one line.

## Why

Most Sphinx themes are drawn with Bootstrap or with a stylesheet of their own. daisyUI gives a
component library and 35 ready-made colour themes on Tailwind's tokens, each with a light and a
dark variant. A theme built on it gets every one of those themes for free, and a site that
already uses daisyUI elsewhere gets documentation that looks like the rest of it.

Switching theme usually means rewriting `conf.py`. This theme accepts the options the two most
used modern themes already define, so the configuration a site has keeps working.

## Status

Pre-alpha. The package registers the `daisyui` theme and ships its compiled stylesheet. The
layout, navigation, search and option handling are being built.

## Usage

```bash
pip install sphinx-daisyui
```

```python
# conf.py
html_theme = "daisyui"
```

## Scope & philosophy

**What it is**

- A Sphinx HTML theme drawn with daisyUI 5.
- A drop-in for a site configured for Furo or pydata-sphinx-theme: their options are read as
  they are written.
- Every colour comes from a daisyUI token, so any daisyUI theme works, in light and dark.
- The page layout can be rearranged with one option.

**What it is not**

- A collection of new directives or roles. It styles what Sphinx and common extensions such as
  sphinx-design already write.
- A Bootstrap compatibility layer. Markup written for Bootstrap is not restyled.
- Something that needs Node to use. The compiled stylesheet ships in the package. A site
  changes the look with daisyUI's CSS variables in its own static files.

**When two goals conflict**, a configuration that already builds with Furo or
pydata-sphinx-theme keeping on building wins over a new option of this theme's own.

### Prior art

- [Furo](https://github.com/pradyunsg/furo) and
  [pydata-sphinx-theme](https://github.com/pydata/pydata-sphinx-theme) are the themes most
  modern Sphinx sites use. pydata-sphinx-theme is drawn with Bootstrap 5. Furo has a stylesheet of
  its own. This theme follows their layout and reads their options rather than competing with
  them on new ones.
- [Shibuya](https://github.com/lepture/shibuya) and
  [sphinxawesome-theme](https://github.com/kai687/sphinxawesome-theme) are modern themes with their
  own options. sphinxawesome-theme is built on Tailwind.
- None of them uses daisyUI, and none reads another theme's options.

## Contributing

See [CONTRIBUTING.md](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CONTRIBUTING.md).

## License

MIT. See [LICENSE](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/LICENSE).
