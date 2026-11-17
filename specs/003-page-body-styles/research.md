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

## Against `main` after the page frame and site navigation

Run on 2026-11-17 against `main` at `cba7e48`, the merge of site navigation.

### Where the page body is changed

The body is changed while Sphinx writes it, by a translator mixin, and never by parsing the
written HTML. ADR 0001 rules out an HTML parser for toctrees, and the same reasons hold for the
rest of the body: the prototype parsed every page's `body` with BeautifulSoup, which `main` does
not carry.

- **A doctree handler cannot do it all.** `doctree-resolved` runs inside
  `apply_post_transforms`, before `get_and_resolve_doctree` resolves the page's toctrees, so a
  toctree in a page is still an unresolved `toctree` node there. The admonition titles of `note`,
  `warning` and the rest are added by `HTML5Translator.visit_admonition` at write time, and a
  heading link is written by `add_permalink_ref`. None of them is a node before writing.
- **A translator mixin can.** pydata-sphinx-theme does the same thing
  (`pydata_sphinx_theme/translator.py`): at `builder-inited` it builds a class from its mixin and
  the builder's translator, or each translator already registered for an HTML builder, and sets
  it with `app.set_translator(..., override=True)`. Keeping the registered class as the base
  keeps another extension's translator working. The mixin overrides:
  - `visit_table` and `depart_table`: an outermost table opens and closes a scroll region, named
    by the table's title node or the translated "Table".
  - `visit_math_block`: a numbered equation writes its number and heading link first, then its
    notation inside a scroll region, by handing the renderer a copy of the node with no number.
    The number is Sphinx's own, from `sphinx.util.math.get_node_equation_number`.
  - `add_permalink_ref`: the link gains an `aria-label` of Sphinx's title and the text of what it
    links to, the signature's name for an API entry.
  - `visit_attribution`: one thin space after the dash, and the text's own leading space dropped.
  - `visit_title` under an admonition, and `visit_versionmodified`: the kind's icon from `ICONS`.
  - `visit_compact_paragraph` for a `toctree-wrapper`: the resolved toctree is decorated with the
    site navigation's own code before its children are written (story 2).
- **The region's markup is written with `starttag`**, which escapes attribute values, so a
  caption or equation number holding markup characters reaches the page escaped (FR-020).

### The toctree in a page

`SiteNavigation.decorate_list` and `decorate_item` already do what story 2 needs: the classes
the menu styles read, the toggle with its translated, escaped name, and the open state from a
level count. They read nothing from the instance but each other, so they become methods of a
small class the site navigation and the mixin both call, and nothing is copied. With
`show_nav_level` at 2 the first two levels are open (`depth < show_nav_level - 1`). The menu's
styles in `assets/frame.css` and the toggle script in `navigation.js` are not scoped to the
sidebar, so they apply to the toctree in a page as they are. A hidden toctree resolves to nothing
in Sphinx itself.

### The page-body styles and `@scope`

`layout.html` on `main` writes `<article class="daisy-sphinx-content">` around the body. The
prototype's `@scope (.daisy-sphinx-content) to (.daisy-sphinx-escape)` scopes to it. `@scope`
is in Chrome 118, Safari 17.4 and Firefox 146 (December 2025), so the theme supports the browsers
released since then. The toctree in a page is drawn by the site navigation's rules, so the scope
also stops at `.toctree-wrapper`, which keeps the page body's list rules off it.

### Pygments

- Sphinx adds `pygments.css` to every page. It is removed from `css_files` on every page, whether
  or not a Pygments option is set: with a style set for one mode, Sphinx's stylesheet would
  otherwise colour the other mode's code and mix into the token highlighting.
- The styles are written at `builder-inited` into `_static/styles/pygments-modes.css` in the
  output, and linked with `app.add_css_file`. `builder-inited` runs once per build in the main
  process, before any page is written, so incremental and parallel builds see the same file.
  Sphinx's own bridge, `PygmentsBridge.get_stylesheet`, takes one style and no selector, so it
  cannot key a style on a mode.
- `main` has no mode attributes on `<html>` yet. The logo picks its mode from
  `prefers-color-scheme`. The modes feature (#7) adds `data-mode` on `<html>` with the mode the
  page shows. Each style is written twice: under `html[data-mode="<mode>"]`, and under
  `html:not([data-mode])` inside the matching `prefers-color-scheme` query, so it follows the
  system until that feature lands and the page's mode once it does.
- A mode with a style starts its rules by resetting the token colours on `.highlight` spans, and
  every rule carries more specificity than the token rules, so the token highlighting does not
  mix in.

### The admonition icons

`assets/content.css` in the prototype draws each kind's icon as a CSS mask over a data URI, a
second copy of Lucide's icons. The mixin writes the icon into the title as inline SVG from
`ICONS`, the same way the frame draws every other icon, and the stylesheet sizes and colours it.
The icons the kinds need are added to the icon script's Lucide list and `icons.json` is
regenerated. The tick of a task list's checkbox is drawn with CSS, as daisyUI's own `checkbox`
draws it, since it is not an icon of a kind.

### The kitchen sink

The pages, `docs/_ext/palette.py` and the extensions come across from the prototype as the
planning notes list. sphinx-design and sphinx-copybutton join the `docs` dependency group only.
The pages keep their paths, `docs/kitchen-sink/`, so the same addresses exist on both builds.

## What already exists

- Scroll regions for tables and equations: new code, in the translator mixin. Sphinx writes no
  wrapper and no installed package adds one.
- Naming heading links: new code. Sphinx writes a `title` only.
- The attribution's space: new code, a two-line override of Sphinx's visitor.
- Admonition and version-note icons: this repo, `ICONS.svg`.
- The toctree in a page: this repo, `SiteNavigation`'s decoration, moved into a class both use.
- The toggle's script and styles: this repo, `navigation.js` and `assets/frame.css`.
- The section label: this repo, `.daisy-section-label`.
- Dimmed text and lines: this repo, `--daisy-text-muted` and `--daisy-border` in
  `assets/tokens.css`.
- Pygments styles under a selector: Pygments, `HtmlFormatter.get_style_defs`.
- Installing a translator mixin: pydata-sphinx-theme's pattern, written for this theme.
- The page-body look: the prototype's `assets/content.css` and `frame.css:228-296`, ported.
