# Tasks: Find the way around the site and the page

**Input**: `spec.md`, `plan.md`, `research.md`, `planning-notes.md` in `specs/002-navigation/`.
The prototype is the `prototype-theme` branch; "port" means copy across and clean to `main`'s
standards, never redraw.

**Tests**: test-first for every behaviour (`docs/contributing/standards/testing.md`). No test of
wording, CSS classes chosen for looks, layout, widths or design choices. Template and page tests
live in `tests/test_templates/`.

## Phase 1: Foundational

- [ ] T001 `ThemeOptions.number` and `ThemeOptions.records` in `src/sphinx_daisyui/options.py`,
  with tests in `tests/test_options.py`; the nine options of this feature in
  `theme/daisyui/theme.toml` with the spec's defaults; `docutils` in `dependencies`.

## Phase 2: User Story 1 - A reader moves through the whole site from the primary sidebar (P1)

### Group 1

- [ ] T002 [US1] The test site `tests/roots/test-nav/` (five levels, a caption, a second
  toctree, a hidden toctree, an external entry, an orphan, a title with markup and `&`), and
  `CurrentLink` and `SiteNavigation.menu` in `src/sphinx_daisyui/navigation.py`, registered in
  `setup()`. Tests in `tests/test_navigation.py`.
- [ ] T003 [US1] `daisy.navigation` in `events.py` and the ported `components/sidebar-nav.html`.
  Tests in `tests/test_templates/test_sidebar_nav.py`: US1 scenarios 1-4 and 6-10, 13 and 14,
  the orphan, `dirhtml`, `singlehtml`, digit strings.
- [ ] T014 [US1] A contributor page on how the theme is built, naming its Python, and the test
  sites' `copyright` exempt from the builtin-shadowing lint.

### Group 2

- [ ] T011 [US1] A component list and `external_links` take a Python list only: `ThemeOptions.components`
  and `records` read no string form, `theme.toml` defaults become arrays, and FS-001's FR-006 and
  `docs/reference/options.md` say so. Tests first in `tests/test_options.py`.
- [ ] T004 [US1] Port the site navigation styles and `.daisy-section-label` into
  `assets/frame.css` and `navigation.js` into `theme/daisyui/static/scripts/`, with its script
  tag in `layout.html`. Rebuild the stylesheet. Check the toggles and scrolling into view in
  headless Chrome.
- [ ] T005 [US1] Port `components/breadcrumbs.html`. Tests in
  `tests/test_templates/test_breadcrumbs.py`: US1 scenarios 11, 12 and 14, the orphan.
- [ ] T006 [US1] Translation: `scripts/messages.ini` extracts the theme's Python, the catalogue
  template is regenerated, and tests in `tests/test_templates/test_translation.py` cover the new
  text. Documentation of the US1 options and components, and CHANGELOG.
- [ ] T015 [US1] Group the parent-markup breadcrumb test in a class and wrap a long test line.

## Phase 3: User Story 3 - A reader finds their place on the page (P1)

### Group 3

- [ ] T012 [US3] `secondary_sidebar_items` reaches the templates under its own name: it joins the
  component options in `events.py`, the `secondary` key goes, and `layout.html` and the tests read
  it by name (issue 47).
- [ ] T013 [US3] The secondary sidebar and the On this page disclosure are left out on every index
  page: search, `genindex` and its split pages, and the domain indices such as `py-modindex`.
  Tests with a split index and a Python domain index (issue 44).
- [ ] T007 [US3] `PageContents` in `navigation.py`, `daisy.page_toc`, `page_toc_count` and
  `show_toc_level`, the ported `components/page-toc.html` and the disclosure in `layout.html`.
  Tests in `tests/test_navigation.py` and `tests/test_templates/test_page_toc.py`: US3 scenarios
  1, 2, 5 (the depth markers), 6 (the disclosure's presence and closed state), 7 and 9.
- [ ] T008 [US3] Port the On this page styles and `page-toc.js`, with its script tag. Check
  scenarios 3, 4, 5, 6 and 8 in headless Chrome. Documentation of `show_toc_level` and
  `page-toc`, and CHANGELOG.

## Phase 4: User Story 2 - A site author puts the site's sections in the header (P2)

### Group 4

- [ ] T009 [US2] The test site `tests/roots/test-sections/` (six top-level sections, a home page
  in no section, `external_links`, `navbar-nav` in `navbar_center`), `SiteNavigation.section_menu`
  and `top_level`, `HeaderLinks`, `daisy.sectioned`, `daisy.header`, `daisy.navbar_align`, the
  ported `components/navbar-nav.html` and the sections at the head of the drawer. Tests: US2
  scenarios 1-6 and 8-11 and the edge cases on `header_links_before_dropdown`.
- [ ] T010 [US2] `navbar_align` styles, Escape closing the header menu in `navigation.js`, a
  `navbar-nav` build in `scripts/variants.sh`, documentation of the US2 options and component
  and a page in `docs/developer/`, CHANGELOG. Check scenarios 3 and 7 in headless Chrome.
- [ ] T016 [US2] Header links mark the current section with `aria-current="true"`, since the
  link leads to the section, not the page being read. Wrap a long line in `docs/conf.py`.
