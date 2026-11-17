# The page

What the theme leaves on every page for a site's own CSS and scripts to read.

## Widths

Three custom properties set the width of the page's columns. They are set on the `.daisy-layout` element, so a site
changes one by setting it again on that element in a stylesheet listed in `html_css_files`.

| Property | Default | Sets |
|---|---|---|
| `--daisy-primary-width` | `18rem` | The width of the primary sidebar |
| `--daisy-main-width` | `54rem` | The width of the page |
| `--daisy-secondary-width` | `15rem` | The width of the secondary sidebar |

For example, `_static/custom.css` can set the primary sidebar to 16rem:

```css
.daisy-layout {
  --daisy-primary-width: 16rem;
}
```

`conf.py` then lists the stylesheet:

```python
html_css_files = ["custom.css"]
```

## Attributes on the body

The `<body>` element carries five attributes that the theme's scripts read and a site's scripts
may read too.

| Attribute | Holds |
|---|---|
| `data-daisy-root` | The path from the page to the site's root, such as `./` or `../` |
| `data-daisy-suffix` | The file suffix of the pages, such as `.html` |
| `data-daisy-link-suffix` | The suffix that links to pages use, such as `.html` |
| `data-daisy-builder` | The name of the builder that wrote the page, such as `html` |
| `data-daisy-page` | The page's name, such as `index` or `guide/install` |

## Attributes on the root element

The `<html>` element carries six attributes that describe the colour the page is drawn in. The
theme sets them before the page is first drawn, so a site's stylesheet can rely on them and no
page flashes the wrong colours. A site's own stylesheets and scripts may read them. They are not
a place to write: the theme's script owns them.

| Attribute | Holds |
|---|---|
| `data-theme` | The daisyUI theme the page is drawn with, such as `light` or `dracula` |
| `data-mode` | `light` or `dark`: which of the two the page is drawn in |
| `data-mode-choice` | The reader's choice: `auto`, `light`, `dark` or `theme` for a theme picked by name |
| `data-light-theme` | The theme the light mode draws, from `light_theme` |
| `data-dark-theme` | The theme the dark mode draws, from `dark_theme` |
| `data-default-mode` | The starting mode: `auto`, `light` or `dark`, from `default_mode` |

`data-mode` follows the theme in use. A theme picked by name counts as dark when its colour scheme
is dark. Style something differently in dark mode by keying on it:

```css
html[data-mode="dark"] .diagram {
  filter: invert(1);
}
```

## Translated text

The theme's own text is translatable. Setting `language` in `conf.py` selects the translation, and
Sphinx reads the theme's messages from the `sphinx` domain with the rest of its own. The catalogue
template ships in the package at `sphinx_daisyui/locale/sphinx.pot`.
