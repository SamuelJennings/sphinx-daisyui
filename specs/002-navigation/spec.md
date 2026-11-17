# Feature Specification: Find the way around the site and the page

**Feature Branch**: `002-navigation`

**Created**: 2026-11-17

**Status**: Draft

**Input**: Issue #5, "Find the way around the site and the page", built from the accepted design
on the `prototype-theme` branch (`PROTOTYPE.md`, features 2, 13 and 4).

**Goals**: none recorded yet. The repository has no `GOALS.md`, so this specification cites no
goal id.

**Depends on**: #4, the page frame. This feature draws into the primary sidebar, the navbar, the
drawer, the page's header and the secondary sidebar that #4 builds, and its components are placed
by #4's component lists.

## Summary

A reader finds their way around the site and around the page. The primary sidebar holds the site
navigation: the whole site as a menu whose branches open and close, the current page marked and
scrolled into view, captions labelling each section, with breadcrumbs above the page showing
where it sits. A site author who places `navbar-nav` in the header moves the site's top-level
sections into the navbar, as pydata-sphinx-theme does, and the primary sidebar then shows only
the current section. The secondary sidebar lists the page's own headings and marks the one being
read, or offers them in a disclosure above the page on a narrower screen.

Every option here is borrowed from pydata-sphinx-theme and keeps its name, type and meaning
(Article X). By default the site navigation follows Furo, with the whole tree in the primary
sidebar and no header links.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A reader moves through the whole site from the primary sidebar (Priority: P1)

A reader opens any page and finds every page of the site in the primary sidebar, grouped under
the captions the site's toctrees give. They open and close a branch to see the pages under it,
see which page they are on and the branches that lead to it, and follow any entry to its page.
Above the page, breadcrumbs show where the page sits in the site and lead back up it. On a phone
the same menu is in the drawer. How deep the menu goes and how much of it starts open is what the
site author sets with `navigation_depth`, `show_nav_level`, `collapse_navigation` and
`sidebar_includehidden`.

**Why this priority**: the way a reader gets from one page to any other. Every page of every site
carries it, and the breadcrumbs component is already in the default `article_header_start`.

**Independent Test**: build a test site with nested toctrees, a caption, a hidden toctree and an
external entry, and check each page's built menu: its entries and order, the toggles and their
states, the current and on-path marks, the captions, the external marks and the breadcrumbs.
Check the toggles and the scrolling into view in a browser.

**Acceptance Scenarios**:

1. **Given** a site with no navigation options set, **When** a page is built, **Then** the primary
   sidebar holds every page of the site's toctrees, to four levels deep, in toctree order.
2. **Given** a toctree with a caption, **When** a page is built, **Then** the caption labels the
   group of entries under it in the menu.
3. **Given** an entry with pages under it, **When** a reader activates its toggle, by pointer or
   from the keyboard, **Then** the pages under it are shown or hidden, the toggle reports whether
   it is open, and the entry itself stays a link to its own page.
4. **Given** the page being read, **When** it is built, **Then** its entry is marked as the current
   page for sighted and screen-reader readers alike, the entries above it are marked as on its
   path, and every branch on that path starts open.
5. **Given** a page whose entry lies below the visible part of the primary sidebar, **When** the
   reader opens it, **Then** the sidebar is scrolled so the entry is in view, and the page itself
   is not scrolled.
6. **Given** `show_nav_level` left at its default, **When** a page is built, **Then** only the
   branches on the current page's path start open. **Given** `show_nav_level` set to a higher
   number, **Then** branches above that level start open as well.
7. **Given** `navigation_depth` set to a number, **When** a page is built, **Then** the menu holds
   no entries deeper than that number of levels.
8. **Given** `collapse_navigation` switched on, **When** a page is built, **Then** only the
   branches on the current page's path carry the pages under them, and the other entries carry
   no pages and no toggle.
9. **Given** a toctree marked `:hidden:`, **When** a page is built with `sidebar_includehidden`
   left at its default, **Then** its entries are in the menu. **Given** `sidebar_includehidden`
   switched off, **Then** they are not.
