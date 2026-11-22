# Feature Specification: Draw page bodies with daisyUI tokens

**Feature Branch**: `003-page-body-styles`

**Created**: 2026-11-17

**Status**: Draft

**Input**: Issue #6, "Draw page bodies with daisyUI tokens", built from the accepted design on
the `prototype-theme` branch (`PROTOTYPE.md`, feature 3).

**Goals**: none recorded yet. The repository has no `GOALS.md`, so this specification cites no
goal id.

**Depends on**: #4, the page frame, which places the page body in the page and sets up the
message catalogue and the dimmed-text properties this feature uses. #5, site navigation, for the
branch that opens and closes and the toctree reader that a toctree in a page reuses (story 2
only).

## Summary

Every page a site builds gets its body drawn in the site's daisyUI theme. Headings, text, lists,
quotes, admonitions, code, tables, equations, pictures, footnotes, API entries, and the markup of
sphinx-design and sphinx-copybutton all take their colours from daisyUI's tokens, so any daisyUI
theme works in light and dark with nothing to build. Wide tables and equations scroll in their own
region, which a keyboard reader can reach. A toctree written into a page is drawn as the site
navigation's menu, with branches that open and close.

A site author who embeds raw HTML keeps daisyUI's own look on it with the escape class, and a site
author who prefers a Pygments style for their code brings it back with the
`pygments_light_style` and `pygments_dark_style` options.

A developer whose site already loads daisyUI 5, and shows the theme's pages inside its own, links
the page-body styles on their own and fits them to the site with two custom properties.

The theme adds no directive or role. It styles the HTML that Sphinx and the extensions it
supports already write (Article XIII).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A reader reads a page body in the site's daisyUI theme (Priority: P1)

A reader opens any page and reads its body drawn with the colours of the site's daisyUI theme, in
light or dark mode: headings and their links, inline text (links, glossary terms, inline code,
keys, menu paths), lists, task lists, definition and field lists, quotes and line blocks,
sidebars and rubrics, admonitions, version notes, highlighted code with line numbers, emphasised
lines, prompts and diffs, tables, pictures and figures, equations, footnotes and citations, API
entries from autodoc, and sphinx-design's grids, cards, tabs, dropdowns, badges and buttons. A
code block offers sphinx-copybutton's copy button. A table or display equation wider than the
page scrolls sideways in its own region, without the page scrolling. Sphinx's own generated
pages, the highlighted source code page and the general index, are drawn the same way.

**Why this priority**: the page body is what a reader of a documentation site came to read, on
every page.

**Independent Test**: build a test site holding each kind of block, and check the built page's
markup: the scroll regions, their names and focusability, the heading links' names, the
attribution's spacing, the absence of Pygments' stylesheet. Compare the kitchen sink pages by eye
against the prototype at phone, medium and wide widths, in light and dark.

**Acceptance Scenarios**:

1. **Given** a site that sets no Pygments style, **When** it builds, **Then** no page links
   Pygments' stylesheet, and code blocks are highlighted from the theme's tokens in both modes.
2. **Given** a site whose reader switches between light and dark mode, or a site that picks
   another daisyUI theme, **When** a page is shown, **Then** every part of the page body,
   including code highlighting and sphinx-design's colours, follows the theme in force, with
   nothing rebuilt.
3. **Given** a table at the outermost level of the page body, **When** the page is built,
   **Then** the table sits in a region that takes keyboard focus and is named by the table's
   caption, or by a fixed name for a table when it has none.
4. **Given** a table inside another table, **When** the page is built, **Then** only the outer
   table gets a scroll region.
5. **Given** a display equation, numbered or not, **When** the page is built, **Then** its
   notation sits in a region that takes keyboard focus, named for an equation and its number when
   it has one, and the number stays outside the region.
6. **Given** a table or equation wider than the reading column, **When** a keyboard reader
   focuses its region and presses the arrow keys, **Then** the region scrolls sideways and the
   page does not.
7. **Given** a heading, a caption or an API entry with a link to itself, **When** a screen
   reader reaches the link, **Then** the link is named by the text of what it links to.
8. **Given** a quotation with an attribution, however the source spaces the dash before it,
   **When** the page is built, **Then** the attribution's dash and name are separated by the
   same space.
