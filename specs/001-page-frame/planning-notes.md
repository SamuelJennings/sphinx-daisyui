# Planning notes: 001-page-frame

Notes for research and planning. Each is answered by name before the build starts.

## The prototype

This feature is built from the accepted prototype on the `prototype-theme` branch. Read
`PROTOTYPE.md` on that branch whole, then its features 1 (page frame and layout code), 5 (brand
and logo), 9 (announcement) and 12 (previous, next and back to top). The prototype is served at
http://localhost:8062/ while it is being compared. Its screens and the maintainer's decisions in
its "Decisions" section are agreed. "Which decisions bind which feature" lists the ones that bind
feature 1.

## No design review at the plan stage

The prototype is the design. The plan goes straight to tasks with no separate design review.

## The look: ported, never redrawn

Port means copy across and clean to `main`'s standards. These rows of "The look" belong to this
feature:

| Prototype file | What this feature takes | Lands in `main` at |
|---|---|---|
| `theme/daisyui/layout.html` | All of it except the sections owned by features 4, 6, 7, 11, 13 and 14 (`:8-11`, `:13-29`, `:82-90`, `:106-113`, `:116-121`, `:172`). Features 9 and 12 are this feature's, so `:37-43`, `:126-141` and `:169-171` come too | The same path |
| `theme/daisyui/theme.toml` | Started here, with the options of features 1, 5, 9 and 12 | The same path |
| `components/copyright.html`, `sphinx-version.html`, `theme-version.html`, `last-updated.html`, `navbar-logo.html` | All, with `navbar-logo` carrying the logos (feature 5) | `theme/daisyui/components/` |
| `static/scripts/sphinx-daisyui.js` | `:1-8`, `:56-65`, `:88-90` (frame and drawer), `:127-154` (back to top and arrow keys), `:156-166` (announcement) | `theme/daisyui/static/scripts/`, one module per feature |
| `assets/theme.css` | All but its `@source inline` list (`:8`), which goes to the page-body styles | `assets/theme.css` |
| `assets/frame.css` | `:1-4`, `:18-127`, `:301-308` (frame) and `:6-9` (logo per mode) | `assets/`, imported from `theme.css`; one file or one per area, as the plan decides |
| `src/sphinx_daisyui/icons.json`, `scripts/icons.mjs` | All | The same paths |
| `src/sphinx_daisyui/__init__.py` | `parse_layout`, the layout check in `on_builder_inited`, `template_names` and the option readers (1), `static_url` and `brand` (5), and the `daisy` keys of 1, 5, 9 and 12 in `on_page_context` | `src/sphinx_daisyui/`, grouped in classes (Article IX) |
| `docs/_static/logo-light.svg`, `logo-dark.svg` | Both | `docs/_static/` |
| `docs/conf.py` | The theme's own options and `DAISY_LAYOUT` | `docs/conf.py` |
| `scripts/serve.sh`, `prebuild.sh`, `variants.sh` | All, with the four layout builds under `/layouts/` | `scripts/` |

Each merge is checked side by side against the prototype on the pages in "Pages to compare side
by side" whose rows name features 1, 5, 9 or 12, at 390, 1100 and 1440 pixels wide.

## The shared pieces this feature builds

From "The shared pieces" in `PROTOTYPE.md`. Each is built once here and reused by the features
named.

- **Component list placement.** One Jinja macro in its own template, imported by `layout.html`,
  and one method on the options class. Reused by every feature that adds a component: site
  navigation and On this page (#5), modes, search and the version switcher (#7), icon links, edit
  and view links, and the Furo and pydata-sphinx-theme configurations (#8). Check Sphinx's own
  `sidebars` loop in `basic/layout.html` first.
- **Reading theme options.** A `ThemeOptions` class with typed getters, read once per page and
  once at `builder-inited` (Article IX). Reused by all. Check `app.builder.theme.get_options()`
  first.
- **Icons.** An `Icons` class over the bundled JSON, exposed to templates, and the script that
  writes the JSON. Reused by all. `lucide-static` and `simple-icons` stay the build-time sources.
- **Square icon button.** A Jinja macro (a ghost, small, square button with its label and an
  optional tooltip). Reused by the search dialog (#7), icon links and edit and view links (#8).
  Check daisyUI's `btn` and `tooltip` first.
- **Dimmed text and surfaces.** One set of custom properties in a base layer, used by the frame
  and the page body, so the contrast check of Article XIV is made in one place. Reused by every
  stylesheet, first the page-body styles (#6). Check daisyUI's tokens and Tailwind's opacity
  modifiers first.
- **The layout code's rules.** Python is the one source. The layout playground on the Layout page
  (documentation work after this feature) reads the rules the build writes out, or both are
  tested against the same codes. The header's height is written once, not in Python and again in
  CSS.
- **A path under `_static` or a full URL** (from feature 5). A method on the options class.
  Reused by icon links (#8). Check Sphinx's `pathto(…, 1)` and its handling of URLs in
  `html_logo` first.

## The keyboard helper

"The shared pieces" has the search dialog feature (#7) build the keyboard shortcut helper, with
this feature reusing it for the drawer's Escape and the arrow keys. This feature is built first,
so it writes a small helper (is the reader typing, and one place that registers a shortcut) and
registers its keys through it. The search dialog feature grows the same helper rather than
writing its own. Check first: Sphinx's `doctools.js` already moves to the previous and next page
on the arrow keys when `navigation_with_keys` is on, using the page's `<link rel="prev">` and
`<link rel="next">`, and the `basic` theme already declares the option. Research says whether the
theme uses that and drops its own arrow-key code.

## What the prototype faked that this feature does properly

From "Faked or skipped" in `PROTOTYPE.md`:

- **The layout check's traceback.** A code of the wrong shape stops the build with the message
  alone (FR-004). Raising `ConfigError` in a `builder-inited` handler prints a crash report with a
  traceback on Sphinx 9.2 (see `research.md`). Find where the check can run so Sphinx prints only
  the message.
- **The `theme-version` address written by hand.** Read it from the package's metadata (FR-009).
- **The `navbar_end` components rendered twice.** Draw them once and place them by screen width
  (FR-010). `navbar-logo` is included three times in the prototype's `layout.html` (`:60`, `:75`,
  `:79`) and is written once too.
- **`sticky_banners`.** Accepted and ignored in the prototype. Find which theme defines it and
  what it means, then honour it (FR-028).
- **The announcement and Article V.** Once #3 amends Article V, the announcement is the site
  author's own HTML and every other printed value is escaped with `|e` (FR-011, FR-026). The page
  script's fetched announcement stays inserted as HTML, as the amended article allows.
- **The message catalogue.** Set up for the theme's own text, so a site's `language` applies to it
  (FR-017, Article VIII). Each later feature adds its own text.

## The `<body>` attributes and the public custom properties

This feature owns the `<body>` attributes the page script reads (`data-daisy-root`,
`data-daisy-suffix`, `data-daisy-link-suffix`, `data-daisy-builder`, `data-daisy-page`) and the
custom properties `--daisy-primary-width`, `--daisy-main-width` and `--daisy-secondary-width`,
which are documented for sites and fall under Article XV's naming promise. Check Sphinx's
`DOCUMENTATION_OPTIONS` (`URL_ROOT`, `FILE_SUFFIX`, `LINK_SUFFIX`, `BUILDER`) before adding
`<body>` attributes that repeat it.
