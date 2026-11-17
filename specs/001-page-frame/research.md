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
