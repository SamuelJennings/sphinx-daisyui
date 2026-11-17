# Feature Specification: Arrange the page and fill it from conf.py

**Feature Branch**: `001-page-frame`

**Created**: 2026-11-17

**Status**: Draft

**Input**: Issue #4, "Arrange the page and fill it from conf.py", built from the accepted design
on the `prototype-theme` branch (`PROTOTYPE.md`, features 1, 5, 9 and 12).

**Goals**: none recorded yet. The repository has no `GOALS.md`, so this specification cites no
goal id.

**Depends on**: #3, which amends Article V of the constitution to say how text reaches the HTML
when Sphinx's templates do not autoescape. This specification is written against the amended
article.

## Summary

The theme gets its page. A site author arranges the five areas of the page with a layout code
and fills the header, the two sidebars, the page and the footer with components named in
component lists. They show the site's logo, and put an announcement across the top of every
page. A reader gets the three-column page documentation readers expect, which works on a phone
and from the keyboard, and moves between pages from the foot of each page.

Everything a site author writes here is a theme option in `html_theme_options`. The options that
Furo or pydata-sphinx-theme already define keep their names, types and meaning (Article X).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A site author arranges the page and fills it with components (Priority: P1)

A site author sets the `layout` option to a layout code, such as `hHh LpR lff`, to decide which
area reaches each corner of the page and which areas stay in place as the page scrolls. They name
components in component lists (`navbar_start`, `navbar_center`, `navbar_end`,
`navbar_persistent`, `article_header_start`, `article_header_end`, `article_footer_items`,
`content_footer_items`, `primary_sidebar_end`, `secondary_sidebar_items`, `footer_start`,
`footer_center`, `footer_end`) to fill the header, the sidebars, the page and the footer, in the
order they list them. The theme ships the `copyright`, `sphinx-version`, `theme-version`,
`last-updated` and `navbar-logo` components for these lists.

**Why this priority**: every other feature of the theme draws into this page. Without it there
is nothing to place a component in.

**Independent Test**: build a test site with a chosen layout code and component lists, and check
the built page's areas, the stay-in-place markers and the order of the components in each area.

**Acceptance Scenarios**:

1. **Given** a site that sets no `layout`, **When** it builds, **Then** its pages use the default
   code `hHh LpR lff`: the header spans the top and stays in place, the primary and secondary
   sidebars stay in place, and the footer runs under the page and the secondary sidebar.
2. **Given** a site that sets `layout` to another valid code, such as `lHh LpR lff`, **When** it
   builds, **Then** each corner of the page goes to the area the code names for it, and exactly
   the areas written in upper case are marked to stay in place.
3. **Given** a layout code that leaves no room for the secondary sidebar on a medium screen,
   **When** the page is built, **Then** the build also writes the arrangement for that width, in
   which the secondary sidebar's cells go to the area beside them.
4. **Given** a layout code of the wrong shape (a wrong letter in a position, a missing group, a
   fourth group), **When** the site builds, **Then** the build stops before writing any page, with
   one message that names the option, quotes the code and says what each position may hold, and
   without a traceback.
5. **Given** a layout code written with extra spaces or in mixed case within its rules, **When**
   the site builds, **Then** it is read as the same code.
6. **Given** a component list written as a list or as a comma-separated string, with or without
   the `.html` ending on each name, **When** the site builds, **Then** the components appear in
   that area in the order given.
7. **Given** a component list that names a template the site provides in its own
   `templates_path`, **When** the site builds, **Then** the site's template is drawn in that area.
8. **Given** a component list that names a component which neither the theme nor the site
   provides, **When** the site builds, **Then** the build succeeds and that name draws nothing.
9. **Given** an empty component list, **When** the site builds, **Then** that place on the page
   holds no components.
10. **Given** the default component lists, **When** the site builds, **Then** the navbar starts
    with the site's title linked to its home page, and the footer carries the copyright, the
    Sphinx version and the theme's version with a link to the theme's repository.
11. **Given** `html_show_copyright`, `html_show_sphinx` or `html_last_updated_fmt` turned off or
    unset, **When** the site builds, **Then** the matching component draws nothing.
12. **Given** a site author's text in `copyright`, the project name or a theme option, **When**
    a component prints it, **Then** it reaches the page escaped.
13. **Given** the components listed in `navbar_end`, **When** a page is built, **Then** each is
    in the page's HTML once, shown in the navbar on wide screens and in the drawer on narrow ones.