10. **Given** a toctree entry that links outside the site, **When** a page is built, **Then** its
    entry is marked as leading outside the site, in a way a screen reader announces.
11. **Given** a page below the home page, **When** it is built, **Then** the breadcrumbs lead from
    the home page through each page above it to the current page, which is marked as current and
    is not a link.
12. **Given** the home page, **When** it is built, **Then** no breadcrumbs are drawn.
13. **Given** a site with no toctree, **When** a page is built, **Then** the primary sidebar holds
    no site navigation and the build succeeds.
14. **Given** an entry's or a breadcrumb's page title with markup or special characters, **When**
    it is built, **Then** it reaches the page as Sphinx wrote it.

---

### User Story 2 - A site author puts the site's sections in the header (Priority: P2)

A site author places `navbar-nav` in `navbar_center`, as a pydata-sphinx-theme configuration
does, and the site's top-level sections move into the navbar as header links, with the current
section marked. They add links to other sites with `external_links`, decide with
`header_links_before_dropdown` how many links show before the rest go into a menu, name that menu
with `header_dropdown_text`, and line the links up with `navbar_align`. The primary sidebar then
shows only the pages of the current section. On a phone, where the navbar has no room for them,
the sections are listed at the head of the drawer.

**Why this priority**: the shape of every pydata-sphinx-theme site, which a site switching from
that theme expects to keep. The default layout, following Furo, does without it.

**Independent Test**: build a test site with six top-level sections and an external link, with
`navbar-nav` in `navbar_center`, and check the built navbar's links, their order, the menu and its
name, the current marks, the alignment marker, the primary sidebar's entries on a page in one
section and on the home page, and the sections at the head of the drawer.

**Acceptance Scenarios**:

1. **Given** `navbar-nav` in `navbar_center`, **When** a page is built, **Then** the navbar holds
   a link to each top-level page of the site's toctrees, in toctree order, and the link to the
   section holding the current page is marked as current.
2. **Given** `external_links` listing links with a name and an address, **When** a page is built,
   **Then** they follow the site's sections, in the order given, each marked as leading outside
   the site.
3. **Given** more header links than `header_links_before_dropdown` allows (five by default),
   **When** a page is built, **Then** the first ones are shown in the navbar and the rest are in a
   menu named by `header_dropdown_text`, which a reader opens and moves through from the keyboard.
4. **Given** the current section is one of the links in the menu, **When** a page is built,
   **Then** the menu's control and that link are both marked as current.
5. **Given** `navbar-nav` in `navbar_center`, **When** a page inside a top-level section is built,
   **Then** the primary sidebar's site navigation holds only the pages of that section, with the
   same toggles, marks and options as US1.
6. **Given** `navbar-nav` in `navbar_center`, **When** a page that belongs to no top-level section
   is built, such as the home page, **Then** the primary sidebar holds no site navigation, and no
   empty menu.
7. **Given** `navbar_align` left at `content`, set to `left` or set to `right`, **When** a page is
   built on a wide screen, **Then** the header links line up with the start of the page column,
   sit at the start of the navbar's free space, or sit at its end, as pydata-sphinx-theme places
   them.
8. **Given** `navbar-nav` in `navbar_center` and a narrow screen, **When** the reader opens the
   drawer, **Then** every header link, those in the menu included, is listed at the head of the
   drawer, above the site navigation, with the current section marked.
9. **Given** `navbar-nav` placed in a component list other than `navbar_center`, **When** a page is
   built, **Then** the header links are drawn there and the primary sidebar keeps the whole site.
10. **Given** no `navbar-nav` in any component list, **When** a page is built, **Then** no header
    links are drawn and the primary sidebar holds the whole site, as in US1.
11. **Given** an external link's name or address, or `header_dropdown_text`, holding characters
    that mean something in HTML, **When** a page is built, **Then** each reaches the page escaped.

---

### User Story 3 - A reader finds their place on the page (Priority: P1)

