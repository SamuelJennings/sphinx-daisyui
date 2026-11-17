# Implementation Plan: Find the way around the site and the page

**Branch**: `002-navigation` | **Date**: 2026-11-17 | **Spec**: `spec.md` | **Research**:
`research.md`

## Summary

The theme gets its site navigation, breadcrumbs, header links and On this page, ported from the
accepted prototype on `prototype-theme` (features 2, 13 and 4). The components, the navigation
and On this page styles, and the page script's sections are the prototype's, cleaned to `main`'s
standards. The Python behind them is rebuilt test-first: it reads Sphinx's toctree and the page's
headings as docutils nodes, changes them, and renders them once, so nothing is parsed from HTML
and no runtime dependency is added.

## Technical context

- **Language and stack**: Python 3.11+, Sphinx 7.4+, Jinja templates, Tailwind CSS 4 and
  daisyUI 5 compiled by npm at build time.
- **New runtime dependencies**: none. `docutils` is imported directly for the first time, so it
  is declared in `dependencies` (Sphinx already requires it), and `deptry` passes.
- **Testing**: pytest with `sphinx.testing`, test sites under `tests/roots/`. Behaviour that
  needs a browser (toggles, scrolling the current entry into view, marking the heading being
  read, the disclosure closing, the header menu from the keyboard) is checked in headless Chrome
  while building and at the browser pass.

## Constitution check

- **I, IV**: every behaviour is tested by building a real site and reading its pages.
- **V**: every printed value is escaped. Toctree titles stay Sphinx's markup. Header link titles
  are the plain text of the entry, escaped by the template. The toggle's name is built with
  `Markup.format`, which escapes the title.
- **VI**: every new option is in `theme.toml` and `docs/reference/options.md`, every component in
  `docs/reference/components.md`.
- **VII**: no new runtime dependency. `docutils` is declared because it is imported.
- **VIII**: the fixed text is marked for translation, in templates with `_()` and in Python with
  `translate = get_translation("sphinx")`, and `scripts/messages.sh` extracts both.
- **IX**: the Python is grouped in classes: `SiteNavigation`, `PageContents`, `HeaderLinks`.
- **XIV**: every control is a button or a link with a visible focus state. Dimmed text reads
  `--daisy-text-muted`, whose contrast #4 checks.

## Python

`src/sphinx_daisyui/navigation.py`:

- **`CurrentLink`**, a `nodes.reference` subclass with an HTML visitor that writes
  `<a class="…" href="#" aria-current="page">`. Registered in `setup()` with `app.add_node`.
- **`SiteNavigation`**, built once per page from `global_toctree_for_doc(env, pagename,
  builder, collapse, includehidden, maxdepth, titles_only=True)`.
  - `menu(show_nav_level)`: the whole tree as Markup. Lists get `daisy-nav-list`, entries
    `daisy-nav-item`, links `daisy-nav-link`, captions `daisy-section-label daisy-nav-caption`.
    The current page's link becomes a `CurrentLink` with `menu-active`, links on its path get
    `daisy-on-path`, external links get `daisy-external`, the external-link icon and a visually
    hidden "(leads outside the site)". An entry with pages under it gets `daisy-nav-branch` and a
    toggle from `add_toggle`.
  - `add_toggle(item, is_open)`: appends a `raw` button after the entry's link:
    `button.daisy-nav-toggle.btn.btn-ghost.btn-xs.btn-square`, `aria-expanded`, named "Show the
    pages in {title}", holding the `chevron-right` icon. A branch is open when it is on the
    current page's path or its depth is below `show_nav_level - 1`.
  - `section_menu(show_nav_level)`: the child list of the current top-level entry, decorated the
    same way, or empty Markup when the page is in no section.
  - `top_level()`: one `HeaderLink` per level-one entry: plain-text title, address, whether it
    is current.
  - No toctree (`None`, or the `singlehtml` builder) gives empty menus and no links.
- **`HeaderLinks`**: the top-level links followed by `external_links` (each marked external),
  split at `header_links_before_dropdown` into `shown` and `more`, with `more_text` from
  `header_dropdown_text` (translated "More" when unset) and `more_current`.
- **`PageContents`**, from `document_toc(env, pagename, builder.tags)`: drops the page's own
  title, gives the list as Markup with `daisy-toc-list` lists and `daisy-toc-link` links, and
  marks each nested list deeper than `show_toc_level` with `daisy-toc-deep`. `count` is the
  number of headings. Empty on search and genindex.

`src/sphinx_daisyui/options.py` gains `number(name, default)` (an int, or a string of digits,
otherwise the default) and `records(name)` (a list of dicts, or the list a JSON string holds).

`src/sphinx_daisyui/events.py` sets in `daisy`: `navigation`, `sectioned` (`navbar-nav.html` in
`navbar_center`), `header` (the `HeaderLinks`), `navbar_align`, `page_toc`, `page_toc_count`,
`show_toc_level`. With `sectioned`, `navigation` is the section menu.

## Templates

Ported from the prototype into `theme/daisyui/components/`: `sidebar-nav.html`,
`breadcrumbs.html`, `page-toc.html`, `navbar-nav.html`, each escaping what it prints and reading
only `daisy`. Into `layout.html`: the sections at the head of the drawer (prototype
`layout.html:82-90`), the On this page disclosure above the article (`:116-121`), a
`data-navbar-align` marker on the header's centre slot, and the two script tags.

## Styles

Ported into `assets/frame.css`: the site navigation (prototype `frame.css:129-176`), with the
row's rules on `.daisy-nav-branch`, closed lists hidden by `:has()`, and On this page
(`:178-201`), with `.daisy-toc-deep` shown only inside the section being read. One
`.daisy-section-label` rule for the captions and On this page's label. `navbar_align` rules for
the centre slot.

## Scripts

Ported into `theme/daisyui/static/scripts/`: `navigation.js` (the toggles, scrolling the current
entry into view inside the primary sidebar, Escape closing the header links' menu) and
`page-toc.js` (marking the heading being read with a class and `aria-current="location"`, the
foot of the page marking the last heading, showing deeper headings in the section being read,
the disclosure closing when a heading is followed).

## Documentation

`docs/reference/options.md` and `docs/reference/components.md` gain every option and component
with its default. `docs/developer/` gains a page on the site navigation and header links.
`scripts/variants.sh` gains a build with `navbar-nav` in `navbar_center`, for the side-by-side
check. CHANGELOG under Unreleased.

## Dispatch

Four groups, one at a time, in one worktree: US1 in two groups, US3, then US2. Each is a Sonnet
Implementer.
