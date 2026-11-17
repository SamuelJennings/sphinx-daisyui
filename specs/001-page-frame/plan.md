# Implementation Plan: Arrange the page and fill it from conf.py

**Branch**: `001-page-frame` | **Date**: 2026-11-17 | **Spec**: `spec.md` | **Research**:
`research.md`

## Summary

The theme gets its page, ported from the accepted prototype on `prototype-theme`: one CSS grid
with five named areas arranged by a layout code, component lists placed by one macro, the
`copyright`, `sphinx-version`, `theme-version`, `last-updated` and `navbar-logo` components, the
drawer, the sticky header that takes its line and shadow once the page scrolls, the brand with a
logo for each mode, the announcement, previous and next links, and the back-to-top button. The
markup, classes and stylesheets are the prototype's, cleaned to `main`'s standards. The Python
behind them is rebuilt test-first, grouped in classes.

## Technical context

- **Language and stack**: Python 3.11+, Sphinx 7.4+, Jinja templates, Tailwind CSS 4 and
  daisyUI 5 compiled by npm at build time.
- **New runtime dependencies**: none. `importlib.metadata` and `markupsafe` (installed with
  Jinja, which Sphinx requires) are used. `markupsafe` is imported directly, so it is declared in
  `dependencies`.
- **New npm dev dependencies**: `lucide-static` and `simple-icons`, read only by
  `scripts/icons.mjs` to write `icons.json`. Nothing from npm reaches a site (Article VII).
- **Testing**: pytest with `sphinx.testing`, test sites under `tests/roots/`. The page script's
  behaviour is checked in headless Chrome while building (`research.md`).

## Constitution check

- **I, IV**: every behaviour is tested by building a real site and reading the pages.
- **II, III**: four small classes, each with a present use. No base classes.
- **V**: every printed option value is escaped with `|e`, except the announcement and Sphinx's
  own markup (`body`, `prev.title`, `next.title`).
- **VI**: the reference gains every option, component, custom property and `<body>` attribute,
  and the layout code letter by letter. README and CHANGELOG are updated.
- **VII**: no new runtime dependency beyond `markupsafe`, which is already installed.
- **VIII**: the theme's fixed text is marked with `_()` and the catalogue template ships.
- **IX**: `LayoutCode`, `ThemeOptions`, `Icons`, `Brand`. The handlers stay functions connected
  in `setup()`, as Sphinx owns that grouping.
- **X**: every option is the theme's own, named and shaped after pydata-sphinx-theme's where it
  has the same setting, with one name and one shape.
- **XI**: every colour is a daisyUI token or a `color-mix` of tokens.
- **XII**: the icons are inline SVG from the package.
- **XIV**: skip link, named landmarks, keyboard-reachable drawer controls, AA contrast on the
  dimmed text.

## Design

### Python (`src/sphinx_daisyui/`)

