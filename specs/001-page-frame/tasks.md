# Tasks: Arrange the page and fill it from conf.py

**Input**: `spec.md`, `plan.md`, `research.md`, `planning-notes.md` in `specs/001-page-frame/`.
The prototype is the `prototype-theme` branch; "port" means copy across and clean to `main`'s
standards, never redraw.

**Tests**: test-first for every behaviour (`docs/contributing/standards/testing.md`). No test of
wording, layout, widths or design choices. Template and page tests live in `tests/test_templates/`,
declared as a non-mirror path.

## Phase 1: Foundational

- [ ] T001 Add the test sites `tests/roots/test-pages/` (three pages in order under a toctree,
  one in a subdirectory) and `tests/roots/test-logo/` (`_static/` with two images), declare
  `tests/test_templates/` under `[tool.forge.conformance] non-mirror-paths` in `pyproject.toml`,
  and add `markupsafe` to `dependencies`.
- [ ] T002 Port `src/sphinx_daisyui/icons.json` and `scripts/icons.mjs`, add `lucide-static`,
  `simple-icons` and an `icons` script to `package.json`, and add `Icons` in
  `src/sphinx_daisyui/icons.py` with `tests/test_icons.py`.

## Phase 2: User Story 1 - A site author arranges the page and fills it with components (P1)

### Group 1

- [ ] T003 [US1] `LayoutCode` and `LayoutCodeError` in `src/sphinx_daisyui/layout.py`, with
  `tests/test_layout.py`: the default, every valid shape, sticky flags from case only, the medium
  arrangement, spaces and mixed case, wrong letters, missing and extra groups, non-string values.
- [ ] T004 [US1] `ThemeOptions` in `src/sphinx_daisyui/options.py`, with `tests/test_options.py`:
  `text`, `flag`, `mapping`, `components` (list, comma string, with and without `.html`, empty),
  `layout`.
- [ ] T005 [US1] `check_layout` on `builder-inited` in `src/sphinx_daisyui/__init__.py`: a code of
  the wrong shape logs one error naming `layout`, quoting the code and stating the rules, and
  raises `SystemExit(2)` before any page is written, with no traceback. Tests in
  `tests/test_init.py`.
- [ ] T006 [US1] `add_page_context` on `html-page-context` setting `daisy` (layout, icon, version,
  repository from package metadata, the component lists, `secondary`), and the options of this
  feature declared in `theme/daisyui/theme.toml` with the prototype's defaults. Tests in
  `tests/test_init.py`.

### Group 2

- [ ] T007 [US1] Port `layout.html` (the frame: header, primary, main, secondary, footer, the
  grid's style and `data-*` markers) and add `components/macros.html` (`components`,
  `icon_button`). Tests in `tests/test_templates/test_layout.py`: the areas and markers for the
  default and another code, components in order, a site template drawn, an unknown name drawing
  nothing, an empty list, a component in two lists, `navbar_end` once in the HTML, singlehtml
  builds.
- [ ] T008 [US1] Port `copyright`, `sphinx-version`, `theme-version`, `last-updated` and a
  title-only `navbar-logo` into `components/`, escaping every value. Tests in
  `tests/test_templates/test_components.py`: each honours its Sphinx setting, the default lists
  give the title link and the three footer components, the theme's address and version come
  from the metadata, a site author's text reaches the page escaped.
- [ ] T009 [US1] Port `assets/frame.css` (`:1-4`, `:18-127`, `:301-308`) and the prototype's
  `assets/theme.css`, add `assets/tokens.css` with the dimmed text and border properties, and
  rebuild the stylesheet.
- [ ] T010 [US1] Documentation: `docs/reference/options.md`, `docs/reference/components.md`,
  `docs/reference/layout-code.md` (letter by letter), `docs/developer/arrange-the-page.md`, the
  toctrees, `docs/index.md`'s features, README, CHANGELOG. Port `docs/conf.py`'s own options
  and `DAISY_LAYOUT`, and `scripts/serve.sh`, `prebuild.sh`, `variants.sh` with the four layout
  builds. The docs build clean with `-W`.

