# Research: 003-page-body-styles

## Assumptions checked

Run on 2026-11-17 against `main` at `0ffa3a3`, with Sphinx 9.2.0, Pygments 2.21.0 and
Python 3.13.

- **Sphinx links Pygments' stylesheet on every page.** A test site built with the scaffold's
  theme links `_static/pygments.css` before the theme's stylesheet. `StandaloneHTMLBuilder` adds
  it unconditionally (`sphinx/builders/html/__init__.py`, `add_css_file('pygments.css',
  priority=200)`), so the theme removes it from the page's `css_files` rather than asking Sphinx
  not to write it (FR-004).
- **Sphinx's dark Pygments stylesheet keys on a media query.** The same builder adds
  `pygments_dark.css` with `media='(prefers-color-scheme: dark)'` only when the theme sets
  `pygments_dark_style`. The daisyui theme does not, and the `basic` theme sets no dark style, so
  no such stylesheet is written. A media query ignores the mode a reader picks, which is why the
  Pygments styles key on the mode attribute on `<html>` instead (D6).
- **Pygments writes a style under any selector.** `HtmlFormatter(style=...).get_style_defs(
  'html[data-mode="dark"] .highlight')` prefixes every rule with that selector, so one stylesheet
  can hold a style per mode.
- **An unknown style name raises `ClassNotFound`.** `pygments.styles.get_style_by_name("nope")`
  raises `pygments.util.ClassNotFound`, which the theme catches to warn and keep the token
  highlighting (FR-015).
- **The markup the body rewrite reads is what Sphinx 9.2 writes.** A test site with a numbered
  display equation, a captioned table and an attributed quotation builds to `<div class="math
  notranslate nohighlight">` with a `<span class="eqno">` inside, a `<table>` with a `<caption>`,
  and `<p class="attribution">`. Raw HTML passes through unchanged, so an escape-class element
  reaches the page as written.
- **The page body's scope class comes with the frame.** The prototype's `layout.html:122` writes
  `<article class="daisy-sphinx-content" role="main">` around the body, in the part of
  `layout.html` the page frame (#4) ports. The page-body styles scope to it.
- **The scaffold carries none of the kitchen sink's extensions.** `main`'s `docs/conf.py` loads
  only `myst_parser`, and the `docs` dependency group holds `myst-parser` and `sphinx-autobuild`.
  The kitchen sink pages need sphinx-design, sphinx-copybutton, autodoc, viewcode, MathJax and
  MyST's extensions, added to the documentation site only (D7).