14. **Given** the built pages, **When** a site author reads the theme's documentation, **Then**
    every option and component in this story is documented with its default, and the layout code
    is explained letter by letter.

---

### User Story 2 - A reader reads a page on any screen (Priority: P1)

A reader opens any page and finds the site's navigation on the left, the page in a readable
column in the middle and the page's own tools on the right. The header stays in reach and
separates itself from the page once they scroll. On a phone the left sidebar becomes a drawer
opened from the navbar. A keyboard reader skips straight to the page's content.

**Why this priority**: this is what every reader of every site meets on every page.

**Independent Test**: build a test site and check the built page's landmarks, the skip link's
target, the drawer's controls, and the markers the page script reads. Look at the page by eye at
phone, medium and wide widths against the prototype.

**Acceptance Scenarios**:

1. **Given** a built page, **When** a reader arrives with the keyboard, **Then** the first thing
   they reach is a link that moves focus to the page's main content.
2. **Given** a built page, **When** a screen reader lists its landmarks, **Then** the header,
   the site navigation, the main content, the page tools and the footer are each named.
3. **Given** a wide screen, **When** a reader opens a page, **Then** the page shows three columns,
   and the page column stays centred with the two sidebars taking the spare width.
4. **Given** a medium screen with no room for the secondary sidebar, **When** a reader opens a
   page, **Then** the page uses the build's arrangement for that width.
5. **Given** a narrow screen, **When** a reader opens a page, **Then** the page is one column and
   the primary sidebar is reached from a menu button in the navbar, which opens it as a drawer.
6. **Given** the drawer is open, **When** the reader presses Escape, follows a link in it, presses
   its close button or presses outside it, **Then** the drawer closes.
7. **Given** a layout code with a sticky header, **When** the reader scrolls away from the top,
   **Then** the header is marked as scrolled, and the mark goes when they return to the top.
8. **Given** a layout code with a sticky sidebar under a sticky header, **When** the reader
   scrolls, **Then** the sidebar stays in place below the header rather than under it.
9. **Given** a layout code with no sticky areas, such as `hhh lpr fff`, **When** the reader
   scrolls, **Then** every area scrolls with the page.
10. **Given** a page with no secondary sidebar components, or Sphinx's search or index page,
    **When** it is built, **Then** the page holds no secondary sidebar.
11. **Given** a site whose `language` is set, **When** a page is built, **Then** the theme's own
    fixed text on the page, such as the skip link and the drawer's control names, is taken from
    the message catalogue in that language where a translation exists.

---

### User Story 3 - A site author shows the site's logo (Priority: P2)

A site author shows a logo for light mode and one for dark mode, with or without the site's name
beside it, linked to the page they choose. They write it in Furo's shape (`light_logo`,
`dark_logo`, `sidebar_hide_name`) or in pydata-sphinx-theme's (`logo` with `text`,
`image_light`, `image_dark`, `alt_text`, `link`, and `logo_link`), and Sphinx's own `html_logo`
works when neither is set. When the layout code runs the primary sidebar to the top of the page,
the logo moves to the head of that sidebar.

**Why this priority**: a site's identity on every page, and the first option most sites copied
from another theme will carry.

**Independent Test**: build test sites with each shape of option and with `html_logo` only, and
check the built brand's images, their addresses, the name, the alternative text and the link.

**Acceptance Scenarios**:

1. **Given** no logo options and no `html_logo`, **When** the site builds, **Then** the brand is
   the site's title, linked to the home page.
2. **Given** `html_logo` only, **When** the site builds, **Then** that image is the logo in both
   modes.
3. **Given** a logo for each mode in either shape, **When** the site builds, **Then** the brand
   carries both images, and the one for the reader's current mode is the one shown.
4. **Given** only a light logo, **When** the site builds, **Then** the same image serves dark mode.
5. **Given** a logo path relative to `_static`, a path starting `_static/`, or a full address,
   **When** the site builds, **Then** every page, at any depth, points at the right file or
   address.
6. **Given** `sidebar_hide_name` switched on, or a pydata-style `logo` with images and no
   `text`, **When** the site builds, **Then** the brand shows the logo without the site's name,
   and the logo's alternative text names the site.
7. **Given** a pydata-style `logo.text`, **When** the site builds, **Then** that text is shown
   beside the logo, and the logo's alternative text is empty so the name is not read twice.
8. **Given** `logo.link` or `logo_link`, **When** a reader follows the brand, **Then** they reach
   that address. Without either, they reach the home page.