## Phase 3: User Story 2 - A reader reads a page on any screen (P1)

### Group 3

- [ ] T011 [US2] The skip link to `#main-content`, the named landmarks (one `main`), the five
  `data-daisy-*` attributes on `<body>`, and the secondary sidebar left out when empty and on
  the search and index pages. Tests in `tests/test_templates/test_layout.py`.
- [ ] T012 [US2] The message catalogue: `app.add_message_catalog("sphinx", …)` in `setup()`,
  every fixed text in the templates marked with `_()` or `{% trans %}`,
  `src/sphinx_daisyui/locale/sphinx.pot`, `scripts/messages.sh`. Tests: a site with a language
  and a compiled catalogue gets the translated skip link, and the shipped template lists every
  message the templates mark.
- [ ] T013 [US2] Page scripts `keys.js` and `frame.js` in `theme/daisyui/static/scripts/`,
  loaded from `layout.html`: the scrolled mark, the header's measured height, the drawer closing
  on Escape and on a link, `navbar_end` moved into the drawer below the `sm` width and back.
  Test that each page links both scripts. Behaviour checked in headless Chrome.
- [ ] T014 [US2] Documentation: the custom properties and `<body>` attributes in
  `docs/reference/layout-code.md`, CHANGELOG.

## Phase 4: User Story 3 - A site author shows the site's logo (P2)

### Group 4

- [ ] T015 [US3] `ThemeOptions.static_url` and `Brand` in `src/sphinx_daisyui/brand.py`, with
  `tests/test_brand.py` and `tests/test_options.py`: each part of `logo`, `html_logo` only,
  a light image only, `_static` relative, `_static/` prefixed and full addresses, the hidden name
  and its alternative text, `logo.text` with empty alternative text, `logo.link`.
- [ ] T016 [US3] `navbar-logo` with the logos (port), the brand at the head of the primary
  sidebar when the code gives it the top-left corner, the frame's logo-per-mode rules with the
  `prefers-color-scheme` fallback, and `docs/_static/logo-light.svg` and `logo-dark.svg` used by
  `docs/conf.py`. Tests in `tests/test_templates/test_brand.py`: addresses from a page at any
  depth, escaping, which copy carries the wide-screen marker.
- [ ] T017 [US3] Documentation: the logo options in the reference and the how-to, CHANGELOG.

## Phase 5: User Story 5 - A reader moves to the previous or next page, or back to the top (P2)

### Group 5

- [ ] T018 [US5] The previous and next links (port `layout.html:126-141`) and `show_prev_next`.
  Tests: both links with titles and `rel`, first and last page, switched off, search and index
  pages, a title with markup, an escaped address.
- [ ] T019 [US5] The back-to-top button (port `layout.html:169-171`), `back_to_top_button`, and
  `back-to-top.js`. Tests: present by default, absent when switched off. Behaviour checked in
  headless Chrome.
- [ ] T020 [US5] `navigation_with_keys` through Sphinx's own handler: a test that the option
  reaches `DOCUMENTATION_OPTIONS` on and off. Documentation and CHANGELOG.

## Phase 6: User Story 4 - A site author puts an announcement across every page (P3)

### Group 6

- [ ] T021 [US4] The announcement banner (port `layout.html:37-43`): text and the site author's
  HTML printed as markup, a URL in an escaped attribute for `announcement.js`, a named region
  before the header. Tests: none, text, HTML, URL.
- [ ] T022 [US4] `sticky_banners`: the banner inside the header area when on. Tests on and off.
  Fetch behaviour (success, failure, empty) checked in headless Chrome.
- [ ] T023 [US4] Documentation and CHANGELOG.

## Phase 7: Own options

- [ ] T030 [US3] Drop `light_logo`, `dark_logo`, `sidebar_hide_name` and `logo_link` from the
  theme, its tests, its documentation and the docs site's own configuration, so the logo is
  `logo` only, with `html_logo` as the fallback (decisions D15).
