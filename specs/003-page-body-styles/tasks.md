# Tasks: Draw page bodies with daisyUI tokens

**Input**: `spec.md`, `plan.md`, `research.md`, `planning-notes.md` in
`specs/003-page-body-styles/`. The prototype is the `prototype-theme` branch; "port" means copy
across and clean to `main`'s standards, never redraw.

**Tests**: test-first for every behaviour (`docs/contributing/standards/testing.md`). No test of
wording, icons, CSS classes chosen for looks, layout, widths or design choices. Template and page
tests live in `tests/test_templates/`.

## Phase 1: User Story 1 - A reader reads a page body in the site's daisyUI theme (P1)

### Group 1

- [x] T001 [US1] The test site `tests/roots/test-body/` (captioned, uncaptioned and nested
  tables, a numbered and an unnumbered display equation, an inline equation, quotations with
  attributions spaced three ways, every admonition kind and version note, an API entry, captions
  and headings with markup characters), and `PageBodyTranslator` with `install_translator` in
  `src/sphinx_daisyui/body.py`, connected in `setup()`. Scroll regions, named heading links and
  the attribution's space. Tests in `tests/test_body.py`: US1 scenarios 3-8, 13, the edge cases
  for inline equations, captions of markup alone, `dirhtml` and `singlehtml`, and a site on
  another theme left alone.
- [x] T002 [US1] Admonition and version-note icons from `ICONS`: the Lucide names added to
  `scripts/icons.mjs` and `icons.json` regenerated.
- [x] T003 [US1] Sphinx's `pygments.css` removed from every page; `pygments` declared as a
  dependency. "Table", "Equation" and "Equation %(number)s" marked for translation and the
  catalogue template regenerated; US1 scenario 14 in `tests/test_templates/test_translation.py`.

### Group 2

- [x] T004 [US1] Port `docs/kitchen-sink/` and `docs/_ext/palette.py`; the extensions, MyST
  settings and `_ext` path in `docs/conf.py`; sphinx-design and sphinx-copybutton in the `docs`
  group; the kitchen sink linked from the documentation's contents. The site builds with
  warnings as errors (SC-001). US1 scenarios 12 and 15.

### Group 3

- [x] T005 [US1] Port `assets/content.css` and `frame.css:228-296` from the prototype into
  `assets/content.css`, imported from `assets/theme.css`, cleaned to the plan: the frame's dimmed
  text and lines, the inline SVG icons, no toctree or caption rules, the scope stopping at
  `.toctree-wrapper` and `.daisy-sphinx-escape`. The `@source inline` list in `theme.css`.
  Rebuild the stylesheet. Check in headless Chrome that no kitchen sink page is wider than a
  390 px window and that the copy button shows on hover and focus.
- [x] T006 [US1] Document the page body in `docs/reference/`: the extensions styled, the support
  target, and the reference page's link to the kitchen sink. CHANGELOG.

## Phase 2: User Story 2 - A reader opens a page from a toctree in a page (P2)

### Group 4

- [x] T007 [US2] Move the site navigation's decoration into `NavigationMenu` in `navigation.py`,
  used by `SiteNavigation` with no change to its output. The mixin decorates a `toctree-wrapper`
  with it, first two levels open, its caption a section label. Test site
  `tests/roots/test-page-toctree/` and tests in `tests/test_body.py`: US2 scenarios 1-8 and the
  external entry. The toggles checked by keyboard in headless Chrome.

## Phase 3: User Story 3 - A site author steps outside the page-body styles (P2)

### Group 5

- [x] T008 [US3] `pygments_light_style` and `pygments_dark_style` in `theme.toml`, and
  `PygmentsStyles` in `src/sphinx_daisyui/pygments.py`: the stylesheet for the modes with a
  style, its reset of the token colours, the warning for an unknown name. Tests in
  `tests/test_pygments.py`: US3 scenarios 5-8.
- [x] T009 [US3] Document the escape class, the daisyUI components compiled in for raw HTML and
  the two options with their defaults in `docs/reference/` (US3 scenario 9). Check in headless
  Chrome that raw HTML inside the escape class keeps daisyUI's look and outside it does not (US3
  scenarios 1-4). CHANGELOG.

## Phase 4: Convergence

- [x] T010 [US1] Break each behaviour the new tests name once and confirm a test fails.
- [x] T011 [US1] Side-by-side comparison with the prototype at 390 and 1440 wide: the equation
  number at the end of its line, MathJax's margin inside the region, the toctree in a page read as
  body text, the API page's entry order, the Python cross-reference, and daisyUI's key size.
