# ADR 0001 — Read Sphinx's toctrees as document nodes

**Status:** accepted

## Decision

The theme reads the site's toctrees with Sphinx's `global_toctree_for_doc` and a page's headings
with `document_toc`, changes the document nodes they return, and renders them once with the
builder's `render_partial`. It never parses Sphinx's HTML back into a tree, and it takes no HTML
parsing library as a dependency. Markup the theme adds inside those trees, such as a branch's
toggle, is a `raw` node, and a link that needs attributes the HTML writer cannot give is a node
class of the theme's own with its own visitor, registered with `app.add_node`.

## Why

The site navigation, the header links, On this page and a toctree drawn in a page body all need
Sphinx's toctree with classes and controls added. Rendering it to HTML and parsing it again
renders every toctree twice and needs a parser such as `beautifulsoup4` at run time, a dependency
every site would carry. Both functions return nodes before rendering, with the same signature from
Sphinx 7.4 to 9.2, so the theme does the same work Sphinx does for its own `toctree()` and no more.

## Revisit if

Sphinx stops exposing the toctree as nodes before it renders them, or changes the signature of
`global_toctree_for_doc` or `document_toc`.
