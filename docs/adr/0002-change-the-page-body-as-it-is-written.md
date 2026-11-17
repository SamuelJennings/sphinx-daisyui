# ADR 0002 — Change the page body while Sphinx writes it

**Status:** accepted

## Decision

What the theme adds to a page body (the scroll regions round tables and display equations, the
names of heading links, the attribution's space, the admonition icons and a toctree drawn as the
site navigation's menu) is written by `PageBodyTranslator`, a mixin over the HTML translator. At
`builder-inited` the theme builds a class from the mixin and the translator registered for the
builder, or the builder's default, and sets it with `app.set_translator(..., override=True)`. It
never parses the HTML Sphinx has written.

## Why

The admonition titles, the heading links and a resolved toctree in a page exist only while the
page is written: Sphinx adds an admonition's title and writes a permalink inside the translator,
and resolves a page's toctrees after the `doctree-resolved` event. Parsing the written HTML would
need an HTML parser at run time, which ADR 0001 keeps out, and would read every page twice.
Keeping the registered translator as the base keeps another extension's translator working, as
pydata-sphinx-theme does with its own mixin.

## Revisit if

Sphinx changes how a builder's translator is chosen, or stops writing admonition titles, permalinks
or resolved toctrees through the translator's visitors.
