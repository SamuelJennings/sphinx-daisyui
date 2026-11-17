# ADR 0003 — Support the browsers that have CSS `@scope`

**Status:** accepted

## Decision

The page-body styles are scoped with `@scope (.daisy-sphinx-content) to (.daisy-sphinx-escape,
.toctree-wrapper)`. The theme supports the browsers that implement `@scope`: Chrome 118, Safari
17.4, Firefox 146 and later.

## Why

`@scope` keeps the page-body rules inside the article and stops them at raw HTML a site author
marks with the escape class, with no class added to every element Sphinx writes and no rule made
more specific to win. Every major browser engine has shipped it, Firefox last in December 2025.

## Revisit if

A site needs the page body drawn in a browser released before those versions.
