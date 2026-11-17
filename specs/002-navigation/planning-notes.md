# Planning notes: 002-navigation

Notes for research and planning. Each is answered by name before the build starts.

## The prototype

This feature is built from the accepted prototype on the `prototype-theme` branch. Read
`PROTOTYPE.md` on that branch whole, then its features 2 (site navigation), 13 (header links) and
4 (on this page). The prototype is served at http://localhost:8062/ while it is being compared.
Its screens and the maintainer's decisions in its "Decisions" section are agreed. "Which decisions
bind which feature" binds this feature twice: the default follows Furo, with the whole tree in
the primary sidebar (2), and putting `navbar-nav` in `navbar_center` switches to the sectioned
layout (13).

## No design review at the plan stage

The prototype is the design. The plan goes straight to tasks with no separate design review.

## The look: ported, never redrawn

Port means copy across and clean to `main`'s standards. These rows of "The look" belong to this
feature:

| Prototype file | What this feature takes | Lands in `main` at |
|---|---|---|
| `theme/daisyui/components/sidebar-nav.html`, `breadcrumbs.html` | All (2) | `theme/daisyui/components/` |
| `theme/daisyui/components/page-toc.html` | All (4) | `theme/daisyui/components/` |
| `theme/daisyui/components/navbar-nav.html` | All (13) | `theme/daisyui/components/` |
| `theme/daisyui/layout.html` | `:82-90`, the sections at the head of the drawer (13), and `:116-121`, the On this page disclosure above the page (4), into the frame #4 ports | The same path |
| `theme/daisyui/theme.toml` | The options `navigation_depth`, `show_nav_level`, `collapse_navigation`, `sidebar_includehidden` (2), `external_links`, `header_links_before_dropdown`, `header_dropdown_text`, `navbar_align` (13), `show_toc_level` (4) | The same path |
| `static/scripts/sphinx-daisyui.js` | `:67-87`, the toggles and scrolling the current entry into view (2; `:88-90` is the drawer's, ported by #4), and `:92-125`, marking the heading being read and closing the disclosure (4) | `theme/daisyui/static/scripts/`, one module per feature |
| `assets/frame.css` | `:129-176`, the site navigation (2), and `:178-201`, On this page (4) | `assets/`, beside the frame's files as #4's plan lays them out |
| `src/sphinx_daisyui/__init__.py` | `navigation_markup` (2), `page_toc` (4), `header_links` (13), and their `daisy` keys in `on_page_context`: `navigation`, `header_links`, `header_more`, `header_more_text`, `sectioned`, `page_toc`, `page_toc_count`, `show_toc_level` | `src/sphinx_daisyui/`, grouped in classes (Article IX) |

Each merge is checked side by side against the prototype on the pages in "Pages to compare side
by side" whose rows name features 2, 4 or 13, at 390, 1100 and 1440 pixels wide: Home with the
drawer open, Typography, A toctree in a page, A deep page, Tall secondary sidebar, and As
pydata-sphinx-theme.

## The shared pieces this feature builds

From "The shared pieces" in `PROTOTYPE.md`. Each is built once here and reused by the features
named.

- **A branch that opens and closes.** One Python method that adds the row and toggle to a list
  item, one CSS rule set for `.daisy-nav-row` and `.daisy-nav-toggle`, one script module. Built
  here for the site navigation (prototype `__init__.py:194-212`, `frame.css:144-176`,
  `sphinx-daisyui.js:71-78`). Reused by the page-body styles for a toctree in a page (#6,
  prototype `__init__.py:276-298`, `content.css:660-724`). Check first: daisyUI's collapsible
  `menu` uses `<details>`, which can't keep the entry a link. A button beside the link stays.
- **Reading Sphinx's toctree output.** One class that reads a toctree once and gives the menu, the
  top-level links and the page's headings. Built here for the site navigation, and used here by
  On this page and the header links. Reused by the page-body styles for a toctree in a page (#6).
  The prototype parses with BeautifulSoup at `__init__.py:168`, `226`, `245` and `271`, and renders
  the site toctree twice per page at `:485-486`. Check first: Sphinx's `toctree()` arguments, and
  docutils' doctree in place of re-parsing HTML where it is reachable (see `research.md`).
- **The site-navigation component under three names.** One component. The other names include it.
  Built here as `sidebar-nav.html`. Reused by the Furo configurations (`sidebar/navigation.html`)
  and the pydata-sphinx-theme configurations (`sidebar-nav-bs.html`), both #8. Check first:
  nothing.
- **Section label.** One CSS class, for the site navigation's captions (prototype
  `frame.css:134-142`) and On this page's label (`page-toc.html:3`). Reused by the page-body
  styles for a toctree's caption in a page (#6, `content.css:648-654`), and by the layout
  playground on the Layout page (`layout-playground.css:7`, documentation work). Check first:
  nothing.

## The shared pieces this feature reuses

- **From #4**: component list placement, `ThemeOptions`, Icons, the square icon button, and dimmed
  text and surfaces. The toggles' dimmed colour and the navigation's dimmed text use the dimmed
  text properties, so their contrast is checked where #4 checks it.
- **The navbar dropdown macro** is built by #7 (modes and daisyUI themes). The header links'
  overflow menu uses daisyUI's `dropdown` directly here, and #7 folds it into the macro, whichever
  merges second.

## What the prototype faked that this feature does properly

From "Faked or skipped" in `PROTOTYPE.md`:

- **`navbar_align` only partly honoured.** The prototype approximates `content` with a fixed
  inset (`layout.html:64`) and reads `theme_navbar_align` directly. Line the header links up with
  the page column's start, as pydata-sphinx-theme does (FR-011), and read the option through the
  page context (FR-023).
- **`beautifulsoup4` as a runtime dependency with no stated reason.** This is the first feature
  that needs it. Either justify it, with the reason recorded where Article VII asks, or replace it
  with docutils' doctree (FR-021). `research.md` records that Sphinx's
  `global_toctree_for_doc` returns docutils nodes before they are rendered to HTML, and that the
  page's `doctree` reaches the `html-page-context` handler, so the doctree route is reachable on
  Sphinx 9.2. Confirm it on the oldest Sphinx `main` supports (7.4). The page-body styles (#6)
  read the same decision for the page body.
- **Escaping.** Every value printed is escaped per amended Article V (constitution 1.1.0 on
  `main`). The prototype prints `link.href` and `link.title` unescaped in `navbar-nav.html` and
  `layout.html:86`, and builds the toggle's name with an f-string from the entry's text
  (`__init__.py:205`). Toctree titles are Sphinx's own markup and stay markup (FR-018).
- **Translation.** The theme's fixed text here is marked for translation in the message catalogue
  #4 sets up: the landmark names ("Documentation", "Breadcrumb", "Sections"), the home crumb's
  name, the toggles' names, "On this page" and its disclosure, and the default of
  `header_dropdown_text` (FR-019).

## What the prototype does that the spec settles

- **`show_toc_level`.** The prototype only tells level 1 from the rest (`frame.css:185`). The spec
  takes pydata-sphinx-theme's meaning, deeper headings shown while the reader is in their section
  (FR-016). Research confirms how pydata-sphinx-theme shows them before it is built. The default
  stays 2, as on the prototype's screens.
- **The heading being read, for a screen reader.** The prototype marks it with a class only. The
  spec asks for a mark assistive technology reads too (FR-015, Article XIV). The same holds for
  external entries (FR-006).
- **The disclosure's script** is in the prototype at `sphinx-daisyui.js:97` and the marking reads
  `.daisy-secondary` (`:96`). Both are ported with On this page.