A reader on a long page sees its headings listed in the secondary sidebar, with the heading they
are reading marked as they scroll, and follows any of them to its section. On a screen too narrow
for the secondary sidebar, the same headings are in a disclosure above the page that they open
when they want it. How many levels show at once is what the site author sets with
`show_toc_level`.

**Why this priority**: how a reader moves around a long reference or guide page, and what tells
them where they are in it. The `page-toc` component is already the default of
`secondary_sidebar_items`.

**Independent Test**: build a test site with a page of three heading levels and a page with no
headings below its title, and check the built list's entries, the level marker, the disclosure
and its absence. Check the marking while scrolling, at the foot of the page, and the disclosure
closing, in a browser.

**Acceptance Scenarios**:

1. **Given** a page with headings below its title and `page-toc` in `secondary_sidebar_items`,
   **When** it is built, **Then** the secondary sidebar lists the page's headings in order, nested
   by level, each linking to its heading, and leaves out the page's own title.
2. **Given** a page with no headings below its title, **When** it is built, **Then** no list and
   no disclosure of the page's headings are drawn.
3. **Given** a reader scrolling the page, **When** a heading reaches the top of the reading area,
   **Then** its entry is marked as the one being read, for sighted and screen-reader readers
   alike, and the mark leaves the entry before it.
4. **Given** a reader at the foot of the page, **When** the last heading never reaches the top,
   **Then** the last heading's entry is the one marked.
5. **Given** `show_toc_level` left at its default, **When** the page is built, **Then** headings
   down to the second level are listed at all times. **Given** `show_toc_level` set to another
   number, **Then** headings down to that level are listed at all times, and deeper headings are
   shown while the reader is in the section that holds them, as pydata-sphinx-theme shows them.
6. **Given** a screen too narrow for the secondary sidebar, **When** a reader opens a page with
   headings, **Then** a closed disclosure above the page body holds the same headings, and
   following one of them closes it.
7. **Given** `page-toc` not in `secondary_sidebar_items`, **When** a page is built, **Then** no
   disclosure of the page's headings is drawn on narrow screens either.
8. **Given** a heading whose anchor holds characters outside ASCII, **When** the reader scrolls to
   it, **Then** its entry is marked like any other.
9. **Given** Sphinx's search or index page, **When** it is built, **Then** no list of the page's
   headings is drawn.

---

### Edge Cases

- A page in no toctree (an orphan): the menu is drawn with no entry marked, and the breadcrumbs
  lead from the home page to the page.
- A toctree entry that is a bare address with no title: the menu shows it as Sphinx titles it.
- A page title long enough to wrap: the entry wraps within the primary sidebar and its toggle stays
  beside it.
- A site built with the `dirhtml` builder: every menu, header and breadcrumb link reaches its page.
- A site built with a builder that gives no toctree, such as `singlehtml`: the build succeeds.
- `header_links_before_dropdown` set to zero: every header link is in the menu.
- `header_links_before_dropdown` at or above the number of links: no menu is drawn.
- `navigation_depth`, `show_nav_level`, `show_toc_level` or `header_links_before_dropdown` given as
  a string of digits, as `-D` on the command line gives it: read as the number.
