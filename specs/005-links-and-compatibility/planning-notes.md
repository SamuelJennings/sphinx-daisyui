# Planning notes: 005-links-and-compatibility

Notes for research and planning. Each is answered by name before the build starts.

## The prototype

This feature is built from the accepted prototype on the `prototype-theme` branch. Read
`PROTOTYPE.md` on that branch whole, then its features 10 (icon links), 11 (edit and view source
links), 14 (Furo configurations) and 15 (pydata-sphinx-theme configurations). The prototype is
served at http://localhost:8062/ while it is being compared. Its screens and the maintainer's
decisions in its "Decisions" section are agreed. "Which decisions bind which feature" binds
feature 14: Furo's sidebar brand and search templates are accepted and draw nothing.

## No design review at the plan stage

The prototype is the design. The plan goes straight to tasks with no separate design review.

## The look: ported, never redrawn

Port means copy across and clean to `main`'s standards. These rows of "The look" belong to this
feature:

| Prototype file | What this feature takes | Lands in `main` at |
|---|---|---|
| `components/navbar-icon-links.html` | All | `theme/daisyui/components/` |
| `components/edit-this-page.html`, `sourcelink.html` | All, written as one button (see below) | `theme/daisyui/components/` |
| `components/sidebar/*.html` | All eight, `sidebar/navigation.html` including the site navigation component | `theme/daisyui/components/sidebar/` |
| `components/sidebar-nav-bs.html`, `sidebar-collapse.html`, `sidebar-ethical-ads.html` | All three, `sidebar-nav-bs.html` including the site navigation component | `theme/daisyui/components/` |
| `theme/daisyui/layout.html` | `:8-11` (Furo's CSS variables, 14) and `:106-113` (edit and view buttons beside the breadcrumbs, 11), and the footer icons at `:158-163` | The same path |
| `assets/frame.css` | `:298-299` (Furo's brand-content override, 14) | `assets/`, in the file the page frame's plan chose |
| `src/sphinx_daisyui/__init__.py` | `icon_links`, `footer_icons`, `FONT_AWESOME`, `fa_icon` (10), `source_links` and the `top_buttons` and `use_edit_page_button` lines of `on_page_context` (11), `css_variables` (14) | `src/sphinx_daisyui/`, grouped in classes (Article IX) |
| `docs/conf.py` | The Furo preset and the pydata-sphinx-theme preset | `docs/conf.py` |
| `scripts/variants.sh` | The `/as-furo/` and `/as-pydata/` builds | `scripts/variants.sh`, which the page frame brings |
| `docs/get-started/from-furo.md`, `from-pydata.md` | Both guides | `docs/developer/`, under `main`'s documentation standard |

Each merge is checked side by side against the prototype on the pages in "Pages to compare side
by side" whose rows name features 10, 11, 14 or 15: Home, Typography, As Furo and As
pydata-sphinx-theme, at 390, 1100 and 1440 pixels wide, in light and dark where the row says so.

## The shared pieces

From "The shared pieces" in `PROTOTYPE.md`.

Built here:

- **Accepted names that draw nothing.** `sidebar-collapse.html`, `sidebar-ethical-ads.html`,
  `sidebar/brand.html`, `sidebar/ethical-ads.html`, `sidebar/rtd-versions.html`,
  `sidebar/scroll-end.html`, `sidebar/scroll-start.html`, `sidebar/search.html` and
  `sidebar/variant-selector.html` become one list of accepted names that resolve to an empty
  template. Built by the Furo configurations (14), reused by the pydata-sphinx-theme
  configurations (15), which add `prev-next`, `indices` and `searchbox` to the list (see
  `decisions.md`, D5). Check first: Jinja's `ignore missing` on the include, which already skips
  unknown names.
- **One edit and source button.** The edit and source buttons in the secondary sidebar
  (`edit-this-page.html:2`, `sourcelink.html:2`) are the same button with a different link.
  Edit and view source links (11) write it once. The buttons beside the breadcrumbs
  (`layout.html:106-113`) are the square icon button the page frame builds.

Reused here:

- **A path under `_static` or a full URL.** Built by the page frame (#4, for the logo). Icon links
  (10) use it for `local` icon links, which the prototype left unresolved.
- **The site-navigation component under three names.** Built by site navigation (#5).
  `sidebar/navigation.html` (14) and `sidebar-nav-bs.html` (15) include it.
- **The search button under three names.** Built by the search dialog (#7). The pydata-sphinx-theme
  configurations (15) rely on its `search-button`, `search-field` and `search-button-field` names.
- **Square icon button.** Built by the page frame (#4). Icon links and the edit and view buttons
  use it.
- **Icons.** Built by the page frame (#4). `FONT_AWESOME` and `fa_icon` map onto its names, and
  any icon this feature needs that the bundle lacks is added through its build script.
- **Component list placement.** Built by the page frame (#4). Every component here is placed
  through it.
- **The mode attributes.** Built by modes (#7). Furo's CSS variables key on them, as the
  prototype's `css_variables` does with `data-mode`.

## What the prototype faked that this feature does properly

From "Faked or skipped" in `PROTOTYPE.md`:

- **`<img>` tags built with an f-string.** The `url` and `local` icon links build an `<img>` tag
  from the option text with an f-string (`__init__.py:380`, `:382`). Build it with `markupsafe`
  (Article V, FR-006). The two branches are identical in the prototype and become one.
- **`local` icon links not resolved against `_static`.** Resolve them with the page frame's
  static-path method (FR-004).
- **`light_css_variables` mapping only the main Furo names.** Eight of Furo's 107 variables are
  mapped. Map every one with a daisyUI counterpart (FR-018). The variable names are in
  `research.md`.
- **`analytics`, `shorten_urls` and `surface_warnings` doing nothing.** Accepted and ignored is
  allowed, and the reference says so for each (FR-022, `decisions.md` D9).
- **Values printed without escaping.** Every value this feature prints is escaped per amended
  Article V, including `icon_links_label`, which the prototype reads directly as
  `theme_icon_links_label` (`navbar-icon-links.html:2`). The footer icons' own markup is the one
  exception, and needs Article V to name it (`decisions.md` D3).
- **Fixed text not translatable.** "Edit this page", "Show source" and the buttons' labels are
  marked for translation in the message catalogue the page frame sets up (FR-023).
- **A CSS variable value written straight into a `<style>` element.** The prototype writes the
  name and value as given. A value holding `</style>` or `}` could end the rule (FR-019).

## Differences from the prototype that research confirms

Found while specifying, by reading the two themes' 0.24 and 2025.12 wheels:

- **The Bitbucket edit address.** pydata-sphinx-theme builds
  `…/src/{version}/{doc_path}{file}?mode=edit`. The prototype builds `…/src/{version}/…` with no
  `?mode=edit`, which opens the file rather than the editor.
- **The GitLab and Bitbucket view addresses.** The prototype builds `…/blob/…` for all three
  hosts. GitLab's is `…/-/blob/…` and Bitbucket's is `…/src/…`. Check each host's address form.
- **Furo's view address.** Furo's `view-this-page` builds a GitHub view link with `?plain=true`
  on Read the Docs, and otherwise takes it from sphinx-basic-ng's `determine_page_view_link`.
  Read that macro and match its addresses for `source_repository`.
- **`edit-this-page` and `use_edit_page_button`.** See `decisions.md` D4.
- **pydata-sphinx-theme's provider name.** Its edit link reads "Edit on GitHub", naming the host.
  The spec asks that the link names the host it leads to (US2, scenario 5).

## The documentation

The two switching guides move into `docs/developer/` under `main`'s documentation standard, as
how-to pages. The options this feature adds go into `docs/reference/theme.md`. The links from the
guides to the `/as-furo/` and `/as-pydata/` builds are written from the site root in the
prototype, which only works on the development server. Fixing those links belongs to the
documentation-site work, so the guides link to the builds the same way the rest of the
documentation does once that work lands.
