# Feature Specification: Icon and source links, and switching from Furo or pydata-sphinx-theme

**Feature Branch**: `005-links-and-compatibility`

**Created**: 2026-11-17

**Status**: Draft

**Input**: Issue #8, "Icon and source links, and switching from Furo or pydata-sphinx-theme",
built from the accepted design on the `prototype-theme` branch (`PROTOTYPE.md`, features 10, 11,
14 and 15).

**Goals**: none recorded yet. The repository has no `GOALS.md`, so this specification cites no
goal id.

**Depends on**: #4 (the page frame: component lists, the bundled icons, the square icon button,
the message catalogue and resolving a path under `_static`), #5 (the site navigation component
and the breadcrumbs), #6 (the page-body styles that Furo's link colour reaches) and #7 (the modes
that Furo's CSS variables follow, and the search button). It is written against Article V as
amended in constitution 1.1.0.

## Summary

A site author links the site's repository, chat or package index as icons in the navbar or the
footer, and points every page at its source so a reader can edit it or view it on GitHub, GitLab
or Bitbucket, or open Sphinx's copy of it. A site author whose `conf.py` was written for Furo or
for pydata-sphinx-theme switches to this theme by changing `html_theme` only: every option and
template name those themes define is accepted, the ones with a meaning here act on it, and the
rest draw nothing.

Everything a site author writes here is a theme option, an `html_sidebars` name, a component
name or an `html_context` key that Furo or pydata-sphinx-theme already defines. Each keeps its
name, type and meaning (Article X).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A site author links the site's accounts as icons (Priority: P2)

A site author links the site's repository, chat, package index or other accounts as icons, in
the navbar or in the footer. They write the links in pydata-sphinx-theme's shape (`github_url`,
`gitlab_url`, `bitbucket_url`, `twitter_url`, `icon_links` with `name`, `url`, `icon`, `type` and
`attributes`, and `icon_links_label`) or in Furo's (`footer_icons` with `name`, `url`, `html` and
`class`). A Font Awesome name such as `fa-brands fa-github` is matched to an icon bundled with the
theme, so no icon font is loaded. The `navbar-icon-links` component places pydata-style links,
wherever a component list names it.

**Why this priority**: most sites link their repository, and both themes' configurations carry
these options, but a site reads without them.

**Independent Test**: build test sites with each shape of option, and check each built link's
address, its accessible name, the icon it carries and where it sits on the page.

**Acceptance Scenarios**:

1. **Given** `github_url`, `gitlab_url`, `bitbucket_url` or `twitter_url`, **When** the site
   builds, **Then** the `navbar-icon-links` component carries a link to that address, named for
   the service and drawn with that service's bundled icon.
2. **Given** an `icon_links` entry whose `icon` is a Font Awesome name with a bundled
   counterpart, **When** the site builds, **Then** the link carries that bundled icon, whatever
   the order and prefixes of the classes in the name.
3. **Given** an `icon_links` entry whose `icon` is a Font Awesome name with no bundled
   counterpart, **When** the site builds, **Then** the link carries the theme's generic link icon
   and the build succeeds.
4. **Given** an `icon_links` entry of type `url`, **When** the site builds, **Then** the link
   carries the image at that address.
5. **Given** an `icon_links` entry of type `local`, with a path relative to `_static`, a path
   starting `_static/` or a full address, **When** the site builds, **Then** every page, at any
   depth, points the image at the right file.
6. **Given** an `icon_links` entry with `attributes`, **When** the site builds, **Then** those
   attributes are on the link, replacing the theme's own where they name the same one.
7. **Given** `icon_links_label`, **When** a screen reader reaches the icon links, **Then** the
   list is named with that text.
8. **Given** Furo's `footer_icons`, **When** the site builds, **Then** each entry is a link at
   the end of the footer, named with its `name`, leading to its `url` and drawn with its own
   `html`.
9. **Given** an icon link, **When** a keyboard reader reaches it, **Then** it can be focused,
   shows its focus, and is announced by its name.
10. **Given** a site author's name, address, label, attribute or image path in any of these
    options, **When** the link is built, **Then** each reaches the page escaped, and the image
    markup is built from it with escaping rather than by joining strings.
11. **Given** no icon link options, **When** the site builds, **Then** no page carries an empty
    list of icon links.

---

### User Story 2 - A site author points each page at its source (Priority: P2)

