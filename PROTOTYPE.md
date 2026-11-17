# sphinx-daisyui prototype

The record of the prototype on branch `prototype-theme`, and its hand-over to `main`. This branch
is never merged. It stays as the reference that every specification and plan for `main` reads,
and `main` is built to look like it.

The words used here are defined in `CONTEXT.md` on `main`.

## The idea

> All of the major sphinx themes are centered around bootstrap which IMO is getting a little
> outdated. I find daisyui to be much fresher and more modern. We also have a lot of the page
> structure and styling necessary to integrate with sphinx and sphinx-design. […] I would be
> looking to support similar html theme options to Furo or pydata sphinx theme so that users can
> easily switch.

## What it's based on

- **A configuration written for another theme builds unchanged.** The theme declares every
  option Furo 2025.12 and pydata-sphinx-theme 0.24 declare (read from their `theme.conf`), and
  the template names both use in `html_sidebars` and the component lists. Source: the two
  packages' own `theme.conf` files.
- **The look comes from django-mvp-sphinx.** Its page-body stylesheet (`content.css`, drawn
  with daisyUI tokens: admonitions, code, tables, signatures, sphinx-design) is ported, not redrawn.
  So is its rule that a wide table or equation scrolls in its own focusable region.
- **Three columns, as documentation readers expect.** Site navigation on the left, the page in
  a column of about 75 characters, the page's own headings on the right, collapsing to a drawer
  and an "On this page" disclosure on a phone. This is the shared layout of Furo,
  pydata-sphinx-theme, Docusaurus and Starlight, so readers arriving from any of them find
  things where they expect.
- **Every colour is a daisyUI token,** including code highlighting and sphinx-design's
  variables, so any of daisyUI's 35 themes works in light and dark with nothing to build.
- **No Node for users.** The compiled stylesheet ships in the wheel. A custom theme is CSS
  variables in `html_static_path`.

## What was built

- **Theme package** `src/sphinx_daisyui/`: `theme.toml`, `layout.html`, 22 components under
  `components/`, one script, one stylesheet built by Tailwind 4 + daisyUI 5 from `assets/`.
- **Option handling** in `__init__.py`: Furo's and pydata's options normalised into one
  `daisy` context. Logo (both shapes), icon links (Font Awesome names mapped to bundled
  Lucide/Simple Icons SVGs), edit and view links (Furo `source_*` or pydata `html_context`, for
  GitHub, GitLab and Bitbucket), Furo CSS variables mapped onto daisyUI tokens, pydata component
  lists, header links with overflow menu, sectioned sidebar when `navbar-nav` is in the header.
- **Navbar**: brand, header links, search button with shortcut, version switcher, mode and
  theme menu (system, light, dark, plus an optional picker of daisyUI themes with swatches), icon
  links. Announcement banner, from text or a URL.
- **Sidebar**: the toctree redrawn as a menu with open/close toggles, current page marked and
  scrolled into view, captions as section labels.
- **Page**: breadcrumbs, edit/view buttons, page body, previous/next cards, footer components,
  back-to-top button, arrow-key navigation when switched on.
- **On this page**: right column with the heading being read marked as you scroll. A
  disclosure above the page on narrower screens.
- **Search**: a dialog opened by Ctrl/⌘K or `/`, results as you type from Sphinx's own
  `searchindex.js`: pages, section titles linked to their heading, and API objects. Arrow keys
  and Enter. Enter with nothing chosen opens Sphinx's full search page, which is restyled.
- **Version switcher**: reads pydata's `switcher.json`. Choosing a version opens the same page
  there when it exists.
- **Documentation site** `docs/`: install, switching guides, options reference, and a kitchen
  sink (typography, admonitions, code, tables, lists, maths, sphinx-design, autodoc). Built three
  times: with the theme's own options at `/`, with a Furo configuration at `/as-furo/`, and with
  a pydata-sphinx-theme configuration at `/as-pydata/`.
- **Layout code**: the `layout` option, in Quasar's notation (`"hHh LpR lff"`). The page is
  one CSS grid with five named areas (header, primary, main, secondary, footer). Python
  validates the code, writes `grid-template-areas` for wide screens and for screens without
  room for the right sidebar, and marks which areas stay in place. Below `lg` the page is one
  column and the sidebar is a drawer. When the sidebar reaches the top, the logo moves to its
  head. Compared at `/layouts/<code>/` for four codes besides the default.
- **Layout playground** on the Layout page: a daisyUI browser mock-up whose page is the same
  five-area grid, redrawn as you type a code or pick a recipe, at wide, medium and phone width.
  It scrolls inside the window, so the areas that stay in place stay. Each letter is shown as a
  chip in its area's colour, with a sentence per area saying what the code does, and the
  `html_theme_options` line to copy. Docs-only files: `docs/_static/layout-playground.*`. Its
  parser repeats `parse_layout` in JavaScript.
- **`daisy-sphinx-escape`**: raw HTML inside an element with this class is left out of the
  page-body styles, so embedded components keep daisyUI's own look. `mockup-browser`, `input`,
  `join` and a few others are compiled into the stylesheet for raw HTML to use.
- **Serving**: `scripts/serve.sh` (sphinx-autobuild, rebuilding the stylesheet and all three
  sites on change), on port 8062.

## Decided on my own

- The brand sits in the navbar for every configuration. Furo's sidebar brand and search
  templates are accepted and draw nothing.
- Default layout follows Furo: full tree in the sidebar, no header links. Putting `navbar-nav`
  in `navbar_center` switches to pydata's sectioned layout.
- Code highlighting comes from the theme's tokens by default and Pygments' own stylesheet is
  dropped. `pygments_light_style` and `pygments_dark_style` bring Pygments styles back.
- Article on `base-100`, sidebar on `base-200` on a phone and transparent beside it on a
  desktop. django-mvp-sphinx lays pages on `base-200`, because it sits inside an app shell.
