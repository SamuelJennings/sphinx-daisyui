# Options

The theme options a site sets in `html_theme_options` in `conf.py`. Each is described the same
way: its type, its default and what it does.

A component list is a Python list of names, and a name may be written with or without `.html`.
These are the same:

```python
html_theme_options = {
    "footer_start": ["copyright", "sphinx-version"],
}
html_theme_options = {
    "footer_start": ["copyright.html", "sphinx-version.html"],
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
to `_static`. Sphinx's `html_logo` is used for both modes when `logo` gives no image.

### `logo`

- **Type:** dict
- **Default:** empty
- **Meaning:** The brand as a whole. Every key is optional:
  - `text`: the name beside the logo. Without it the site's title is shown, unless the dict
    gives an image, and then no name is shown.
  - `image_light` and `image_dark`: the logos for light and dark mode. The light logo is also
    shown in dark mode when `image_dark` is not set.
  - `alt_text`: the logo's `alt` text. The default is the project name.
  - `link`: where the brand leads. The default is the site's home page.

## Moving between pages

### `show_prev_next`

- **Type:** boolean
- **Default:** `True`
- **Meaning:** Whether each page ends with links to the previous and the next page in the
  site's table of contents. A page with neither, and the search and index pages, show none.

### `navigation_with_keys`

- **Type:** boolean
- **Default:** `False`
- **Meaning:** Whether the left and right arrow keys move to the previous and the next page.
  Sphinx's own script does the moving, and it ignores the keys while the reader types in a field
  or holds a modifier key. The meaning is the one Sphinx's `basic` theme gives the option.

### `back_to_top_button`

- **Type:** boolean
- **Default:** `True`
- **Meaning:** Whether a button appears while the reader scrolls up, far down a page, that scrolls
  back to the top.

### `announcement`

- **Type:** text
- **Default:** empty
- **Meaning:** A banner across the top of every page. Text, including HTML of your own, is
  printed as written and is not escaped. Text that starts with `http://` or `https://` is an
  address instead: the page script fetches it and puts the HTML it returns in the banner. The
  banner is removed when the address cannot be fetched, answers with an error or returns nothing,
  which includes a site opened from the file system. An empty value shows no banner.

### `sticky_banners`

- **Type:** boolean
- **Default:** `False`
- **Meaning:** Whether the banner sits inside the header, so that it stays with the header when
  the layout code keeps the header in place. When off, the banner is the first thing on the page
  and scrolls away.

## Site navigation

The navigation in the primary sidebar is the site's table of contents, drawn from its `toctree`
directives.

### `navigation_depth`

- **Type:** integer
- **Default:** `4`
- **Meaning:** How many levels of entries the navigation lists. Deeper entries are left out. Zero lists them all.

### `show_nav_level`

- **Type:** integer
- **Default:** `1`
- **Meaning:** How many levels of entries are open before the reader opens any. The entries on
  the way to the current page are always open.

### `collapse_navigation`

- **Type:** boolean
- **Default:** `False`
- **Meaning:** Whether the navigation leaves out the children of every entry that is not on the
  way to the current page.

### `sidebar_includehidden`

- **Type:** boolean
- **Default:** `True`
- **Meaning:** Whether the navigation lists the pages of a `toctree` marked `:hidden:`.

## On this page

The `page-toc` component lists the headings of the page being read.

### `show_toc_level`

- **Type:** integer
- **Default:** `2`
- **Meaning:** How many levels of headings are shown before the reader reaches them. Headings
  under that depth stay hidden until the section above them is being read. A level of `1`
  shows only the headings directly under the page's title, and a level larger than the page's
  deepest heading shows them all.

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
  empty, and on the search page and every index page.

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
