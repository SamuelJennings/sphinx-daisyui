# Plan: Theme, search and version tools in the header

**Inputs**: `spec.md`, `research.md`, `planning-notes.md`, `decisions.md`, and the accepted
prototype on `prototype-theme` (`PROTOTYPE.md`, features 6, 7 and 8).

## Approach

Each tool is a component, a little Python that reads its options into the `daisy` context, and a
script of its own beside the page script's base. The look is the prototype's, ported: its
templates and styles are copied across and cleaned to `main`'s standards. What the prototype
faked is done properly here.

### Modes and themes (US1, US2)

- **`ThemeOptions.names(name)`** in `options.py` reads a list, a tuple or a comma-separated
  string of names, trimmed, empty ones dropped, each once in its first place.
- **`src/sphinx_daisyui/modes.py`** holds `Modes`, read from `ThemeOptions`: `light_theme`
  (default `light`), `dark_theme` (default `dark`), `default_mode` (`auto`, `light` or `dark`,
  anything else `auto`) and `picker`: empty, every name in `THEMES` for `True` or `"all"`, or the
  names given. `THEMES` is read from `src/sphinx_daisyui/themes.json`, which
  `scripts/themes.mjs` writes from daisyUI's `functions/themeOrder.js`, the list `themes: all`
  compiles. `npm run build` runs it before Tailwind, and the file is committed, as `icons.json`
  is. `check_modes`, connected to `builder-inited` beside `check_layout`, warns once on a
  `default_mode` the theme does not know (`type="daisyui"`, `subtype="modes"`). The page context
  gains `daisy.modes`.
- **`static/scripts/mode.js`** is loaded in `<head>` after the stylesheets, without `defer`, from
  the `extrahead` block, with `<meta name="color-scheme" content="light dark">`. The site's
  values reach it as `data-` attributes on its own `<script>` element, escaped: the two themes,
  the starting mode and the offered themes. It sets the six mode attributes on `<html>` and
  exposes `sphinxDaisyui.mode.apply(choice)`, the one function that applies a choice, and
  `choose(choice)`, which applies and stores it. A choice is `auto`, `light`, `dark` or
  `theme:<name>`, kept under one `localStorage` key per site, named from `data-content_root`
  resolved against the page's address. A picked theme sets `data-mode` from the computed
  `color-scheme`. A stored choice that is not offered, cannot be read or cannot be stored falls
  back to the starting mode, inside `try`, so the page never carries a script error.
- **`navbar_dropdown`** joins `components/macros.html`: a `{% call(part) %}` macro drawing
  daisyUI's `dropdown dropdown-end` with the trigger part and the panel part, and the class
  `daisy-dropdown`. `navbar-nav.html`'s More menu moves onto it with the same output, and
  `navigation.js` binds `.daisy-dropdown` wherever it is, so the menus keep Escape and keyboard
  opening inside the drawer.
- **`components/theme-switcher.html`** is the prototype's, on the macro: the button showing the
  current choice's icon, three mode choices and the picker with each theme's swatch. Its text is
  translated, the names escaped, the current choice named for a screen reader in a visually
  hidden span the script keeps up to date from translated `data-` strings.
- **`static/scripts/theme-menu.js`** wires the choices to `mode.choose`, marks the current one
  (`menu-active` and `aria-pressed`), follows the system while the choice is `auto`, and closes
  the menu after a choice.
- **`assets/frame.css`**: the logo rule moves onto `data-mode`, keeping the media query for a
  page without the attribute; the mode icon rules (`frame.css:11-16` in the prototype) are
  ported.

### Search (US3, US4)

- **`keys.js`** gains `on(key, handler, { modifier: true })` for a shortcut that needs Ctrl or ⌘,
  and stays the one place shortcuts are registered. `theme.toml` sets
  `enable_search_shortcuts = "false"`, so Sphinx's own `/` listener stays off.
