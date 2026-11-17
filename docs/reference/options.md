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

## Brand

The brand is the logo and name at the start of the navbar. When `layout` gives the top-left
corner to the primary sidebar, the brand heads that sidebar on wide screens and stays in the
navbar on narrow ones. A logo is a full address, a path starting `_static/`, or a path relative
to `_static`. Sphinx's `html_logo` is used for both modes when none of these options gives a
logo.

### `light_logo`

- **Type:** string
- **Default:** empty
- **Source:** Furo's `light_logo`
- **Meaning:** The logo shown in light mode. It is also shown in dark mode when `dark_logo` is
  empty.

### `dark_logo`

- **Type:** string
- **Default:** empty
- **Source:** Furo's `dark_logo`
- **Meaning:** The logo shown in dark mode.

### `sidebar_hide_name`

- **Type:** flag
- **Default:** empty, which is off
- **Source:** Furo's `sidebar_hide_name`
- **Meaning:** Hides the site's name beside the logo. The logo's `alt` text then names the site.
  It does not hide a name set with `logo["text"]`.

### `logo`

- **Type:** dict
- **Default:** empty
- **Source:** pydata-sphinx-theme's `logo`
- **Meaning:** The brand as a whole. Every key is optional:
  - `text`: the name beside the logo. Without it the site's title is shown, unless the dict
    gives an image, and then no name is shown.
  - `image_light` and `image_dark`: the logos, read like `light_logo` and `dark_logo`, and
    taking precedence over them.
  - `alt_text`: the logo's `alt` text. The default is the project name.
  - `link`: where the brand leads. The default is `logo_link`, then the site's home page.

### `logo_link`

- **Type:** string
- **Default:** empty, which is the site's home page
- **Source:** pydata-sphinx-theme's `logo_link`
- **Meaning:** Where the brand leads, when `logo["link"]` is not set.

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
