# ADR 0004 — Search with Sphinx's own search functions

**Status:** accepted

## Decision

The search dialog finds its results by calling `Search._parseQuery` and `Search._performSearch`
from Sphinx's `searchtools.js`, which it loads with `language_data.js` and `searchindex.js` the
first time it opens. The theme has no matching or ranking code of its own. It only draws the
results Sphinx returns.

## Why

The dialog and Sphinx's full search page must find the same pages for the same words, in the
site's `language`. Sphinx's query parsing uses the stemmer and stop words it writes for that
language, and its search combines titles, index entries, API objects and the page text with its
own scores. A second matcher would drift from the full search page and could only ever cover
the languages it was written for. The two functions take and return the same values on every
supported Sphinx version, 7.4 to 9.2.

## Revisit if

A Sphinx release changes or removes either function, or Sphinx publishes a supported interface
for running a search without drawing the full search page.
