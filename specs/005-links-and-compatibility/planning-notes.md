# Planning notes: 005-links-and-compatibility

Notes for research and planning. Each is answered by name before the build starts.

## The prototype

This feature is built from the accepted prototype on the `prototype-theme` branch. Read
`PROTOTYPE.md` on that branch whole, then its features 10 (icon links) and 11 (edit and view
source links). The prototype is served at http://localhost:8062/ while it is being compared. Its
screens are agreed. Its option handling is not: the theme has its own options, with one name and
one shape each, so the prototype's handling of Furo's and pydata-sphinx-theme's shapes is left
behind (`decisions.md`, D1, D3, D6).

## No design review at the plan stage

The prototype is the design. The plan goes straight to tasks with no separate design review.

## The look: ported, never redrawn

Port means copy across and clean to `main`'s standards. These rows of "The look" belong to this
feature:

| Prototype file | What this feature takes | Lands in `main` at |
|---|---|---|
| `components/navbar-icon-links.html` | All, reading the label from the page context instead of `theme_icon_links_label` | `theme/daisyui/components/` |
| `components/edit-this-page.html`, `sourcelink.html` | Both, written as one button (see below) | `theme/daisyui/components/` |
| `theme/daisyui/layout.html` | `:106-113`, the edit and view buttons beside the breadcrumbs | The same path |
| `src/sphinx_daisyui/__init__.py` | `icon_links` without the service shortcuts and Font Awesome names (10), `source_links` from `source_repository` only, and the `top_buttons` line of `on_page_context` (11) | `src/sphinx_daisyui/`, grouped in classes (Article IX) |
| `docs/conf.py` | The theme's own `icon_links`, `source_*` and `top_of_page_buttons` values | `docs/conf.py` |

`FONT_AWESOME`, `fa_icon`, `footer_icons`, `css_variables`, the Furo and pydata-sphinx-theme
presets, their builds in `variants.sh`, the switching guides, `components/sidebar/*.html`,
`sidebar-nav-bs.html`, `sidebar-collapse.html` and `sidebar-ethical-ads.html` are not ported.

Each merge is checked side by side against the prototype on the Home and Typography rows of
"Pages to compare side by side", at 390, 1100 and 1440 pixels wide, in light and dark where the
row says so.

## The shared pieces

From "The shared pieces" in `PROTOTYPE.md`.

Built here:

- **One edit and source button.** The edit and source links in the secondary sidebar
  (`edit-this-page.html:2`, `sourcelink.html:2`) are the same button with a different link. Write
  it once. The buttons beside the breadcrumbs (`layout.html:106-113`) are the square icon button
  the page frame builds.

Reused here:

- **A path under `_static` or a full URL.** Built by the page frame (#4, for the logo). Icon links
  use it for `local` entries, which the prototype left unresolved.
- **Square icon button.** Built by the page frame (#4). Icon links and the edit and view buttons
  use it.
- **Icons.** Built by the page frame (#4). `icon_links` names its icons. An icon this feature's
  documentation lists that the bundle lacks is added through its build script.
- **Component list placement.** Built by the page frame (#4). The three components are placed
  through it.

## The component-list defaults

The page frame (FS-001) sets the component lists' defaults to the prototype's `theme.toml`
values. `navbar_end` lists `navbar-icon-links`, and `secondary_sidebar_items` is `page-toc` alone,
so a site places `edit-this-page` and `sourcelink` itself.

## What the prototype faked that this feature does properly

From "Faked or skipped" in `PROTOTYPE.md`:

- **`<img>` tags built with an f-string.** The `url` and `local` icon links build an `<img>` tag
  from the option text with an f-string (`__init__.py:380`, `:382`). Build it with `markupsafe`
  (Article V, FR-005). The two branches are identical in the prototype and become one.
- **`local` icon links not resolved against `_static`.** Resolve them with the page frame's
  static-path method (FR-004).
- **Values printed without escaping.** Every value this feature prints is escaped per amended
  Article V, including `icon_links_label`, which the prototype reads directly
  (`navbar-icon-links.html:2`).
- **Fixed text not translatable.** "Edit this page", "Show source", the buttons' labels and the
  icon list's default name are marked for translation in the message catalogue the page frame sets
  up (FR-014).

## Differences from the prototype

- **The addresses per host.** The prototype builds `…/edit/{branch}/…` and `…/blob/{branch}/…`
  for every repository. GitLab's are `…/-/edit/…` and `…/-/blob/…`. Bitbucket's are
  `…/src/{branch}/…?mode=edit` and `…/src/{branch}/…`. Research confirms each host's current form.
- **An empty `top_of_page_buttons`.** The prototype fell back to `top_of_page_button` and drew the
  edit button. Here an empty list shows none, and there is no `top_of_page_button`.
- **An unknown icon name.** The prototype drew the generic icon silently. Here it warns
  (`decisions.md`, D4).

## The documentation

The options and components this feature adds go into `docs/reference/theme.md`, with the list of
bundled icon names. A how-to page in `docs/developer/` shows linking the repository as an icon and
setting up edit links.
