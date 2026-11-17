# Research: 004-reader-tools

Started at specification. The full research is written before the plan.

## Assumptions checked

- **Sphinx writes the search index and language support the dialog reads.** On Sphinx 9.2 (the
  repository's environment), `basic/static/` ships `searchtools.js`, `language_data.js.jinja`
  (stop words and the stemmer for the site's `language`) and `documentation_options.js.jinja`.
  `searchtools.js` exposes `Search.setIndex`, `Search._parseQuery`, `Search.query`,
  `Search.performObjectSearch` and `Search.performTermsSearch`, and the index carries
  `alltitles`, `titleterms` and `objnames`. Holds. Not yet checked on Sphinx 7.4, the oldest
  supported version: research checks each supported version before the plan relies on calling
  `Search` directly.
- **pydata-sphinx-theme defines the borrowed names with these defaults.** Its `theme.conf` on its
  main branch declares `search_bar_text = Search the docs ...`, `disable_search = False`,
  `search_as_you_type = False`, `switcher =`, `check_switcher = True`,
  `show_version_warning_banner = False`, and `navbar_end = theme-switcher, navbar-icon-links`,
  `navbar_persistent = search-button-field`. Holds, with `search_as_you_type`'s default
  differing on purpose (`decisions.md`, 2).
- **The page frame this feature extends.** Not yet on `main`: FS-001 (#4) is approved on its draft
  pull request. Its specification provides the component lists, the square icon button, the options
  class, the icon set, the message catalogue, the keyboard helper and the `<body>` attributes this
  feature uses. Checked against its approved `spec.md` and `planning-notes.md`.
