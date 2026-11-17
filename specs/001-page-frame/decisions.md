# Decisions: 001-page-frame

Decisions made while specifying, with the reason each is defensible. Each stands until the
maintainer changes it.

## D1. Five stories, not four

The prototype names four features (page frame, brand and logo, announcement, previous and next).
The page frame holds a site author's part (arranging the page with the layout code and component
lists) and a reader's part (the three-column page, the drawer, the sticky header, the skip link).
Issue #4 lists them as two separate bullets. A site author's and a reader's stories are never
merged into one, so the page frame is two stories, and the spec has five.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D2. Component lists keep pydata-sphinx-theme's defaults

`navbar_end` defaults to the version switcher, the theme switcher and the icon links,
`navbar_persistent` to the search button, `article_header_start` to the breadcrumbs and
`secondary_sidebar_items` to On this page. None of those components exists until its own feature
is built. A name that resolves to no template draws nothing, so the defaults are set now and each
component appears when its feature lands, with no default to change later. The defaults are the
ones the prototype uses.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D3. The layout check stops the build without a traceback

Checked against Sphinx 9.2 (`research.md`, "Assumptions checked"): a `ConfigError` raised in a
`builder-inited` handler, as the prototype does, makes Sphinx print its crash report with a
traceback. The requirement (FR-004) is the outcome the issue asks for, "a clear message". How the
check reaches Sphinx without the crash report is planning work.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D4. `sticky_banners` is honoured here

The prototype accepts the option and does nothing, and names the announcement feature as the one
that does it properly. FR-028 says it keeps its source theme's meaning. Research confirms which
theme defines it and what it does before it is built (Article X).

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D5. The announcement is printed as markup

Furo and pydata-sphinx-theme both print the announcement as the site author's HTML, and #3 amends
Article V to say the same. Every other value is escaped.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D6. The theme's repository address comes from package metadata

The prototype writes the address into `theme-version.html`. The spec asks for the address and the
version to come from the package's metadata, so a fork or a moved repository needs no template
change.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D7. The message catalogue is set up here

Article VIII asks for the theme's own text to be translatable. This feature writes the first such
text (the skip link, the drawer's controls, "Previous", "Next", "Back to top"), so it sets up the
catalogue, and later features add their own text to it.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D8. The keyboard helper starts here, small

The prototype's hand-over has the search dialog feature build the keyboard helper and this
feature reuse it. This feature is built first, so it writes a small helper for the arrow keys and
the drawer's Escape, and the search dialog feature grows it. Recorded in `planning-notes.md`.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D9. No goal id

The repository has no `GOALS.md` yet, so the spec cites no goal and the issue carries no goal
footer.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D10. The layout check exits with the message alone

Every exception that leaves a Sphinx build is printed with Sphinx's crash report, whatever its
class. The check logs its message through Sphinx's logger and raises `SystemExit(2)`, which
Sphinx's handler does not catch, so the build stops before any page with one line (`research.md`).

**ADR:** none — local to how one check reaches the console, nothing downstream inherits it.

## D11. The arrow keys use Sphinx's own handler

Sphinx's `doctools.js` already moves to the previous and next page when `navigation_with_keys` is
on, with the exceptions FR-032 lists. The prototype's arrow-key code is not ported. The theme's
keyboard helper starts with Escape for the drawer.

**ADR:** none — follows from the option's existing meaning in Sphinx's `basic` theme.

## D12. `navbar_end` is written once and moved by the page script

The components are written in the navbar and moved into the drawer on a narrow screen, so the
HTML holds each once (FR-010). The brand is written twice, in the navbar and at the head of the
primary sidebar, and one shows at each width (FR-025).

**ADR:** none — a template detail of this feature.

## D13. `sticky_banners` keeps the banner with the header

pydata-sphinx-theme's option pins its banners and its navbar together. Here the banner moves into
the header area, which stays in place as the layout code says.

**ADR:** none — follows from the option's meaning in pydata-sphinx-theme.

## D14. The page script's behaviour is checked in a headless browser, not in CI

A browser suite in CI needs a workflow change. The scrolled header, the drawer, the moved
components, back to top and the fetched announcement are driven in headless Chrome while
building, and the CI suite is left to a change that can edit the workflows.

**ADR:** none — a testing arrangement for this feature.

## D15. The logo is `logo` only

The maintainer ruled that the theme has its own options, modelled on pydata-sphinx-theme's, with
one name and one shape per setting, and Article X was rewritten to say so. Furo's `light_logo`,
`dark_logo` and `sidebar_hide_name` and pydata-sphinx-theme's `logo_link` are dropped. The
specification is amended to match (FR-021, FR-024, SC-003 and User Story 3).

**ADR:** none — the rule is the constitution's Article X; this records how this feature follows it.
