# Decisions: 003-page-body-styles

Decisions made while specifying, with the reason each is defensible. Each stands until the
maintainer changes it.

## D1. The reading of the issue, taken as agreed

The feature is the prototype's feature 3, whose screens and decisions are already agreed: a
reader gets every page body drawn with daisyUI's tokens, and a site author keeps daisyUI's look on
raw HTML or brings Pygments styles back. Its boundary is the prototype's split: the frame, the
site navigation, On this page, modes and the theme picker, search, and the other themes'
configurations belong to #4, #5, #7 and #8. The kitchen sink pages come with this feature, as
`PROTOTYPE.md` says, because they are the pages its look is checked on.

## D2. Three stories

The issue gives a reader's part and a site author's part, and the two are never merged. The
reader's part is split once more: opening a page from a toctree in a page is a thing a reader sets
out to do apart from reading, and it depends on the site navigation's branch toggle (#5), where
the rest of the page body depends only on the frame. A separate story lets the build deliver the
reading story first. The escape class and the Pygments options stay one site author's story: both
are ways out of the theme's defaults, and neither is a distinct goal.

## D3. Two options bring Pygments back, one per mode

The prototype's decision is that code is highlighted from the tokens and Pygments' stylesheet is
dropped, unless `pygments_light_style` or `pygments_dark_style` is set. The theme has its own
configuration, with one name and one shape per setting, so these two options are the only way:
no second spelling and no option read from another theme. The names are pydata-sphinx-theme's,
taken as the theme's own because they fit. Sphinx's own `pygments_style` setting is left as it
is: honouring it would bring Pygments' colours back on every site that kept Sphinx's default,
against the decision.

## D4. An unknown Pygments style warns, and the mode keeps token highlighting

A misspelt style name is a site author's slip that the rest of the page does not depend on, so it
warns rather than failing the build, and a build run with warnings as errors still catches it. The
fallback is the theme's own token highlighting, which is this theme's default.

## D5. The dark Pygments style follows the page's mode, not the system's

Sphinx's own `pygments_dark_style` theme setting keys the dark stylesheet on a media query, which
ignores a reader who picked a mode in the navbar. The prototype keys on the mode attribute on
`<html>`, so the style follows the mode the reader sees, including auto. The modes feature (#7)
owns that contract. Until it lands, the page frame's attributes are the ones read.

## D6. Neither sphinx-design nor sphinx-copybutton becomes a dependency

The theme styles their markup when a site loads them (Article XIII). Making either a dependency
would install it on sites that do not use it (Article VII). The documentation site adds both to
its own dependency group for the kitchen sink pages.

## D7. The fixed names are translated, and the region names are not pinned

The prototype names a table's region "Table" and an equation's "Equation", and a toggle
"Show the pages in …". The specification requires a fixed name and its translation (FR-019), not
the words, so tests check that a name is present and comes from the catalogue, not its text.

## D8. The body is changed by a translator mixin

The heading links, admonition titles and a toctree in a page exist only while Sphinx writes the
page, and parsing the written HTML would bring back the parser ADR 0001 kept out. A mixin over
each HTML builder's translator, built at `builder-inited` as pydata-sphinx-theme builds its own,
changes them at write time and keeps another extension's translator as its base.

**ADR:** pending S5

## D9. Sphinx's Pygments stylesheet is dropped on every page

With a style set for only one mode, Sphinx's `pygments.css` would still colour the other mode's
code, mixing Sphinx's default style into the token highlighting that FR-014 keeps. The theme's own
stylesheet carries every Pygments style a site sets.

**ADR:** pending S5

## D10. The Pygments styles follow the system until the page has a mode

`main` writes no mode attribute yet. Each style is keyed on `data-mode` on `<html>`, which the
modes feature adds, and on `prefers-color-scheme` while that attribute is absent, as the logo is.

**ADR:** pending S5

## D11. The admonition icons are inline SVG

FR-021 wants the icons from the icon set with no second copy in the stylesheet. The mixin writes
them into each title from `ICONS`, as the frame draws its icons. A task list's tick is drawn with
CSS, since it is not the icon of a kind.

**ADR:** pending S5

## D12. The supported browsers are those with `@scope`

The page-body styles are scoped with `@scope`, in Chrome 118, Safari 17.4 and Firefox 146. That
becomes the theme's documented support target.

**ADR:** pending S5