A site author says where the site's sources live, so that each page can offer a link to edit it
and a link to view it on GitHub, GitLab or Bitbucket. They write it in Furo's shape
(`source_repository`, `source_branch`, `source_directory`, `source_edit_link`,
`source_view_link`, and `top_of_page_buttons` or the older `top_of_page_button` to choose which
buttons sit beside the breadcrumbs) or in pydata-sphinx-theme's (`use_edit_page_button` with the
`html_context` keys `github_user`, `github_repo`, `github_version`, their GitLab and Bitbucket
equivalents, `doc_path`, a self-hosted `github_url`, `gitlab_url` or `bitbucket_url`, and
`edit_page_url_template`). They place the `edit-this-page` and `sourcelink` components where
they want links rather than buttons.

**Why this priority**: an edit link is how documentation gets fixed by its readers, and most
configurations copied from either theme set one.

**Independent Test**: build test sites with each shape of option for each host, and check the
built edit and view addresses for a page at the top of the site and one several folders deep.

**Acceptance Scenarios**:

1. **Given** Furo's `source_repository`, `source_branch` and `source_directory`, **When** a page
   is built, **Then** its edit and view addresses lead to that page's source file on that branch,
   as Furo builds them.
2. **Given** `source_edit_link` or `source_view_link` with `{filename}` in it, **When** a page is
   built, **Then** that address is used with the page's source file name filled in, in place of
   the one built from `source_repository`.
3. **Given** `top_of_page_buttons` listing `view`, `edit` or both, **When** a page with a source
   is built, **Then** those buttons sit beside the breadcrumbs in the order listed, and a button
   whose address is unknown is left out.
4. **Given** `top_of_page_buttons` set to an empty list, **When** a page is built, **Then** no
   button sits beside the breadcrumbs. **Given** only the older `top_of_page_button`, **Then** it
   is read as a list of one.
5. **Given** `use_edit_page_button` switched on and `html_context` naming a GitHub, GitLab or
   Bitbucket user, repository and version, **When** a page is built, **Then** the
   `edit-this-page` component links to that host's edit page for the page's source, under
   `doc_path`, as pydata-sphinx-theme builds it, and names the host it leads to.
6. **Given** a self-hosted `github_url`, `gitlab_url` or `bitbucket_url` in `html_context`, or
   `edit_page_url_template`, **When** a page is built, **Then** the edit address uses that host or
   that template.
7. **Given** `use_edit_page_button` switched on and the `edit-this-page` component in no
   component list, **When** a page is built, **Then** the edit link is added to the secondary
   sidebar. **Given** `use_edit_page_button` left off, **Then** the `edit-this-page` component
   draws nothing, wherever it is listed.
8. **Given** `use_edit_page_button` switched on and no host in `html_context`, **When** the site
   builds, **Then** the build succeeds and no page carries an edit link.
9. **Given** Sphinx's search page, index page or any other page with no source file, **When** it
   is built, **Then** it carries no edit or view button or link.
10. **Given** a site author's repository, branch, directory, template or `html_context` value,
    **When** an address is built from it, **Then** it reaches the page escaped.

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

### User Story 4 - A site author switches from Furo (Priority: P1)

A site author whose `conf.py` was written for Furo changes `html_theme` to `daisyui` and keeps
everything else. Every Furo option and every `html_sidebars` name Furo ships is accepted. The
ones with a meaning here act on it: the logo, the announcement, footer icons, the source buttons,
the arrow keys and Furo's CSS variables, which are mapped onto the daisyUI tokens they
correspond to. The rest draw nothing. A guide in the documentation says what each Furo option
does here, and the documentation is also built with Furo's own documentation's configuration to
show the result.

**Why this priority**: the theme's reason to exist is that a site can switch to it from the
themes most sites use without rewriting its configuration.

**Independent Test**: build a test site with Furo's documentation's own `html_theme_options` and
an `html_sidebars` naming every Furo sidebar template, with warnings as errors. Check that it
builds, and that the options with a meaning act on it.

**Acceptance Scenarios**:

1. **Given** a configuration that sets every option Furo 2025.12 declares, **When** the site
   builds with warnings as errors, **Then** it builds.
2. **Given** `html_sidebars` naming any of `sidebar/brand.html`, `sidebar/search.html`,
   `sidebar/navigation.html`, `sidebar/scroll-start.html`, `sidebar/scroll-end.html`,
   `sidebar/ethical-ads.html`, `sidebar/rtd-versions.html` or `sidebar/variant-selector.html`,
   **When** the site builds, **Then** it builds, `sidebar/navigation.html` draws the site
   navigation, and the others draw nothing, because the brand and search are in the navbar.
