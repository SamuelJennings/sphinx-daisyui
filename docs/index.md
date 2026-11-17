# sphinx-daisyui

A Sphinx theme drawn with [daisyUI](https://daisyui.com) 5 and Tailwind CSS 4. It reads the
options of Furo and pydata-sphinx-theme, so a project can try it by changing one line.

```python
html_theme = "daisyui"
```

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} {octicon}`rocket` Get started
:link: get-started/install
:link-type: doc

Install the theme and build your first page in two minutes.
:::

:::{grid-item-card} {octicon}`arrow-switch` Switch from Furo
:link: get-started/from-furo
:link-type: doc

Keep your `html_theme_options`. Every Furo option is read.
:::

:::{grid-item-card} {octicon}`arrow-switch` Switch from pydata-sphinx-theme
:link: get-started/from-pydata
:link-type: doc

Header links, the version switcher and template placement carry over.
:::

:::{grid-item-card} {octicon}`paintbrush` Themes and colours
:link: configure/themes
:link-type: doc

Every daisyUI theme, light and dark, and a picker for your readers.
:::
::::

## Why another theme

The themes most Python projects use are drawn with Bootstrap or with hand-written CSS. A project
whose product is built on Tailwind and daisyUI ends up with documentation that looks like a
different product. This theme draws every part of a page with daisyUI's components and colour
tokens, so the documentation takes on the same theme as the application, and any of daisyUI's
35 themes works without a build step.

- **Readable first.** A measure of about 75 characters, a type scale with clear steps, and
  generous space above headings.
- **Every theme, light and dark.** Code, notices, tables and sphinx-design components all draw
  from the theme's tokens, so nothing is left in the wrong colours.
- **Search as you type.** Pages, sections and API names, from Sphinx's own index, with no
  server and no third-party service.
- **Drop-in options.** Configurations written for Furo or pydata-sphinx-theme build unchanged.

```{toctree}
:caption: Get started
:hidden:

get-started/install
get-started/from-furo
get-started/from-pydata
```

```{toctree}
:caption: Configure
:hidden:

configure/options
configure/themes
configure/layout
configure/search-and-versions
```

```{toctree}
:caption: Kitchen sink
:hidden:

kitchen-sink/typography
kitchen-sink/admonitions
kitchen-sink/code
kitchen-sink/tables
kitchen-sink/lists
kitchen-sink/media
kitchen-sink/design
kitchen-sink/api
kitchen-sink/deeper/index
```

```{toctree}
:caption: Project
:hidden:

changelog
daisyUI <https://daisyui.com>
```
