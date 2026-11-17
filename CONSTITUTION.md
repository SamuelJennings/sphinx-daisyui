# sphinx-daisyui Constitution

The rules every change to this repository follows. The words in it are defined in
[`CONTEXT.md`](CONTEXT.md).

## Core articles

### Article I — Testing
Every change follows [`docs/contributing/standards/testing.md`](docs/contributing/standards/testing.md): what gets a test
and what does not, the test-first cycle, test structure and fixtures, and the coverage floors.

### Article II — Simplicity
Start with the simplest design that satisfies the specification. New dependencies, new
abstractions and new infrastructure each need a stated reason in the plan or the pull request.
No speculative generality.

### Article III — Anti-Abstraction
No wrapper layers, base classes or "future-proofing" indirection without a present, concrete
second use. Prefer duplication over the wrong abstraction. A second use also counts as present
when it is in another approved specification built in the same batch, such as several features
specified together from one prototype.

### Article IV — Integration-First
The theme's contract is what a site author writes in `conf.py` and what the build writes out.
Tests build a real site through `sphinx.testing` and check the pages it produces, the way a site
author and a reader meet them.

### Article V — Security & data-safety
Sphinx's template environment does not autoescape, so escaping is written out.

- A template escapes every value it prints from a theme option, `html_context` or the page
  context with `|e`. The exception is markup Sphinx itself produced, such as `body` or `toc`.
- Python that builds markup from option text escapes it with `markupsafe.escape`, never an
  f-string.
- An announcement is the site author's own HTML, as in Furo and pydata-sphinx-theme, and is
  printed as markup. That includes one fetched from a URL the site author names.
- The page script inserts page and search-index text with `textContent`, never by assigning
  HTML built from it.
- Secrets live in runtime configuration, never in code, test sites or version control.

### Article VI — Documentation
Public API changes ship their docs in the same pull request: README and CHANGELOG updated.
Docstrings and code comments follow
[`docs/contributing/standards/code-documentation.md`](docs/contributing/standards/code-documentation.md). The pages
under `docs/` and the README's quickstart follow
[`docs/contributing/standards/documentation.md`](docs/contributing/standards/documentation.md), and the
documentation builds clean with warnings as errors. The README follows the package README
standard, including its badge row and a *Scope & philosophy* section.

### Article VII — Dependency discipline
A new runtime dependency, Python or npm, needs a stated reason. `deptry` must pass: no unused,
missing or transitively relied-upon dependencies. npm packages are build tools only and never
reach a site.

### Article VIII — Internationalization
Fixed text the theme writes into a page, such as "On this page" or "Previous", is marked for
translation with Sphinx's message catalogue (`_()` in templates), so a site's `language` setting
applies to it. Text from the site's own configuration and pages is never translated by the theme.

### Article IX — Cohesion (Python)
Related behaviour is grouped in a class, not scattered across module-level functions.

**The test:** two or more module-level functions that share a *subject* belong on a class. They
share a subject when they operate on the same data, take the same first argument, are only
meaningful in sequence, or are named around the same noun (`build_x`, `validate_x`, `render_x`).

**Why.** In a published package a class is the extension point. A site that needs different
behaviour subclasses it and overrides one method. A module of functions can only be
monkey-patched, which is not a supported interface.

**Sphinx first.** Where Sphinx already owns the grouping, use it rather than inventing a class:
an event handler connected in `setup()` for work done at a stage of the build, a template or
component for markup.

**Exceptions**, stated rather than assumed: a standalone pure function with no siblings, the
module-level `setup()` Sphinx requires, `conftest.py` fixtures, and a module of independent
utilities that genuinely share no subject.

**This does not license abstraction.** Article III still holds.

## Project articles

### Article X — Another theme's configuration builds unchanged
A theme option, `html_sidebars` template name or component name that Furo or
pydata-sphinx-theme defines is accepted under the same name, with the same type and meaning.
An option the theme can't honour yet is accepted and ignored, never an error. When an option of
this theme's own and a borrowed option would set the same thing, the borrowed option keeps its
meaning. A change that makes a configuration which built before warn or fail is a breaking
change.

### Article XI — Every colour is a daisyUI token
Stylesheets and templates name colours only through daisyUI's tokens (`base-100`, `primary`,
`base-content` and the rest) and Tailwind utilities built on them. No hard-coded colour value,
so every daisyUI theme works, in light and dark. This includes code highlighting and the
variables of extensions the theme styles, such as sphinx-design's. A site may choose colours of
its own, such as a Pygments style or Furo's CSS variables, and the theme applies them as given.

### Article XII — No Node for users
The compiled stylesheet ships in the wheel and the sdist. Installing or using the theme never
runs npm, and a site changes the look through daisyUI's CSS variables in its own static files.
The theme loads nothing from another host: its stylesheet, script and icons are in the package.

### Article XIII — Styles, never new markup to write
The theme styles the HTML that Sphinx and the extensions it supports already write. It adds no
directive or role. Raw HTML inside an element with the escape class keeps daisyUI's own look and
is never restyled by the page-body styles.

### Article XIV — Accessible by default
Everything the theme adds to a page can be reached and used with the keyboard, carries a visible
focus state, and names its landmarks and controls for a screen reader. Text the theme dims still
meets WCAG 2.2 AA contrast on daisyUI's default light and dark themes.

### Article XV — Compatibility and stack
- Python 3.11 or later, Sphinx 7.4 or later. Every supported Sphinx minor version is tested in
  CI. Dropping a Python or Sphinx version is a minor release, recorded in `CHANGELOG.md`.
- uv-managed, built with hatchling. The stylesheet is compiled from `assets/` by Tailwind CSS 4
  and daisyUI 5 with npm during the build. Tests use pytest with `sphinx.testing`.
- Semantic versioning. Theme options, template and component names, and CSS classes documented
  for a site to use do not change without a major version, and a deprecated option warns for at
  least one minor version before it is removed. Below 1.0.0 that deprecation window is advisory,
  because there is no stable surface yet.

## Articles not adopted

- Data-model conventions (Django), and the Django standards page: this package has no models and
  does not use Django.

## Quality bar

Read at plan and review. Applies to every change.

- Test coverage meets the floors in `docs/contributing/standards/testing.md` (`codecov.yml` is
  the reference).
- Every public API change updates README and CHANGELOG in the same pull request.
- Lint, type-check (`mypy`) and `deptry` pass.
- The package builds with its stylesheet inside, its metadata is valid, the README renders on
  PyPI with absolute links, and the public API honours the deprecation policy in Article XV.

## Non-negotiables

- Tests, build and lint pass before a change merges. Nobody overrides a red check.
- The default branch requires one approval, and the author of a change never approves it.

---

**Version**: 1.1.0 | **Ratified**: 2026-11-17 | **Last Amended**: 2026-11-17
