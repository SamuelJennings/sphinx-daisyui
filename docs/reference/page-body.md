# The page body

What the theme draws inside the page: the content Sphinx writes between the breadcrumbs and the
previous and next links. A site does nothing to turn this on. The styles follow the daisyUI
theme in use and its light and dark modes.

The [kitchen sink](../kitchen-sink/index.md) shows every block below, in the theme.

## What the theme draws

| Block | Includes |
|---|---|
| Headings and inline text | Headings with their permalinks, emphasis, inline code, links, keyboard keys and abbreviations |
| Lists | Bulleted, numbered, definition, field and option lists, and task lists |
| Quotes | Block quotes, pull quotes and their attributions, and epigraphs |
| Admonitions | Every admonition kind, each with its own colour and icon, and the version notes (added, changed, deprecated and removed) |
| Code | Literal blocks with Pygments highlighting, line numbers, emphasised lines and captions, and inline code |
| Tables | Simple, grid and list tables, with their captions |
| Figures and pictures | Images, figures with captions, and the footnotes and citations that refer to them |
| Equations | Inline and display math, with equation numbers |
| API entries | The entries autodoc writes for modules, classes, functions, methods and attributes |

## Extensions the styles cover

The theme styles the markup these extensions write:

- **MyST** for Markdown pages, including task lists, definition lists and admonitions in colon
  fences.
- **autodoc** for the API entries.
- **sphinx-design** for grids, cards, tabs, dropdowns, badges and buttons. Its colours follow the
  daisyUI theme.
- **sphinx-copybutton** for the copy button on a code block. The button appears when the pointer is
  over the block or when it has keyboard focus.

The theme requires neither sphinx-design nor sphinx-copybutton. Their styles apply when a site loads
them, and a site that does not load them is not changed.

## Scroll regions

A table or a display equation that is wider than the page scrolls inside its own region, so the
page never scrolls sideways.

- A table sits in a region named by its caption, or named "Table" when it has none. A table inside
  another table is part of the outer table's region.
- A display equation's notation sits in a region named by its number, or named "Equation" when it
  has none. The number stays outside the region, so it does not scroll away from the equation.

Each region is exposed to assistive technology with the `region` role and takes keyboard focus, so
a reader without a pointer can scroll it with the arrow keys.

## Supported browsers

The page-body styles use CSS `@scope`. They work in Chrome 118, Safari 17.4 and Firefox 146, and
in later versions of each. A browser without `@scope` does not draw the page body: the content is still there and
readable, but without the theme's styles.