9. **Given** each admonition directive (`note`, `warning`, `tip`, `danger` and the rest, and a
   generic `admonition` with its own title) and each version note (`versionadded`,
   `versionchanged`, `deprecated`, `versionremoved`), **When** the page is built and shown,
   **Then** each kind carries its own icon and is told apart from the other kinds, in colours
   that follow the daisyUI theme in force.
10. **Given** a code block, **When** a reader moves the pointer over it or reaches its copy
    button with the keyboard, **Then** the copy button is shown, and while the button has focus
    it carries a visible focus state.
11. **Given** a site that uses sphinx-design, **When** a page holds its grids, cards, tabs,
    dropdowns, badges and buttons, **Then** each is drawn with daisyUI's tokens, and tabs and
    dropdowns open with the keyboard.
12. **Given** a site that loads neither sphinx-design nor sphinx-copybutton, **When** it builds,
    **Then** the build succeeds and the theme asks for neither.
13. **Given** a caption, heading or equation number holding a site author's text with markup
    characters, **When** it names a scroll region or a link, **Then** it reaches the page
    escaped.
14. **Given** a site whose `language` is set, **When** a page is built, **Then** the fixed names
    the theme writes into the page body (a table's and an equation's region with no caption) are
    taken from the message catalogue in that language where a translation exists.
15. **Given** the built kitchen sink pages, **When** a reader opens them, **Then** every kind of
    block this story lists is shown on one of them, as the theme's documentation of its look.

---

### User Story 2 - A reader opens a page from a toctree in a page (Priority: P2)

A reader on a section's index page finds its contents, written by the site author as a toctree in
the page, drawn as the site navigation's menu. Entries with pages of their own have a toggle that
opens and closes them, the first two levels start open, and the reader follows an entry to open
its page.

**Why this priority**: section index pages are how a reader finds their way into a large part of
a site, and this is a decision the maintainer made on the prototype. It builds on the site
navigation's branch toggle (#5), so it can only be built after that feature.

**Independent Test**: build a test site whose index page holds a toctree three levels deep with a
caption, and check the built page's toggles, their state, their names and the hidden levels.
Check the toggles by keyboard in a browser.

**Acceptance Scenarios**:

1. **Given** a toctree in a page whose entries have pages below them, **When** the page is built,
   **Then** each such entry stays a link and gets a toggle beside it, and entries with no pages
   below them get none.
2. **Given** a toctree three or more levels deep, **When** the page is built, **Then** the first
   two levels are open and the levels below them start closed.
3. **Given** a toggle, **When** a reader presses it with the pointer or the keyboard, **Then** the
   entry's pages open or close, and the toggle's state says which to a screen reader.
4. **Given** a toggle, **When** a screen reader reaches it, **Then** it is named by the entry it
   opens, and the name is taken from the message catalogue in the site's language where a
   translation exists.
5. **Given** a toctree with a caption, **When** the page is built, **Then** the caption is drawn
   as a section label, the same way the site navigation labels its sections.
6. **Given** a hidden toctree, **When** the page is built, **Then** nothing is drawn for it.
7. **Given** a page with more than one toctree, **When** the page is built, **Then** each is drawn
   on its own with its own toggles.
8. **Given** an entry title holding a site author's text with markup characters, **When** it
   names a toggle, **Then** it reaches the page escaped.

---

### User Story 3 - A site author steps outside the page-body styles (Priority: P2)

A site author embeds raw HTML in a page, such as a daisyUI component, and wraps it in an element
with the escape class `daisy-sphinx-escape`, so the page-body styles leave it alone and it keeps
daisyUI's own look. A site author who wants a Pygments style for their code sets
`pygments_light_style` and `pygments_dark_style`, and the code is highlighted with those styles in
the matching mode.

**Why this priority**: both are ways out of the theme's defaults that a site author reaches for
once the defaults are in place.

**Independent Test**: build test sites with raw HTML inside and outside the escape class, and
with each Pygments option set alone, both set and with an unknown style name, and check which stylesheets the page links and what they hold.

**Acceptance Scenarios**:

1. **Given** raw HTML inside an element with the escape class, **When** the page is shown,
   **Then** none of the page-body styles apply to it, and it is drawn by daisyUI's own styles.
2. **Given** an element with the escape class inside an admonition, a table or a list, **When**
   the page is shown, **Then** the escape still holds for what is inside it, and the block around
   it keeps its page-body look.
