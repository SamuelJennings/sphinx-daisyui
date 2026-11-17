# Plan: Icon and source links

**Inputs**: `spec.md`, `research.md`, `planning-notes.md`, `decisions.md`, and the accepted
prototype on `prototype-theme` (`PROTOTYPE.md`, features 10 and 11).

## Approach

Three components, the Python that reads their options into the `daisy` context, and one change
to the layout. The look is the prototype's, ported: its templates are copied across and cleaned
to `main`'s standards. Everything the prototype faked is done properly here.

### Icon links (US1)

- **`src/sphinx_daisyui/links.py`** holds `IconLink` (a frozen dataclass: `name`, `url`, `image`,
  the markup drawn inside the link) and `IconLinks`, read from `ThemeOptions`:
  - `IconLinks.from_options(options, pathto)` returns the links to draw. An entry with no `url`
    is left out. A missing `name` gives the address as the name. With no `type`, `image` is
    `ICONS.svg(icon)`. With `type` `url` or `local`, `image` is one `<img alt="">` built with
    `Markup(...).format(...)`, whose address is `options.static_url(icon, pathto)` for `local`
    and the address as given for `url`.
  - `IconLinks.problems(options)` returns the warning text for an `icon_links` given as a string
    (naming the option) and for each entry whose bundled `icon` is unknown (naming the entry and
    the icon).
  - `check_icon_links(app)`, connected to `builder-inited` beside `check_modes`, logs each
    problem once with `type="daisyui"`, `subtype="icon_links"`.
- `theme.toml` gains `icon_links = []` and `icon_links_label = ""`. The page context gains
  `daisy.icon_links` and `daisy.icon_links_label` (the option's text, empty when unset).
- **`icon_button`** in `components/macros.html` gains `href=""` and `tooltip_class=""`. With an
  address it draws an `<a href>` with the same classes, otherwise the `<button>` it draws today.
  `tooltip_class` adds a daisyUI placement class such as `tooltip-bottom`, written out in full so
  Tailwind finds it. Called with `{% call %}`, the caller's markup replaces the named icon, which
  is how an icon link carries its image and the edit and view buttons their smaller icon. The
  search dialog's close button keeps the same output.
- **`components/navbar-icon-links.html`** is ported: a `<ul>` named by
  `daisy.icon_links_label or _("Icon links")`, one `<li>` per link, each an `icon_button` link
  with `tooltip-bottom`, and nothing when there are no links.

### Source links (US2, US3)

- **`SourceHost`** in `links.py` is a frozen dataclass of one host's edit and view address
  forms, with `HOSTS` keyed by `github.com`, `gitlab.com` and `bitbucket.org` (the table in
  `research.md`). `SourceHost.for_repository(address)` reads the host with `urlsplit`,
  lowercased and without `www.`, and returns `None` for any other.
- **`SourceLinks`**, a frozen dataclass of `edit`, `view` and `source`, each empty when unknown:
  - `SourceLinks.from_options(options, context)` reads `source_repository` (trailing slash and
    `.git` dropped), `source_branch` (default `main`) and `source_directory` (slashes trimmed),
    and builds the page's path from `pagename` and `page_source_suffix`. A page with no
    `sourcename` gets no links, and a repository on no known host no edit or view link. `source`
    is `pathto("_sources/" + sourcename, 1)` when `show_source` and `has_source` are both true.
  - `SourceLinks.buttons(names)` returns the names from `top_of_page_buttons` (`edit`, `view`)
    whose address exists, in the order given.
- `theme.toml` gains `source_repository = ""`, `source_branch = ""`, `source_directory = ""` and
  `top_of_page_buttons = ["edit"]`, read with `options.names`. The page context gains
  `daisy.sources` and `daisy.top_buttons`. On an index or search page both are empty.
- **`layout.html`**: the article header is drawn when `article_header_start`, `article_header_end`
  or `top_buttons` has anything, and the buttons follow `article_header_end` in its right-hand
  group, ported from the prototype's `layout.html:106-113`: each an `icon_button` link with
  `tooltip-left` and a `size-4` icon, labelled "Edit this page" or "View this page's source".
- **`source_link(href, icon, label, rel="")`** joins `components/macros.html`: the ghost link
  with an icon and its text, ported from the prototype's `edit-this-page.html:2`.
  **`components/edit-this-page.html`** draws it with `daisy.sources.edit`, the `pencil` icon and
  "Edit this page", and **`components/sourcelink.html`** with `daisy.sources.source`,
  `file-code`, "Show source" and `rel="nofollow"`. Each draws nothing without its address.
- Every fixed text is `_()` and joins `locale/sphinx.pot` through `scripts/messages.sh`.

### Escaping (Article V)

Templates print every name, address and label with `|e`. The only markup built in Python is the
`<img>` of an image icon link, through `Markup.format`, and the bundled SVG, as today.

### The documentation

- `docs/reference/options.md`: an "Icon links" section (`icon_links`, `icon_links_label`, with
  the list of bundled icon names) and a "Source links" section (`source_repository`,
  `source_branch`, `source_directory`, `top_of_page_buttons`).
- `docs/reference/components.md`: `navbar-icon-links`, `edit-this-page`, `sourcelink`, and the
  macros list updated for `icon_button`'s address and `source_link`.
- `docs/developer/link-the-sources.md`, a how-to: link the repository and other accounts as
  icons, in the navbar and the footer, and set up the edit and view buttons and links.
- `docs/conf.py` ported from the prototype's main build: `icon_links` for GitHub and PyPI,
  `source_repository`, `source_branch`, `source_directory`, `top_of_page_buttons: ["edit"]` and
  `secondary_sidebar_items: ["page-toc", "sourcelink"]`. Two environment switches, as
  `DAISY_LAYOUT` already does, build the variants the look comparison needs:
  `DAISY_SOURCE_SIDEBAR` places `edit-this-page` and `sourcelink` in the secondary sidebar, and
  `DAISY_FOOTER_ICONS` places `navbar-icon-links` in `footer_end`.
- CHANGELOG under Unreleased.

## Tests

Test-first, per `docs/contributing/standards/testing.md`. No test of wording, icons, classes
chosen for looks or layout.

- `tests/test_links.py`: `IconLinks` and `SourceLinks` read directly from `ThemeOptions`, with
  each host, branch, directory and suffix case, and the warnings.
- `tests/test_templates/test_icon_links.py` and `tests/test_templates/test_source_links.py`
  against a test site `tests/roots/test-links/` with a page three folders deep and a `.txt` page
  (a second suffix that needs no extension), for the built addresses, names, placement, escaping
  and absence.
- The translation test gains the new messages in the one catalogue fixture.
- In headless Chrome, the keyboard walk for SC-003 and the look comparison for SC-004.

## Cost

Three dispatches on Sonnet, one per story. Expected well under the soft budget.
