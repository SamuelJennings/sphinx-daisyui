# Research: 001-page-frame

## Assumptions checked

Run on 2026-11-17 against `main` at `34eaea5`, with Sphinx 9.2.0 and Python 3.13.

- **The theme registers and builds a site.** `uv run pytest` on `main`: the two smoke tests pass,
  so a site that sets `html_theme = "daisyui"` builds with the scaffold's `theme.toml` and
  stylesheet. This feature extends that build.
- **A `ConfigError` raised in a `builder-inited` handler prints a traceback.** A test site whose
  `conf.py` connects a handler that raises `ConfigError` stops with exit code 2, but Sphinx prints
  its crash report: a "Configuration error!" heading, the versions table, a traceback, and the
  address of a saved crash log. The prototype checks the layout code this way, which is the
  traceback its "Faked or skipped" list records. FR-004 asks for the message alone, so the plan
  must find another place for the check.
- **Sphinx's template environment does not autoescape.** `sphinx.jinja2glue` builds a
  `SandboxedEnvironment` with no `autoescape` argument. Every value a template prints from an
  option is escaped by hand (`|e`), which is what #3's amendment to Article V requires.
- **`navigation_with_keys` is already a `basic` theme option, and Sphinx already acts on it.**
  The `basic` theme's `theme.toml` declares `navigation_with_keys = "False"`, and Sphinx's
  `doctools.js` moves to `link[rel="prev"]` and `link[rel="next"]` on the arrow keys when
  `DOCUMENTATION_OPTIONS.NAVIGATION_WITH_KEYS` is set. The daisyui theme inherits `basic`, so the
  option exists before this feature declares it. Research decides whether the theme relies on
  Sphinx's handler (see `planning-notes.md`, "The keyboard helper").

## Planning notes, answered

Each heading is a note in `planning-notes.md`, in its own words.

### The prototype

**Adopted.** `PROTOTYPE.md` read whole, then features 1, 5, 9 and 12, the code behind them
(`layout.html`, `__init__.py`, `frame.css`, `theme.css`, the page script, the five components,
`theme.toml`, `icons.mjs`, the three serving scripts and `docs/conf.py`), and the decisions that
bind feature 1. Each is a requirement in the plan.

### No design review at the plan stage

**Adopted.** The plan goes straight to tasks.

### The look: ported, never redrawn

**Adopted.** Every row of the table is ported: the prototype's markup and classes are copied and
cleaned (escaping, translation, the sections other features own taken out), never redrawn.
`frame.css` lands as one file, `assets/frame.css`, holding the frame, because the frame's rules
for the grid, the drawer and the sticky areas are read together. The shared colour properties go
to their own file, `assets/tokens.css`, because the page-body styles import them too. The page
script lands as one file per feature, under `theme/daisyui/static/scripts/`.

### Component list placement

**Adopted.** Sphinx's `sidebars` loop in `basic/layout.html` includes each name with
`{%- include sidebartemplate %}` and fails on a missing name, so it is not reused as it stands.
The prototype's macro (`include ["components/" ~ name, name] ignore missing`) is the whole job: it
looks in the theme's components first, then the site's templates, and draws nothing for an
unknown name. It becomes one macro in `components/macros.html`, imported by `layout.html`, and
`ThemeOptions.components()` turns an option into the template names.

### Reading theme options

**Adopted.** `app.builder.theme.get_options(app.config.html_theme_options)` merges the theme's
defaults with the site's overrides, and every page's context carries the same values as
`theme_<name>`. A `ThemeOptions` class wraps either mapping with typed getters (`text`, `flag`,
`mapping`, `components`, `static_url`), built once at `builder-inited` and once per page.

### Icons

**Adopted.** `icons.json` and `scripts/icons.mjs` are ported whole. An `Icons` class reads the
JSON once and returns an icon as markup with its classes; templates call it as `daisy.icon`.
`lucide-static` and `simple-icons` become npm dev dependencies, used only by the icon script.

### Square icon button

**Adopted.** daisyUI's `btn btn-ghost btn-sm btn-square` plus `tooltip` is the button. A macro
in `components/macros.html` takes the label, the icon and an optional tooltip. This feature's
users of it are the drawer's menu and close buttons.

### Dimmed text and surfaces

**Adopted.** Tailwind's opacity modifiers dim text, but each one is a separate contrast decision.
One set of custom properties (`--daisy-text-muted`, `--daisy-border`) in `assets/tokens.css`,
built from daisyUI's tokens with `color-mix`, is used by the frame's footer, the previous and
next labels and the scrollbars. The muted text is 72% of `base-content`, which holds AA contrast
(4.5:1) on daisyUI's default light and dark themes.

### The layout code's rules

**Adopted, Python only for now.** `LayoutCode` holds the rules and is the one source. The
playground is documentation work after this feature and does not exist on `main`, so nothing is
written out for it yet. The header's height is written once, in CSS (`--daisy-header-height`).
Python writes `var(--daisy-header-height)` or `0px` for a sticky sidebar's top, and the page
script measures the header and updates the property, so a navbar that wraps or carries a sticky
banner still lines up.

### A path under `_static` or a full URL

**Adopted.** Sphinx's `pathto(path, 1)` resolves a file path from any page depth, and its
handling of `html_logo` already accepts a full URL (`logo_url`). `ThemeOptions.static_url()` puts
a bare file name under `_static/`, keeps a path starting `_static/`, and passes a URL through,
then resolves the path with `pathto`.

### The keyboard helper