3. **Given** raw HTML outside any element with the escape class, **When** the page is shown,
   **Then** it is drawn by the page-body styles like the rest of the body.
4. **Given** raw HTML that uses one of the daisyUI components the theme's documentation lists as
   compiled in for raw HTML, **When** the page is shown, **Then** the component is drawn, though
   no template of the theme uses it.
5. **Given** `pygments_light_style` and `pygments_dark_style` both set, **When** the site builds,
   **Then** each mode's code is highlighted with its style, and the theme's token highlighting
   does not mix into it.
6. **Given** only one of the two set, **When** the site builds, **Then** that mode uses the named
   style and the other mode keeps the theme's token highlighting.
7. **Given** a Pygments style name that Pygments does not know, **When** the site builds,
   **Then** the build succeeds with one warning naming the option and the value, and that mode
   keeps the theme's token highlighting.
8. **Given** a reader whose mode is auto and whose system is dark, **When** a page is shown on a
   site with a dark Pygments style, **Then** the dark style is the one in force.
9. **Given** the theme's documentation, **When** a site author reads it, **Then** the escape
   class, the daisyUI components compiled in for raw HTML, and the two Pygments options are
   documented with their defaults.

---

### User Story 4 - A developer styles page bodies inside a site that already loads daisyUI (Priority: P3)

A developer whose site already loads daisyUI 5 shows the theme's pages inside pages of their own,
for example from the `.fjson` files of `sphinx-build -b json`. They link the page-body stylesheet
the build writes, put the page-body class on the element holding a page's body, and get the
theme's page-body look without a second copy of Tailwind and daisyUI. They set the reading width
and the surface the page sits on to fit their site, and put the escape class on their own markup
inside the body to keep it out of the styles.

**Why this priority**: a site that embeds its documentation would otherwise keep its own copy of
these styles, which drifts from the theme's.

**Independent Test**: build test sites with the `html` and `json` builders and check that each
writes the page-body stylesheet, that every custom property the stylesheet reads is declared in it
or is one a daisyUI 5 page already has, and that the JSON build's page bodies carry the theme's
page-body changes.

**Acceptance Scenarios**:

1. **Given** a site with `html_theme = "daisyui"`, **When** it builds with the `html`, `dirhtml`,
   `singlehtml` or `json` builder, **Then** the build writes the page-body stylesheet to
   `_static/styles/sphinx-daisyui-content.css` beside the theme's stylesheet.
2. **Given** a site built with the `json` builder, **When** the build runs, **Then** it succeeds
   without warnings, and each page's body holds the same page-body changes (scroll regions, named
   permalinks, admonition icons) as the `html` builder writes.
3. **Given** a page that loads daisyUI 5 and the page-body stylesheet but none of the theme's other
   styles, **When** it shows a page body inside an element with the page-body class, **Then**
   the body is drawn as the theme draws it.
4. **Given** a host that sets `--daisy-sphinx-max-width` or `--daisy-sphinx-page-bg` on the
   page-body element or an element around it, **When** a page body is shown, **Then** the reading
   column takes that width, and the sunken surfaces are mixed from that surface.
5. **Given** a host that sets neither property, **When** a page body is shown, **Then** it looks
   as it does in the theme.
6. **Given** a host's own markup inside the page-body element with the escape class, **When** the
   page is shown, **Then** the page-body styles leave it alone.
7. **Given** the theme's documentation, **When** a developer reads it, **Then** the stylesheet's
   path, the page-body class, the escape class and the two custom properties with their defaults
   are documented.

---

### Edge Cases

- A page with an empty body, such as Sphinx's search page before a search, builds and is left as
  Sphinx wrote it.
- A table caption that holds only a link to itself, or a caption made only of markup, still gives
  its region a name.
- An equation written inline (`$x$` or `:math:`) gets no scroll region. Only display equations
  do.
- A toctree entry that links to another site has no pages below it and gets no toggle.
- A page built by `dirhtml` or `singlehtml` gets the same page body as one built by `html`.
- A Pygments style set while the reader's mode is not yet known before the first paint: the style
  for the mode the page starts in is the one shown, with no flash of the other.
- A contents list in a page shown by a host is left out of the page-body styles, as it is in the
  theme, where the site navigation's styles draw it. The host draws it.
- An escape-class element written directly in reStructuredText with the `class` directive, rather
  than in raw HTML, leaves its contents out of the page-body styles just the same.

