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

## On this page

`PageContents` in `sphinx_daisyui.navigation` reads the page's headings from `document_toc`,
which Sphinx builds from the page's table of contents, as docutils nodes. It drops the page's own
title, marks each list with `daisy-toc-list`, each link with `daisy-toc-link` and each list at or
below `show_toc_level` with `daisy-toc-deep`, and renders them once. `add_page_context` gives
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
