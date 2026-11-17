# Feature Specification: Theme, search and version tools in the header

**Feature Branch**: `004-reader-tools`

**Created**: 2026-11-17

**Status**: Draft

**Input**: Issue #7, "Theme, search and version tools in the header", built from the accepted
design on the `prototype-theme` branch (`PROTOTYPE.md`, features 6, 7 and 8).

**Goals**: none recorded yet. The repository has no `GOALS.md`, so this specification cites no
goal id.

**Depends on**: #4 (FS-001), which builds the page frame, the component lists these tools are
placed in, the square icon button, the options class, the icon set, the message catalogue and the
`<body>` attributes the page script reads.

## Summary

The header gets the three tools readers reach for on a documentation site. A site author picks a
daisyUI theme for each mode and the mode a reader starts in, and can offer readers a picker of
daisyUI themes. A reader switches between the system's mode, light and dark, or picks a theme, and
the choice is kept and applied before the page first paints. A reader opens a search dialog from
the keyboard or the header and sees matching pages, sections and API names as they type, with
Sphinx's full search page behind it. A site author lists the site's published versions in a
`switcher.json` file, and a reader moves to the same page in another version.

Every option and component here is the theme's own, with one name and one shape. Where
pydata-sphinx-theme has a good option for the same thing, its name and shape are used
(`search_bar_text`, `disable_search`, `switcher`, the `theme-switcher` and `version-switcher`
components). Every option has a meaning here: none is accepted only to be ignored.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A site author chooses the site's daisyUI themes and starting mode (Priority: P1)

A site author sets `light_theme` and `dark_theme` to the daisyUI theme each mode shows, sets
`default_mode` to the mode a new reader starts in, and sets `theme_picker` to offer readers a list
of daisyUI themes to pick from, either every theme the stylesheet carries or the ones they name.
They place the `theme-switcher` component in a component list, where it is by default.

**Why this priority**: every page is drawn in a daisyUI theme. Choosing which one is the first
thing a site author changes to make the site their own.

**Independent Test**: build test sites with each option set and unset, and check the attributes
the built page carries on `<html>`, the picker's entries and the theme menu's presence.

**Acceptance Scenarios**:

1. **Given** a site that sets none of these options, **When** it builds, **Then** light mode shows
   daisyUI's `light` theme, dark mode shows its `dark` theme, a new reader starts by following
   their system's setting, and the theme menu offers the three modes and no picker.
2. **Given** `light_theme` and `dark_theme` set to other daisyUI themes, **When** a reader is in
   light or dark mode, **Then** the page shows the theme named for that mode.
3. **Given** `default_mode` set to `light` or `dark`, **When** a reader who has made no choice
   opens a page, **Then** the page starts in that mode whatever their system's setting.
4. **Given** `default_mode` set to a value other than `auto`, `light` or `dark`, **When** the site
   builds, **Then** the build warns once, naming the option and the values it takes, and pages
   start by following the system's setting.
5. **Given** `theme_picker` set to `True` or `"all"`, **When** a reader opens the theme menu,
   **Then** it offers every daisyUI theme the stylesheet carries, and no other.
6. **Given** `theme_picker` set to a list of names, or a comma-separated string of them, **When**
   a reader opens the theme menu, **Then** it offers those themes in that order.
7. **Given** `theme_picker` unset or empty, **When** the site builds, **Then** the theme menu
   offers the three modes only.
8. **Given** a theme name the site defines in its own stylesheet in `html_static_path`, **When**
   it is named in `light_theme`, `dark_theme` or `theme_picker`, **Then** the build accepts it and
   the page uses it.
9. **Given** `theme-switcher` left out of every component list, **When** the site builds,
   **Then** no page carries the theme menu, and the site's themes and starting mode still apply.
10. **Given** a site author's theme names and mode, **When** the page prints them, **Then** each
    reaches the page escaped.
11. **Given** the built site, **When** a site author reads the theme's documentation, **Then**
    each option and the component are documented with their defaults, and the attributes the
    theme sets on `<html>` are documented for a site's own stylesheets and scripts to read.

---

### User Story 2 - A reader switches mode or picks a theme (Priority: P1)

A reader opens the theme menu in the header and switches between following their system's
setting, light and dark, or picks one of the daisyUI themes the site offers. Every page they open
afterwards, and every visit after that, starts in what they chose, with no flash of another theme
as it loads.

