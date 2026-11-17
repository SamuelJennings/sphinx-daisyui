# Decisions: 004-reader-tools

Decisions taken while specifying and building this feature, where the issue and the accepted
design were silent. Each is recorded here so it can be reviewed and reversed.

## D1. The reading of the feature

Who can newly do what: a site author chooses the site's daisyUI themes, starting mode, theme
picker, search options and published versions; a reader switches mode or theme, searches from a
dialog, and moves to the same page in another version. The interpretation was written from issue
#7 and `PROTOTYPE.md` features 6, 7 and 8, and taken as agreed.

- **What it does and for whom.** The three header tools of the accepted design, each with the
  part a site author configures and the part a reader uses.
- **Boundary.** The page frame, the components lists, the logo, the announcement and the keyboard
  helper's first keys are #4. Site navigation, On this page and header links are #5. Page-body
  styles and Pygments styles are #6. Icon links and edit and view links are #8.
- **Constraints.** Article V as amended (escaping, `textContent`), Article VIII (fixed text in the
  message catalogue), Article XI (tokens only on the full search page), Article XIV (keyboard and
  screen reader).

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D2. Six stories

Each tool splits into the site author's part and the reader's part, because the two are never
merged into one story. Search options (`search_bar_text`, `disable_search`,
`search_as_you_type`, the search button) are a site author's story of their own, small, rather
than scenarios under the reader's story. The search button is one component,
`search-button-field`, the name the default `navbar_persistent` uses.

**ADR:** none — how this feature's stories are cut, nothing downstream inherits it.

## D3. `search_as_you_type` is kept, on by default

It changes what the reader gets, so it stays as the theme's own option. The accepted design lists
results as the reader types, so it is on by default. Off, no results are listed as the reader
types.

**ADR:** none — the behaviour of one option, documented with it.

## D4. `check_switcher` warns and builds

The build reads the file once and warns when it cannot. A warning fails a build run with warnings
as errors, and the option turns the check off.

**ADR:** none — the behaviour of one option, documented with it.

## D5. `show_version_warning_banner` is a banner before the header

On pages of versions other than the preferred one, linking to the same place in the preferred
version. With no preferred entry in the file, no banner.

**ADR:** none — the behaviour of one option, documented with it.

## D6. Unknown theme names are accepted

daisyUI themes are CSS variables, and the accepted design's documentation shows a site defining
colours in its own stylesheet. Warning on an unknown name would break a warnings-as-errors build
for such a site. A `default_mode` outside `auto`, `light` and `dark` warns, because no fourth
value can mean anything.

**ADR:** none — the behaviour of the options, documented with them.

## D7. The starting mode has one option, `default_mode`

Nothing else sets it.

**ADR:** none — follows from the ruling that each setting has one option.

## D8. A reader's choice is kept per site

Two sites on the same host must not share or break each other's stored choice. The choice is
one `localStorage` entry whose key is named from the site's root address, which Sphinx writes on
`<html>` as `data-content_root`.

**ADR:** none — documented with the mode attributes.

## D9. A stored theme the site no longer offers falls back to the starting mode

Rather than showing a theme the site author removed.

**ADR:** none — the behaviour of one option, documented with it.

## D10. A version link is made only from a web address

`switcher.json` is the site author's file, but it is fetched at read time and may be served from
elsewhere, so a `javascript:` address is refused like any other value written into the page
(Article V).

**ADR:** none — follows from Article V.

## D11. Matching uses Sphinx's own search

The design's light stemmer is replaced by Sphinx's own query parsing and search
(`Search._parseQuery` and `Search._performSearch` in `searchtools.js`), with the stemmer and stop
words Sphinx writes for the site's `language`, so the dialog and the full search page find the
same pages. Both functions were read on Sphinx 7.4, 8.2 and 9.2 and are the same on each.

**ADR:** docs/adr/0004-search-with-sphinxs-own-search-functions.md

## D12. The picker's full list has one source with the stylesheet's compiled themes

The design wrote the 35 names out by hand beside `themes: all`. `scripts/themes.mjs` writes
`themes.json` from daisyUI's `themeOrder.js`, the list `themes: all` compiles, each time the
stylesheet is built.

**ADR:** none — the same pattern as `icons.json`, recorded in the contributing guide.

## D13. The mode is applied by a script in `<head>`, reading its values from its own element

The site's two themes, starting mode and offered themes reach `mode.js` as escaped `data-`
attributes on its `<script>` element, so no site value is written into script text. It is loaded
without `defer` after the stylesheets, so the attributes are set before the body is drawn and a
picked theme's `color-scheme` can be read.

**ADR:** none — documented with the mode attributes in the page reference.

## D14. The page scripts' fixed text is printed by the templates

Sphinx's `Documentation.gettext` reads only Sphinx's own JavaScript catalogue. The templates
print each translated string the scripts write into a `data-` attribute, so all of the theme's
text is in one catalogue.

**ADR:** none — local to this feature's scripts.

## D15. Sphinx's own `/` shortcut is switched off

`theme.toml` sets `enable_search_shortcuts = "false"`, so `/` has one listener, the dialog's.
Sphinx's arrow-key navigation is a separate setting and is unchanged.

**ADR:** none — one setting in `theme.toml`, explained there.

## D16. A version's address is read the way `json_url` is

A full address and a path from the server's root are used as given, and any other address is read
from the site's root. The documentation's `switcher.json` can then list its own build as `./`,
which works wherever the site is published.

**ADR:** none — the behaviour of one option, documented with the file's format.

## D17. `check_switcher` reads the built file

A relative `json_url` is read from the build's output at `build-finished`, after Sphinx has
copied the static files, so the check reads the file the reader will be sent.

**ADR:** none — the behaviour of one option, documented with it.
