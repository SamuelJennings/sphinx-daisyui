# Decisions: 001-page-frame

Decisions made while specifying, with the reason each is defensible. Each stands until the
maintainer changes it.

## D1. Five stories, not four

The prototype names four features (page frame, brand and logo, announcement, previous and next).
The page frame holds a site author's part (arranging the page with the layout code and component
lists) and a reader's part (the three-column page, the drawer, the sticky header, the skip link).
Issue #4 lists them as two separate bullets. A site author's and a reader's stories are never
merged into one, so the page frame is two stories, and the spec has five.

## D2. Component lists keep pydata-sphinx-theme's defaults

`navbar_end` defaults to the version switcher, the theme switcher and the icon links,
`navbar_persistent` to the search button, `article_header_start` to the breadcrumbs and
`secondary_sidebar_items` to On this page. None of those components exists until its own feature
is built. A name that resolves to no template draws nothing, so the defaults are set now and each
component appears when its feature lands, with no default to change later. The defaults are the
ones the prototype uses.

## D3. The layout check stops the build without a traceback

Checked against Sphinx 9.2 (`research.md`, "Assumptions checked"): a `ConfigError` raised in a
`builder-inited` handler, as the prototype does, makes Sphinx print its crash report with a
traceback. The requirement (FR-004) is the outcome the issue asks for, "a clear message". How the
check reaches Sphinx without the crash report is planning work.

## D4. `sticky_banners` is honoured here

The prototype accepts the option and does nothing, and names the announcement feature as the one
that does it properly. FR-028 says it keeps its source theme's meaning. Research confirms which
theme defines it and what it does before it is built (Article X).

## D5. The announcement is printed as markup

Furo and pydata-sphinx-theme both print the announcement as the site author's HTML, and #3 amends
Article V to say the same. Every other value is escaped.

## D6. The theme's repository address comes from package metadata

The prototype writes the address into `theme-version.html`. The spec asks for the address and the
version to come from the package's metadata, so a fork or a moved repository needs no template
change.

## D7. The message catalogue is set up here

Article VIII asks for the theme's own text to be translatable. This feature writes the first such
text (the skip link, the drawer's controls, "Previous", "Next", "Back to top"), so it sets up the
catalogue, and later features add their own text to it.

## D8. The keyboard helper starts here, small

The prototype's hand-over has the search dialog feature build the keyboard helper and this
feature reuse it. This feature is built first, so it writes a small helper for the arrow keys and
the drawer's Escape, and the search dialog feature grows it. Recorded in `planning-notes.md`.

## D9. No goal id

The repository has no `GOALS.md` yet, so the spec cites no goal and the issue carries no goal
footer.
