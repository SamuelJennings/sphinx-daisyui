# Planning notes: 003-page-body-styles

Notes for research and planning. Each is answered by name before the build starts.

## The prototype

This feature is built from the accepted prototype on the `prototype-theme` branch. Read
`PROTOTYPE.md` on that branch whole, then its feature 3 (page-body styles). The prototype is
served at http://localhost:8062/ while it is being compared. Its screens and the maintainer's
decisions in its "Decisions" section are agreed. "Which decisions bind which feature" lists the
ones that bind feature 3: article-info items on one line, a thin space after a quotation's dash,
lists more compact (4px between one-line items, wider only when an item holds several blocks), a
toctree in a page drawn as the sidebar's menu with its first two levels open, the page named
Admonitions after the directive, and code highlighted from the tokens with Pygments' own
stylesheet dropped unless a Pygments style is set.

## No design review at the plan stage

The prototype is the design. The plan goes straight to tasks with no separate design review.

## The look: ported, never redrawn

Port means copy across and clean to `main`'s standards. These rows of "The look" belong to this
feature:

| Prototype file | What this feature takes | Lands in `main` at |
|---|---|---|
| `assets/content.css` | All of it, cleaned as the notes below say: the admonition icons from the icon set, the dimmed-text properties from the frame's shared set, the toctree menu rules and the section label from the site navigation's | `assets/content.css`, imported from `assets/theme.css` |
| `assets/theme.css` | Its `@source inline` list (`:8`): the daisyUI components compiled in for raw HTML | `assets/theme.css`. The list is documented for sites (FR-018), so the plan settles which components it holds |
| `assets/frame.css` | `:228-296`: sphinx-copybutton's button, and sphinx-design's colour variables mapped onto the tokens | `assets/`, beside `content.css` or inside it, as the plan decides |
| `src/sphinx_daisyui/__init__.py` | `rewrite_body` (`:258-328`), the Pygments half of `on_builder_inited` (`:577-590`), and the `pygments.css` filter in `on_page_context` (`:510-513`) | `src/sphinx_daisyui/`, grouped in a class (Article IX) |
| `theme/daisyui/theme.toml` | `pygments_light_style`, `pygments_dark_style`, `pygment_light_style`, `pygment_dark_style` | The same path |
| `docs/kitchen-sink/` | Every page: typography, admonitions, code, tables, lists, media, design, api, the `deeper/` tree and `conf-snippet.py` | `docs/kitchen-sink/`, linked from the documentation's table of contents and moved into `main`'s documentation standard |
| `docs/_ext/palette.py` | All of it, the module the API page documents | `docs/_ext/palette.py` |
| `docs/conf.py` | The extensions and MyST settings the kitchen sink needs (`sphinx_design`, `sphinx_copybutton`, autodoc, viewcode, MathJax, MyST's `colon_fence`, `deflist`, `tasklist`, `dollarmath`, `fieldlist`, `substitution`) and the `_ext` path | `docs/conf.py`, with the extensions added to the `docs` dependency group |

Each merge is checked side by side against the prototype on the pages in "Pages to compare side
by side" whose rows name feature 3: Typography, Admonitions, Code, Tables, Lists, Pictures and
maths, sphinx-design, API reference, Source code page, Index, and A toctree in a page, at 390,
1100 and 1440 pixels wide, in light mode, and in dark mode where the row says so.

## The shared pieces this feature reuses

From "The shared pieces" in `PROTOTYPE.md`. None is built here. Each is reused as the feature
named builds it.

- **A branch that opens and closes.** Built by site navigation (#5): "One Python method that adds
  the row and toggle to a list item, one CSS rule set for `.daisy-nav-row` and
  `.daisy-nav-toggle`, one script module." Reused here for the toctree in a page, which in the
  prototype repeats it at `__init__.py:276-298` and `content.css:660-724`. Check first: daisyUI's
  collapsible `menu` uses `<details>`, which can't keep the entry a link. A button beside the
  link stays.
- **Reading Sphinx's toctree output.** Built by site navigation (#5): "One class that reads a
  toctree once and gives the menu, the top-level links and the page's headings." Reused by On this
  page and header links (#5) and here, for the toctree in a page. Check first: Sphinx's
  `toctree()` arguments, and docutils' doctree in place of re-parsing HTML where it is reachable.
- **Section label.** Built by site navigation (#5): "One CSS class." Reused by On this page (#5)
  and here, for a toctree's caption in a page, which the prototype draws again at
  `content.css:648-654`.
- **Dimmed text and surfaces.** Built by the page frame (#4): "One set of custom properties in a
  base layer, used by the frame and the page body, so the contrast check of Article XIV is made in
  one place." Reused by every stylesheet. Here it replaces the page body's own
  `--daisy-sphinx-muted` and its neighbours (`content.css:29-47`).
- **The mode attributes.** Built by modes and daisyUI themes (#7): "One documented contract on
  `<html>`, with one function that applies a choice, used by both the inline script and the page
  script." Reused by the logo (#4), the Furo configurations (#8) and here, for the Pygments
  styles (`__init__.py:586` in the prototype). Until #7 lands, the Pygments styles key on the
  attributes the page frame writes. Check first: Sphinx's own `pygments_dark_style` in
  `theme.toml`, which keys on a media query rather than an attribute.
- **Icons.** Built by the page frame (#4): "An `Icons` class over the bundled JSON." Reused here
  for the admonition and version-note icons and the toggle's chevron.

## What the prototype faked that this feature does properly

From "Faked or skipped" and "Duplication to remove" in `PROTOTYPE.md`:

- **The admonition icons as data URIs** in `content.css:110-118`, a second copy of Lucide icons
  outside `icons.json`. The icon script writes them too (FR-021).
- **Escaping.** Every value the feature prints is escaped per amended Article V (constitution
  1.1.0 on `main`): caption and heading text in a region's or link's name, an entry title in a
  toggle's name (FR-020). The prototype builds the toggle's label with an f-string
  (`__init__.py:292`).
- **Translation.** The feature's own fixed text, the names of uncaptioned table and equation
  regions and of a toctree's toggles, is marked for translation in the message catalogue the page
  frame sets up (FR-019, Article VIII). The prototype writes it in English in Python.

## Questions for research

- **Where the page body is rewritten.** The prototype re-parses `body` with BeautifulSoup on every
  page in `html-page-context`. BeautifulSoup arrives as a runtime dependency with site navigation
  (#5), which states its reason (Article VII). Check first whether a docutils transform, a
  `doctree-resolved` handler or Sphinx's HTML translator can wrap tables and equations and name
  heading links at write time, and say which part, if any, still needs the HTML.
- **The element the page-body styles are scoped to.** The prototype scopes `content.css` with
  `@scope (.daisy-sphinx-content) to (.daisy-sphinx-escape)`, on an element in `layout.html` that
  the page frame (#4) ports. Confirm the class the frame's port writes, and that `@scope` holds in
  the browsers the theme supports. Record the support target if none is written down.
- **pydata-sphinx-theme's handling of an unknown Pygments style.** Confirm it warns and falls back
  (D5), and match the warning's shape.
- **Where the Pygments stylesheet is written.** The prototype writes `daisy-pygments.css` into the
  output directory at `builder-inited`. Check that this survives incremental builds and parallel
  writes, and whether Sphinx's own highlighter bridge can produce the styles instead.