9. **Given** a layout code whose top-left corner belongs to the primary sidebar, such as
   `lHh LpR lff`, **When** a page is built, **Then** on a wide screen the brand appears once, at
   the head of the primary sidebar, and on a narrow screen it stays in the navbar.
10. **Given** a site author's logo text, alternative text or link, **When** the brand is built,
    **Then** each reaches the page escaped.

---

### User Story 4 - A site author puts an announcement across every page (Priority: P3)

A site author sets `announcement` to text, which may hold HTML of their own, or to a URL that
returns HTML, and a banner runs across the top of every page.

**Why this priority**: an occasional need (a release, a deprecation, a survey), and one both
Furo and pydata-sphinx-theme offer, so configurations copied from them expect it.

**Independent Test**: build test sites with a text announcement, an HTML announcement and a URL
announcement, and check the built banner and the address the page script reads.

**Acceptance Scenarios**:

1. **Given** no `announcement`, **When** the site builds, **Then** no page carries a banner.
2. **Given** an announcement as text or as the site author's own HTML, **When** the site builds,
   **Then** every page carries it at the top, with its HTML kept as markup.
3. **Given** an announcement that is a URL, **When** a reader opens a page, **Then** the HTML that
   URL returns is shown in the banner.
4. **Given** an announcement URL that fails, cannot be reached or returns nothing, **When** a
   reader opens a page, **Then** no banner is left on the page.
5. **Given** `sticky_banners` switched on, **When** the reader scrolls, **Then** the announcement
   behaves as that option means in the theme that defines it.
6. **Given** a banner, **When** a screen reader reaches it, **Then** it is announced as a named
   region before the header.

---

### User Story 5 - A reader moves to the previous or next page, or back to the top (Priority: P2)

A reader at the foot of a page moves to the previous or next page from cards that name them. When
the site author switches `navigation_with_keys` on, the left and right arrow keys do the same.
Far down a long page, when the reader scrolls back up, a button is offered that returns them to
the top.

**Why this priority**: how readers work through a guide in order, and the way back from the foot
of a long reference page.

**Independent Test**: build a test site with three pages in order and check each page's previous
and next links and titles, the marker that switches the arrow keys on, and the back-to-top
button's presence. Check the scroll and key behaviour in a browser.

**Acceptance Scenarios**:

1. **Given** a page with a previous and a next page, **When** a reader reaches its foot, **Then**
   two links name those pages and lead to them, marked as previous and next.
2. **Given** the first or the last page, **When** it is built, **Then** only the link that exists
   is shown.
3. **Given** `show_prev_next` switched off, or Sphinx's search or index page, **When** it is
   built, **Then** no previous and next links are shown.
4. **Given** `navigation_with_keys` switched on, **When** the reader presses the left or right
   arrow key, **Then** they move to the previous or next page.
5. **Given** `navigation_with_keys` switched on, **When** the reader presses an arrow key while
   typing in a field or holding a modifier key, **Then** nothing happens.
6. **Given** `navigation_with_keys` left at its default, **When** the reader presses an arrow key,
   **Then** the page does not change.
7. **Given** a long page, **When** the reader scrolls far down and then back up, **Then** a
   back-to-top button is offered. It is withdrawn while they scroll down and near the top.
8. **Given** the back-to-top button, **When** the reader presses it, **Then** the page returns to
   the top and focus moves to the main content.
9. **Given** `back_to_top_button` switched off, **When** the site builds, **Then** no page carries
   the button.
10. **Given** a page title with markup or special characters, **When** it is shown in a previous
    or next link, **Then** it reaches the page as Sphinx wrote it, and the link's address is
    escaped.

---

### Edge Cases

- A layout code given as a non-string value (a number, a list) is rejected with the same message
  as a code of the wrong shape.
- A component list that names `navbar-logo` while the layout code moves the logo to the primary
  sidebar: the navbar keeps it on narrow screens only.
- A component named in two lists is drawn in both places.
- A site that overrides `layout.html` blocks inherited from Sphinx's `basic` theme keeps working
  where those blocks still exist.
- A page built by a builder other than `html` and `dirhtml`, such as `singlehtml`, still builds.
- An announcement URL on a site opened from the file system, where the page script cannot fetch
  it: no banner is left on the page.

## Requirements *(mandatory)*

### Functional Requirements

**Layout code and component lists (US1)**

- **FR-001**: The theme MUST accept a `layout` option holding a layout code: three groups of three
  letters, the top row `h` or `l`, then `h`, then `h` or `r`; the middle row `l`, `p`, `r`; the
  bottom row `f` or `l`, then `f`, then `f` or `r`. The default MUST be `hHh LpR lff`.
