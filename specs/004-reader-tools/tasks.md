# Tasks: Theme, search and version tools in the header

**Input**: `spec.md`, `plan.md`, `research.md`, `planning-notes.md` in
`specs/004-reader-tools/`. The prototype is the `prototype-theme` branch; "port" means copy across
and clean to `main`'s standards, never redraw.

**Tests**: test-first for every behaviour (`docs/contributing/standards/testing.md`). No test of
wording, icons, CSS classes chosen for looks, layout, widths or design choices. Template and page
tests live in `tests/test_templates/`. Script behaviour is checked in headless Chrome.

## Phase 1: User Story 1 - A site author chooses the site's daisyUI themes and starting mode (P1)

### Group 1

- [ ] T001 [US1] `ThemeOptions.names`; `scripts/themes.mjs` writing `src/sphinx_daisyui/themes.json`
  from daisyUI's `themeOrder.js`, run by `npm run build`; `Modes` and `check_modes` in
  `src/sphinx_daisyui/modes.py`; the four options in `theme.toml`; `daisy.modes` in the page
  context. Tests: US1 scenarios 1-8 (the values reaching the page), the warning and its absence.
- [ ] T002 [US1] `static/scripts/mode.js`, loaded in `<head>` after the stylesheets with the
  site's values as escaped `data-` attributes on its element, and the `color-scheme` meta. Tests:
  the element's attributes and their escaping (scenario 10). In headless Chrome: the six
  attributes on `<html>` before the body is drawn, for each starting mode and each theme pair.

### Group 2

- [ ] T003 [US1] `navbar_dropdown` in `components/macros.html`; `navbar-nav.html`'s More menu on
  it with the same output; `navigation.js` binding `.daisy-dropdown`; `components/theme-switcher.html`
  ported on it; the logo rule on `data-mode` and the mode icon rules in `assets/frame.css`. Tests:
  US1 scenarios 1, 5-7, 9, 10, the duplicate picker name, translation of the menu's text.
- [ ] T004 [US1] Documentation: "Modes and themes" in the options reference, `theme-switcher` in
  the components reference, the attributes on `<html>` in the page reference, the guide
  `docs/developer/choose-the-themes.md`, `theme_picker` in `docs/conf.py`, CHANGELOG, the
  message catalogue template (scenario 11).

## Phase 2: User Story 2 - A reader switches mode or picks a theme (P1)

### Group 3

- [ ] T005 [US2] `static/scripts/theme-menu.js`: choices applied and stored through
  `sphinxDaisyui.mode`, the current one marked and named, the system followed in `auto`, the menu
  closed after a choice. In headless Chrome: US2 scenarios 1-9, two sites on one host, and the
  menu inside the drawer at 390.

## Phase 3: User Story 3 - A reader finds a page, section or API name from the search dialog (P1)

### Group 4

- [ ] T006 [US3] `keys.js` shortcuts that need Ctrl or ⌘; `static/scripts/page-address.js`;
  `enable_search_shortcuts = "false"` in `theme.toml`. In headless Chrome: the address of a page
  and an anchor for `html` and `dirhtml`, and a shortcut with and without the modifier.
- [ ] T007 [US3] `components/search-button-field.html` and `components/search-modal.html`
  ported, the dialog included once per page, `daisy.search` with its defaults. Tests: the dialog
  once on every page, the hooks the script reads, escaping, translation (scenarios 13, 18).
- [ ] T008 [US3] `static/scripts/search.js` and the search styles in `assets/frame.css`, the full
  search page on daisyUI tokens. A test site with pages, sections and API objects. In headless
  Chrome: US3 scenarios 1-12, 14, 16, 17 and the edge cases, and the dialog's results against
  the full search page's for a set of queries (SC-003).

## Phase 4: User Story 4 - A site author sets up search or leaves it out (P2)

### Group 5

- [ ] T009 [US4] `search_bar_text`, `disable_search` and `search_as_you_type` in `theme.toml`
  and `daisy.search`, honoured by the templates and `search.js`. Tests: US4 scenarios 1-5. In
  headless Chrome: scenario 4 and the shortcuts doing nothing with search off.
- [ ] T010 [US4] Documentation: "Search" in the options reference, `search-button-field` in the
  components reference, the search half of `docs/developer/set-up-search-and-versions.md`,
  CHANGELOG (scenario 6).

## Phase 5: User Story 5 - A site author lists the site's published versions (P2)

### Group 6

- [ ] T011 [US5] `VersionSwitcher` and `check_switcher` in `src/sphinx_daisyui/versions.py`;
  `switcher`, `check_switcher` and `show_version_warning_banner` in `theme.toml`;
  `components/version-switcher.html` ported on the dropdown macro; the banner's placeholder.
  Tests: US5 scenarios 1-6, the warning for each kind of address and its absence.
- [ ] T012 [US5] Documentation: "Versions" in the options reference, `version-switcher` in the
  components reference, the versions half of the guide with the file's format,
  `docs/_static/switcher.json` and `switcher` in `docs/conf.py`, CHANGELOG (scenario 7).

## Phase 6: User Story 6 - A reader moves to another version of the page they are on (P2)

### Group 7

- [ ] T013 [US6] `static/scripts/versions.js`: the list, the marks, the same page or the home
  page, the banner. In headless Chrome against two served builds: US6 scenarios 1-9 and the edge
  cases, for `html` and `dirhtml`.
