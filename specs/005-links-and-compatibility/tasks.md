# Tasks: Icon and source links

**Input**: `spec.md`, `plan.md`, `research.md`, `planning-notes.md` in
`specs/005-links-and-compatibility/`. The prototype is the `prototype-theme` branch; "port" means
copy across and clean to `main`'s standards, never redraw.

**Tests**: test-first for every behaviour (`docs/contributing/standards/testing.md`). No test of
wording, icons, CSS classes chosen for looks, layout, widths or design choices. Template and page
tests live in `tests/test_templates/`.

## Phase 1: User Story 1 - A site author links the site's accounts as icons (P1)

### Group 1

- [ ] T001 [US1] `IconLink`, `IconLinks` and `check_icon_links` in `src/sphinx_daisyui/links.py`;
  `icon_links` and `icon_links_label` in `theme.toml`; `daisy.icon_links` and
  `daisy.icon_links_label` in the page context; the handler connected in `setup()`. Tests: US1
  scenarios 1-4, 8 and 9 on the objects, the two warnings and their absence, the edge cases.
- [ ] T002 [US1] `icon_button` in `components/macros.html` with `href`, `tooltip_class` and a
  caller; `components/navbar-icon-links.html` ported. Test site `tests/roots/test-links/`. Tests:
  US1 scenarios 1-9 on the built pages (address, accessible name, icon or image, a page three
  folders deep, the navbar and a footer list, the list's name and its translated default,
  escaping, nothing when empty); the search dialog's close button unchanged.
- [ ] T003 [US1] Documentation: "Icon links" in the options reference with the bundled icon
  names, `navbar-icon-links` and `icon_button` in the components reference, the icon links part
  of `docs/developer/link-the-sources.md`, `icon_links` in `docs/conf.py` with the
  `DAISY_FOOTER_ICONS` switch, CHANGELOG.

## Phase 2: User Story 2 - A site author points each page at its source (P2)

### Group 2

- [ ] T004 [US2] `SourceHost`, `HOSTS` and `SourceLinks` in `src/sphinx_daisyui/links.py`; the
  four options in `theme.toml`; `daisy.sources` and `daisy.top_buttons` in the page context,
  empty on index and search pages. Tests: US2 scenarios 1, 2, 5-9 and the edge cases on the
  objects, for each host, at the top and three folders deep.
- [ ] T005 [US2] The edit and view buttons in `layout.html`, ported from the prototype's
  `layout.html:106-113`; `source_link` in `components/macros.html`;
  `components/edit-this-page.html` ported on it. Tests: US2 scenarios 1-8 on the built pages,
  the buttons in the order listed, none for an empty list, none on the search and index pages,
  the `.txt` page's suffix, escaping.
- [ ] T006 [US2] Documentation: "Source links" in the options reference, `edit-this-page` and
  `source_link` in the components reference, the source links part of
  `docs/developer/link-the-sources.md`, the `source_*` and `top_of_page_buttons` values in
  `docs/conf.py` with the `DAISY_SOURCE_SIDEBAR` switch, CHANGELOG (scenario 10).

## Phase 3: User Story 3 - A reader opens the page's source (P2)

### Group 3

- [ ] T007 [US3] `components/sourcelink.html` ported on `source_link`, `sourcelink` in the
  components reference and in `secondary_sidebar_items` in `docs/conf.py`. Tests: US3 scenarios
  2 and 3 (`html_show_sourcelink` and `html_copy_source` each off), from a page at any depth.
- [ ] T008 [US3] Every new text in `locale/sphinx.pot` through `scripts/messages.sh`, and the
  translation test's catalogue fixture gaining them (scenario 5). In headless Chrome, the
  keyboard walk over the icon links, the edit and view buttons and the sidebar links: each
  focused visibly and named (US3 scenarios 1 and 4, SC-003).
