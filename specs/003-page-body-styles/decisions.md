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

## D3. Only pydata-sphinx-theme's options bring Pygments back

The prototype's decision is that code is highlighted from the tokens and Pygments' stylesheet is
dropped, unless `pygments_light_style` or `pygments_dark_style` is set. Sphinx's own
`pygments_style` setting is left as it is: honouring it would bring Pygments' colours back on
every site that kept Sphinx's default, against the decision. Furo reads `pygments_dark_style` as
a `conf.py` setting, not a theme option, and whether a Furo configuration's highlighting is
honoured is decided with the Furo configurations in #8.

## D4. The correctly spelt option wins

pydata-sphinx-theme renamed `pygment_light_style` and `pygment_dark_style` to the correctly spelt
names. A site that sets both spellings is mid-migration, and the name the source theme documents
today is the one it means. The prototype declares both spellings in `theme.toml`.

## D5. An unknown Pygments style warns, and the mode keeps token highlighting

Article X forbids an error for an option the theme accepts. pydata-sphinx-theme warns and falls
back to a default style when Pygments does not know the name. Here the fallback is the theme's
own token highlighting, which is this theme's default. Research confirms pydata-sphinx-theme's
behaviour before it is built.

## D6. The dark Pygments style follows the page's mode, not the system's

Sphinx's own `pygments_dark_style` theme setting keys the dark stylesheet on a media query, which
ignores a reader who picked a mode in the navbar. The prototype keys on the mode attribute on
`<html>`, so the style follows the mode the reader sees, including auto. The modes feature (#7)
owns that contract. Until it lands, the page frame's attributes are the ones read.

## D7. Neither sphinx-design nor sphinx-copybutton becomes a dependency

The theme styles their markup when a site loads them (Article XIII). Making either a dependency
would install it on sites that do not use it (Article VII). The documentation site adds both to
its own dependency group for the kitchen sink pages.

## D8. The fixed names are translated, and the region names are not pinned

The prototype names a table's region "Table" and an equation's "Equation", and a toggle
"Show the pages in …". The specification requires a fixed name and its translation (FR-019), not
the words, so tests check that a name is present and comes from the catalogue, not its text.
