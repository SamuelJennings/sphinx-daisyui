# How the theme is built

The theme is a set of Jinja templates and one stylesheet, with a little Python between Sphinx
and the templates. This page says where each part lives, for a change that has to find it.

## The page context

Sphinx calls `add_page_context` in `sphinx_daisyui.events` for every page it writes. It reads the
theme's options with `ThemeOptions` from `sphinx_daisyui.options` and gives the templates one
dictionary, `daisy`, which is the only place a template reads an option from. `check_layout`
stops the build when the `layout` option is not a layout code, which `LayoutCode` in
`sphinx_daisyui.layout` reads.

## The site navigation

`SiteNavigation` in `sphinx_daisyui.navigation` reads the site's toctrees once for a page as
docutils nodes, with Sphinx's `global_toctree_for_doc`. It marks the nodes for the stylesheet,
adds a toggle beside every entry with pages under it, and renders them once with the builder.
Nothing is parsed back from HTML.

The HTML writer's link takes no `aria-current`, so the link to the current page is swapped for a
`CurrentLink` node, which the theme registers with `visit_current_link` and
`depart_current_link` to write it.

Fixed text the Python writes, such as a toggle's name, is marked for translation with
`translate`, Sphinx's translator for the `sphinx` message domain that the templates use too.

## Header links

`SiteNavigation.top_level` lists the entries at the first level of the same cached tree as
`HeaderLink` records: the entry's title, its address and whether it is on the current page's path.
`HeaderLinks` takes those, the `external_links` records, `header_links_before_dropdown` and
`header_dropdown_text`, and splits them into `shown` and `more` with `more_text` and
`more_current`. `SiteNavigation.section_menu` draws the pages under the current top-level entry
with the same marks as `menu`, which is what the primary sidebar shows when `navbar-nav` is in
`navbar_center`. `add_page_context` sets `daisy.sectioned`, which is true when `NAVBAR_NAV` is in `navbar_center`,
`daisy.header`, built when `NAVBAR_NAV` is in any component list, and `daisy.navbar_align`, one of
`NAVBAR_ALIGNMENTS`.
`static/scripts/navigation.js` sets the margin that starts the header links where the article
starts, and keeps the header menu closed after Escape.

## On this page

`PageContents` in `sphinx_daisyui.navigation` reads the page's headings from `document_toc`,
which Sphinx builds from the page's table of contents, as docutils nodes. It drops the page's own
title, marks each list with `daisy-toc-list`, each link with `daisy-toc-link` and each list
deeper than `show_toc_level` with `daisy-toc-deep`, and renders them once. `add_page_context` gives
the templates the result as `daisy.page_toc`, with `daisy.page_toc_count` and
`daisy.show_toc_level`. `static/scripts/page-toc.js` marks the heading being read with
`aria-current="location"` and its entries with `daisy-toc-on-path`, which shows the deeper
headings of that section.

`is_index_page` in `sphinx_daisyui.events` tells the search page, the domain indexes and the
general indexes from other pages by the template Sphinx renders them with. They have no headings
of their own, so `add_page_context` gives them an empty secondary sidebar and no contents.

## Icons

`Icons` in `sphinx_daisyui.icons` reads the bundled `icons.json`, and `ICONS` is the one instance
the templates and the Python share.

## Theme names

`themes.json` lists every theme daisyUI ships, in daisyUI's own order, which is the list a
site's `theme_picker = true` offers. `scripts/themes.mjs` writes it from daisyUI's
`themeOrder.js`, and `npm run build` rewrites it when the list changes, so a daisyUI upgrade needs no edit by hand.

## Modes and themes

`Modes` in `sphinx_daisyui.modes` reads `light_theme`, `dark_theme`, `default_mode` and
`theme_picker` into `daisy.modes`. `check_modes` warns once at the start of the build when
`default_mode` is not `auto`, `light` or `dark`. The site's values reach the page on the
`<script>` element that loads `static/scripts/mode.js`, which sets the attributes on `<html>`
before the page is drawn and holds the one function that applies a reader's choice.
`static/scripts/theme-menu.js` wires the theme menu to it.

## Search

`SearchSettings` in `sphinx_daisyui.search` reads `search_bar_text`, `disable_search` and
`search_as_you_type` into `daisy.search`. `static/scripts/search.js` loads Sphinx's own
`language_data.js`, `searchtools.js` and `searchindex.js` the first time the dialog opens, and
finds results with Sphinx's own search functions (ADR 0004). `static/scripts/page-address.js`
turns a page's name into its address for the build, for the search dialog and the version
switcher.

## Versions

`VersionSwitcher` in `sphinx_daisyui.versions` reads the `switcher` option and
`show_version_warning_banner` into `daisy.switcher`. `check_switcher`, connected to the end of
the build, reads the site's `switcher.json` once and warns when it cannot be used.
`static/scripts/versions.js` lists the versions in the page and fills the banner.

## Icon links and source links

`IconLinks` in `sphinx_daisyui.links` reads `icon_links` into `daisy.icon_links`, one `IconLink`
per entry with an address, each holding its name, its address and the icon or image drawn in
it. `check_icon_links` warns once at the start of the build when the option is text, and for
each entry whose icon is not bundled.

`SourceLinks` reads `source_repository`, `source_branch` and `source_directory` into
`daisy.sources`: the page's edit and view addresses and the address of Sphinx's copy of its
source. `SourceHost` holds one host's address forms, and `HOSTS` the three the theme knows.
`daisy.top_buttons` is the part of `top_of_page_buttons` whose addresses exist.
