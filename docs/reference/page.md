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

## Translated text

The theme's own text is translatable. Setting `language` in `conf.py` selects the translation, and
Sphinx reads the theme's messages from the `sphinx` domain with the rest of its own. The catalogue
template ships in the package at `sphinx_daisyui/locale/sphinx.pot`.
