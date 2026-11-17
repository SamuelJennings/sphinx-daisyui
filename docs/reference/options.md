# Options

The theme options a site sets in `html_theme_options` in `conf.py`. Each is described the same
way: its type, its default and what it does.

A component list may be a Python list or a comma-separated string, and a name may be written with
or without `.html`. These are the same:

```python
html_theme_options = {
    "footer_start": ["copyright", "sphinx-version"],
}
html_theme_options = {
    "footer_start": "copyright.html, sphinx-version.html",
}
```

Each name is a template. The theme looks for it in its own `components/` directory first, then in
the site's `templates_path`. A name that no template has draws nothing and raises no warning.
[Components](components.md) lists the five the theme provides.

## Layout

### `layout`

- **Type:** string
- **Default:** `"hHh LpR lff"`
- **Meaning:** The layout code. It places the header, the primary sidebar, the page, the
  secondary sidebar and the footer, and sets which of them stay in view while the page scrolls.
  An empty value means the default. A value that is not a layout code stops the build with a
  message naming the option. [The layout code](layout-code.md) explains each letter.

## Component lists

### `navbar_start`

- **Type:** list of component names
- **Default:** `"navbar-logo"`
- **Meaning:** The components at the start of the navbar, after the button that opens the
  navigation on a narrow screen.

### `navbar_center`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components in the middle of the navbar. They are hidden below 64rem.

### `navbar_end`

- **Type:** list of component names
- **Default:** `"version-switcher, theme-switcher, navbar-icon-links"`
- **Meaning:** The components at the end of the navbar. They are written once in the page and
  hidden on the narrowest screens.

### `navbar_persistent`

- **Type:** list of component names
- **Default:** `"search-button-field"`
- **Meaning:** The components at the end of the navbar that stay on every screen width.

### `article_header_start`

- **Type:** list of component names
- **Default:** `"breadcrumbs"`
- **Meaning:** The components at the start of the line above the page's content. The line is
  left out when this list and `article_header_end` are both empty.

### `article_header_end`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components at the end of the line above the page's content.

### `article_footer_items`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components directly below the page's content.

### `content_footer_items`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components at the very end of the content column, below
  `article_footer_items`.

### `primary_sidebar_end`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components at the end of the primary sidebar, after Sphinx's own sidebar
  templates.

### `secondary_sidebar_items`

- **Type:** list of component names
- **Default:** `"page-toc"`
- **Meaning:** The components in the secondary sidebar. The sidebar is left out when the list is
  empty.

### `footer_start`

- **Type:** list of component names
- **Default:** `"copyright, sphinx-version"`
- **Meaning:** The components at the start of the footer.

### `footer_center`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components in the middle of the footer.

### `footer_end`

- **Type:** list of component names
- **Default:** `"theme-version"`
- **Meaning:** The components at the end of the footer.