**Why this priority**: readers who read in a dark room or need higher contrast expect the switch
on every documentation site, and the wrong theme flashing on each page is the most visible defect a
theme can have.

**Independent Test**: build a test site and, in a browser, choose each mode and a picked theme,
then reload and open another page, checking the attributes on `<html>` before the stylesheet
paints and after the page script runs.

**Acceptance Scenarios**:

1. **Given** a reader who has made no choice, **When** they open a page, **Then** it is drawn in
   the site's starting mode, and when that is `auto`, in the daisyUI theme for their system's
   setting.
2. **Given** a reader who chooses light, dark or the system's setting from the menu, **When** the
   choice is made, **Then** the page changes at once, the menu marks that choice as current, and
   the header's theme button shows which choice is in force.
3. **Given** a reader who has made a choice, **When** they reload the page, open another page of
   the site, or come back on a later visit in the same browser, **Then** the page is drawn in
   their choice from its first paint.
4. **Given** a reader following the system's setting, **When** the system switches between light
   and dark while the page is open, **Then** the page follows without a reload.
5. **Given** a site that offers a picker, **When** the reader picks a daisyUI theme, **Then** the
   page is drawn in that theme in both modes until they choose a mode again, and the parts of the
   page that differ by mode, such as the logo, follow whether that theme is light or dark.
6. **Given** a site that offers a picker, **When** the reader looks down its list, **Then** each
   entry gives a preview of that theme's colours beside its name.
7. **Given** a reader who picked a theme the site no longer offers, or whose stored choice cannot
   be read, **When** they open a page, **Then** the page is drawn in the site's starting mode.
8. **Given** a browser that blocks the page from storing anything, **When** the reader makes a
   choice, **Then** it applies to the page they are on and the page carries no error.
9. **Given** a keyboard reader, **When** they reach the theme button, **Then** they open the menu,
   move through its entries, make a choice and close it without a pointer, and a screen reader
   names the button and announces the current choice.
10. **Given** a site whose `language` is set, **When** the theme menu is built, **Then** its own
    fixed text is taken from the message catalogue in that language where a translation exists.

---

### User Story 3 - A reader finds a page, section or API name from the search dialog (Priority: P1)

A reader presses Ctrl+K, ⌘K or `/`, or presses the search button in the header, and a search
dialog opens. As they type, it lists the pages, the sections within pages and the API names
(functions, classes, options) that match. They move through the results with the arrow keys and
open one with Enter, or press Enter with nothing chosen to open Sphinx's full search page for the
same words, which is drawn in the theme's style.

**Why this priority**: search is how most readers arrive at the page they want on a reference
site, and the keyboard shortcut is what readers of other modern documentation sites expect.

**Independent Test**: build a test site with pages, sections and API entries, then in a browser
open the dialog by each shortcut, type queries and check the results listed, their addresses, the
keyboard movement, and where Enter leads. Check the built search page's markup and the dialog's
names for a screen reader.

**Acceptance Scenarios**:

1. **Given** any page, **When** the reader presses Ctrl+K or ⌘K, anywhere on the page, **Then**
   the search dialog opens with focus in its field.
2. **Given** any page, **When** the reader presses `/` while not typing in a field, **Then** the
   search dialog opens. **When** they press `/` while typing in a field, **Then** the character is
   typed and the dialog stays closed.
3. **Given** the search button in the header, **When** the reader presses it, **Then** the dialog
   opens, and the shortcut the button shows is the one for the reader's platform.
4. **Given** the open dialog, **When** the reader types a word that appears in a page's text,
   **Then** that page is listed, linked to the page.
5. **Given** the open dialog, **When** the reader types words in a section's title, **Then** that
   section is listed with the page it is on, linked to its heading.
6. **Given** the open dialog, **When** the reader types part of an API name, **Then** that object
   is listed with its kind and page, linked to its entry.
7. **Given** a query, **When** results are listed, **Then** a word typed in a different form
   (such as a plural) finds what Sphinx's full search page finds for it, using the stemming of the
   site's `language`.
8. **Given** a list of results, **When** the reader presses the down and up arrow keys, **Then**
   the chosen result moves through the list, wrapping at either end, stays in view, and is
   announced to a screen reader.
9. **Given** a chosen result, **When** the reader presses Enter or clicks a result, **Then** they
   reach that result's page and place, and the dialog closes.
