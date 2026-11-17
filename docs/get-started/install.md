# Install

Install the theme from PyPI, next to Sphinx.

::::{tab-set}
:::{tab-item} pip
```console
$ pip install sphinx-daisyui
```
:::
:::{tab-item} uv
```console
$ uv add --group docs sphinx-daisyui
```
:::
:::{tab-item} Poetry
```console
$ poetry add --group docs sphinx-daisyui
```
:::
::::

Then name it in `conf.py`:

```{code-block} python
:caption: conf.py
:emphasize-lines: 2

project = "My project"
html_theme = "daisyui"
```

Build as usual:

```console
$ sphinx-build -b html docs docs/_build/html
```

```{note}
The stylesheet ships compiled inside the package. You never need Node, npm or a Tailwind
build to use the theme, or to change its colours.
```

## What you get without configuring anything

- Your project's name in the navbar, and your `html_logo` beside it if you set one.
- The table of contents in the sidebar, with the page you are reading opened and marked.
- The page's own headings in a column on the right, following you as you scroll.
- daisyUI's `light` theme, or `dark` when the reader's system asks for it, with a switch in the
  navbar.
- Search as you type, opened with {kbd}`Ctrl+K`, {kbd}`⌘K` or {kbd}`/`.