3. **Given** `light_css_variables` or `dark_css_variables` naming a Furo variable that has a
   daisyUI counterpart, **When** a reader views the page in that mode, **Then** the counterpart
   token takes the value given, so everything drawn with that token follows it.
4. **Given** a Furo CSS variable with no daisyUI counterpart, **When** the site builds, **Then**
   it is set on the page as written, and the build succeeds.
5. **Given** a CSS variable value that tries to end the style it is written into or add rules of
   its own, **When** the site builds, **Then** it cannot change anything beyond that one variable.
6. **Given** the theme's documentation, **When** a site author opens the guide to switching from
   Furo, **Then** every Furo option and sidebar name is listed with what it does here, including
   those that draw nothing.
7. **Given** the theme's documentation, **When** it is built a second time with Furo's
   documentation's configuration, **Then** that build succeeds with warnings as errors and shows
   the logo, announcement, footer icons, source buttons and brand colour that configuration sets.

---

### User Story 5 - A site author switches from pydata-sphinx-theme (Priority: P1)

A site author whose `conf.py` was written for pydata-sphinx-theme changes `html_theme` to
`daisyui` and keeps everything else, `html_context` included. Every option pydata-sphinx-theme
declares and every component name it ships is accepted, the ones with a meaning here act on it,
and the ones this theme can't honour yet are accepted and ignored. A guide in the documentation
says what each pydata-sphinx-theme option does here, and the documentation is also built with a
pydata-sphinx-theme configuration to show the result.

**Why this priority**: as for User Story 4, for the other theme most sites use.

**Independent Test**: build a test site whose configuration sets every pydata-sphinx-theme option
and places every component name it ships, with warnings as errors.

**Acceptance Scenarios**:

1. **Given** a configuration that sets every option pydata-sphinx-theme 0.24 declares, **When**
   the site builds with warnings as errors, **Then** it builds.
2. **Given** component lists and `html_sidebars` naming any component pydata-sphinx-theme 0.24
   ships, **When** the site builds, **Then** it builds, `sidebar-nav-bs` draws the site
   navigation, `icon-links` draws the icon links, and a name with no counterpart here draws
   nothing.
3. **Given** `analytics`, `shorten_urls`, `surface_warnings` or `templates_skip_empty_check`,
   **When** the site builds, **Then** it builds and the option changes nothing, and the theme's
   reference says the option is accepted and ignored.
4. **Given** the theme's documentation, **When** a site author opens the guide to switching from
   pydata-sphinx-theme, **Then** every option and component name is listed with what it does here,
   including those accepted and ignored.
5. **Given** the theme's documentation, **When** it is built a third time with a
   pydata-sphinx-theme configuration, **Then** that build succeeds with warnings as errors and
   shows the logo, icon links, header links, version switcher and edit and source links that
   configuration sets.

---

### Edge Cases

- An `icon_links` entry with no `type` is read as Font Awesome, as pydata-sphinx-theme reads it.
- An `icon_links` entry whose `icon` names one of the theme's bundled icons directly, such as
  `pypi`, carries that icon.
- An icon link with no `url`, or an empty one, is left out rather than drawn as a dead link.
- `footer_icons` entries whose `html` is empty are drawn as named links with no icon.
- A page whose source file has a suffix other than `.rst`, such as `.md` from MyST, gets edit and
  view addresses with its own suffix.
- `source_directory` and `doc_path` written with or without a trailing slash give the same
  address.
- A Furo configuration and a pydata-sphinx-theme configuration mixed in one `conf.py` (both
  `top_of_page_buttons` and `use_edit_page_button`, say) builds, and each option keeps its own
  meaning.
- A site that provides a template of its own under one of the accepted names in its
  `templates_path` gets its own template drawn.
- Options of pydata-sphinx-theme versions older than 0.24 that it has since removed are not
  promised.

## Requirements *(mandatory)*

### Functional Requirements

**Icon links (US1)**

- **FR-001**: The theme MUST accept pydata-sphinx-theme's `github_url`, `gitlab_url`,
  `bitbucket_url`, `twitter_url`, `icon_links` and `icon_links_label`, and Furo's `footer_icons`,
  each with its source theme's meaning.
