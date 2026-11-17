# Research: 004-reader-tools

Written against `main` after FS-001 (page frame), FS-002 (site navigation) and FS-003 (page-body
styles) merged, with the accepted prototype on `prototype-theme` (`PROTOTYPE.md`, features 6, 7
and 8) as the agreed design.

## Assumptions checked

- **Sphinx's search functions can be called directly on every supported version.**
  `searchtools.js` was read on Sphinx 7.4.7, 8.2.3 and 9.2.0. All three expose the same
  `Search` object: `setIndex`, `hasIndex`, `_parseQuery(query)` and `_performSearch(query,
  searchTerms, excludedTerms, highlightTerms, objectTerms)`. `_parseQuery` uses the `Stemmer`,
  `stopwords` and `splitQuery` that `language_data.js` writes for the site's `language`, and
  `_performSearch` returns the full search page's own result list, each entry
  `[docname, title, anchor, descr, score, filename]` (8.2 and later add a seventh field, the
  result's kind). `_performSearch` empties `#search-progress` through a helper that tolerates the
  element being absent, so it runs on any page. Holds: the dialog calls these two and so finds
  exactly what the full search page finds (FR-015, SC-003). The leading underscore is Sphinx's
  name, not ours.
- **The scripts the dialog needs are only on the search page.** Sphinx's `search.html` adds
  `_static/language_data.js`, `_static/searchtools.js` and `searchindex.js`, and no other page
  does. The dialog adds the three, in that order, the first time it opens, unless `Search`
  already exists (the search page). `searchindex.js` calls `Search.setIndex`. Script elements
  load from the file system too, so "search is not available" is shown only when one fails to
  load (FR-019).
- **Sphinx's own `/` shortcut.** `doctools.js` focuses the first `input[name=q]` on `/` while
  `enable_search_shortcuts` is on, its default. With the dialog owning `/` that would be a second
  listener on the same key, so `theme.toml` sets `enable_search_shortcuts = "false"`. Sphinx's
  arrow-key navigation (`navigation_with_keys`, used by FS-001) is a separate setting and keeps
  its listener.
- **The site's root is on `<html>` before the body exists.** Sphinx 7.2 and later write
  `data-content_root` on `<html>`, so the script that runs before the first paint can key the
  reader's stored choice by site.
- **The theme list's source.** `themes: all` in `assets/theme.css` compiles the 35 themes listed
  in daisyUI's `functions/themeOrder.js`. A small script reads that same module and writes the
  list into the package, so the picker's full list and the stylesheet come from one source
  (FR-003).
- **A picked theme's own colour scheme.** Every daisyUI theme sets `color-scheme`. Read with
  `getComputedStyle(document.documentElement).colorScheme` once `data-theme` is set, it says
  whether the picked theme is light or dark, including a theme a site defines in its own
  stylesheet (FR-010). A script in `<head>` after the stylesheets runs once they have loaded, so
  this holds before the first paint.

## Against `main` after FS-001 to FS-003

### What the frame already gives

- `ThemeOptions` (`options.py`) reads text, flags, numbers, lists of dicts and dicts. The picker
  takes `True`, `"all"`, a list or a comma-separated string, which no reader takes yet: a
  `names` reader is added there.
- The component macro and `icon_button` live in `components/macros.html`. The navbar dropdown is
  added beside them.
- `ICONS` already holds every icon the three tools draw (`sun`, `moon`, `sun-moon`, `palette`,
  `search`, `history`, `chevron-down`, `x`, `file-code`, `list`, `book-open`). No icon is added.
- `keys.js` holds `isTyping` and `on(key, handler)`, which refuses a key pressed with Ctrl or
  Meta. Ctrl+K and ⌘K need the opposite, so `on` gains an option for a shortcut that needs Ctrl
  or ⌘.
- The `<body>` carries `data-daisy-root`, `data-daisy-suffix`, `data-daisy-link-suffix`,
  `data-daisy-builder` and `data-daisy-page`, which the page-address module reads.
- `navigation.js` makes every `.daisy-navbar .dropdown` close on Escape and reopen from the
  keyboard. Below 40rem `frame.js` moves the `navbar_end` items into the drawer, outside
  `.daisy-navbar`, so the dropdown macro carries its own class and that script binds it instead.
- `--daisy-text-muted` (`tokens.css`) is the dimmed text that holds AA contrast.

### The two rules waiting on the mode attributes

- **The logo per mode** (`frame.css:6-10`) uses `prefers-color-scheme`. It moves onto
  `data-mode`, keeping the media query only for a page whose script has not run.
- **The Pygments styles** (`pygments.py`) already key on `html[data-mode]`, with the media query
  for a page without the attribute. Nothing to move: this feature writes the attribute they read.

### The header links menu

`navbar-nav.html:13-20` is the same trigger and panel the prototype's theme and version menus
use. It moves onto the dropdown macro with no change to what it renders.

## What already exists

- The mode attributes on `<html>`: daisyUI reads `data-theme`, and nothing else exists. New code,
  `static/scripts/mode.js`.
- Applying a mode before the first paint: nothing in Sphinx or daisyUI. New code, in the same
  file, one function used by both callers (FR-008).
- The theme menu's page script: new code, `static/scripts/theme-menu.js`.
- The navbar dropdown: daisyUI's `dropdown` with focus, as `navbar-nav.html` already uses it.
  This repo, a macro in `components/macros.html` over that markup.
- Matching search results: Sphinx, `Search._parseQuery` and `Search._performSearch`.
- The search dialog: the browser's `<dialog>` with daisyUI's `modal`, as the prototype. New code
  only for the results and keys, `static/scripts/search.js`.
- The page's address: Sphinx's `DOCUMENTATION_OPTIONS` exists only on pages that load
  `documentation_options.js` and holds no page name. This repo, the `<body>` attributes FS-001
  writes. New code, `static/scripts/page-address.js`.
- Keyboard shortcuts: this repo, `keys.js`, grown.
- The theme names: daisyUI's `themeOrder.js`, written into `src/sphinx_daisyui/themes.json` by
  `scripts/themes.mjs`.
- Reading `switcher.json` at build time: the standard library, `urllib.request` and `json`.
- The version menu's page script: new code, `static/scripts/versions.js`.
- Translated text for the page scripts: Sphinx's `Documentation.gettext` reads only Sphinx's own
  JavaScript catalogue. This repo: templates print the translated strings into `data-` attributes
  the scripts read, as FS-001's templates print every other string.

## The planning notes, answered

- **The prototype.** Adopted. Features 6, 7 and 8 are the design, and their files are ported as
  "The look" lists.
- **No design review at the plan stage.** Adopted.
- **The look: ported, never redrawn.** Adopted. Every row is ported, cleaned to `main`'s
  standards: escaped values, `daisy` context only, translated text, no `innerHTML`.
- **Navbar dropdown.** Adopted: a `navbar_dropdown` macro over daisyUI's `dropdown`, used by the
  theme menu, the version switcher and the header links' menu.
- **The mode attributes.** Adopted: `mode.js`, loaded in `<head>` without `defer`, sets all six
  and exposes the one function that applies a choice. Sphinx's `pygments_dark_style` was checked
  and not used: it keys on the media query, so it cannot follow a reader's choice.
- **Task: move the logo per mode onto the mode attributes.** Adopted, with the media query kept
  for a page without a script.
- **The search button under three names.** Adopted: `search-button-field` only.
- **The page's address.** Adopted: `page-address.js` from the `<body>` attributes.
  `DOCUMENTATION_OPTIONS` was checked and not used: it carries no page name.
- **Keyboard shortcuts.** Adopted: `keys.js` gains Ctrl and ⌘ shortcuts, and Sphinx's own `/`
  listener is switched off in `theme.toml` so the dialog owns the key.
- **Component-list defaults.** Adopted unchanged.
- **Reused from the page frame.** Adopted: `icon_button` for the dialog's close button,
  `ThemeOptions`, `ICONS`.
- **The search ranking.** Adopted: Sphinx's own `_parseQuery` and `_performSearch`, checked on
  7.4, 8.2 and 9.2.
- **`search_as_you_type`.** Adopted: on by default, off lists nothing as the reader types.
- **Results built with `innerHTML`.** Adopted: elements and text nodes, the matched words wrapped
  in `<mark>` elements built the same way.
- **`show_version_warning_banner` and `check_switcher`.** Adopted, as FR-028 and FR-033 give them.
  pydata-sphinx-theme 0.24 checks the file at `builder-inited` and warns. This theme checks at
  `build-finished`, when a relative file has been copied into the output.
- **The daisyUI theme list written out by hand.** Adopted: `themes.json` written from daisyUI's
  `themeOrder.js`.
- **Values printed unescaped.** Adopted: every value through `|e`. The script that runs before
  the first paint reads the site's values from `data-` attributes on its own `<script>` element,
  so no value is written into script text.
- **Fixed text not translatable.** Adopted: templates mark it with `_()`, and text a script writes
  comes from `data-` attributes printed by the template.
- **Templates reading `theme_*` directly.** Adopted: every template reads `daisy`.
- **`switcher.json` addresses from the site root.** Adopted: the documentation's file lists this
  build only, at an address relative to the site's root, which works wherever it is published.