## Requirements *(mandatory)*

### Functional Requirements

**The page body a reader reads (US1)**

- **FR-001**: The theme MUST draw the HTML that Sphinx, MyST, autodoc, sphinx-design and
  sphinx-copybutton write into a page body (headings, inline text, lists, quotes, admonitions,
  version notes, code, tables, pictures, equations, footnotes, citations, API entries, and
  sphinx-design's grids, cards, tabs, dropdowns, badges and buttons) in every daisyUI theme, in
  light and dark.
- **FR-002**: Every colour the page-body styles use, including code highlighting and
  sphinx-design's colour variables, MUST come from daisyUI's tokens (Article XI). The only
  exception is a Pygments style the site author sets (FR-014).
- **FR-003**: Text the page body dims MUST use the frame's shared dimmed-text properties and meet
  WCAG 2.2 AA contrast on daisyUI's default light and dark themes (Article XIV).
- **FR-004**: When no Pygments style is set, the theme MUST leave Pygments' own stylesheet out of
  every page and highlight code from its tokens.
- **FR-005**: Every table at the outermost level of a page body MUST be placed in a region that
  scrolls sideways on its own, takes keyboard focus, and is named by the table's caption or, with
  no caption, by a fixed name for a table.
- **FR-006**: Every display equation's notation MUST be placed in a region that scrolls sideways
  on its own, takes keyboard focus and is named for an equation and its number, with the
  equation's number left outside the region.
- **FR-007**: Every link to a heading, caption or API entry MUST be named for a screen reader by
  the text of what it links to.
- **FR-008**: A quotation's attribution MUST be separated from its dash by one consistent space,
  whatever spacing the source used.
- **FR-009**: Every control the page-body styles show (the copy button, sphinx-design's tabs and
  dropdowns, scroll regions) MUST be reachable by keyboard with a visible focus state.
- **FR-010**: The theme MUST draw the page bodies of Sphinx's own generated pages, the highlighted
  source code page and the general index, with the same styles.
- **FR-011**: The theme MUST NOT require sphinx-design or sphinx-copybutton. Their styles apply
  when a site loads them.

**A toctree in a page (US2)**

- **FR-012**: A toctree in a page MUST be drawn as the site navigation's menu: each entry stays a
  link, an entry with pages below it gets a toggle beside it whose state is exposed to a screen
  reader and which is named by its entry, the first two levels start open and the levels below
  start closed, and a caption is drawn as a section label.
- **FR-013**: The toggle, the menu's look and the reading of the toctree MUST be the ones the site
  navigation feature (#5) builds, not a second copy.

**Stepping outside the page-body styles (US3)**

- **FR-014**: The theme MUST accept the options `pygments_light_style` and
  `pygments_dark_style`, each defaulting to no style. A style set for a mode MUST highlight that
  mode's code, and a mode with no style set MUST keep the token highlighting.
- **FR-015**: A Pygments style name that Pygments does not know MUST produce one build warning
  naming the option and the value, and MUST NOT fail the build.
- **FR-016**: A Pygments style MUST apply in the reader's mode as the page resolves it, including
  auto mode, through the mode attributes the page carries on `<html>`.
- **FR-017**: Content inside an element with the class `daisy-sphinx-escape` MUST be left out of
  every page-body style, wherever in the page body the element sits (Article XIII).
- **FR-018**: The stylesheet MUST include a documented set of daisyUI components for raw HTML to
  use, which no theme template needs.

**Across the feature**

- **FR-019**: Fixed text the theme writes into a page body (the names of scroll regions with no
  caption, the names of a toctree's toggles) MUST be marked for translation in the theme's
  message catalogue (Article VIII).
- **FR-020**: Every value from the page or its configuration that the theme writes into an
  attribute or the page body (caption and heading text in a region's or link's name, an entry
  title in a toggle's name) MUST be escaped (Article V).
- **FR-021**: The admonition and version-note icons MUST come from the theme's bundled icon set,
  with no second copy of them in the stylesheet.
- **FR-022**: Every option this feature adds MUST be declared in `theme.toml`, and the options,
  the escape class and the extensions the theme styles MUST be documented in the theme's
  reference (Article VI).
- **FR-023**: The documentation site MUST carry the kitchen sink pages, which show every kind of
  block FR-001 lists, built with the theme on every documentation build.

**The page-body styles outside the theme (US4)**

- **FR-024**: Every build with the theme by an HTML builder, the JSON and pickle builders
  included, MUST write the page-body styles on their own as
  `_static/styles/sphinx-daisyui-content.css`, and the package MUST ship that file compiled.
- **FR-025**: The page-body stylesheet MUST read no custom property from the theme's other
  stylesheets. Anything it reads is declared in it, or is a daisyUI token, a Tailwind font or a
  sphinx-design property, which a page that loads daisyUI 5 already has.
- **FR-026**: The reading width and the surface the page sits on MUST be custom properties,
  `--daisy-sphinx-max-width` and `--daisy-sphinx-page-bg`, that a host sets on the page-body
  element or an element around it. Their defaults MUST be the theme's own values, so the theme's
  look does not change.
- **FR-027**: A build with the JSON or pickle builder MUST succeed, with the page-body changes in
  every page's body.

### Key Entities

- **Page body**: the HTML Sphinx writes for a page's content, which the page-body styles draw.
- **Scroll region**: a named, focusable region around a wide table or a display equation's
  notation.
- **Escape class**: `daisy-sphinx-escape`, the class that leaves its contents out of the
  page-body styles.
- **Pygments style option**: one of the two options that set a Pygments style for a mode.
- **Page-body stylesheet**: `sphinx-daisyui-content.css`, the page-body styles compiled on their
  own for a host that already loads daisyUI 5.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The documentation site, with its kitchen sink pages, builds with warnings as errors.
- **SC-002**: Each kitchen sink page, the source code page, the general index and the toctree in
  a page matches the prototype's corresponding page side by side at 390, 1100 and 1440 pixels
  wide, in light mode, and in dark mode for the admonitions, code and sphinx-design pages.
- **SC-003**: The page-body stylesheet names no colour value of its own: every colour resolves to
  a daisyUI token, so changing the daisyUI theme recolours every page body with nothing rebuilt.
- **SC-004**: Every page passes a keyboard walk: every scroll region, copy button, sphinx-design
  tab and dropdown, and toctree toggle is reached and used without a pointer, with a visible
  focus state.
- **SC-005**: A site that sets `pygments_light_style`, `pygments_dark_style` or both shows
  those styles in the matching mode, and the token highlighting in a mode with none.
- **SC-006**: No value from a page or its configuration reaches the page body unescaped, except
  markup Sphinx produced.

## Clarifications

### Session 2026-11-17

- Q: How many stories? The issue names one reader's part and one site author's part. → A: Three.
  Reading the page body and opening a page from a toctree in a page are two things a reader sets
  out to do, and the second depends on site navigation (#5) where the first does not. The site
  author's two ways out of the defaults (the escape class and Pygments styles) are one story,
  because both step outside the page-body styles and neither is set out to on its own terms.
- Q: Which settings bring Pygments styles back? → A: The two theme options
  `pygments_light_style` and `pygments_dark_style`, one per mode (FR-014). Sphinx's own
  `pygments_style` setting does not, because it is set on every site and would undo the token
  highlighting.
- Q: What happens with a style name Pygments does not know? → A: One warning and the token
  highlighting for that mode, never a failed build (FR-015).
- Q: Does the theme depend on sphinx-design or sphinx-copybutton? → A: No. Their styles apply
  when a site loads them (FR-011). The documentation site loads both for its kitchen sink pages.

## Assumptions

- The page frame (#4) places the page body in an element the page-body styles are scoped to,
  sets up the message catalogue, ships the icon set, writes the mode attributes on `<html>` and
  provides the shared dimmed-text properties.
- The site navigation feature (#5) builds the branch toggle, the menu's look, the section label
  and the toctree reader that story 2 reuses.
- The mode attributes on `<html>` are owned by the modes feature (#7). Until it lands, the
  Pygments styles key on the attributes the page frame writes.
- The decisions the maintainer made on the prototype bind this feature: article-info items on one
  line, a small space after a quotation's dash, compact lists that widen only when an item holds
  several blocks, a toctree in a page drawn as the sidebar's menu with its first two levels open,
  the page named Admonitions, and code highlighted from the tokens unless a Pygments style is set.
- Out of scope, owned by sibling features: the page frame and the drawer (#4), the site
  navigation, On this page and header links (#5), modes, the theme picker and the search page
  (#7), and icon links and edit and view links (#8).
