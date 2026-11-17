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

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D2. Three stories

The issue gives a reader's part and a site author's part, and the two are never merged. The
reader's part is split once more: opening a page from a toctree in a page is a thing a reader sets
out to do apart from reading, and it depends on the site navigation's branch toggle (#5), where
the rest of the page body depends only on the frame. A separate story lets the build deliver the
reading story first. The escape class and the Pygments options stay one site author's story: both
are ways out of the theme's defaults, and neither is a distinct goal.

**ADR:** none — how this feature's stories are cut, nothing downstream inherits it.

## D3. Two options bring Pygments back, one per mode

The prototype's decision is that code is highlighted from the tokens and Pygments' stylesheet is
dropped, unless `pygments_light_style` or `pygments_dark_style` is set. The theme has its own
configuration, with one name and one shape per setting, so these two options are the only way:
no second spelling and no option read from another theme. The names are pydata-sphinx-theme's,
taken as the theme's own because they fit. Sphinx's own `pygments_style` setting is left as it
is: honouring it would bring Pygments' colours back on every site that kept Sphinx's default,
against the decision.

**ADR:** none — the two options are documented in the options reference, which is their record.

## D4. An unknown Pygments style warns, and the mode keeps token highlighting

A misspelt style name is a site author's slip that the rest of the page does not depend on, so it
warns rather than failing the build, and a build run with warnings as errors still catches it. The
fallback is the theme's own token highlighting, which is this theme's default.

**ADR:** none — the behaviour of one option, documented with it.

## D5. The dark Pygments style follows the page's mode, not the system's

Sphinx's own `pygments_dark_style` theme setting keys the dark stylesheet on a media query, which
ignores a reader who picked a mode in the navbar. The prototype keys on the mode attribute on
`<html>`, so the style follows the mode the reader sees, including auto. The modes feature (#7)
owns that contract. Until it lands, the page frame's attributes are the ones read.

**ADR:** none — follows from the mode attributes, whose contract the modes feature records.

## D6. Neither sphinx-design nor sphinx-copybutton becomes a dependency

The theme styles their markup when a site loads them (Article XIII). Making either a dependency
would install it on sites that do not use it (Article VII). The documentation site adds both to
its own dependency group for the kitchen sink pages.

**ADR:** none — a dependency choice for the documentation site, recorded in pyproject.toml.

## D7. The fixed names are translated, and the region names are not pinned

The prototype names a table's region "Table" and an equation's "Equation", and a toggle
"Show the pages in …". The specification requires a fixed name and its translation (FR-019), not
the words, so tests check that a name is present and comes from the catalogue, not its text.

**ADR:** none — local to this feature's tests.

## D8. The body is changed by a translator mixin

The heading links, admonition titles and a toctree in a page exist only while Sphinx writes the
page, and parsing the written HTML would bring back the parser ADR 0001 kept out. A mixin over
each HTML builder's translator, built at `builder-inited` as pydata-sphinx-theme builds its own,
changes them at write time and keeps another extension's translator as its base.

**ADR:** docs/adr/0002-change-the-page-body-as-it-is-written.md

## D9. Sphinx's Pygments stylesheet is dropped on every page

With a style set for only one mode, Sphinx's `pygments.css` would still colour the other mode's
code, mixing Sphinx's default style into the token highlighting that FR-014 keeps. The theme's own
stylesheet carries every Pygments style a site sets.

**ADR:** none — a consequence of D3 local to this feature.

## D10. The Pygments styles follow the system until the page has a mode

`main` writes no mode attribute yet. Each style is keyed on `data-mode` on `<html>`, which the
modes feature adds, and on `prefers-color-scheme` while that attribute is absent, as the logo is.

**ADR:** none — temporary until the modes feature writes data-mode, which supersedes it.

## D11. The admonition icons are inline SVG

FR-021 wants the icons from the icon set with no second copy in the stylesheet. The mixin writes
them into each title from `ICONS`, as the frame draws its icons. A task list's tick is drawn with
CSS, since it is not the icon of a kind.

**ADR:** none — follows from the icon set the page frame already records as the one source of icons.

## D12. The supported browsers are those with `@scope`

The page-body styles are scoped with `@scope`, in Chrome 118, Safari 17.4 and Firefox 146. That
becomes the theme's documented support target.

**ADR:** docs/adr/0003-support-the-browsers-with-css-scope.md

## D13. The site navigation's decoration is one class both menus use

The toctree in a page needs the sidebar's toggles, classes and caption label (FR-013). The
decoration moved out of `SiteNavigation` into `NavigationMenu`, which the sidebar and the page
body both call. The sidebar's own menu is written by the same translator already decorated, so a
toctree whose lists carry the menu's class is left alone.

**ADR:** none — the shared-piece decision is ADR 0001's, this is where its code sits.

## D14. The copy button gets a visible focus outline

The prototype's copy button had no outline and no shadow on focus, which fails FR-009. It gains a
2px outline in the primary colour on keyboard focus. Nothing else about it changes.

**ADR:** none — a fix to meet the specification, local to one rule.

## D15. The kitchen sink has its own index page

The documentation standard gives each section of the documentation an index, so the kitchen sink
pages sit under one entry in the sidebar where the prototype listed them flat. Their addresses
and bodies are the prototype's.

**ADR:** none — documentation placement, recorded by the documentation standard.

## D16. The message catalogue is regenerated with the code that adds a message

The test that every marked message is in the shipped catalogue template would be red at any
commit that adds a message without it, so each commit that adds a message regenerates the
template, and the translation tests share the one test catalogue, because Sphinx keeps the first
catalogue it loads in a process.

**ADR:** none — local to how this repository's tests are written.
