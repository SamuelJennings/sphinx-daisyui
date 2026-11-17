# Research: 005-links-and-compatibility

## Assumptions checked

Run on 2026-11-17 against the published wheels of Furo 2025.12.19 and pydata-sphinx-theme 0.24.0,
and the `prototype-theme` branch.

- **The prototype declares every option both themes declare.** Every `[options]` key in Furo's
  `theme.conf` (14 keys) and pydata-sphinx-theme's (50 keys) is in the prototype's `theme.toml`.
  FR-016 and FR-020 are a port, not new work.
- **Furo's `html_sidebars` names match the prototype's templates.** Furo ships
  `sidebar/brand.html`, `ethical-ads.html`, `navigation.html`, `rtd-versions.html`,
  `scroll-end.html`, `scroll-start.html`, `search.html` and `variant-selector.html`. The prototype
  has all eight.
- **pydata-sphinx-theme ships four component names the prototype lacks.** Its `components/` holds
  `icon-links.html`, `indices.html`, `prev-next.html` and `searchbox.html`, with no template of
  the same name in the prototype. A configuration naming them builds today, because the
  component include skips unknown names, but draws nothing for `icon-links`. Decided in
  `decisions.md`, D5.
- **pydata-sphinx-theme's `edit-this-page` draws only with `use_edit_page_button` on.** Its
  template tests `theme_use_edit_page_button==true`. The prototype draws it whenever an address
  exists. Decided in `decisions.md`, D4.
- **pydata-sphinx-theme's edit address.** `edit_this_page.py` reads `edit_page_url_template`
  first, then Bitbucket, GitHub and GitLab, each with a self-hosted `*_url` override defaulting to
  the public host, and raises `ExtensionError` when none is complete. Bitbucket's address ends
  `?mode=edit`, GitLab's uses `/-/edit/`. The prototype handles neither the template nor the
  self-hosted hosts, and drops `?mode=edit`.
- **Furo's CSS variables.** Furo's stylesheet sets 107 variables: 104 `--color-*` and three
  `--font-stack*`. The prototype maps eight. The full list is in Furo's `furo.css`, the source
  for FR-018's mapping.
- **Furo's `footer_icons` `html` is raw SVG.** Furo's own documentation and the prototype's Furo
  preset pass an `<svg>` element as a string. Printing it escaped would show the markup as text.
  Decided in `decisions.md`, D3.
- **The surfaces this feature extends are not on `main` yet.** Component lists, the icon set, the
  square icon button, the message catalogue and the static-path method come with the page frame
  (#4, draft pull request 12). Nothing in this feature can be run on `main` until it merges, which
  is why the issue depends on #4 to #7.