- All 35 daisyUI themes are compiled in (30 KB gzipped for the whole stylesheet).
- Icons are inline SVG (Lucide under ISC, Simple Icons under CC0), never an icon font.

## Faked or skipped

Each item names the feature (see "The features" below) that does it properly in `main`.

| What was faked or skipped | Done properly by |
|---|---|
| A layout code of the wrong shape stops the build with a clear message, but Sphinx prints it inside a traceback, because the check runs in an event handler. | 1. Page frame and layout code |
| No tests. | Every feature, for what it adds, through `sphinx.testing` builds (Article IV) |
| No accessibility audit beyond keyboard paths and named regions. | Every feature, for what it adds (Article XIV) |
| The search ranking is a light stemmer and prefix matcher, not Sphinx's Porter stemmer, and isn't language-aware. | 7. Search dialog |
| `analytics`, `shorten_urls` and `surface_warnings` are accepted and do nothing. | 15. pydata-sphinx-theme configurations |
| `show_version_warning_banner` and `check_switcher` are accepted and do nothing. | 8. Version switcher |
| `sticky_banners` is accepted and does nothing. | 9. Announcement |
| `search_as_you_type` is accepted and does nothing. | 7. Search dialog |
| `navbar_align` is only partly honoured. | 13. Header links |
| The theme's own text ("On this page", "Previous") isn't translatable yet. | Every feature, for its own text. The page frame sets up the message catalogue (Article VIII) |
| The `theme-version` footer line writes the repository's address into the template by hand. | 1. Page frame and layout code |
| `light_css_variables` only maps the main Furo variable names. The rest are set as written. | 14. Furo configurations |
| The navbar and drawer each render the `navbar_end` components, so a phone build carries the theme picker twice in the HTML. | 1. Page frame and layout code |
| Sphinx's template environment doesn't autoescape, and the templates print option values (addresses, names, labels) without `\|e`. The `url` and `local` icon links build an `<img>` tag from the option text with an f-string (`__init__.py:380`, `:382`). | Every feature, for the values it prints (Article V). 10. Icon links for the `<img>` tags |
| The search dialog writes its results and its "Nothing matches" line by assigning HTML built from escaped strings (`sphinx-daisyui.js:349`, `:360`), where Article V asks for `textContent`. | 7. Search dialog |
| An announcement fetched from a URL is inserted as HTML (`sphinx-daisyui.js:164`), as pydata-sphinx-theme does. Text announcements are printed as HTML too, as both Furo and pydata-sphinx-theme do. | 9. Announcement, which records how Article V and Article X meet here |
| A `local` icon link's path isn't resolved against `_static`, as a logo's path is. | 10. Icon links |
| The list of daisyUI themes the picker offers is written out by hand (`__init__.py:22-28`), separately from `themes: all` in the stylesheet. | 6. Modes and daisyUI themes |
| `beautifulsoup4` is a runtime dependency with no stated reason. | 2. Site navigation, the first feature that needs it (Article VII) |
| The prototype's `pyproject.toml` asks for Python 3.10 and Sphinx 7.3. | Nothing to do: `main`'s scaffold (Python 3.11, Sphinx 7.4) stands |
| The documentation links to the other builds with addresses from the site root (`/as-furo/`, `/layouts/…/`, and `switcher.json`), which only work on the development server. | Fixes and docs work: the documentation site |

## Decisions

- 2026-11-17 Sam: prototype it locally before onboarding anything. Support Furo's and
  pydata-sphinx-theme's options so users can switch easily.
- 2026-11-17 Sam: article-info items stay on one line. A quotation's attribution gets a small
  space after its dash. The page is called Admonitions, after the directive. Lists are more
  compact: 4px between one-line items, wider spacing only when an item holds several blocks.
  A toctree in a page is drawn as the sidebar's menu, with toggles, and the first two levels
  start open.
- 2026-11-17 Sam: the layout is configurable with a Quasar-style code over named CSS grid
  areas. Default `hHh LpR lff`. Decided on my own: the option is called `layout`. The page
  column stays centred on wide screens, with the two sidebar columns taking the spare width.
  The logo moves into the sidebar when the sidebar reaches the top, rather than relying on
  Furo's `sidebar/brand.html`.
- 2026-11-17 Sam: show the layout system as a live mock-up driven by a form, in daisyUI's
  browser mock-up. Decided on my own: recipes and a screen-size switch beside the code field,
  colour-coded letter chips, and a plain-language reading of the code under the mock-up.
- 2026-11-17 Sam: centre the letter chips. The code field refuses what a layout code can't hold.
  A sticky sidebar in the mock-up sticks at once. No line under the logo when the sidebar
  reaches the top. The header gets its line and a small shadow only once the page scrolls, as
  on daisyUI's site. Decided on my own: the field refuses a letter as it's typed, with a
  sentence naming what that position takes, adds the spaces itself, and also carries the same
  rule as an HTML `pattern`.
- 2026-11-17 Sam: header shadow on scroll is Tailwind's `shadow-xs`, switched at once with no
  fade. Sticky mock-up sidebars keep their top edge.
- 2026-11-17 Sam: prototype accepted ("ready to get this show on the road"). Next: set up the
  repository, then build `main` from this branch, feature by feature, each one specified,
  planned, built, reviewed and merged on its own.
- 2026-11-17 Sam: no compatibility layer for Furo or pydata-sphinx-theme. The theme has its own
  options, modelled on pydata-sphinx-theme's names and shapes where they fit, with one name and
  one shape per setting. Nothing maps, aliases or accepts another theme's options, template
  names, `html_context` keys or CSS variables, and a site coming from either theme reconfigures.
  The layout code is how a site gets a page like either one. The `/as-furo/` and `/as-pydata/`
  builds, the switching guides and feature 14 and 15 go, and features 5, 7, 10 and 11 keep one
  shape of their options. This replaces "A configuration written for another theme builds
  unchanged" under "What it's based on".

