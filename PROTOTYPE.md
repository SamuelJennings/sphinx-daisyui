# sphinx-daisyui prototype

The record of the prototype on branch `prototype-theme`. Until the repository is on GitHub, this
file is the record that would otherwise be its issue.

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
- Icons are inline SVG (Lucide, ISC; Simple Icons, CC0), never an icon font.

## Faked or skipped

- A layout code of the wrong shape stops the build with a clear message, but Sphinx prints it
  inside a traceback, because the check runs in an event handler.

- No tests. No accessibility audit beyond keyboard paths and named regions.
- The search ranking is a light stemmer and prefix matcher, not Sphinx's Porter stemmer, and
  isn't language-aware.
- `analytics`, `show_version_warning_banner`, `sticky_banners`, `check_switcher`,
  `shorten_urls`, `surface_warnings` and `search_as_you_type` are accepted and do nothing.
  `navbar_align` is only partly honoured.
- The theme's own text ("On this page", "Previous") isn't translatable yet.
- The `theme-version` footer line links to a repository that doesn't exist yet.
- `light_css_variables` only maps the main Furo variable names. The rest are set as written.
- The navbar and drawer each render the `navbar_end` components, so a phone build carries the
  theme picker twice in the HTML.

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
- 2026-11-17 Sam: prototype accepted ("ready to get this show on the road"). Next: onboard the
  repository, then build `main` from this branch through the full lanes.