10. **Given** words typed and no result chosen, **When** the reader presses Enter, **Then**
    Sphinx's full search page opens for the same words.
11. **Given** words that match nothing, **When** the reader stops typing, **Then** the dialog says
    nothing matches, and a screen reader announces it.
12. **Given** the open dialog, **When** the reader presses Escape, presses its close button or
    presses outside it, **Then** it closes and focus returns to where it was.
13. **Given** a page title, section title or API name that holds markup or special characters,
    **When** it is listed, **Then** it is shown as text and never interpreted as HTML.
14. **Given** a site opened where the page script cannot read Sphinx's search index, such as from
    the file system, **When** the reader opens the dialog, **Then** it says search is not
    available here, and Enter still opens Sphinx's full search page.
15. **Given** Sphinx's full search page, **When** the reader opens it with words, **Then** its
    results are drawn with the theme's page-body styles, in daisyUI's tokens, in both modes.
16. **Given** a narrow screen, **When** the reader opens the dialog, **Then** it fits within the
    screen, its results scroll inside it, and every control in it is reachable.
17. **Given** a site built with the `dirhtml` builder, **When** the reader opens a result, **Then**
    they reach the right page.
18. **Given** a site whose `language` is set, **When** the dialog is shown, **Then** its own fixed
    text is taken from the message catalogue in that language where a translation exists.

---

### User Story 4 - A site author sets up search or leaves it out (Priority: P2)

A site author places the `search-button-field` component, sets `search_bar_text` for the text
shown in the button and the dialog's field, turns results as you type off with
`search_as_you_type`, or leaves search out of the site with `disable_search`.

**Why this priority**: the defaults serve most sites. These options are for sites that place
search elsewhere, word it for their readers, or have no use for it.

**Independent Test**: build test sites with the component placed and each option set, and check the
built header's button, the dialog's presence and field, and the markers the page script reads.

**Acceptance Scenarios**:

1. **Given** the default component lists, **When** the site builds, **Then** the header carries
   the search button in `navbar_persistent`, and every page carries the search dialog once.
2. **Given** `search-button-field` named in another component list, **When** the site builds,
   **Then** the search button is drawn there.
3. **Given** `search_bar_text` set, **When** a page is built, **Then** that text is shown in the
   search button and the dialog's field, escaped.
4. **Given** `search_as_you_type` switched off, **When** a reader types in the dialog, **Then** no
   results are listed as they type, and Enter opens Sphinx's full search page for the words.
5. **Given** `disable_search` switched on, **When** the site builds, **Then** no page carries the
   search button or the dialog, and the shortcuts do nothing.
6. **Given** the built site, **When** a site author reads the theme's documentation, **Then** each
   option and the component are documented with their defaults.

---

### User Story 5 - A site author lists the site's published versions (Priority: P2)

A site author publishes a `switcher.json` file listing each
version's name, version and address and which one is preferred, and sets `switcher` with its
`json_url` and the `version_match` of the version being built. They place the `version-switcher`
component, which is in `navbar_end` by default. They keep `check_switcher` on to have the build
check the file, and switch `show_version_warning_banner` on to warn readers of other versions.

**Why this priority**: only sites that publish several versions need it.

**Independent Test**: build test sites with a valid file, an unreadable address and a file of the
wrong shape, with each option set, and check the built component's markers and the build's
warnings.

**Acceptance Scenarios**:

1. **Given** no `switcher` option, or one without `json_url`, **When** the site builds, **Then**
   no page carries the version switcher.
2. **Given** `switcher` with `json_url` and `version_match`, **When** the site builds, **Then**
   every page carries the version switcher, labelled with the version being built.
3. **Given** a `json_url` that is a full address, a path from the site's root, or a path relative
   to the built site, **When** a page at any depth is opened, **Then** the switcher reads the file
   from the right place.
4. **Given** `check_switcher` on, its default, **When** the site builds and the file cannot be
   read or is not a list of versions, **Then** the build warns once, naming the address, and
   builds the pages.
5. **Given** `check_switcher` switched off, **When** the site builds, **Then** the file is not
   read at build time.
6. **Given** a site author's `json_url` and `version_match`, **When** a page prints them, **Then**
   each reaches the page escaped.
7. **Given** the built site, **When** a site author reads the theme's documentation, **Then** the
   file's format, each option and the component are documented with their defaults.

---

### User Story 6 - A reader moves to another version of the page they are on (Priority: P2)

