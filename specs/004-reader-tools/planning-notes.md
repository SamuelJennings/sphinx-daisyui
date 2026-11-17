# Planning notes: 004-reader-tools

Notes for research and planning. Each is answered by name before the build starts.

## The prototype

This feature is built from the accepted prototype on the `prototype-theme` branch. Read
`PROTOTYPE.md` on that branch whole, then its features 6 (modes and daisyUI themes), 7 (search
dialog) and 8 (version switcher). The prototype is served at http://localhost:8062/ while it is
being compared. Its screens and the maintainer's decisions in its "Decisions" section are agreed.
"Which decisions bind which feature" binds feature 6 to all 35 daisyUI themes compiled in.

## No design review at the plan stage

The prototype is the design. The plan goes straight to tasks with no separate design review.

## The look: ported, never redrawn

Port means copy across and clean to `main`'s standards. These rows of "The look" belong to this
feature:

| Prototype file | What this feature takes | Lands in `main` at |
|---|---|---|
| `components/theme-switcher.html` | All, drawn with the shared navbar dropdown | `theme/daisyui/components/` |
| `components/search-button-field.html`, `search-button.html`, `search-field.html` | One button; the other two names include it | `theme/daisyui/components/` |
| `components/search-modal.html` | All | `theme/daisyui/components/` |
| `components/version-switcher.html` | All, drawn with the shared navbar dropdown | `theme/daisyui/components/` |
| `theme/daisyui/layout.html` | `:13-29` (the mode attributes set before the first paint, and `color-scheme`), `:172` (the dialog's include) | The same path, into the frame FS-001 ports |
| `static/scripts/sphinx-daisyui.js` | `:10-54` (modes and themes), `:168-180` and `:219-397` (page address and search), `:182-217` (versions) | `theme/daisyui/static/scripts/`, one module per tool, beside the page script's base from FS-001 |
| `assets/frame.css` | `:11-16` (the theme button's current choice), `:203-226` (search dialog and the full search page) | `assets/`, where FS-001's plan puts the frame's styles |
| `src/sphinx_daisyui/__init__.py` | `DAISYUI_THEMES`, replaced by a list read from the stylesheet's source (FR-003); the `daisy` keys `light_theme`, `dark_theme`, `default_mode`, `picker`, `search_bar_text`, `switcher` | `src/sphinx_daisyui/`, on the options class FS-001 builds (Article IX) |
| `theme/daisyui/theme.toml` | `light_theme`, `dark_theme`, `default_mode`, `theme_picker`, `search_bar_text`, `disable_search`, `search_as_you_type`, `switcher`, `check_switcher`, `show_version_warning_banner` | The same path |
| `docs/_static/switcher.json` | All, with addresses that work on the published site as well as the development server | `docs/_static/` |
| `docs/configure/themes.md` (modes and picker only), `docs/configure/search-and-versions.md` | The pages, in `main`'s documentation shape | `docs/`, as the documentation standard places them |

Each merge is checked side by side against the prototype on the rows of "Pages to compare side by
side" that name features 6, 7 or 8: Home in light and dark, Theme menu (open, then `dracula`
picked), Search dialog (Ctrl+K, "layout" typed, the second result chosen), Full search page
(`search.html?q=layout`), Version menu, and As pydata-sphinx-theme for the version switcher. At
390, 1100 and 1440 pixels wide.

## The shared pieces this feature builds

From "The shared pieces" in `PROTOTYPE.md`. Each is built once here and reused by the features
named.

- **Navbar dropdown.** A Jinja macro taking the trigger and the panel's content. Used here by the
  theme menu and the version switcher, and reused by the header links menu (#5). Check daisyUI's
  `dropdown` first.
- **The mode attributes.** One documented contract on `<html>` (`data-theme`, `data-mode`,
  `data-mode-choice`, `data-light-theme`, `data-dark-theme`, `data-default-mode`), with one
  function that applies a choice, used by both the inline script that runs before the first paint
  and the page script. Read by the page-body styles' Pygments styles (#6), the logo per mode
  (#4), and Furo's CSS variables (#8). Check daisyUI's `data-theme`, and Sphinx's own
  `pygments_dark_style` in `theme.toml`, which keys on a media query rather than an attribute,
  first. FS-001's logo reads `data-mode`: research says what the frame shows for the logo before
  this feature lands.
- **The search button under three names.** One component; `search-button.html` and
  `search-field.html` include `search-button-field.html`. Reused by the pydata-sphinx-theme
  configurations (#8). Check: nothing.
- **The page's address.** A shared script module that turns a document name and anchor into the
  page's address for the build (`html`, `dirhtml`), from the `<body>` attributes FS-001 sets. Used
  here by the search dialog and reused by the version switcher. Check Sphinx's
  `DOCUMENTATION_OPTIONS` (`URL_ROOT`, `FILE_SUFFIX`, `LINK_SUFFIX`, `BUILDER`) in
  `documentation_options.js` first.
- **Keyboard shortcuts.** FS-001 starts a small helper (is the reader typing, and one place that
  registers a shortcut) for the drawer's Escape and the arrow keys. This feature grows the same
  helper with Ctrl+K, ⌘K and `/`, and writes no listener of its own. Reused by the page frame and
  previous and next (#4). Check Sphinx's own `navigation_with_keys` handling in `doctools.js`
  first.

It reuses from FS-001 (#4): the square icon button (the dialog's close button), `ThemeOptions`
(every option here is read through it) and `Icons` (every icon in the three tools).

## What the prototype faked that this feature does properly

From "Faked or skipped" in `PROTOTYPE.md`:

- **The search ranking.** A light stemmer and prefix matcher, not language-aware. Use Sphinx's own
  search language support: the stemmer and stop words in `language_data.js` for the site's
  `language`, and research whether Sphinx's `Search` object in `searchtools.js` (`_parseQuery`,
  `performTermsSearch`, `performObjectSearch`) can be called directly on every supported Sphinx
  version (7.4 to 9.2), rather than reimplemented (FR-016, SC-003).
- **`search_as_you_type`.** Accepted and ignored. Honour it: default on, off stops results as the
  reader types (FR-024).
- **Results built with `innerHTML`.** The results and the "nothing matches" line assign HTML built
  from escaped strings (`sphinx-daisyui.js:349`, `:360`). Build them with elements and
  `textContent`, including the marking of matched words (FR-019, Article V).
- **`show_version_warning_banner` and `check_switcher`.** Accepted and ignored. Honour both with
  pydata-sphinx-theme's meanings (FR-029, FR-034). Read pydata-sphinx-theme 0.24's handling of both
  first.
- **The daisyUI theme list written out by hand** (`__init__.py:22-28`), separately from
  `themes: all` in the stylesheet. Give the picker's full list one source with the compiled
  stylesheet (FR-003).
- **Values printed unescaped.** Every value these templates print is escaped with `|e`, per amended
  Article V (constitution 1.1.0): `search_bar_text`, `json_url`, `version_match`, theme names
  (FR-037). The inline script's values stay passed through `tojson`.
- **Fixed text not translatable.** Mark the menu's, dialog's, switcher's and banner's own text for
  translation in the message catalogue FS-001 sets up, including text the page script writes
  (FR-038). Research how the page script receives translated strings.
- **Templates reading `theme_*` directly.** `search-*.html:1` and `search-modal.html:1` read
  `theme_disable_search`. Read it through the `daisy` context (FR-039).
- **`switcher.json` addresses from the site root.** The documentation's file lists `/`,
  `/as-furo/` and `/as-pydata/`, which only work on the development server. Give it addresses that
  work where the documentation is published.
