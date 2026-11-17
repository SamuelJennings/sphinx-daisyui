# Decisions: 004-reader-tools

Decisions taken while specifying this feature, where the issue and the accepted design were
silent. Each is recorded here so it can be reviewed and reversed.

## The reading of the feature

Who can newly do what: a site author chooses the site's daisyUI themes, starting mode, theme
picker, search options and published versions; a reader switches mode or theme, searches from a
dialog, and moves to the same page in another version. The interpretation below was written from
issue #7 and `PROTOTYPE.md` features 6, 7 and 8, and taken as agreed.

- **What it does and for whom.** The three header tools of the accepted design, each with the part
  a site author configures and the part a reader uses.
- **Boundary.** The page frame, the components lists, the logo, the announcement and the keyboard
  helper's first keys are #4. Site navigation, On this page and header links are #5. Page-body
  styles and Pygments styles are #6. Icon links, edit and view links and the two configuration
  presets are #8.
- **Constraints.** Article V as amended (escaping, `textContent`), Article VIII (fixed text in the
  message catalogue), Article X (borrowed names keep their meaning), Article XI (tokens only on the
  full search page), Article XIV (keyboard and screen reader).

## Self-resolved

1. **Six stories.** Each tool splits into the site author's part and the reader's part, because
   the two are never merged into one story. Search options (`search_bar_text`, `disable_search`,
   `search_as_you_type`, the three button names) are a site author's story of their own, small,
   rather than scenarios under the reader's story.
2. **`search_as_you_type` defaults to on.** pydata-sphinx-theme defaults it to off, but the accepted
   design lists results as the reader types and sets the option's default to on. The accepted look
   wins on the default. Off keeps pydata-sphinx-theme's meaning, so a pydata configuration that
   sets it acts as it does there. Component list defaults already differ from pydata-sphinx-theme
   in the same way (`version-switcher` in `navbar_end`).
3. **`check_switcher` warns and builds.** As in pydata-sphinx-theme: the build reads the file once
   and warns when it cannot. A warning fails a build run with warnings as errors, which is the
   option's meaning there, and the option turns it off.
4. **`show_version_warning_banner` is a banner before the header**, on pages of versions other than
   the preferred one, linking to the same place in the preferred version. That is
   pydata-sphinx-theme's meaning. With no preferred entry in the file, no banner.
5. **Unknown theme names are accepted.** daisyUI themes are CSS variables, and the accepted design's
   documentation shows a site defining colours in its own stylesheet. Warning on an unknown name
   would break a warnings-as-errors build for such a site. A `default_mode` outside `auto`, `light`
   and `dark` warns, because no fourth value can mean anything.
6. **`html_context["default_mode"]` is honoured.** pydata-sphinx-theme reads the starting mode from
   `html_context`, so a configuration copied from it would otherwise lose its mode (Article X). The
   theme option takes precedence when both are set, since a site author who sets it has written it
   for this theme.
7. **A reader's choice is kept per site.** Two sites on the same host must not share or break each
   other's stored choice. How it is kept is for the plan.
8. **A stored theme the site no longer offers falls back to the starting mode**, rather than
   showing a theme the site author removed.
9. **A version link is made only from a web address.** `switcher.json` is the site author's file,
   but it is fetched at read time and may be served from elsewhere, so a `javascript:` address is
   refused like any other value written into the page (Article V).
10. **Matching uses Sphinx's search language support.** The design's light stemmer is replaced by
    the stemmer and stop words Sphinx writes for the site's `language`, so the dialog and the full
    search page agree. The success criterion is that the dialog finds every page the full search
    page finds for the same words.
11. **The picker's full list has one source** with the stylesheet's compiled themes. The design
    wrote the 35 names out by hand beside `themes: all`.
