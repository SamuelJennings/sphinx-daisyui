# sphinx-daisyui

sphinx-daisyui is a Sphinx theme drawn with daisyUI 5 and Tailwind CSS 4. It has its own
theme options, many named after pydata-sphinx-theme's, and every daisyUI colour theme works with
it in light and dark.

```{toctree}
:hidden:

Home <self>
developer/index
reference/index
contributing/index
Changelog <https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CHANGELOG.md>
```

## Features

- [The `daisyui` theme](developer/installation.md), with its stylesheet compiled into the package,
  so using it never needs Node.
- [The page frame](developer/arrange-the-page.md): a header, two sidebars and a footer, arranged
  by one layout code and filled from lists of components.

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

## Next steps

- [Developer guide](developer/index.md): installing the theme and configuring it.
- [Reference](reference/index.md): the theme's name and what it registers.

## About the project

- [Domain model](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CONTEXT.md): the words this project uses and what each means.
- [Constitution](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CONSTITUTION.md): the rules every change follows.
- [Changelog](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/CHANGELOG.md): what changed in each release.

## Support

Report a problem in the [issue tracker](https://github.com/SamuelJennings/sphinx-daisyui/issues). Everyone taking part is expected to follow the
[Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## Licence

MIT. See [LICENSE](https://github.com/SamuelJennings/sphinx-daisyui/blob/main/LICENSE).