- **FR-002**: An upper-case header, sidebar or footer letter MUST mark that area to stay in place
  as the page scrolls. Case MUST make no other difference.
- **FR-003**: The build MUST write, from the code, the arrangement of the five areas for wide
  screens and for medium screens without room for the secondary sidebar.
- **FR-004**: A layout code of the wrong shape MUST stop the build before any page is written,
  with a single message naming the option, quoting the code and stating the rules, and with no
  traceback.
- **FR-005**: The layout code's rules MUST have one source in the package's Python.
- **FR-006**: The theme MUST accept the component lists `navbar_start`, `navbar_center`,
  `navbar_end`, `navbar_persistent`, `article_header_start`, `article_header_end`,
  `article_footer_items`, `content_footer_items`, `primary_sidebar_end`,
  `secondary_sidebar_items`, `footer_start`, `footer_center` and `footer_end`, with
  pydata-sphinx-theme's names, types and defaults, each as a list or a comma-separated string of
  names with or without `.html`.
- **FR-007**: Each component list MUST draw its components in its area in the order given,
  looking first in the theme's components and then in the site's templates, and MUST skip a name
  that resolves to no template without failing the build.
- **FR-008**: The theme MUST ship the components `copyright`, `sphinx-version`, `theme-version`,
  `last-updated` and `navbar-logo`, each honouring the Sphinx setting that switches its content
  on.
- **FR-009**: The `theme-version` component MUST take the theme's repository address and version
  from the package's metadata.
- **FR-010**: Each component MUST be in a page's HTML once, including the `navbar_end`
  components, which are shown in the navbar or the drawer by screen width.
- **FR-011**: Every value a template prints from a theme option, `html_context` or the page
  context MUST be escaped, except markup Sphinx produced, as amended Article V states.

**The page a reader gets (US2)**

- **FR-012**: Every page MUST place the header, primary sidebar, main content, secondary sidebar
  and footer in the areas the layout code gives, with the main content in a centred column of
  readable width.
- **FR-013**: On a narrow screen, below the width of the medium arrangement, the page MUST be one
  column, and the primary sidebar
  MUST open as a drawer from a menu button in the navbar and close with Escape, a link inside it,
  its close button or a press outside it.
- **FR-014**: Every page MUST start with a skip link to the main content, and MUST name its
  header, site navigation, main content, page tools and footer landmarks.
- **FR-015**: A sticky header MUST be marked as scrolled while the page is scrolled away from the
  top, and a sticky sidebar under a sticky header MUST stay in place below it.
- **FR-016**: The secondary sidebar MUST be left out when it has no components and on Sphinx's
  search and index pages.
- **FR-017**: Fixed text the theme writes into a page MUST be marked for translation with
  Sphinx's message catalogue, and the package MUST ship the catalogue's template so translations
  can be added (Article VIII).
- **FR-018**: The page MUST carry, on `<body>`, the site root, file suffix, link suffix, builder
  name and page name that the page script reads.
- **FR-019**: The sidebar and page widths MUST be adjustable by a site through the custom
  properties `--daisy-primary-width`, `--daisy-main-width` and `--daisy-secondary-width`, which
  are documented as public.
- **FR-020**: Text the frame dims MUST meet WCAG 2.2 AA contrast on daisyUI's default light and
  dark themes, and every control the frame adds MUST be reachable by keyboard with a visible
  focus state (Article XIV).

**Brand and logo (US3)**

- **FR-021**: The theme MUST accept Furo's `light_logo`, `dark_logo` and `sidebar_hide_name`, and
  pydata-sphinx-theme's `logo` (`text`, `image_light`, `image_dark`, `alt_text`, `link`) and
  `logo_link`, each with its source theme's meaning, and MUST fall back to Sphinx's `html_logo`.
- **FR-022**: A logo given as a path relative to `_static`, a path starting `_static/`, or a full
  address MUST resolve correctly from every page.
- **FR-023**: The brand MUST show the logo for the reader's current mode, and the dark logo MUST
  fall back to the light one.
- **FR-024**: The brand MUST link to `logo.link` or `logo_link` when set, and to the site's home
  page otherwise.
- **FR-025**: When the layout code gives the top-left corner to the primary sidebar, the brand
  MUST appear at the head of the primary sidebar on wide screens and in the navbar on narrow
  ones, and once only on each.