- **`static/scripts/page-address.js`** is `sphinxDaisyui.pageAddress`: `url(docname, anchor)`
  for the build (`html`, `dirhtml`, and the build's own suffix for any other builder) from the
  `<body>` attributes, and `path()`, the current page's address from the site's root.
- **`components/search-button-field.html`** and **`components/search-modal.html`** are the
  prototype's, reading `daisy.search` only, the close button `icon_button`. `layout.html`
  includes the dialog once at the end of the page when search is on.
- **`static/scripts/search.js`** opens the dialog on Ctrl+K, ⌘K, `/` (not while typing) and the
  button, loads `language_data.js`, `searchtools.js` and `searchindex.js` the first time, unless
  `Search` already exists, and calls `Search._parseQuery` and `Search._performSearch` as the
  reader types. Each result is drawn with elements and text nodes: a page, a section (its title
  with the page title under it) or an API object (its kind from Sphinx's description). The
  matched words are `<mark>` elements. The arrow keys move the chosen result, wrapping, kept in
  view and named by `aria-activedescendant`. Enter opens it, or Sphinx's search page with the
  words when none is chosen. A query of fewer than two characters lists nothing. A script that
  fails to load shows "search is not available here". Its messages come from the dialog's `data-`
  strings. Calls to `localStorage` Sphinx makes are inside `try`.
- **`assets/frame.css`** gains the prototype's search section (`frame.css:203-226`): the dialog,
  the marked words, and Sphinx's full search page on daisyUI tokens, its dimmed text on
  `--daisy-text-muted`.
- **Options** (US4): `search_bar_text` (default: a translated "Search the docs"),
  `disable_search` (default off) and `search_as_you_type` (default on), read into
  `daisy.search`.

### Versions (US5, US6)

- **`src/sphinx_daisyui/versions.py`** holds `VersionSwitcher`, read from the `switcher` option
  (`json_url`, `version_match`) and `show_version_warning_banner`, and `check_switcher`,
  connected to `build-finished`. With `check_switcher` on and a `json_url`, it reads the file
  once: a full address with `urllib.request` (ten-second timeout), anything else from the build's
  output directory. It warns once, naming the address (`type="daisyui"`,
  `subtype="switcher"`), when the file cannot be read or is not a list of entries each holding a
  `version` and a `url`. The page context gains `daisy.switcher`.
- **`components/version-switcher.html`** is the prototype's, on the dropdown macro, drawn only
  with a `json_url`. The banner's placeholder sits before the header when the banner is on.
- **`static/scripts/versions.js`** resolves `json_url` from the site's root (a full address and a
  path from the server's root as given, anything else from the site's root), fetches it, and
  lists the entries in order by `name` or `version`, the current and the preferred marked. A
  version's `url` is resolved the same way and becomes a link only when the result is `http` or
  `https`. Picking a version checks the same page there with a `HEAD` request
  (`pageAddress.path()`) and opens it, or the version's home page. A file that cannot be read
  removes the switcher. With the banner on and a preferred entry other than the current one, it
  fills the banner: a named region saying so, linked to the same page in the preferred version.

### Documentation

- `docs/reference/options.md` gains "Modes and themes", "Search" and "Versions";
  `docs/reference/components.md` gains `theme-switcher`, `search-button-field` and
  `version-switcher`; `docs/reference/page.md` gains "Attributes on the root element", the
  contract of the six attributes.
- Two guides in `docs/developer/`, ported from the prototype's pages:
  `choose-the-themes.md` (modes and the picker) and `set-up-search-and-versions.md`.
- `docs/_static/switcher.json` lists this build, at an address relative to the site's root.
  `docs/conf.py` sets `theme_picker` and `switcher`.
- `CHANGELOG.md` and the message catalogue template.

## Packages and tools

- No new dependency. `urllib.request` and `json` from the standard library.
- Sphinx's own `searchtools.js` and `language_data.js` do the matching.
- daisyUI's `themeOrder.js`, already installed for the stylesheet, gives the theme names.

## Each planning note

Answered under "The planning notes, answered" in `research.md`.

## Testing

- `sphinx.testing` builds for every option, template and warning, read with
  `tests/test_templates/page.py`: the attributes and hooks the scripts read, presence and
  absence, escaping, translation, warnings and their absence. No wording, icon or style is
  asserted.
- The scripts' behaviour (first paint, storage, keyboard, results, versions) is driven in headless
  Chrome against built test sites, one line per check, the scripts kept in the run's evidence.
- The look is compared with the prototype on 8062, at 390 and 1440 wide, before review.

## Risks

- `_parseQuery` and `_performSearch` are not documented as public. They are the same on every
  supported version, and a version that changes them is caught by the browser check of the search
  dialog. Recorded as an ADR.
