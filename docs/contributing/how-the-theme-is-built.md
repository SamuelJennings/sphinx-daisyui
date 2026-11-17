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

## Icons

`Icons` in `sphinx_daisyui.icons` reads the bundled `icons.json`, and `ICONS` is the one instance
the templates and the Python share.
