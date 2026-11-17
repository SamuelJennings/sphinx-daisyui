# Plan: Draw page bodies with daisyUI tokens

**Inputs**: `spec.md`, `research.md`, `planning-notes.md`, `decisions.md`, and the accepted
prototype on `prototype-theme` (`PROTOTYPE.md`, feature 3).

## Approach

The body is changed as Sphinx writes it, by a translator mixin, and drawn by a stylesheet ported
from the prototype. Nothing parses the written HTML.

- **`src/sphinx_daisyui/body.py`** holds `PageBodyTranslator`, a mixin over Sphinx's HTML
  translator, and `install_translator`, connected to `builder-inited`, which builds the class
  from the mixin and each HTML builder's translator, as pydata-sphinx-theme does. It is installed
  only when the site's theme is `daisyui`. It writes the scroll regions round outermost tables and
  display equations' notation, names heading links, spaces the attribution, puts each
  admonition's and version note's icon in from `ICONS`, and decorates a toctree in a page.
- **The toctree in a page** reuses the site navigation's decoration. `decorate_list`,
  `decorate_item` and their helpers move from `SiteNavigation` into a `NavigationMenu` class in
  `navigation.py` that `SiteNavigation` and the mixin both use, with the first two levels open.
- **`src/sphinx_daisyui/pygments.py`** holds `PygmentsStyles`, which reads the two options once at
  `builder-inited`, warns on a name Pygments does not know, writes
  `_static/styles/pygments-modes.css` for the modes that have a style and links it. Sphinx's
  `pygments.css` is removed from every page in the page context.
- **`assets/content.css`** is the prototype's, ported: scoped with `@scope (.daisy-sphinx-content)
  to (.daisy-sphinx-escape, .toctree-wrapper)`, its dimmed text and lines on `--daisy-text-muted`
  and `--daisy-border`, its icon masks replaced by rules for the inline SVG, its toctree and
  caption rules dropped for the site navigation's. sphinx-copybutton's button and sphinx-design's
  colour variables (`frame.css:228-296` in the prototype) join it. `assets/theme.css` imports it
  and gains the `@source inline` list of daisyUI components for raw HTML.
- **The kitchen sink** comes across whole: `docs/kitchen-sink/`, `docs/_ext/palette.py`, and the
  extensions in `docs/conf.py`, with sphinx-design and sphinx-copybutton in the `docs` group.

## Packages and tools

- No new runtime dependency. Pygments comes with Sphinx and is declared as a dependency, since
  the theme imports it.
- sphinx-design and sphinx-copybutton in the `docs` dependency group only (D6).
- `lucide-static`, already a development dependency, supplies the new icons through `npm run
  icons`.

## The planning notes, answered

- **The prototype**: read whole. Its decisions bind the stylesheet port and the toctree in a page.
  Adopted.
- **No design review at the plan stage**: adopted. The prototype is the design.
- **The look: ported, never redrawn**: adopted, with two changes the notes ask for. The icons are
  inline SVG from the icon set rather than masks over data URIs, and the toctree and caption
  rules are the site navigation's. The copy button and sphinx-design rules go into
  `assets/content.css`, beside the rest of the page body.
- **A branch that opens and closes**: adopted. The toctree in a page uses the site navigation's
  decoration, styles and script. A button beside the link stays, since daisyUI's `<details>` menu
  cannot keep the entry a link.
- **Reading Sphinx's toctree output**: adopted. Sphinx resolves a toctree in a page into nodes
  before it is written, and the mixin decorates those nodes, as ADR 0001 decided.
- **Section label**: adopted. A caption gets `daisy-section-label`, as in the sidebar.
- **Dimmed text and surfaces**: adopted. The page body's own muted properties go and the frame's
  are used.
- **The mode attributes**: adopted as far as they exist. `main` has none yet, so each style keys
  on `data-mode` and, while it is absent, on `prefers-color-scheme` (research, Pygments).
- **Icons**: adopted. The admonition and version-note icons and the toggle's chevron come from
  `ICONS`.
- **The admonition icons as data URIs**: removed, as above.
- **Escaping**: adopted. Region names go through `starttag`, which escapes them, and the toggle's
  name through the site navigation's `Markup.format`.
- **Translation**: adopted. "Table", "Equation" and "Equation %(number)s" are marked for
  translation and the catalogue template is regenerated.
- **Where the page body is rewritten**: a translator mixin, at write time (research). No part
  needs the HTML.
- **The element the page-body styles are scoped to**: `article.daisy-sphinx-content` from the
  page frame. `@scope` holds in Chrome 118, Safari 17.4 and Firefox 146, which becomes the
  documented support target.
- **Where the Pygments stylesheet is written**: at `builder-inited`, once per build, before any
  page is written. Sphinx's bridge takes no selector, so it cannot key a style on a mode.

## Tasks in brief

1. The translator mixin, its test site and the pygments.css removal (story 1, group 1).
2. The kitchen sink pages and the documentation site's extensions (story 1, group 2).
3. The page-body stylesheet, ported, with the icons from the icon set (story 1, group 3).
4. The toctree in a page on the site navigation's decoration (story 2, group 4).
5. The Pygments options and the escape class, with their documentation (story 3, group 5).

## Cost

Five dispatches on Sonnet, one review. Expected within the soft budget.