A reader opens the version menu in the header, sees the site's published versions with the one
they are reading and the preferred one marked, and picks one. They land on the same page in that
version when it exists there, or on that version's home page when it does not. Reading a version
other than the preferred one, they are told so, with a way to the preferred version, when the site
author has switched that warning on.

**Why this priority**: readers who arrive from a search engine on an old version need the way to
the current one, and readers of a released version need the same page in the version they use.

**Independent Test**: serve two builds of a test site with a `switcher.json` listing both, then in
a browser pick each version from pages that exist in both and in one only, and check where the
reader lands and the banner's presence.

**Acceptance Scenarios**:

1. **Given** a page with the version switcher, **When** the reader opens it, **Then** it lists
   every version in the file, in the file's order, by its name, with the current version and the
   preferred version each marked.
2. **Given** a version picked whose build holds the page the reader is on, **When** they pick it,
   **Then** they land on that page in that version.
3. **Given** a version picked whose build does not hold the page, or cannot be reached to check,
   **When** they pick it, **Then** they land on that version's home page.
4. **Given** a site built with the `dirhtml` builder, **When** the reader picks a version, **Then**
   the same page is found by its directory address.
5. **Given** a `switcher.json` that cannot be read when the page opens, **When** the reader looks
   at the header, **Then** no empty version switcher is left there.
6. **Given** `show_version_warning_banner` switched on and a page of a version other than the
   preferred one, **When** the reader opens it, **Then** a banner at the top of the page says this
   is not the preferred version and links to the same place in the preferred one, and it is a
   named region for a screen reader.
7. **Given** `show_version_warning_banner` switched on and a page of the preferred version, or the
   option left off, **When** the reader opens it, **Then** no version banner is shown.
8. **Given** a version's name or address from the file that holds markup or special characters,
   **When** it is listed, **Then** it is shown as text and the link is never `javascript:` or
   another non-web address.
9. **Given** a keyboard reader, **When** they reach the version switcher, **Then** they open it,
   move through the versions, pick one and close it without a pointer.
10. **Given** a site whose `language` is set, **When** the switcher and banner are shown, **Then**
    their own fixed text is taken from the message catalogue in that language where a translation
    exists.

---

### Edge Cases

- A reader who picked a theme on one site visits another site using this theme on the same host:
  each site's choice is its own, and one site's stored choice never breaks another's page.
- A daisyUI theme name in `theme_picker` repeated: offered once.
- `light_theme` and `dark_theme` set to the same theme: both modes show it, and the mode
  switch still records the reader's choice.
- The theme menu and the version switcher open at the right-hand edge of a narrow screen: each
  stays within the screen.
- A search typed before the search index has loaded: results appear once it loads, without the
  reader typing again.
- A query of one character, or only spaces: the dialog lists nothing and asks for more.
- A `switcher.json` entry with no `name`: listed by its `version`.
- A `switcher.json` with no preferred entry: no version is marked preferred and no banner is shown.
- Both the theme menu and the version switcher in the header: opening one closes the other.
- A page built by a builder other than `html` and `dirhtml`, such as `singlehtml`: the site still
  builds, and search and the version switcher lead to the build's own page addresses.

## Requirements *(mandatory)*

### Functional Requirements

**Themes and modes for a site author (US1)**

- **FR-001**: The theme MUST accept the own options `light_theme` (default `light`), `dark_theme`
  (default `dark`), `default_mode` (`auto`, `light` or `dark`, default `auto`) and `theme_picker`
  (empty, `True`, `"all"`, a list or a comma-separated string of names, default empty).
- **FR-002**: A `default_mode` the theme does not know MUST produce one build warning naming the
  option and its values, and pages MUST then start in `auto`.
- **FR-003**: A `theme_picker` of `True` or `"all"` MUST offer every daisyUI theme the stylesheet
  carries, taken from the same source the stylesheet is built from, never from a list written out
  separately.
- **FR-004**: Theme names in `light_theme`, `dark_theme` and `theme_picker` MUST be accepted as
  given, so a theme a site defines in its own static stylesheet can be named.
- **FR-005**: The theme MUST ship the `theme-switcher` component and keep it in `navbar_end` by
  default.
- **FR-006**: Every page MUST carry on `<html>` the attributes `data-theme`, `data-mode`,
  `data-mode-choice`, `data-light-theme`, `data-dark-theme` and `data-default-mode`, set before
  the page first paints. They MUST be documented as the public contract that a site's own
  stylesheets and scripts, and the theme's other features, read.