## The hand-over

How the prototype becomes `main`. Every specification and plan reads this section first. The
prototype is served at http://localhost:8062/ from this branch: the theme's own options at `/`,
a Furo configuration at `/as-furo/`, a pydata-sphinx-theme configuration at `/as-pydata/`, and
four other layout codes under `/layouts/`. `main` holds the package scaffold only.

### The features

A feature is one new way for a **site author** (in `conf.py`) or a **reader** (on the page) to
do something. Each is specified, built and merged on its own, in this order. A feature depends
only on features above it.

**1. Page frame and layout code.** *Builds on:* `main`'s scaffold.
- A site author arranges the five areas with the `layout` code and fills the header, sidebars
  and footer with components named in component lists. A reader gets the three-column page, a
  sticky header that takes its line and shadow once the page scrolls, the drawer on a phone, and
  a skip link.
- Pages: http://localhost:8062/ ,
  http://localhost:8062/layouts/lHh-LpR-lff/ ,
  http://localhost:8062/layouts/hHh-LpR-fff/ ,
  http://localhost:8062/layouts/hhh-lpr-fff/ ,
  http://localhost:8062/layouts/hHr-LpR-lfr/
- Theme options: `layout`, `navbar_start`, `navbar_center`, `navbar_end`, `navbar_persistent`,
  `article_header_start`, `article_header_end`, `article_footer_items`,
  `content_footer_items`, `primary_sidebar_end`, `secondary_sidebar_items`, `footer_start`,
  `footer_center`, `footer_end`. Components: `copyright`, `sphinx-version`, `theme-version`,
  `last-updated`, and a plain `navbar-logo` (the site's title as a link home).
- `daisy` context: `layout`, `brand_in_sidebar`, `version`, `icon`, and every component list
  (`navbar_start` … `footer_end`, `secondary`).
- Also brings: the options class, the icon set and its build script, the component macro, the
  page script's base, and the shared colour properties (see "The shared pieces").

**2. Site navigation.** *Builds on:* 1.
- A reader moves through the whole site from the primary sidebar: branches open and close, the
  current page is marked and scrolled into view, captions label each section, and breadcrumbs
  show where the page sits. A site author sets how deep it goes and how much starts open.
- Pages: http://localhost:8062/kitchen-sink/deeper/deepest/leaf.html ,
  http://localhost:8062/kitchen-sink/deeper/index.html
- Theme options: `navigation_depth`, `show_nav_level`, `collapse_navigation`,
  `sidebar_includehidden`. `html_sidebars` names: `sidebar-nav.html`. Components: `breadcrumbs`.
- `daisy` context: `navigation`.

**3. Page-body styles.** *Builds on:* 1, and 2 for the toctree in a page.
- A reader gets every page body drawn with daisyUI's tokens: headings, inline text, lists,
  quotes, admonitions, version notes, code (highlighted from the tokens), tables and equations
  that scroll in their own focusable region, pictures, footnotes, API entries, sphinx-design's
  grids, cards, tabs, dropdowns, badges and buttons, sphinx-copybutton, and a toctree in a page
  drawn as the sidebar's menu. A site author keeps daisyUI's look on raw HTML with the escape
  class, or brings Pygments styles back.
- Pages: http://localhost:8062/kitchen-sink/typography.html ,
  http://localhost:8062/kitchen-sink/admonitions.html ,
  http://localhost:8062/kitchen-sink/code.html ,
  http://localhost:8062/kitchen-sink/tables.html ,
  http://localhost:8062/kitchen-sink/lists.html ,
  http://localhost:8062/kitchen-sink/media.html ,
  http://localhost:8062/kitchen-sink/design.html ,
  http://localhost:8062/kitchen-sink/api.html ,
  http://localhost:8062/kitchen-sink/deeper/index.html ,
  http://localhost:8062/_modules/palette.html ,
  http://localhost:8062/genindex.html
- Theme options: `pygments_light_style`, `pygments_dark_style`, and pydata-sphinx-theme's
  misspelt `pygment_light_style` and `pygment_dark_style`. CSS class: `daisy-sphinx-escape`.
- `daisy` context: none. It rewrites `body` (`rewrite_body`) and drops `pygments.css`.

**4. On this page.** *Builds on:* 1.
- A reader sees the page's own headings in the secondary sidebar, with the heading being read
  marked as they scroll, or in a disclosure above the page on a narrower screen.
- Pages: http://localhost:8062/kitchen-sink/typography.html ,
  http://localhost:8062/configure/layout-code.html
- Theme options: `show_toc_level`. Components: `page-toc` (the default of
  `secondary_sidebar_items`).
- `daisy` context: `page_toc`, `page_toc_count`, `show_toc_level`.

**5. Brand and logo.** *Builds on:* 1.
- A site author shows a logo for each mode, with or without the site's name, linked where they
  choose, in either theme's shape of option. When the layout code runs the primary sidebar to the
  top, the logo moves to its head.
- Pages: http://localhost:8062/ , http://localhost:8062/as-pydata/ ,
  http://localhost:8062/layouts/lHh-LpR-lff/
- Theme options: `light_logo`, `dark_logo`, `sidebar_hide_name`, `logo` (`text`, `image_light`,
  `image_dark`, `alt_text`, `link`), `logo_link`. Sphinx's `html_logo` as the fallback.
- `daisy` context: `brand`.

**6. Modes and daisyUI themes.** *Builds on:* 1.
- A site author picks a daisyUI theme for each mode and the starting mode, and can offer readers
  a picker of daisyUI themes. A reader switches between system, light and dark, or picks a theme,
  and the choice is remembered and applied before the first paint.
- Pages: http://localhost:8062/ (theme menu open, then a theme picked),
  http://localhost:8062/configure/themes.html , http://localhost:8062/as-furo/ (no picker)
- Theme options: `light_theme`, `dark_theme`, `default_mode`, `theme_picker`. Components:
  `theme-switcher`.
- `daisy` context: `light_theme`, `dark_theme`, `default_mode`, `picker`.

**7. Search dialog.** *Builds on:* 1.
- A reader opens search with Ctrl+K, ⌘K or `/`, sees pages, sections and API names as they
  type, moves with the arrow keys and opens with Enter. Enter with nothing chosen opens Sphinx's
  full search page, which is restyled.
- Pages: http://localhost:8062/ (dialog open, "layout" typed),
  http://localhost:8062/search.html?q=layout ,
  http://localhost:8062/configure/search-and-versions.html
- Theme options: `search_bar_text`, `disable_search`, `search_as_you_type`. Components:
  `search-button-field`, `search-button`, `search-field`, and the dialog itself.
- `daisy` context: `search_bar_text`.

**8. Version switcher.** *Builds on:* 1, and 7 for the shared page-address script.
- A site author lists published versions in `switcher.json`. A reader picks one, and lands on the
  same page in that version when it exists there, or on its home page.
- Pages: http://localhost:8062/ (version menu open), http://localhost:8062/as-pydata/
- Theme options: `switcher` (`json_url`, `version_match`), `check_switcher`,
  `show_version_warning_banner`. Components: `version-switcher`.
- `daisy` context: `switcher`.

**9. Announcement.** *Builds on:* 1.
- A site author puts a banner across the top of every page, from text or from a URL that returns
  HTML.
- Pages: http://localhost:8062/as-furo/ , http://localhost:8062/as-pydata/ ,
  http://localhost:8062/layouts/hhh-lpr-fff/
- Theme options: `announcement`, `sticky_banners`.
- `daisy` context: `announcement`.

**10. Icon links.** *Builds on:* 1, and 5 for resolving static paths.
- A site author links the site's repository, chat or package index as icons in the navbar or
  footer, by the options of either theme, with Font Awesome names matched to bundled icons.
- Pages: http://localhost:8062/ , http://localhost:8062/as-pydata/ ,
  http://localhost:8062/as-furo/ (footer icons)
- Theme options: `github_url`, `gitlab_url`, `bitbucket_url`, `twitter_url`, `icon_links`,
  `icon_links_label`, `footer_icons`. Components: `navbar-icon-links`.
- `daisy` context: `icon_links`, `footer_icons`.

**11. Edit and view source links.** *Builds on:* 1.
- A reader opens the page's source to edit or view it on GitHub, GitLab or Bitbucket, or opens
  Sphinx's copy of the source, from buttons beside the breadcrumbs or links in the secondary
  sidebar.
- Pages: http://localhost:8062/kitchen-sink/typography.html ,
  http://localhost:8062/as-furo/kitchen-sink/typography.html ,
  http://localhost:8062/as-pydata/kitchen-sink/typography.html
- Theme options: `source_repository`, `source_branch`, `source_directory`, `source_edit_link`,
  `source_view_link`, `top_of_page_button`, `top_of_page_buttons`, `use_edit_page_button`.
  `html_context` keys: `github_user`, `github_repo`, `github_version`, and the GitLab and
  Bitbucket equivalents, `doc_path`. Components: `edit-this-page`, `sourcelink`.
- `daisy` context: `sources`, `top_buttons`.

**12. Previous, next and back to top.** *Builds on:* 1, and 7 for the keyboard helper.
- A reader moves to the previous or next page from cards at the foot of the page, or with the
  arrow keys when the site author switches them on, and returns to the top of a long page from a
  button offered when they scroll back up.
- Pages: http://localhost:8062/kitchen-sink/code.html (foot of the page, then scrolled back up)
- Theme options: `show_prev_next`, `navigation_with_keys`, `back_to_top_button`.
- `daisy` context: `show_prev_next`, `navigation_with_keys`, `back_to_top`.

**13. Header links.** *Builds on:* 2.
- A site author places `navbar-nav` and the top-level sections move into the navbar, with the
  rest in a menu, external links added, and the primary sidebar showing only the current
  section. On a phone the sections are listed at the head of the drawer.
- Pages: http://localhost:8062/as-pydata/ ,
  http://localhost:8062/as-pydata/kitchen-sink/deeper/index.html ,
  http://localhost:8062/configure/layout.html
- Theme options: `external_links`, `header_links_before_dropdown`, `header_dropdown_text`,
  `navbar_align`. Components: `navbar-nav`.
- `daisy` context: `header_links`, `header_more`, `header_more_text`, `sectioned`.

**14. Furo configurations.** *Builds on:* 1 to 12.
- A site author switches from Furo by changing `html_theme` only. Every Furo option and
  `html_sidebars` name is accepted, the ones with a meaning here act on it, Furo's CSS variables
  are mapped onto tokens, and the rest draw nothing.
- Pages: http://localhost:8062/as-furo/ , http://localhost:8062/get-started/from-furo.html
- Theme options: `light_css_variables`, `dark_css_variables`, and every remaining Furo option
  declared in `theme.toml`. `html_sidebars` names: `sidebar/brand.html`, `sidebar/search.html`,
  `sidebar/navigation.html`, `sidebar/scroll-start.html`, `sidebar/scroll-end.html`,
  `sidebar/ethical-ads.html`, `sidebar/rtd-versions.html`, `sidebar/variant-selector.html`.
- `daisy` context: `css_variables`.
- Also brings: the `/as-furo/` build and the switching guide.

**15. pydata-sphinx-theme configurations.** *Builds on:* 1 to 13.
- A site author switches from pydata-sphinx-theme by changing `html_theme` only, keeping
  `html_context`. Every pydata-sphinx-theme option and component name is accepted, and the ones
  this theme can't honour yet are accepted and ignored.
- Pages: http://localhost:8062/as-pydata/ , http://localhost:8062/get-started/from-pydata.html
- Theme options: `analytics`, `shorten_urls`, `surface_warnings`, `templates_skip_empty_check`,
  and every remaining pydata-sphinx-theme option declared in `theme.toml`. Components and
  `html_sidebars` names: `sidebar-nav-bs`, `sidebar-collapse`, `sidebar-ethical-ads`.
- `daisy` context: none.
- Also brings: the `/as-pydata/` build and the switching guide.

Features 2 to 12 depend only on the frame and can be built in parallel, except where a line above
says otherwise. Each feature that adds a borrowed option adds it to `theme.toml` itself, so
Article X holds at every merge. Features 14 and 15 then declare the rest and add the two build
variants that prove a configuration builds unchanged.

### Work that isn't a feature

These give nobody a new way to do something. Each is a fix or docs change, not a specification.

- **The layout playground** on the Layout page
  (http://localhost:8062/configure/layout-code.html): the browser mock-up, its recipes, screen
  switch, letter chips, field that refuses what a layout code can't hold, and the sentence per
  area. Docs-only files: `docs/_static/layout-playground.css`, `docs/_static/layout-playground.js`
  and the raw HTML block in `docs/configure/layout-code.md`. After feature 1.
- **The documentation site.** `main` has `docs/developer/` and `docs/reference/`. The
  prototype's `get-started/`, `configure/` and `kitchen-sink/` pages move into that shape under
  `main`'s documentation standard. Each feature ships the pages for what it adds (Article VI).
  This work is the home page, the site's own `conf.py`, the changelog page, and the links between
  the builds (see "Faked or skipped").
- **The kitchen sink pages** (`docs/kitchen-sink/`, `docs/_ext/palette.py`) come in with feature 3,
  since they are the pages its look is checked on.
- **The development server**: `scripts/serve.sh`, `scripts/prebuild.sh` and `scripts/variants.sh`.
  Feature 1 brings them with the layout builds. Features 14 and 15 add their builds to
  `variants.sh`.

### The option and context surface

The theme has no data. Its surface is what a site author writes and what the templates read.

- **`theme.toml`** declares every theme option, own and borrowed. Each feature above lists the
  options it owns. Feature 1 adds `layout` and the component lists, and each later feature adds
  its own.
- **The `daisy` context**, set in `on_page_context` (`__init__.py:468-563`), is the one dict every
  template reads. Each feature above lists the keys it owns. `pygments_custom` (`:561`) is set and
  never read, so it isn't carried over.
- **Three templates read `theme_*` values directly** instead of `daisy`:
  `components/search-*.html:1` and `search-modal.html:1` (`theme_disable_search`),
  `components/navbar-icon-links.html:2` (`theme_icon_links_label`), and `layout.html:64`
  (`theme_navbar_align`). In `main` every template reads `daisy` only.
- **The attributes on `<html>`** that scripts and stylesheets share: `data-theme`, `data-mode`,
  `data-mode-choice`, `data-light-theme`, `data-dark-theme`, `data-default-mode`. Feature 6 owns
  them. Feature 1 owns the `<body>` attributes the page script reads (`data-daisy-root`,
  `data-daisy-suffix`, `data-daisy-link-suffix`, `data-daisy-builder`, `data-daisy-page`).
- **CSS custom properties a site may set**: `--daisy-primary-width`, `--daisy-main-width` and
  `--daisy-secondary-width` (feature 1). These are documented for sites, so they fall under
  Article XV's naming promise.

### The shared pieces

Patterns that recur across features. Each is built once, by the feature named, and reused by the
others. "Check first" is what to look for before writing it (the repository, an installed
package, Sphinx, daisyUI or the browser may already have it).

| Piece | Where it occurs | Becomes | Built by | Reused by | Check first |
|---|---|---|---|---|---|
| Component list placement | `layout.html:4-6` (macro), called at `layout.html:64`, `66`, `67`, `81`, `93`, `103`, `105`, `125`, `142`, `148`, `154`, `155`, `157`; written out again by hand at `layout.html:59-62` and `92`; names to files in `template_names`, `__init__.py:97-102`, used at `:477`, `:497`, `:542-554` | One Jinja macro in its own template, imported by `layout.html`, and one method on the options class | 1 | Every feature that adds a component | Sphinx's own `sidebars` loop in `basic/layout.html` |
| Reading theme options | `as_list`, `as_bool`, `as_int`, `as_dict` at `__init__.py:62-94`, the `opt` closure at `:472-474`, and options merged a second time at `:570` | A `ThemeOptions` class with typed getters, read once per page and once at `builder-inited` (Article IX) | 1 | All | `app.builder.theme.get_options()` |
| Icons | `icons()` and `icon()` at `__init__.py:42-50`, `icons.json`, `scripts/icons.mjs:5-6`; called at `__init__.py:193`, `208`, `295`, `374`, `384`, `386`, and through `daisy.icon` at `layout.html:57`, `76`, `108`, `110`, `130`, `137`, `170`, `breadcrumbs.html:4`, `edit-this-page.html:2`, `sourcelink.html:2`, `page-toc.html:3`, `navbar-nav.html:4`, `8`, `11`, `search-button*.html:3`, `search-modal.html:5`, `8`, `theme-switcher.html:3-6`, `10-12`, `version-switcher.html:4` | An `Icons` class over the bundled JSON, exposed as `daisy.icon`, and the script that writes the JSON | 1 | All | `lucide-static` and `simple-icons` stay the build-time sources |
| A branch that opens and closes | Python at `__init__.py:194-212` (site navigation) and `:276-298` (toctree in a page); CSS at `frame.css:144-176` and `content.css:660-724`; script at `sphinx-daisyui.js:71-78` | One Python method that adds the row and toggle to a list item, one CSS rule set for `.daisy-nav-row` and `.daisy-nav-toggle`, one script module | 2 | 3 | daisyUI's collapsible `menu` uses `<details>`, which can't keep the entry a link. A button beside the link stays |
| Reading Sphinx's toctree output | BeautifulSoup parses at `__init__.py:168`, `226`, `245`, `271`; the site toctree is rendered twice at `:485-486` | One class that reads a toctree once and gives the menu, the top-level links and the page's headings | 2 | 4, 13, 3 | Sphinx's `toctree()` arguments, and docutils' doctree in place of re-parsing HTML where it is reachable |
| Navbar dropdown | `theme-switcher.html:1-2`, `8`; `version-switcher.html:2-3`, `6`; `navbar-nav.html:7-9`: the same trigger and `dropdown-content … rounded-box border border-base-300 bg-base-100 p-2 shadow-lg` panel | A Jinja macro taking the trigger and the panel's content | 6 | 8, 13 | daisyUI's `dropdown` |
| Square icon button | `navbar-icon-links.html:4`, `layout.html:57`, `76`, `108`, `110`, `161`, `search-modal.html:8` | A Jinja macro (`btn btn-ghost btn-sm btn-square`, with its label and optional tooltip) | 1 | 7, 10, 11 | daisyUI's `btn` and `tooltip` |
| The site-navigation component under three names | `sidebar-nav.html:1-3`, `sidebar-nav-bs.html:1-3`, `sidebar/navigation.html:1-3`, identical | One component. The other names include it | 2 | 14 (`sidebar/navigation.html`), 15 (`sidebar-nav-bs.html`) | Nothing |
| The search button under three names | `search-button.html:1-7`, `search-field.html:1-7`, `search-button-field.html:1-7`, identical | One component. The other names include it | 7 | 15 | Nothing |
| Accepted names that draw nothing | `sidebar-collapse.html:1`, `sidebar-ethical-ads.html:1`, `sidebar/brand.html:1`, `sidebar/ethical-ads.html:1`, `sidebar/rtd-versions.html:1`, `sidebar/scroll-end.html:1`, `sidebar/scroll-start.html:1`, `sidebar/search.html:1`, `sidebar/variant-selector.html:1` | One list of accepted names that resolve to an empty template | 14 | 15 | Jinja's `ignore missing` on the include, which already skips unknown names |
| The mode attributes | Set before the first paint at `layout.html:16-29` and again by the script at `sphinx-daisyui.js:14-36`; read at `frame.css:7-8` (logo), `frame.css:12-16` (mode icon), `__init__.py:455` (Furo CSS variables), `__init__.py:586` (Pygments styles) | One documented contract on `<html>`, with one function that applies a choice, used by both the inline script and the page script | 6 | 3, 5, 14 | daisyUI's `data-theme`, and Sphinx's own `pygments_dark_style` in `theme.toml`, which keys on a media query rather than an attribute |
| The page's address | `<body>` attributes at `layout.html:33`, `pageUrl` at `sphinx-daisyui.js:172-180`, used at `:209` and `:354` | A shared script module | 7 | 8 | Sphinx's `DOCUMENTATION_OPTIONS` (`URL_ROOT`, `FILE_SUFFIX`, `LINK_SUFFIX`, `BUILDER`) in `documentation_options.js` |
| Keyboard shortcuts | "Is the reader typing" at `sphinx-daisyui.js:149` and `:258`; key listeners at `:90`, `:147`, `:257` | One helper and one place that registers shortcuts | 7 | 1 (Escape closes the drawer), 12 (arrow keys) | Sphinx's own `navigation_with_keys` handling in `doctools.js` |
| Dimmed text and surfaces | `color-mix(in oklab, var(--color-base-content) N%, transparent)` at `frame.css:141`, `161`, `164`, `172`, `191`, `216`, `225`, `262`, `290`, `307`; `text-base-content/60` and `/70` at `page-toc.html:3`, `breadcrumbs.html:2`, `layout.html:152`, `search-modal.html:11`, `14`; the page body's own `--daisy-sphinx-muted` and its neighbours at `content.css:29-47` | One set of custom properties in a base layer, used by the frame and the page body, so the contrast check of Article XIV is made in one place | 1 | All stylesheets | daisyUI's tokens and Tailwind's opacity modifiers |
| Section label | `frame.css:134-142` (navigation caption), `page-toc.html:3`, `content.css:648-654` (toctree caption in a page), `layout-playground.css:7` | One CSS class | 2 | 4, 3 | Nothing |
| A path under `_static` or a full URL | `static_url` at `__init__.py:331-339`, used at `:347-348`; not used for `local` icon links at `:381-382` | A method on the options class | 5 | 10 | Sphinx's `pathto(…, 1)` and its handling of URLs in `html_logo` |
| The layout code's rules | `parse_layout` and `LAYOUT_SHAPE` at `__init__.py:109-153`; again in `layout-playground.js:9-39`; again as the field's `pattern` in `docs/configure/layout-code.md:42`; the header height at `__init__.py:112` and `frame.css:30` | Python is the one source. The playground reads the rules the build writes out, or both are tested against the same codes | 1 | The layout playground (docs) | Nothing |

17 pieces.

### Duplication to remove

- The search button template, three times (`search-button.html`, `search-field.html`,
  `search-button-field.html`).
- The site-navigation template, three times (`sidebar-nav.html`, `sidebar-nav-bs.html`,
  `sidebar/navigation.html`).
- Nine one-line templates that draw nothing.
- The branch toggle, written twice in Python and twice in CSS.
- The layout code's rules, in Python, in the playground's script and in an HTML `pattern`.
- The header's height, in Python (`HEADER_HEIGHT`, `__init__.py:112`) and in CSS
  (`--daisy-header-height`, `frame.css:30`, which nothing reads).
- Applying a mode, in the inline script (`layout.html:22-27`) and the page script
  (`sphinx-daisyui.js:20-28`).
- The `url` and `local` branches of `icon_links` (`__init__.py:379-382`), identical.
- `navbar-logo` included three times in `layout.html` (`:60`, `:75`, `:79`), and the
  `navbar_end` components rendered twice (`:67`, `:81`).
- The site toctree rendered twice per page (`__init__.py:485-486`) and parsed four times.
- The edit and source buttons in the secondary sidebar (`edit-this-page.html:2`,
  `sourcelink.html:2`), the same button with a different link. Feature 11 writes it once.
- The admonition icons as data URIs in `content.css:110-118`, a second copy of Lucide icons
  outside `icons.json`. The icon script writes them too.
- Theme options read through `daisy` in most templates and directly as `theme_*` in three.

### The look

Port means copy across and clean to `main`'s standards, never redraw. Every file that makes what
Sam approved, with the feature that ports it and where it lands in `main`:

| Prototype file | Ported by | Lands in `main` at |
|---|---|---|
| `src/sphinx_daisyui/theme/daisyui/layout.html` | 1, except: `:8-11` (14), `:13-29` (6), `:37-43` (9), `:82-90` (13), `:106-113` (11), `:116-121` (4), `:126-141` and `:169-171` (12), `:172` (7) | The same path |
| `theme/daisyui/theme.toml` | 1 starts it. Each feature adds its options | The same path |
| `components/copyright.html`, `sphinx-version.html`, `theme-version.html`, `last-updated.html` | 1 | `theme/daisyui/components/` |
| `components/navbar-logo.html` | 1 (title only), 5 (logos) | `theme/daisyui/components/` |
| `components/sidebar-nav.html`, `breadcrumbs.html` | 2 | `theme/daisyui/components/` |
| `components/page-toc.html` | 4 | `theme/daisyui/components/` |
| `components/theme-switcher.html` | 6 | `theme/daisyui/components/` |
| `components/search-button-field.html`, `search-button.html`, `search-field.html`, `search-modal.html` | 7 | `theme/daisyui/components/` |
| `components/version-switcher.html` | 8 | `theme/daisyui/components/` |
| `components/navbar-icon-links.html` | 10 | `theme/daisyui/components/` |
| `components/edit-this-page.html`, `sourcelink.html` | 11 | `theme/daisyui/components/` |
| `components/navbar-nav.html` | 13 | `theme/daisyui/components/` |
| `components/sidebar/*.html`, `sidebar/navigation.html` | 14 | `theme/daisyui/components/sidebar/` |
| `components/sidebar-nav-bs.html`, `sidebar-collapse.html`, `sidebar-ethical-ads.html` | 15 | `theme/daisyui/components/` |
| `static/scripts/sphinx-daisyui.js` | By section: `:1-8` and `:56-65` (1), `:10-54` (6), `:67-90` (2, with `:88-90` to 1), `:92-125` (4), `:127-154` (12), `:156-166` (9), `:168-180` and `:219-397` (7), `:182-217` (8) | `theme/daisyui/static/scripts/`, one module per feature |
| `assets/theme.css` | 1. Its `@source inline` list (`:8`) goes to 3 | `assets/theme.css`, which `main` already has |
| `assets/frame.css` | By section: `:1-4`, `:18-127`, `:301-308` (1), `:6-9` (5), `:11-16` (6), `:129-176` (2), `:178-201` (4), `:203-226` (7), `:228-296` (3), `:298-299` (14) | `assets/`, imported from `theme.css`, one file per area or one file, as the plan of feature 1 decides |
| `assets/content.css` | 3 | `assets/content.css` |
| `src/sphinx_daisyui/icons.json`, `scripts/icons.mjs` | 1 | The same paths |
| `src/sphinx_daisyui/__init__.py` | By function: `parse_layout`, the layout check in `on_builder_inited`, `template_names` and the option readers (1), `navigation_markup` (2), `rewrite_body` and the Pygments half of `on_builder_inited` (3), `page_toc` (4), `static_url` and `brand` (5), `DAISYUI_THEMES` (6), `icon_links`, `footer_icons`, `FONT_AWESOME`, `fa_icon` (10), `source_links` (11), `header_links` (13), `css_variables` (14) | `src/sphinx_daisyui/`, grouped in classes (Article IX) |
| `docs/_static/logo-light.svg`, `logo-dark.svg` | 5 | `docs/_static/` |
| `docs/_static/switcher.json` | 8 | `docs/_static/` |
| `docs/_static/layout-playground.css`, `layout-playground.js` | The layout playground (docs) | `docs/_static/` |
| `docs/conf.py` | 1 (the theme's own options and `DAISY_LAYOUT`), 14 (the Furo preset), 15 (the pydata-sphinx-theme preset) | `docs/conf.py` |

**Pages to compare side by side.** Each feature's merge is checked against the prototype on these
pages, at 390, 1100 and 1440 pixels wide, in light mode, and in dark mode where the row says so.
1100 is the width with no secondary sidebar, and 390 shows the drawer and the "On this page"
disclosure.

| Page | Address on the prototype | Build | State to open it in | Features |
|---|---|---|---|---|
| Home | http://localhost:8062/ | Own options | At the top, then scrolled (header line and shadow). Light and dark | 1, 5, 6, 10 |
| Home, drawer open | http://localhost:8062/ | Own options | 390 only, menu button pressed | 1, 2 |
| Typography | http://localhost:8062/kitchen-sink/typography.html | Own options | Scrolled to the middle, a heading marked in "On this page" | 3, 4, 11 |
| Admonitions | http://localhost:8062/kitchen-sink/admonitions.html | Own options | Light and dark | 3 |
| Code | http://localhost:8062/kitchen-sink/code.html | Own options | A block hovered (copy button), then the foot of the page, then scrolled back up (back to top). Light and dark | 3, 12 |
| Tables | http://localhost:8062/kitchen-sink/tables.html | Own options | As loaded | 3 |
| Lists | http://localhost:8062/kitchen-sink/lists.html | Own options | As loaded | 3 |
| Pictures and maths | http://localhost:8062/kitchen-sink/media.html | Own options | As loaded | 3 |
| sphinx-design | http://localhost:8062/kitchen-sink/design.html | Own options | Light and dark | 3 |
| API reference | http://localhost:8062/kitchen-sink/api.html | Own options | As loaded | 3 |
| Source code page | http://localhost:8062/_modules/palette.html | Own options | As loaded | 3 |
| Index | http://localhost:8062/genindex.html | Own options | As loaded | 3 |
| A toctree in a page | http://localhost:8062/kitchen-sink/deeper/index.html | Own options | As loaded | 2, 3 |
| A deep page | http://localhost:8062/kitchen-sink/deeper/deepest/leaf.html | Own options | As loaded, and with the drawer open at 390 | 2 |
| Theme menu | http://localhost:8062/ | Own options | Menu open, then the `dracula` theme picked | 6 |
| Search dialog | http://localhost:8062/ | Own options | Ctrl+K, "layout" typed, the second result chosen with the arrow keys | 7 |
| Full search page | http://localhost:8062/search.html?q=layout | Own options | As loaded | 7 |
| Version menu | http://localhost:8062/ | Own options | Menu open | 8 |
| Layout page | http://localhost:8062/configure/layout-code.html | Own options | Each recipe, and each of the playground's screen sizes | 1, the playground |
| Furo's layout | http://localhost:8062/layouts/lHh-LpR-lff/ | `layout = "lHh LpR lff"` | Home, and http://localhost:8062/layouts/lHh-LpR-lff/kitchen-sink/typography.html | 1, 5, 9 |
| pydata-sphinx-theme's layout | http://localhost:8062/layouts/hHh-LpR-fff/ | `layout = "hHh LpR fff"` | Home, scrolled to the foot | 1 |
| Nothing sticky | http://localhost:8062/layouts/hhh-lpr-fff/ | `layout = "hhh lpr fff"` | Home, scrolled | 1 |
| Tall secondary sidebar | http://localhost:8062/layouts/hHr-LpR-lfr/ | `layout = "hHr LpR lfr"` | http://localhost:8062/layouts/hHr-LpR-lfr/kitchen-sink/typography.html | 1, 4 |
| As Furo | http://localhost:8062/as-furo/ | Furo configuration | Home, and http://localhost:8062/as-furo/kitchen-sink/typography.html (view and edit buttons, footer icons). Light and dark | 9, 10, 11, 14 |
| As pydata-sphinx-theme | http://localhost:8062/as-pydata/ | pydata-sphinx-theme configuration | Home, http://localhost:8062/as-pydata/kitchen-sink/deeper/index.html (header links, one section in the sidebar), http://localhost:8062/as-pydata/kitchen-sink/typography.html (edit and source links in the secondary sidebar), and the drawer open at 390 (sections at its head) | 5, 8, 10, 11, 13, 15 |

### Which decisions bind which feature

Sam's decisions are listed under "Decisions" above, and the ones made without him under "Decided
on my own". They bind the features like this:

- **1. Page frame and layout code**: the layout code over named grid areas, default
  `hHh LpR lff`, the option named `layout`. The page column centred, with the sidebar columns
  taking the spare width. The logo moving to the head of the primary sidebar when it reaches the
  top, with no line under it. The header's line and Tailwind's `shadow-xs` appearing only once
  the page scrolls, switched at once with no fade. The brand in the navbar for every
  configuration. Article on `base-100`, primary sidebar on `base-200` in the drawer and clear
  beside the page. Icons as inline SVG, never an icon font.
- **2. Site navigation**: the default follows Furo, with the whole tree in the primary sidebar.
- **3. Page-body styles**: article-info items on one line. A thin space after a quotation's
  dash. Lists more compact, 4px between one-line items and wider only when an item holds several
  blocks. A toctree in a page drawn as the sidebar's menu, its first two levels open. The page
  named Admonitions, after the directive. Code highlighted from the tokens, with Pygments' own
  stylesheet dropped unless a Pygments style is set.
- **6. Modes and daisyUI themes**: all 35 daisyUI themes compiled in.
- **13. Header links**: putting `navbar-nav` in `navbar_center` switches to the sectioned
  layout.
- **14. Furo configurations**: Furo's sidebar brand and search templates are accepted and draw
  nothing.
- **The layout playground**: daisyUI's browser mock-up driven by a form, with recipes, a screen
  switch, centred colour-coded letter chips and a sentence per area. The field refuses a letter
  as it's typed with a sentence naming what that position takes, adds the spaces itself, and
  carries the same rule as an HTML `pattern`. A sticky sidebar in the mock-up sticks at once and
  keeps its top edge.

### What it replaces

Nothing on `main` beyond the scaffold, which the features extend rather than remove:

- `src/sphinx_daisyui/__init__.py`: `setup()` registering the theme. Feature 1 adds the event
  handlers beside it.
- `theme/daisyui/theme.toml`: inherits `basic` and links the stylesheet. Each feature adds its
  options.
- `assets/theme.css`: Tailwind and daisyUI with every theme. Feature 1 adds the imports.
- The documentation skeleton: `docs/index.md` (its "Features" list grows with each feature),
  `docs/developer/installation.md`, and `docs/reference/theme.md` (gains each feature's options).

Removing any of it costs nothing. There is no data and no released version.
