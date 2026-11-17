# Navbar, sidebars and footer

Each area of the page holds a list of components, named as pydata-sphinx-theme names them.

```{list-table} Components
:header-rows: 1
:widths: 30 70

* - Component
  - What it draws
* - `navbar-logo`
  - The logo and project name
* - `navbar-nav`
  - The top-level pages, with the rest in a menu
* - `search-button-field`
  - The search button, with its shortcut
* - `version-switcher`
  - The version menu, from `switcher.json`
* - `theme-switcher`
  - The mode and theme menu
* - `navbar-icon-links`
  - Icon links to GitHub, PyPI and the rest
* - `breadcrumbs`
  - Where the page sits in the documentation
* - `page-toc`
  - The page's own headings
* - `edit-this-page`, `sourcelink`
  - Links to the page's source
* - `copyright`, `sphinx-version`, `theme-version`, `last-updated`
  - Footer lines
```

## A component of your own

Put a template in `templates_path` and name it:

```python
templates_path = ["_templates"]
html_theme_options = {"footer_center": ["made-with-love"]}
```

The template sees the whole Sphinx page context, and `daisy`, the theme's own values.

## Header links, as pydata-sphinx-theme draws them

```python
html_theme_options = {"navbar_center": ["navbar-nav"], "header_links_before_dropdown": 4}
```

The top-level pages move into the navbar and the sidebar shows only the section you are in.
On a phone, the sections are listed at the top of the navigation drawer.