**Switching for a reader (US2)**

- **FR-007**: A reader's choice of mode or picked theme MUST be kept in the browser, per site,
  and applied before the first paint of every later page of that site.
- **FR-008**: Applying a choice MUST be one function, used by the script that runs before the
  first paint and by the page script.
- **FR-009**: In `auto`, the page MUST follow the system's setting while it is open.
- **FR-010**: A picked daisyUI theme MUST set `data-mode` to light or dark from that theme's own
  colour scheme.
- **FR-011**: A stored choice that is no longer offered, cannot be read, or cannot be stored MUST
  leave the page in the site's starting mode or the current choice, with no script error.
- **FR-012**: The theme menu MUST mark the current choice for sight and for a screen reader, and
  MUST be usable from the keyboard alone (Article XIV).

**The search dialog for a reader (US3)**

- **FR-013**: Every page with search enabled MUST carry one search dialog, opened by Ctrl+K and
  ⌘K at any time, by `/` when the reader is not typing in a field, and by the search button.
- **FR-014**: The dialog MUST list, as the reader types, the pages, section titles and API
  objects from the search index Sphinx writes for the build, each linked to its page and anchor.
- **FR-015**: Matching MUST use Sphinx's own search language support for the site's `language`
  (its stemmer and stop words), so the dialog and Sphinx's full search page find the same pages
  for a word.
- **FR-016**: The arrow keys MUST move the chosen result, Enter MUST open it, and Enter with none
  chosen MUST open Sphinx's full search page with the reader's words. The chosen result MUST be
  exposed to a screen reader as the field's active option.
- **FR-017**: Escape, the close button and a press outside the dialog MUST close it and return
  focus to where it was.
- **FR-018**: Results and the dialog's messages MUST be written into the page as text, never by
  assigning HTML built from index or query text (Article V).
- **FR-019**: When the search index cannot be read, the dialog MUST say search is not available
  and still send Enter to the full search page.
- **FR-020**: Sphinx's full search page MUST be drawn with the theme's styles and daisyUI's
  tokens only (Article XI).
- **FR-021**: The keyboard shortcuts MUST be registered through the one keyboard helper the page
  frame starts, which this feature grows, and which tells whether the reader is typing.

**Search options for a site author (US4)**

- **FR-022**: The theme MUST ship one search button component, `search-button-field`, and keep
  it in `navbar_persistent` by default.
- **FR-023**: The theme MUST accept `search_bar_text` (the button's and the field's text),
  `disable_search` (default off) and `search_as_you_type` (default on). Off, `search_as_you_type`
  MUST stop results being listed as the reader types.
- **FR-024**: With `disable_search` on, no page MUST carry the search button or dialog, and the
  shortcuts MUST do nothing.

**Versions for a site author (US5)**

- **FR-025**: The theme MUST accept `switcher` (`json_url`, `version_match`), `check_switcher`
  (default on) and `show_version_warning_banner` (default off), and read a `switcher.json` that
  lists entries of `name`, `version`, `url` and `preferred`.
- **FR-026**: The theme MUST ship the `version-switcher` component and keep it in `navbar_end` by
  default. It MUST draw nothing without a `json_url`.
- **FR-027**: A `json_url` MUST resolve from every page, whether a full address, a path from the
  site's root or a path relative to the built site.
- **FR-028**: With `check_switcher` on, the build MUST read the file once and warn, naming the
  address, when it cannot be read or is not a list of versions, without stopping the build.

**Moving between versions for a reader (US6)**

- **FR-029**: The version switcher MUST list the file's versions in order, marking the one that
  matches `version_match` as current and the preferred one as preferred.
- **FR-030**: Picking a version MUST open the reader's current page in that version when its build
  holds it, and that version's home page otherwise or when it cannot be checked.
- **FR-031**: The same page MUST be found from the page's address as the build writes it,
  including for `dirhtml`, through one page-address module that the search dialog and the version
  switcher share.
- **FR-032**: A file that cannot be read in the browser MUST leave no version switcher on the
  page.
- **FR-033**: With `show_version_warning_banner` on, a page of a version other than the preferred
  one MUST show a named banner before the header, linking to the same place in the preferred
  version.
- **FR-034**: Versions' names and addresses from the file MUST be written as text, and a link MUST
  be made only from a web address (Article V).