- **FR-002**: The theme MUST ship the `navbar-icon-links` component, drawing the pydata-style icon
  links as a named list, and draw Furo's `footer_icons` at the end of the footer.
- **FR-003**: An `icon_links` entry of type `fontawesome` (or no type) MUST carry the bundled icon
  that matches its Font Awesome name, or the generic link icon when none matches. The theme MUST
  load no icon font and nothing from another host (Article XII).
- **FR-004**: An `icon_links` entry of type `url` MUST show the image at its address, and one of
  type `local` MUST resolve its path the way a logo's path is resolved, from every page.
- **FR-005**: An `icon_links` entry's `attributes` MUST be set on its link, overriding the
  theme's own attributes of the same name.
- **FR-006**: Every name, address, label, attribute and image path from these options MUST reach
  the page escaped, and markup built from them in Python MUST be built with `markupsafe`, never
  by joining strings (Article V). A `footer_icons` entry's `html` is the site author's own markup,
  as Furo defines it, and MUST be printed as markup (see Clarifications).
- **FR-007**: Each icon link MUST be reachable by keyboard, show a visible focus state and carry
  an accessible name (Article XIV).

**Source links (US2, US3)**

- **FR-008**: The theme MUST accept Furo's `source_repository`, `source_branch`,
  `source_directory`, `source_edit_link`, `source_view_link`, `top_of_page_button` and
  `top_of_page_buttons`, and pydata-sphinx-theme's `use_edit_page_button`, each with its source
  theme's meaning.
- **FR-009**: The theme MUST read pydata-sphinx-theme's `html_context` keys for GitHub, GitLab and
  Bitbucket (`*_user`, `*_repo`, `*_version`, the self-hosted `*_url`), `doc_path` and
  `edit_page_url_template`, and build the edit address each host uses for a page's source file.
- **FR-010**: The buttons `top_of_page_buttons` names MUST sit beside the breadcrumbs, in its
  order, leaving out any whose address is unknown. An empty list MUST show none.
- **FR-011**: The theme MUST ship the `edit-this-page` and `sourcelink` components with
  pydata-sphinx-theme's meaning: `edit-this-page` draws only while `use_edit_page_button` is on,
  and is added to the secondary sidebar when it is on and no component list names it.
  `sourcelink` draws only when Sphinx shows and copies the page's source.
- **FR-012**: A page with no source file MUST carry no edit, view or source button or link.
- **FR-013**: A missing or incomplete host configuration MUST leave the edit link out without
  failing or warning the build.
- **FR-014**: The edit and view buttons and links MUST each say what they do to a screen reader,
  be reachable by keyboard and show a visible focus state (Article XIV).
- **FR-015**: Every address built from a site author's options or `html_context` MUST reach the
  page escaped (Article V).

**Switching from Furo (US4)**

- **FR-016**: `theme.toml` MUST declare every option Furo 2025.12 declares, with Furo's default.
- **FR-017**: Every `html_sidebars` name Furo 2025.12 ships MUST resolve to a template:
  `sidebar/navigation.html` to the site navigation, and the rest to templates that draw nothing.
- **FR-018**: `light_css_variables` and `dark_css_variables` MUST map every Furo variable that has
  a daisyUI counterpart onto that token for the matching mode, and set any other variable as
  written.
- **FR-019**: A CSS variable's name or value MUST NOT be able to end the style it is written into
  or add rules beyond its own declaration.

**Switching from pydata-sphinx-theme (US5)**

- **FR-020**: `theme.toml` MUST declare every option pydata-sphinx-theme 0.24 declares, with its
  default, except where a sibling feature has already declared it.
- **FR-021**: Every component name pydata-sphinx-theme 0.24 ships MUST resolve to a template:
  `sidebar-nav-bs` to the site navigation, `icon-links` to the icon links, and the rest to
  templates that draw nothing where the theme has no counterpart.
- **FR-022**: `analytics`, `shorten_urls`, `surface_warnings` and `templates_skip_empty_check`
  MUST be accepted and change nothing, and the theme's reference MUST say so for each.

**Across the feature**

- **FR-023**: Fixed text the theme writes for these links and buttons MUST be marked for
  translation in the message catalogue (Article VIII).
- **FR-024**: Every option and component this feature adds MUST be documented in the theme's
  reference with its default, and the documentation MUST carry a guide to switching from each of
  the two themes (Article VI).
- **FR-025**: The documentation MUST build, with warnings as errors, with its own configuration,
  with a Furo configuration and with a pydata-sphinx-theme configuration.