**Adopted: Sphinx's handler for the arrow keys, the theme's helper for Escape.** Sphinx's
`doctools.js` is loaded on every page of a theme that inherits `basic`. With
`navigation_with_keys` on, it moves to the previous and next page on the arrow keys, skips them
while the reader types in an input, textarea, select or button, and ignores them with Alt, Ctrl,
Meta or Shift held. That is FR-032 exactly, so the prototype's arrow-key code is dropped. The
`<link rel="prev">` and `<link rel="next">` tags it follows are already written by
`basic/layout.html`. The theme's helper (`keys.js`) holds the "is the reader typing" test and
the one place that registers a shortcut. This feature registers Escape through it, and the
search dialog feature grows it.

### What the prototype faked that this feature does properly

- **The layout check's traceback.** **Adopted.** Every exception that leaves a Sphinx build goes
  to `sphinx._cli.util.errors.handle_exception`, which prints the crash report whatever the
  exception's class. A `SystemExit` is not an `Exception` and passes `build_main`'s handler, so
  the check logs its one message through Sphinx's logger as an error and raises `SystemExit(2)`,
  at `builder-inited`, before any page is read or written. Exit code 2 matches what Sphinx uses
  for a configuration error.
- **The `theme-version` address.** **Adopted.** `importlib.metadata` gives the version and the
  `Project-URL` entry named `repository`.
- **The `navbar_end` components rendered twice.** **Adopted.** They are written once, in the
  navbar. On a narrow screen the page script moves the one copy into its place in the drawer,
  and back when the screen widens, so the HTML holds them once (FR-010). `navbar-logo` goes from
  three includes to two: the navbar, and the head of the primary sidebar, which is also the
  drawer's head. One of the two is shown at each width (FR-025).
- **`sticky_banners`.** **Adopted.** pydata-sphinx-theme 0.16 defines it (`theme.conf`,
  `sticky_banners = False`). Switched on, it wraps the announcement and the header in one
  element that sticks to the top of the window (`layout.html`, `.pst-sticky-header`). Here the
  banner moves inside the header area, so it stays with the header, and the header stays in
  place as the layout code says. Furo has no such option.
- **The announcement and Article V.** **Adopted.** Article V as amended: the announcement is
  printed as the site author's markup, the fetched one inserted as HTML, every other value
  escaped with `|e`.
- **The message catalogue.** **Adopted.** pydata-sphinx-theme adds its catalogue to Sphinx's own
  domain (`app.add_message_catalog("sphinx", locale_dir)`), so `_()` in a template finds it. The
  theme does the same from `src/sphinx_daisyui/locale/`, ships `sphinx.pot` there, and
  `scripts/messages.sh` regenerates it with Babel (installed with Sphinx) and Jinja's extractor.

### The `<body>` attributes and the public custom properties

**Adopted, with Sphinx's values as the source.** Sphinx writes `data-content_root` on `<html>`
and `BUILDER`, `FILE_SUFFIX` and `LINK_SUFFIX` in `documentation_options.js`, but not the page
name, and FR-018 asks for all five on `<body>`. The `<body>` attributes are written from the same
context values Sphinx uses (`pathto('', 1)`, `file_suffix`, `link_suffix`, `builder`,
`pagename`), so they can never disagree. The three width properties are declared on
`.daisy-layout` and documented as public.

## Prototype items this feature meets

- The logo for the reader's mode: the prototype hides the other mode's logo by `data-mode` on
  `<html>`, which the modes feature sets. Until then no page carries `data-mode`, so the
  stylesheet also follows `prefers-color-scheme` when the attribute is absent, which is how
  daisyUI's own default themes choose light or dark.
- Two `main` landmarks: the prototype has `<main>` and an `<article role="main">` inside it. The
  article loses its role, so a page has one main landmark (FR-014).
- The prototype's `layout.html:33` adds `data-daisy-keys` for its own arrow-key code. With
  Sphinx's handler in use the attribute is not written.

## Decisions taken in research

- The theme's scripts load as plain deferred scripts, not ES modules, so a site opened from the
  file system still runs them.
- A test of the page script's behaviour in a browser needs a browser in CI, which needs a change
  to the workflows. The behaviour is checked in a headless browser while building, and adding a
  browser suite to CI is left to a change that can edit the workflows.

## What already exists

One line per new piece, with where the search stopped.

- Layout code parsing and the grid areas: new code (`LayoutCode`). Nothing in Sphinx or an
  installed package reads Quasar's notation.
- Reading theme options: Sphinx, `Theme.get_options()` and the page context's `theme_*` values.
  New code only for the typed reading (`ThemeOptions`).
- Component list placement: Jinja, `include … ignore missing`. New code: one macro.
- Escaping: Jinja's `|e` filter and `markupsafe.escape`.
- The check's message: Sphinx's logger (`sphinx.util.logging`).
- The theme's version and address: the standard library, `importlib.metadata`.
- Icons: the bundled JSON from `lucide-static` and `simple-icons`. New code: `Icons`.
- A file under `_static` from any page: Sphinx, `pathto(path, 1)`.
- The fallback logo: Sphinx, `logo_url` from `html_logo`.
- Previous and next pages: Sphinx, `prev` and `next` in the page context.
- Arrow keys: Sphinx, `doctools.js` with `navigation_with_keys`.
- The drawer: the browser, a checkbox and `<label for>`, as the prototype has it. New code: the
  script that closes it on Escape and on a link.
- The scrolled header, the back-to-top button, the fetched announcement: new code, ported from
  the prototype's script.
- Translation: Sphinx, `add_message_catalog` and Jinja's `i18n` extension, which Sphinx loads.
  Babel, installed with Sphinx, writes the catalogue template.
- Square icon button: daisyUI's `btn` and `tooltip`.
- The development server: `sphinx-autobuild`, already in the docs group, with the prototype's
  three scripts.
