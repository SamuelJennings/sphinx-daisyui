# Feature Specification: Icon and source links

**Feature Branch**: `005-links-and-compatibility`

**Created**: 2026-11-17

**Status**: Draft

**Input**: Issue #8, "Icon and source links", built from the accepted design on the
`prototype-theme` branch (`PROTOTYPE.md`, features 10 and 11).

**Goals**: none recorded yet. The repository has no `GOALS.md`, so this specification cites no
goal id.

**Depends on**: #4 (the page frame: component lists, the bundled icons, the square icon button,
the message catalogue and resolving a path under `_static`), #5 (the breadcrumbs the source
buttons sit beside) and #39 (the theme's own options in place of another theme's). It is written
against Article V as amended in constitution 1.1.0.

## Summary

A site author links the site's repository, chat, package index or other accounts as icons,
placed in the navbar or the footer like any other component. They say where the site's sources
live, so each page offers links to edit and view its source on GitHub, GitLab or Bitbucket, and
a reader opens them, or opens Sphinx's own copy of the source.

The options are the theme's own, with one name and one shape each. Where pydata-sphinx-theme has
an option for the same thing, its name and shape are used.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A site author links the site's accounts as icons (Priority: P1)

A site author lists the site's repository, chat, package index or other accounts in
`icon_links`. Each entry has a `name`, a `url` and an `icon`, which names one of the icons
bundled with the theme, or an image when the entry's `type` is `url` or `local`. They place the
`navbar-icon-links` component in any component list, such as `navbar_end` or `footer_end`, and
name the list for screen readers with `icon_links_label`.

**Why this priority**: most documentation sites link their repository, and the theme's default
navbar already lists the component.

**Independent Test**: build test sites with each kind of entry, placed in the navbar and in the
footer, and check each built link's address, its accessible name, the icon it carries and where
it sits on the page.

**Acceptance Scenarios**:

1. **Given** an `icon_links` entry whose `icon` names a bundled icon, **When** the site builds,
   **Then** the `navbar-icon-links` component carries a link to the entry's `url`, named with its
   `name` and drawn with that icon.
2. **Given** an entry whose `icon` names no bundled icon, **When** the site builds, **Then** the
   build warns, naming the entry and the icon, and the link is drawn with the theme's generic link
   icon.
3. **Given** an entry of type `url`, **When** the site builds, **Then** the link carries the image
   at that address.
4. **Given** an entry of type `local`, with a path relative to `_static`, a path starting
   `_static/` or a full address, **When** the site builds, **Then** every page, at any depth,
   points the image at the right file.
5. **Given** `navbar-icon-links` in a navbar list and in a footer list, **When** the site builds,
   **Then** the icon links appear in both places.
6. **Given** `icon_links_label`, **When** a screen reader reaches the icon links, **Then** the
   list is named with that text, and without it the list carries the theme's own name, taken from
   the message catalogue.
7. **Given** an icon link, **When** a keyboard reader reaches it, **Then** it can be focused,
   shows its focus, and is announced by its name.
8. **Given** a site author's name, address, label or image path, **When** the link is built,
   **Then** each reaches the page escaped, and image markup is built from it with escaping rather
   than by joining strings.
9. **Given** no `icon_links`, or an entry with no `url`, **When** the site builds, **Then** no
   page carries an empty list or a link that leads nowhere.

---

### User Story 2 - A site author points each page at its source (Priority: P2)

A site author sets `source_repository` to the site's repository on GitHub, GitLab or Bitbucket,
with `source_branch` and `source_directory`, and chooses with `top_of_page_buttons` whether the
edit button, the view button or both sit beside the breadcrumbs. They place the `edit-this-page`
and `sourcelink` components in a component list where they want links rather than buttons.

**Why this priority**: an edit link is how documentation gets fixed by its readers.

**Independent Test**: build test sites with a repository on each of the three hosts, and check
the built edit and view addresses for a page at the top of the site and one several folders deep.

**Acceptance Scenarios**:

1. **Given** `source_repository` on GitHub, GitLab or Bitbucket, with `source_branch` and
   `source_directory`, **When** a page is built, **Then** its edit and view addresses lead to that
   host's editor and file view for the page's source file on that branch.