- **`layout.py`: `LayoutCode`**, a frozen dataclass built by `LayoutCode.parse(value)`. It
  normalises spaces and case, checks the shape, and holds `code`, `areas_wide`, `areas_medium`
  (the secondary sidebar's cells given to the area on their left), the four sticky flags,
  `primary_top` and `secondary_top` (`var(--daisy-header-height)` under a sticky header that
  spans the sidebar, otherwise `0px`) and `brand_in_sidebar`. A code of the wrong shape, or a
  value that is not a string, raises `LayoutCodeError`, a `ValueError`, whose message names the
  option, quotes the code and states the rules. The rules live here only (FR-005).
- **`options.py`: `ThemeOptions`**, built from a mapping of option values:
  `ThemeOptions.from_context(context)` (the page's `theme_*` values) and
  `ThemeOptions(app.builder.theme.get_options(app.config.html_theme_options))` at
  `builder-inited`. Getters: `text(name)`, `flag(name)` (Sphinx's and pydata-sphinx-theme's
  boolean strings), `mapping(name)` (a dict, or a JSON string), `components(name)` (a list or a
  comma-separated string, each name given `.html`), `layout()` and `static_url(path, pathto)`.
- **`icons.py`: `Icons`**, reading `icons.json` once. `Icons.svg(name, classes)` returns the
  SVG as markup with its classes, `aria-hidden` and `focusable="false"`. Exposed as `daisy.icon`.
- **`brand.py`: `Brand`**, a frozen dataclass from `Brand.from_options(options, context)`: the
  light and dark image addresses, the text, the alternative text and the link, read from `logo`
  and falling back to `logo_url`.
- **`__init__.py`**: `setup()` registers the theme, the message catalogue and two handlers.
  `check_layout` (`builder-inited`) reads the layout code for an HTML builder using the theme,
  and on a `LayoutCodeError` logs the message and raises `SystemExit(2)` (`research.md`).
  `add_page_context` (`html-page-context`) sets `daisy`, the one context every template reads
  (FR-035): `layout`, `brand`, `icon`, `version`, `repository`, the component lists
  (`navbar_start` … `footer_end`, `secondary`), `announcement`, `announcement_url`,
  `sticky_banners`, `show_prev_next` and `back_to_top`.

### Templates (`theme/daisyui/`)

- **`layout.html`**: the prototype's, without the sections other features own. Kept from
  `basic`: the `body` block, the `<link rel>` tags and the scripts. `body_tag` carries the five
  `data-daisy-*` attributes. The `header` block holds the skip link and the announcement, which
  moves into the header area when `sticky_banners` is on. The `content` block is the grid. The
  article has no `role`. The secondary sidebar is left out when its list is empty and on the
  search and index pages.
- **`components/macros.html`**: `components(names)` (include each name from `components/` first,
  then the site's templates, skipping a missing one) and `icon_button(label, icon, tooltip)`.
- **`navbar_end`** is written once, in the navbar, beside an empty slot in the drawer
  (`data-daisy-navbar-end` and `data-daisy-navbar-end-slot`). The page script moves it.
- **The brand** is written in the navbar and at the head of the primary sidebar, which is the
  drawer's head on a narrow screen. At a wide width only one shows: the sidebar's when the code
  gives it the top-left corner, otherwise the navbar's.
- **Components**: the five, ported, with their text marked for translation and every value
  escaped. `theme-version` prints `daisy.version` and links `daisy.repository`.

### Styles (`assets/`)

- **`tokens.css`**: the dimmed text and border properties in a base layer.
- **`frame.css`**: the prototype's `:1-9`, `:18-127` and `:301-308`, plus the logo rule for a page
  with no `data-mode` that follows `prefers-color-scheme`, the drawer's `navbar_end` slot, and the
  footer and previous and next labels moved onto `--daisy-text-muted`.
- **`theme.css`**: imports `tokens.css` and `frame.css`, sources the templates and the Python
  (the icon classes).

### Scripts (`theme/daisyui/static/scripts/`)

Plain deferred scripts, one per feature, loaded from `layout.html` in this order:

- `keys.js`: `sphinxDaisyui.keys`, with `isTyping()` and `on(key, handler)`.
- `frame.js`: the scrolled mark on the header, the header's measured height, the drawer closing
  on Escape and on a link, and moving `navbar_end` between the navbar and the drawer.
- `back-to-top.js`: the prototype's `:127-140`.
- `announcement.js`: the prototype's `:156-166`.

### Documentation and serving

- `docs/reference/`: `options.md` (every option with its default), `components.md`,
  `layout-code.md` (letter by letter, the medium arrangement, the custom properties and the
  `<body>` attributes). `docs/developer/arrange-the-page.md`, a how-to covering the layout code,
  component lists, logo and announcement.
- `docs/conf.py`: the prototype's own-options build, reduced to this feature's options, the two
  logos, `DAISY_LAYOUT`.
- `scripts/serve.sh`, `prebuild.sh`, `variants.sh`: ported, with the four layout builds under
  `/layouts/`. The port comes from the
  environment (`PORT`).

## What the plan cannot deliver on screen

Compared with the prototype, on `main` after this feature:

- No site navigation in the primary sidebar, no On this page, no page-body styles, no theme
  menu, search, version switcher or icon links. Their features build them. Their default
  component names draw nothing until then.
- The drawer's head shows the brand beside its close button, as the prototype does, so with the
  drawer open on a phone the brand is in view twice, once under the overlay.

## Complexity tracking

None. No principle is set aside.