- **FR-026**: The theme's templates MUST read every value through the one context the theme sets
  for each page, never `theme_*` values directly.

### Key Entities

- **Icon link**: a name, an address, an icon (a bundled icon, an image or the site author's own
  markup) and, for pydata-style links, extra attributes.
- **Source links**: for one page, its edit address, its view address and the address of Sphinx's
  copy of its source, each present only when known.
- **Accepted name**: an option, `html_sidebars` name or component name of Furo or
  pydata-sphinx-theme that the theme accepts, with what it does here: acts, maps, or draws nothing.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A site using every option, `html_sidebars` name and component name that Furo 2025.12
  or pydata-sphinx-theme 0.24 declares builds with warnings as errors after changing `html_theme`
  only.
- **SC-002**: The theme's documentation builds with warnings as errors three times: with its own
  configuration, with Furo's documentation's configuration and with a pydata-sphinx-theme
  configuration.
- **SC-003**: For a page at the top of the site and one three folders deep, every edit and view
  address built for GitHub, GitLab and Bitbucket leads to that host's page for the page's source.
- **SC-004**: No value from a site's configuration reaches a built page unescaped, except a
  `footer_icons` entry's own markup and markup Sphinx produced.
- **SC-005**: Every icon link, button and link this feature adds passes a keyboard walk, focused
  visibly and announced by name.
- **SC-006**: The home page, "As Furo" and "As pydata-sphinx-theme" pages shown at 390, 1100 and
  1440 pixels wide match the prototype's side by side for the icon links, footer icons, source
  buttons and secondary-sidebar links.

## Clarifications

### Session 2026-11-17

- Q: The prototype names four features; how many stories? → A: Five. Source links have a site
  author who points the pages at their source and a reader who opens it, and those two people's
  stories are never merged. Icon links and the two switching features are a site author's alone.
- Q: Furo's `footer_icons` carries the site author's own SVG in `html`; is it escaped like every
  other option? → A: No. Escaping it would break every Furo configuration that sets it, against
  Article X. It is the site author's own markup, as Furo defines it, and is printed as markup like
  the announcement. Article V names only the announcement today, so it needs the same exception
  written into it before this feature is built.
- Q: Does `edit-this-page` draw whenever an edit address exists, as in the prototype, or only
  with `use_edit_page_button` on, as in pydata-sphinx-theme? → A: Only with it on. A borrowed
  component keeps its meaning (Article X), and a pydata-sphinx-theme site that lists the component
  with the option off gets no link there either. Furo sites get their buttons from
  `top_of_page_buttons`.
- Q: pydata-sphinx-theme 0.24 ships `icon-links`, `indices`, `prev-next` and `searchbox`, which
  the prototype has no template for. Are they in scope? → A: Yes, as names that resolve: every
  shipped component name is accepted (Article X). `icon-links` draws the icon links.
  `prev-next`, `indices` and `searchbox` draw nothing: the frame draws the previous and next links
  from `show_prev_next`, the theme has no index list, and `searchbox` is an empty container for
  Sphinx's search-highlight button.
- Q: What does an explicitly empty `top_of_page_buttons` mean? → A: No buttons, as in Furo. The
  prototype fell back to `top_of_page_button` and showed the edit button.
- Q: `use_edit_page_button` with no host makes pydata-sphinx-theme stop the build. Here? → A: The
  build succeeds and no edit link is drawn. Article X asks that an option the theme can't honour
  is never an error.
- Q: Can `analytics` be honoured later? → A: Not by loading a script, because the theme loads
  nothing from another host (Article XII). It stays accepted and ignored, and the reference says a
  site adds its analytics script itself.

## Assumptions

- Furo 2025.12 and pydata-sphinx-theme 0.24 are the versions whose options and names are promised,
  as the prototype read them.
- The site navigation component (#5), the search button and the modes (#7), the page-body styles
  (#6), and the component lists, icons, square icon button, message catalogue and static-path
  method of the page frame (#4) exist before this feature is built.
- The four layout builds and the development server's build script come with the page frame (#4).
  This feature adds the Furo and pydata-sphinx-theme builds to it.
- Out of scope, owned by sibling features: the logo, announcement, previous and next links and
  arrow keys (#4), site navigation, breadcrumbs, On this page and header links (#5), page-body
  styles and Pygments styles (#6), modes, the theme picker, search and the version switcher (#7).
  The guides list what those options do, but this feature builds none of them.
