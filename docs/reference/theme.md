# Theme

## `daisyui`

- **Set with:** `html_theme` in `conf.py`.
- **Registered by:** the `sphinx.html_themes` entry point `daisyui`, which Sphinx loads when a
  site names the theme.
- **Inherits:** Sphinx's `basic` theme.
- **Stylesheet:** `_static/styles/sphinx-daisyui.css`, linked from every page.
- **Page-body stylesheet:** `_static/styles/sphinx-daisyui-content.css`, the page-body styles on
  their own, which no page of the theme links. It is for a site that shows the pages inside a
  page of its own ([The page body](page-body.md#the-page-body-styles-outside-the-theme)).