**Announcement (US4)**

- **FR-026**: The theme MUST accept `announcement`, shared by Furo and pydata-sphinx-theme, as
  text or HTML printed as the site author's own markup, or as a URL whose returned HTML the page
  shows.
- **FR-027**: An announcement URL that fails or returns nothing MUST leave no banner on the page.
- **FR-028**: The theme MUST accept `sticky_banners` and honour it with the meaning its source
  theme gives it.
- **FR-029**: The banner MUST be a named region placed before the header.

**Previous, next and back to top (US5)**

- **FR-030**: The theme MUST accept `show_prev_next` (default on), `navigation_with_keys` (default
  off) and `back_to_top_button` (default on), with their source themes' meanings.
- **FR-031**: Previous and next links MUST name and lead to the pages Sphinx relates, and be left
  out on Sphinx's search and index pages.
- **FR-032**: With `navigation_with_keys` on, the left and right arrow keys MUST move to the
  previous and next page, except while the reader types in a field or holds a modifier key.
- **FR-033**: The back-to-top button MUST be offered only while the reader scrolls up far from the
  top, and pressing it MUST return to the top and move focus to the main content.

**Across the feature**

- **FR-034**: Every option this feature adds MUST be declared in `theme.toml`, and every option and
  component MUST be documented in the theme's reference with its default (Article VI).
- **FR-035**: The theme's templates MUST read option values through the one context the theme
  sets for each page, never `theme_*` values directly.

### Key Entities

- **Layout code**: the value of `layout`. Gives each corner of the page to an area and says which
  areas stay in place.
- **Component list**: an ordered list of component names for one place on the page.
- **Brand**: the site's logo for each mode, its name, the alternative text and the link.
- **Announcement**: a site author's text, HTML or URL shown across the top of every page.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A site that sets no theme options builds with no warnings and gives every page the
  five areas of the default layout code.
- **SC-002**: Every valid layout code builds, and every code of the wrong shape stops the build
  with one message and no traceback.
- **SC-003**: A configuration's logo, announcement, component lists and previous and next options
  written for Furo or pydata-sphinx-theme build unchanged and act with the meaning they have
  there.
- **SC-004**: Every page passes a keyboard walk: the skip link first, the drawer opened and closed
  without a pointer, and every control the frame adds focused visibly.
- **SC-005**: Each page shown at 390, 1100 and 1440 pixels wide matches the prototype's
  corresponding page side by side, for the home page, the four other layout codes, and the foot
  of a long page with the back-to-top button offered.
- **SC-006**: No value from a site's configuration reaches a built page unescaped, except the
  announcement and markup Sphinx produced.

## Clarifications

### Session 2026-11-17

- Q: How many stories, given the prototype names four features but the issue lists a site
  author's and a reader's part of the page frame separately? → A: Five. The page frame is two
  stories, one for the site author who arranges it and one for the reader who uses it, because a
  site author's and a reader's stories are never merged.
- Q: What do component lists default to when they name components another feature ships (such as
  `theme-switcher` or `page-toc`)? → A: pydata-sphinx-theme's defaults, as the prototype has
  them. A name whose component does not exist yet draws nothing, as FR-007 already requires for
  any unknown name, and starts drawing when its feature lands.
- Q: Does `sticky_banners` belong here or with a later feature? → A: Here. The prototype accepted
  it and did nothing, and names this feature to do it properly (FR-028).
- Q: Where does the `theme-version` component get the repository's address? → A: From the
  package's metadata, never written into the template (FR-009).
- Q: Is the announcement escaped like every other option? → A: No. It is the site author's own
  HTML, as in Furo and pydata-sphinx-theme, and the amended Article V says so (FR-011, FR-026).

## Assumptions

- The constitution's Article V is amended by #3 before this feature is built.
- The theme's own fixed text is in English, and the message catalogue ships with a template and
  no translations.
- `navbar_end` components are shown in the drawer on narrow screens, as the prototype does, from
  one copy in the HTML.
- The keyboard shortcut helper that the search dialog feature builds later is started here,
  small, for the arrow keys and the drawer's Escape key, and that feature grows it.
- Out of scope, owned by sibling features: site navigation and breadcrumbs (#5), On this page
  (#5), page-body styles (#6), modes and the theme picker (#7), the search dialog (#7), the
  version switcher (#7), icon links and edit and view links (#8), header links (#5), and the Furo
  and pydata-sphinx-theme configuration presets (#8). The layout playground and the rest of the
  documentation site are documentation work.
