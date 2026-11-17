# sphinx-daisyui

sphinx-daisyui is a Sphinx theme drawn with [daisyUI](https://daisyui.com) 5 and Tailwind CSS 4.
A project whose product is built on daisyUI gets documentation that takes on the same theme as
the application, and any of daisyUI's colour themes works in light and dark without a build step.
The theme has its own options, many named after pydata-sphinx-theme's.

```{toctree}
:hidden:

Home <self>
developer/index
reference/index
kitchen-sink/index
contributing/index
Changelog <https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CHANGELOG.md>
```

## Features

- [The `daisyui` theme](developer/installation.md), with its stylesheet compiled into the package,
  so using it never needs Node.
- [The page frame](developer/arrange-the-page.md): a header, two sidebars and a footer, arranged
  by one layout code and filled from lists of components.
- [Sections in the header](developer/put-the-sections-in-the-header.md), with the sidebar showing
  only the section being read.
- [Colour themes](developer/choose-the-themes.md): every daisyUI theme, light and dark, and a
  picker for readers.
- [Search and versions](developer/set-up-search-and-versions.md): search as you type from
  Sphinx's own index, and a version switcher.
- [Icon links and source links](developer/link-the-sources.md): accounts as icons, and edit and
  view buttons that lead to each page's source file.
- [Page bodies](reference/page-body.md) drawn with daisyUI's components and colour tokens, so
  code, admonitions, tables and sphinx-design components never sit in the wrong colours.

## Requirements

- Python 3.11 or later
- Sphinx 7.4 or later

## Installation

Install the package:

```bash
pip install sphinx-daisyui
```

Choose the theme in your `conf.py`:

```python
html_theme = "daisyui"
```

[Installation](developer/installation.md) describes each step in full.

## An example

Name the theme, give it a logo and link the repository:

```python
html_theme = "daisyui"
html_theme_options = {
    "logo": {"text": "My project", "image_light": "logo.svg"},
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/example/project",
            "icon": "github",
        },
    ],
    "source_repository": "https://github.com/example/project",
    "source_directory": "docs/",
}
```

The next build has the project's name and logo in the header, a GitHub icon, and an edit button
above each page that leads to the page's source file.

## Next steps

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Developer guide
:link: developer/index
:link-type: doc

Install the theme, arrange the page, and set up search, versions and links.
:::

:::{grid-item-card} Reference
:link: reference/index
:link-type: doc

Every option, component and layout letter the theme accepts.
:::

:::{grid-item-card} Moving from Furo or pydata-sphinx-theme
:link: developer/move-from-furo-or-pydata-sphinx-theme
:link-type: doc

Which option of this theme does what each of theirs did.
:::

:::{grid-item-card} Kitchen sink
:link: kitchen-sink/index
:link-type: doc

Every kind of content a page can hold, drawn in the theme.
:::
::::

## About the project

- [Domain model](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CONTEXT.md): the words this project uses and what each means.
- [Constitution](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CONSTITUTION.md): the rules every change follows.
- [Changelog](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CHANGELOG.md): what changed in each release.

## Support

Report a problem in the [issue tracker](https://github.com/SamuelJennings/sphinx-daisyui/issues). Everyone taking part is expected to follow the
[Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## Licence

MIT. See [LICENSE](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/LICENSE).