2. **Given** `source_branch` unset, **When** a page is built, **Then** the addresses use the
   branch `main`.
3. **Given** `top_of_page_buttons` listing `edit`, `view` or both, **When** a page with a source
   is built, **Then** those buttons sit beside the breadcrumbs in the order listed. An empty list
   shows none.
4. **Given** the `edit-this-page` component in a component list and an edit address, **When** a
   page is built, **Then** it links to the edit address there.
5. **Given** a `source_repository` on a host the theme does not recognise, or none, **When** the
   site builds, **Then** the build succeeds and no page carries an edit or view button or link.
6. **Given** Sphinx's search page, index page or any other page with no source file, **When** it
   is built, **Then** it carries no edit, view or source button or link.
7. **Given** a page whose source has a suffix other than `.rst`, such as `.md`, **When** it is
   built, **Then** its addresses use its own suffix.
8. **Given** `source_directory` written with or without a trailing slash, **When** a page is
   built, **Then** the addresses are the same.
9. **Given** a site author's repository, branch or directory, **When** an address is built from
   it, **Then** it reaches the page escaped.
10. **Given** the built documentation, **When** a site author reads the theme's reference,
    **Then** every option and component in this story is documented with its default.

---

### User Story 3 - A reader opens the page's source (Priority: P2)

A reader who wants to correct or study a page opens its source: the edit page or the file on
GitHub, GitLab or Bitbucket, from the buttons beside the breadcrumbs or the links in the
secondary sidebar, or Sphinx's own copy of the source from the `sourcelink` component.

**Why this priority**: the reader's half of User Story 2, and the reason it exists.

**Independent Test**: build a test site with source links configured and check that each button
and link is named, reachable by keyboard and leads where it says. Walk them in a browser against
the prototype's pages.

**Acceptance Scenarios**:

1. **Given** a page with edit and view buttons beside the breadcrumbs, **When** a reader focuses
   or points at one, **Then** it says what it does, and following it opens the page's source on
   the host.
2. **Given** the `sourcelink` component in a component list and Sphinx's `html_show_sourcelink`
   and `html_copy_source` left on, **When** a reader follows the link, **Then** they reach
   Sphinx's copy of the page's source from any page at any depth.
3. **Given** `html_show_sourcelink` or `html_copy_source` switched off, **When** a page is built,
   **Then** the `sourcelink` component draws nothing.
4. **Given** the edit link and the source link in the secondary sidebar, **When** a reader moves
   through them with the keyboard, **Then** each is focusable, shows its focus and is announced
   by what it does.
5. **Given** a site whose `language` is set, **When** a page is built, **Then** the theme's own
   text on these buttons and links is taken from the message catalogue in that language where a
   translation exists.

---

### Edge Cases

- An `icon_links` entry with no `type` names a bundled icon.
- An `icon_links` entry with no `name` is drawn with its address as its accessible name.
- `icon_links` written as a list of entries in `conf.py` is the only shape. A string is rejected
  with a build warning naming the option.
- A `source_repository` with or without a trailing slash, or ending `.git`, gives the same
  addresses.
- A self-hosted GitLab or Bitbucket is not recognised, and gets no edit or view links (see
  Clarifications).
- A site that provides its own template under `navbar-icon-links`, `edit-this-page` or
  `sourcelink` in its `templates_path` gets its own template drawn.

## Requirements *(mandatory)*

### Functional Requirements

**Icon links (US1)**

- **FR-001**: The theme MUST accept `icon_links`, a list of entries each with `name`, `url`,
  `icon` and an optional `type` of `url` or `local`, and `icon_links_label`.
- **FR-002**: The theme MUST ship the `navbar-icon-links` component, drawing the icon links as a
  named list wherever a component list places it.
- **FR-003**: An entry with no `type` MUST be drawn with the bundled icon its `icon` names. An
  unknown name MUST warn and fall back to the generic link icon. The theme MUST load no icon font
  and nothing from another host (Article XII).
- **FR-004**: An entry of type `url` MUST show the image at its address, and one of type `local`
  MUST resolve its path the way a logo's path is resolved, from every page.