**Across the feature**

- **FR-035**: The theme menu and the version switcher MUST be drawn with one shared navbar
  dropdown, which the page frame's square icon button and icon set feed.
- **FR-036**: Every value a template prints from a theme option, `html_context` or the page
  context MUST be escaped, as amended Article V states.
- **FR-037**: Fixed text the theme writes for these tools, in templates and in the page script,
  MUST be marked for translation in the message catalogue the page frame sets up (Article VIII).
- **FR-038**: Every option this feature adds MUST be declared in `theme.toml`, read through the
  one context the theme sets for each page, and documented with its default (Article VI).
- **FR-039**: Every control these tools add MUST be reachable and usable by keyboard with a
  visible focus state, and named for a screen reader, and dimmed text in them MUST meet WCAG 2.2
  AA contrast on daisyUI's default light and dark themes (Article XIV).

### Key Entities

- **Mode choice**: what the reader chose, `auto`, `light`, `dark`, or a picked daisyUI theme,
  kept in their browser for one site.
- **The mode attributes**: the attributes on `<html>` that say which daisyUI theme and mode are
  showing, what the reader chose and what the site's defaults are.
- **Theme picker**: the list of daisyUI themes a site offers readers.
- **Search index**: the `searchindex.js` Sphinx writes for the build, which the dialog reads.
- **Version list**: the entries of a site's `switcher.json`, each a name, a version, an address
  and whether it is preferred.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On every page, the daisyUI theme the reader chose, or the site's starting mode, is
  in force before the first paint, on a reload, a new page and a later visit.
- **SC-002**: Every option this feature adds changes what a built page carries or how the build
  behaves, and a site that sets none of them builds with no warnings.
- **SC-003**: For a set of queries on the documentation site, the dialog lists every page Sphinx's
  full search page finds for the same words.
- **SC-004**: A reader finds and opens a result, switches mode, picks a theme and picks a version
  with the keyboard alone, and every control is named for a screen reader.
- **SC-005**: Picking a version from a page that exists in it lands on that page, and from a page
  that does not lands on its home page, for `html` and `dirhtml` builds.
- **SC-006**: No value from a site's configuration, its `switcher.json` or its search index
  reaches a page as markup.
- **SC-007**: The theme menu open, a theme picked, the search dialog with results, the full search
  page and the version menu each match the prototype's corresponding screen side by side at 390,
  1100 and 1440 pixels wide.

## Clarifications

### Session 2026-11-17

- Q: How many stories, given the issue lists three tools? → A: Six. Each tool has a site author's
  part and a reader's part, and the two are never merged into one story.
- Q: Does `search_as_you_type` stay, and with what default? → A: Yes, as the theme's own option,
  because it changes what the reader gets. On by default, as in the accepted design. Off, no
  results are listed as the reader types (FR-023).
- Q: What does `check_switcher` do? → A: The build reads the file and warns when it cannot, and
  the pages still build (FR-028).
- Q: What does `show_version_warning_banner` do? → A: A banner on pages of versions other than the
  preferred one, linking to the preferred version (FR-033).
- Q: How many names does the search button have? → A: One, `search-button-field`, the name the
  default `navbar_persistent` uses (FR-022).
- Q: Does the picker's full list come from a list in the package's Python? → A: No. It comes from
  the same source the stylesheet's compiled themes come from, so the two cannot drift (FR-003).
- Q: Is a theme name the theme does not know an error? → A: No. A site may define its own daisyUI
  theme in its static stylesheet, so names are accepted as given (FR-004). A `default_mode` the
  theme does not know warns, because only three values mean anything (FR-002).
- Q: Can the starting mode be set anywhere but `default_mode`? → A: No. One setting has one
  option (FR-001).

## Assumptions

- FS-001 (#4) is built before this feature, and its square icon button, options class, icon set,
  message catalogue, keyboard helper and `<body>` attributes exist.
- The stylesheet carries all 35 daisyUI 5 themes, as the accepted design decided.
- The theme's own fixed text is in English, added to the message catalogue with no translations.
- Out of scope, owned by sibling features: the page frame, logo, announcement and previous and
  next links (#4), site navigation, On this page and header links (#5), the page-body styles and
  Pygments styles (#6), icon links and edit and view links (#8). The header links menu (#5)
  reuses this feature's navbar dropdown, and the logo (#4) and Pygments styles (#6) read its mode
  attributes.