- A page with headings and no secondary sidebar components at all: the frame leaves the secondary
  sidebar out (#4), and the narrow-screen disclosure follows US3 scenario 7.

## Requirements *(mandatory)*

### Functional Requirements

**Site navigation and breadcrumbs (US1)**

- **FR-001**: The theme MUST ship the `sidebar-nav.html` sidebar template, named in the theme's
  default `html_sidebars`, that draws the site's toctrees in the primary sidebar as one menu, in
  toctree order, with each toctree's caption labelling its group.
- **FR-002**: Every menu entry with pages under it MUST carry a toggle beside its link that shows
  and hides those pages, is reachable and operable from the keyboard, exposes its state to
  assistive technology and is named for the entry it belongs to. The entry MUST stay a link.
- **FR-003**: The current page's entry MUST be marked as the current page, including for assistive
  technology, and the entries on its path MUST be marked as on its path and start open.
- **FR-004**: When a page loads, the current page's entry MUST be scrolled into view inside the
  primary sidebar if it is outside it, without scrolling the page.
- **FR-005**: The theme MUST accept `navigation_depth` (default 4), `show_nav_level` (default 1),
  `collapse_navigation` (default off) and `sidebar_includehidden` (default on), with
  pydata-sphinx-theme's types and meanings.
- **FR-006**: A menu entry or header link that leads outside the site MUST be marked as such,
  including for assistive technology.
- **FR-007**: The theme MUST ship the `breadcrumbs` component, which leads from the home page
  through each page above the current one to the current page, marks the current page and does
  not link it, is a named landmark, and draws nothing on the home page.

**Header links (US2)**

- **FR-008**: The theme MUST ship the `navbar-nav` component, which draws a link to each top-level
  page of the site's toctrees, then each of `external_links`, and marks the link to the section
  holding the current page.
- **FR-009**: The theme MUST accept `external_links` (a list of links, each with a `name` and a
  `url`), `header_links_before_dropdown` (default 5), `header_dropdown_text` (default "More") and
  `navbar_align` (`content` by default, `left` or `right`), with pydata-sphinx-theme's types and
  meanings.
- **FR-010**: Header links past `header_links_before_dropdown` MUST be in a menu named by
  `header_dropdown_text`, which opens, moves and closes from the keyboard and is marked as current
  when it holds the current section.
- **FR-011**: `navbar_align` MUST be honoured in full: `content` lines the header links up with
  the start of the page column, `left` puts them at the start of the navbar's free space, and
  `right` at its end.
- **FR-012**: When `navbar-nav` is in `navbar_center`, the primary sidebar's site navigation MUST
  hold only the pages of the current top-level section, and nothing on a page in no section.
  Placed anywhere else, `navbar-nav` MUST leave the site navigation whole.
- **FR-013**: When `navbar-nav` is in `navbar_center`, the drawer MUST list every header link at
  its head on narrow screens, above the site navigation, with the current section marked.

**On this page (US3)**

- **FR-014**: The theme MUST ship the `page-toc` component, which lists the page's headings below
  its title, nested by level, each linking to its heading, as a named landmark, and draws nothing
  on a page with no such headings.
- **FR-015**: As the reader scrolls, the entry of the heading being read MUST be marked, including
  for assistive technology, and at the foot of the page the last heading's entry MUST be marked.
- **FR-016**: The theme MUST accept `show_toc_level` with pydata-sphinx-theme's type and meaning:
  headings down to that level are listed at all times and deeper ones are shown while the reader
  is in the section that holds them. Its default MUST be 2.
- **FR-017**: When `page-toc` is in `secondary_sidebar_items`, a page with headings MUST also
  carry, on screens with no secondary sidebar, a disclosure above the page body that starts closed,
  holds the same headings, and closes when one of them is followed.

**Across the feature**

- **FR-018**: Every value a template prints from a theme option, `html_context` or the page
  context MUST be escaped, except markup Sphinx produced, such as page titles in the toctree, as
  amended Article V states. Markup the theme builds from option text MUST be escaped where it is
  built.
- **FR-019**: Fixed text the theme writes into a page here, such as the landmark names, the
  toggles' names, the disclosure's label and the default of `header_dropdown_text`, MUST be marked
  for translation in the message catalogue #4 sets up (Article VIII). A value the site author sets
  MUST NOT be translated.
- **FR-020**: Every control this feature adds MUST be reachable by keyboard with a visible focus
  state, and text it dims MUST meet WCAG 2.2 AA contrast on daisyUI's default light and dark
  themes (Article XIV).
- **FR-021**: A runtime dependency this feature adds MUST carry a stated reason in the
  documentation of the package's dependencies, and `deptry` MUST pass (Article VII).
- **FR-022**: Every option this feature adds MUST be declared in `theme.toml`, and every option
  and component MUST be documented in the theme's reference with its default (Article VI).
- **FR-023**: The templates MUST read option values through the one context the theme sets for
  each page, never `theme_*` values directly.

### Key Entities

- **Site navigation**: the site's toctrees as a menu of entries, each with a title, a link, the
  pages under it, and whether it is current, on the current page's path, open, or outside the site.
- **Header link**: a top-level section or an external link shown in the navbar, with its title,
  address, whether it is current and whether it is outside the site.
- **Breadcrumbs**: the pages above the current one, from the home page down.
- **On this page**: the page's headings below its title, nested by level, each with its anchor.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A configuration's navigation, header link and On this page options written for
  pydata-sphinx-theme build unchanged and act with the meaning they have there, and a Furo
  configuration, which sets none of them, gets the whole site in the primary sidebar.
- **SC-002**: Every page passes a keyboard walk with no pointer: each branch of the menu opened and
  closed, the header links' menu opened and an entry followed, and the On this page disclosure
  opened and a heading followed, with every control focused visibly.
- **SC-003**: On every page of the theme's documentation site, the current page's entry is in view
  in the primary sidebar once the page has loaded.
- **SC-004**: Each page shown at 390, 1100 and 1440 pixels wide matches the prototype's
  corresponding page side by side, for the rows of "Pages to compare side by side" that name
  features 2, 4 or 13: the home page with the drawer open, Typography scrolled to the middle, a
  toctree in a page, a deep page, the tall secondary sidebar, and the pydata-sphinx-theme
  configuration's pages with the drawer open at 390.
- **SC-005**: No value from a site's configuration reaches a built page unescaped, and every piece
  of fixed text this feature writes is in the message catalogue's template.

## Clarifications

### Session 2026-11-17

- Q: How many stories, when the site navigation has a reader's part and a site author's part? →
  A: Three, one per feature of the prototype. The site author's navigation options only vary what
  the reader's menu holds and how much starts open, so they are scenarios of the reader's story
  (US1 scenarios 6 to 9). Header links are the site author's story, because placing `navbar-nav`
  is something a site author sets out to do.
- Q: What does `show_toc_level` default to? → A: 2, as in the accepted prototype, whose screens
  show two levels. pydata-sphinx-theme defaults to 1. A pydata-sphinx-theme configuration that sets
  it keeps its meaning (FR-016).
- Q: Does placing `navbar-nav` anywhere switch the primary sidebar to the current section? → A:
  Only in `navbar_center`, as the prototype's recorded decision says. Placed elsewhere it draws the
  header links and the sidebar keeps the whole site (FR-012).
- Q: What does the primary sidebar show, with header links in the navbar, on a page in no section,
  such as the home page? → A: No site navigation and no empty menu (US2 scenario 6). Whether the
  frame then leaves the empty area out is the page frame's behaviour (#4).
- Q: Is `header_dropdown_text` translated? → A: Its default is the theme's own text and is
  translated. A value the site author sets is theirs and is printed as written (FR-019).
- Q: What does `collapse_navigation` do? → A: pydata-sphinx-theme's meaning: only the branches on
  the current page's path carry their pages, and other entries carry no toggle (US1 scenario 8).

## Assumptions

- The page frame (#4) is built first: its component lists place `breadcrumbs`, `navbar-nav` and
  `page-toc`, its drawer holds the primary sidebar on narrow screens, and its message catalogue
  takes this feature's text.
- `secondary_sidebar_items` defaults to `page-toc` and `article_header_start` to `breadcrumbs`, as
  #4 sets them. `navbar_center` defaults to empty, as in the accepted prototype, so a site that
  sets nothing gets Furo's shape, with no header links. pydata-sphinx-theme defaults it to
  `navbar-nav`, and a configuration copied from it names it anyway.
- The theme's own fixed text is in English.
- Out of scope, owned by sibling features: the page frame, the logo and the drawer itself (#4); a
  toctree drawn in a page body, which reuses this feature's open-and-close branch (#6); the shared
  navbar menu for the theme and version menus (#7); the edit and source links beside the
  breadcrumbs and in the secondary sidebar (#8); and the Furo and pydata-sphinx-theme names for the
  site navigation template, `sidebar/navigation.html` and `sidebar-nav-bs.html` (#8).