- **FR-005**: Every name, address, label and image path MUST reach the page escaped, and markup
  built from them in Python MUST be built with `markupsafe`, never by joining strings (Article V).
- **FR-006**: Each icon link MUST be reachable by keyboard, show a visible focus state and carry
  an accessible name (Article XIV).

**Source links (US2, US3)**

- **FR-007**: The theme MUST accept `source_repository`, `source_branch` (default `main`),
  `source_directory` and `top_of_page_buttons` (default `["edit"]`).
- **FR-008**: From `source_repository`, the theme MUST recognise GitHub, GitLab and Bitbucket and
  build each host's edit and view address for a page's source file.
- **FR-009**: The buttons `top_of_page_buttons` names MUST sit beside the breadcrumbs, in its
  order, leaving out any whose address is unknown. An empty list MUST show none.
- **FR-010**: The theme MUST ship the `edit-this-page` component, drawing the edit link when an
  edit address exists, and the `sourcelink` component, drawing a link to Sphinx's copy of the
  source when Sphinx shows and copies it.
- **FR-011**: A page with no source file, and every page of a site with no recognised repository,
  MUST carry no edit, view or source button or link, without failing or warning the build.
- **FR-012**: The edit and view buttons and links MUST each say what they do to a screen reader,
  be reachable by keyboard and show a visible focus state (Article XIV).
- **FR-013**: Every address built from a site author's options MUST reach the page escaped
  (Article V).

**Across the feature**

- **FR-014**: Fixed text the theme writes for these links and buttons MUST be marked for
  translation in the message catalogue (Article VIII).
- **FR-015**: Every option and component this feature adds MUST be declared in `theme.toml` and
  documented in the theme's reference with its default (Article VI).
- **FR-016**: The theme's templates MUST read every value through the one context the theme sets
  for each page, never `theme_*` values directly.

### Key Entities

- **Icon link**: a name, an address and an icon, which is a bundled icon or an image.
- **Source links**: for one page, its edit address, its view address and the address of Sphinx's
  copy of its source, each present only when known.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For a page at the top of the site and one three folders deep, every edit and view
  address built for GitHub, GitLab and Bitbucket leads to that host's page for the page's source.
- **SC-002**: No value from a site's configuration reaches a built page unescaped.
- **SC-003**: Every icon link, button and link this feature adds passes a keyboard walk, focused
  visibly and announced by name.
- **SC-004**: The home page and the Typography page shown at 390, 1100 and 1440 pixels wide match
  the prototype's side by side for the icon links, the source buttons and the secondary-sidebar
  links.

## Clarifications

### Session 2026-11-17

- Q: The prototype names two features here; how many stories? → A: Three. Source links have a
  site author who points the pages at their source and a reader who opens it, and those two
  people's stories are never merged.
- Q: How does a site put icon links in the footer? → A: By placing `navbar-icon-links` in a
  footer component list. There is no separate footer option.
- Q: Which option says whether to show the edit and view links? → A: `top_of_page_buttons`, a
  list of `edit` and `view`, for the buttons beside the breadcrumbs. Links in a sidebar are shown
  by placing the `edit-this-page` or `sourcelink` component.
- Q: How is the host chosen? → A: From `source_repository`'s address: `github.com`, `gitlab.com`
  or `bitbucket.org`. Self-hosted instances are not recognised in this feature. An option to name
  the host can be added later without changing these.
- Q: What does an icon name that is not bundled do? → A: It warns and draws the generic link
  icon, so a typo shows in the build log and a build with warnings as errors stops.

## Assumptions

- The component lists, the icons, the square icon button, the message catalogue and the
  static-path method of the page frame (#4), and the breadcrumbs (#5), exist before this feature is
  built.
- The icons a site is likely to link (GitHub, GitLab, Bitbucket, PyPI, Mastodon, Discord, X and
  the rest of the prototype's set) are in the bundled icon set, and the reference lists them.
- Out of scope, owned by sibling features: the logo, announcement and component lists (#4), site
  navigation, breadcrumbs and On this page (#5), page-body styles (#6), modes and search (#7).
