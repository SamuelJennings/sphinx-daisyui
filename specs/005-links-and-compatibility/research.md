# Research: 005-links-and-compatibility

## Assumptions checked

Run on 2026-11-17 against the `prototype-theme` branch.

- **The prototype's source links assume GitHub's address form for every host.** `source_links`
  builds `{repo}/edit/{branch}/{path}` and `{repo}/blob/{branch}/{path}` from `source_repository`
  whatever the host. GitLab and Bitbucket use other forms, so FR-008 is new work, not a port.
- **The prototype's `url` and `local` icon links are identical** and build an `<img>` tag with an
  f-string, with the `local` path not resolved against `_static`.

## Against `main` after FS-001 to FS-004

Read again on 2026-11-17, after FS-004 merged. Nothing delivered since this specification was
written changes one of its scenarios. FS-004 placed `version-switcher` and `theme-switcher` before
`navbar-icon-links` in `navbar_end`, which is where the prototype has them.

### What the frame already gives

- `ThemeOptions` in `options.py` reads every shape this feature needs: `text`, `names` (a list,
  tuple or comma-separated string, trimmed, each once) and `static_url(path, pathto)`, which
  resolves a full address, a path starting `_static/` or a path under `_static` from any page.
  `records` reads a list of dicts but drops a string silently, which is why the check for a
  string `icon_links` reads the raw value.
- `Icons` in `icons.py`: `ICONS.by_name` and `ICONS.svg(name, classes)`, which draws the `link`
  icon for an unknown name. Every icon the prototype's set and this feature's buttons use is in
  `icons.json`, `pencil` and `file-code` included.
- `components/macros.html`: `components(names)` and `icon_button(label, icon, tooltip, data)`,
  which draws a `<button>`. The edit and view buttons and the icon links are links, so the macro
  gains an address and draws an `<a>` when it has one.
- `events.add_page_context` builds the one `daisy` dict, and `check_layout` and `check_modes`
  show how a `builder-inited` check reads the options once and warns.
- Sphinx's page context gives `sourcename` (empty on generated pages), `page_source_suffix`,
  `show_source` (`html_show_sourcelink`) and `has_source` (`html_copy_source`), and the basic
  theme's own `sourcelink.html` links `pathto('_sources/' + sourcename, true)`.

### The address forms per host

Checked against each host's own pages and pydata-sphinx-theme's
`edit_this_page.py`, which builds the same three:

| Host | Edit | View |
|---|---|---|
| `github.com` | `{repo}/edit/{branch}/{path}` | `{repo}/blob/{branch}/{path}` |
| `gitlab.com` | `{repo}/-/edit/{branch}/{path}` | `{repo}/-/blob/{branch}/{path}` |
| `bitbucket.org` | `{repo}/src/{branch}/{path}?mode=edit` | `{repo}/src/{branch}/{path}` |

`{repo}` is `source_repository` without a trailing slash or `.git`, and `{path}` is
`source_directory`, trimmed of slashes, joined to the page's name and its own suffix.

## What already exists

- Reading the options: this repo, `ThemeOptions` (`text`, `names`, `static_url`).
- Drawing a bundled icon and falling back to `link`: this repo, `ICONS.svg`.
- An image's address from any page: this repo, `ThemeOptions.static_url`.
- `<img>` markup from option text: an installed package, `markupsafe.Markup.format`, which
  escapes its arguments.
- The square icon button: this repo, `icon_button` in `components/macros.html`, extended with an
  address and a tooltip side.
- The sidebar link for edit and source: new code, one macro `source_link` in
  `components/macros.html`, used by `edit-this-page.html` and `sourcelink.html`.
- A host's edit and view addresses: new code, `SourceHost` and `SourceLinks` in `links.py`.
  pydata-sphinx-theme has the same table, but the theme takes no other theme as a dependency.
- The address of Sphinx's copy of the source: Sphinx, `pathto('_sources/' + sourcename, 1)`.
- Splitting the host from the address: the standard library, `urllib.parse.urlsplit`.
- Warning once at build start: this repo's pattern, a `builder-inited` handler as `check_modes`.
- Translated text: Sphinx, `_()` in templates and the theme's catalogue.

## The planning notes, answered

- **The prototype**: adopted. Features 10 and 11 are the agreed screens. Its option handling for
  Furo's and pydata-sphinx-theme's shapes is left behind, per the ruling that the theme has its
  own options.
- **No design review at the plan stage**: adopted.
- **The look: ported, never redrawn**: adopted. `navbar-icon-links.html`, `edit-this-page.html`,
  `sourcelink.html` and `layout.html:106-113` are copied across and cleaned. The options reference
  lives in `docs/reference/options.md` and the components in `docs/reference/components.md`
  since FS-001 split the reference, so those are where the documentation goes rather than
  `docs/reference/theme.md`.
- **One edit and source button**: adopted, as the `source_link` macro.
- **A path under `_static` or a full URL**: adopted, `ThemeOptions.static_url` for `local`
  entries.
- **Square icon button**: adopted, extended to draw a link (see above).
- **Icons**: adopted. Every icon the documentation lists is already bundled, so no icon is added.
- **Component list placement**: adopted, nothing new.
- **The component-list defaults**: adopted. `navbar_end` already lists `navbar-icon-links`.
- **What the prototype faked**: adopted, each item: `<img>` built with `markupsafe`, one branch
  for `url` and `local`, `local` resolved against `_static`, every value escaped, fixed text
  translated.
- **Differences from the prototype**: adopted, each item: the address forms in the table above,
  an empty `top_of_page_buttons` shows none, an unknown icon name warns.
- **The documentation**: adopted, in the two reference pages named above and a how-to,
  `docs/developer/link-the-sources.md`.
