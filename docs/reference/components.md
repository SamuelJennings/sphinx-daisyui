# Components

A component is a template that a [component list](options.md) names. The theme provides ten.
Each one draws nothing when what it shows is switched off, so a list can name it without
checking.

## `copyright`

Shows the copyright line from the `copyright` setting, as a link when the site has a page named
`copyright`. It is drawn when `html_show_copyright` is true, which is Sphinx's default, and the
site has a `copyright` setting.

## `sphinx-version`

Shows "Built with Sphinx" and the version of Sphinx that built the site, linked to Sphinx's
website. It is drawn when `html_show_sphinx` is true, which is Sphinx's default.

## `theme-version`

Shows the theme's name, linked to its repository, and the installed version of the theme. It is
always drawn.

## `last-updated`

Shows the date the page was last updated. It is drawn when `html_last_updated_fmt` is set to a
date format, such as `"%d %B %Y"`. Sphinx leaves it unset by default.

## `navbar-logo`

Shows the site's title, linked to the front page.

## `sidebar-nav`

Shows the site's table of contents as a menu: the captions of its `toctree` directives, its
entries, a toggle that opens and closes each entry that has children, and a mark on the current
page. The [options](options.md) `navigation_depth`, `show_nav_level`, `collapse_navigation` and
`sidebar_includehidden` set how much of it is listed and open. The theme puts it in the primary
sidebar, and it draws nothing when the site has no table of contents.

## `navbar-nav`

Shows a link to each top-level page of the site's table of contents, then each of the
[options](options.md) `external_links`, in the order they are given. The link to the section
holding the page is marked. Links past `header_links_before_dropdown` are in a menu labelled
by `header_dropdown_text`, which opens from the keyboard and is marked when the current section is
in it. It draws nothing when the site has no table of contents and no external links.

Named in `navbar_center`, it also changes the primary sidebar: `sidebar-nav` then lists only the
pages of the current section, and nothing on a page that is in no section, such as the front
page. On a narrow window the drawer lists every header link above it. Named in any other
component list, it draws the links there and leaves the sidebar's navigation whole.
[Put the sections in the header](../developer/put-the-sections-in-the-header.md) shows the steps.

## `theme-switcher`

Shows a button that opens a menu of the three modes: match the system, light and dark. When the
[option](options.md) `theme_picker` names themes, the menu lists them below the modes, each with
a swatch of its colours. The button shows the reader's current choice. The theme puts it in
`navbar_end`, and on a narrow window it moves into the drawer with the rest of that list.

The site's themes and its starting mode apply with or without it. A site that leaves the component
out of every list draws no menu, and every page still follows `light_theme`, `dark_theme` and
`default_mode`, and the reader's system when the mode is `"auto"`.

## `version-switcher`

Shows a button labelled with the version being built, which opens a menu of every version in the
file named by the `switcher` [option](options.md). The reader's own version is marked, and so is
the preferred one. The theme puts it in `navbar_end`, and on a narrow window it moves into the
drawer with the rest of that list.

It draws nothing unless `switcher` gives a `json_url`. The `check_switcher` and
`show_version_warning_banner` options set whether the build checks the file and whether a banner
warns on a version that is not the preferred one.

## `search-button-field`

Shows a button that reads Search the docs, or the text set in `search_bar_text`, with the keys
that open the search dialog beside it: {kbd}`Ctrl+K` or {kbd}`⌘K` on any page, and {kbd}`/`
when the reader is not typing in a field. It is named in `navbar_persistent` by default, and a
site may name it in any other [component list](options.md) instead.

The dialog comes with the button: it is written once at the end of every page, whichever list
names the button. A site that sets `disable_search` to `True` draws neither the button nor the
dialog, and the shortcuts do nothing. The [options](options.md) `search_bar_text` and
`search_as_you_type` set its words and whether results appear as the reader types.

## `breadcrumbs`

Shows the path to the page: a link home, a link to each page above it in the table of contents,
and the page's own title as plain text. It draws nothing on the front page. It is named in
`article_header_start` by default.

## `page-toc`

Shows the headings of the page, nested as they are in the page, under the label On this page.
The heading being read is marked as the reader scrolls, and the last heading is marked at the
foot of the page. The [option](options.md) `show_toc_level` sets how deep the list is open.
It draws nothing on a page with no headings below its title, nor on the search page or an
index. It is named in `secondary_sidebar_items` by default, and when it is named there, a
closed On this page disclosure with the same headings appears above the page on narrow windows.

## Your own components

A site adds a component by putting a template in a directory listed in `templates_path`, and
naming it in a [component list](options.md). A template named `status.html` is named `status` or
`status.html`. [Arrange the page](../developer/arrange-the-page.md) shows the steps.

A template has the page's full context, as every Sphinx template does, and the theme's own
values under `daisy`.

A name that matches no template draws nothing and raises no warning.

## Macros

`components/macros.html` holds three macros a component may import:

```jinja
{%- from 'components/macros.html' import components, icon_button with context %}
```

- `components(names)` draws each name in a list, looking in the theme's `components/` directory
  first and then in the site's templates.
- `icon_button(label, icon, tooltip="", data={})` draws a ghost button holding the named icon.
  The label is the button's accessible name. When a tooltip is given, it shows on hover. Each
  entry of `data` becomes a `data-` attribute on the button, so `{"daisy-search-close": ""}`
  writes `data-daisy-search-close`; a page script finds the button by it.
- `navbar_dropdown(tag="div", panel_tag="div", trigger_class="", panel_class="", label="",
  attrs={}, trigger_attrs={})` draws one menu in the navbar and is used with `call`. It draws
  the outer element, the button that opens the menu and the panel, and the caller fills the
  button and the panel:

  ```jinja
  {%- call(part) navbar_dropdown(panel_tag="ul", panel_class="menu w-56") %}
    {%- if part == "trigger" %}Menu{% else %}<li><a href="#">An entry</a></li>{% endif %}
  {%- endcall %}
  ```

  `tag` and `panel_tag` name the outer element and the panel. `trigger_class` and `panel_class`
  add classes to the button and the panel, `label` is the button's accessible name, and `attrs`
  and `trigger_attrs` are dicts of attributes for the outer element and the button. Every value is
  escaped. The outer element carries the class `daisy-dropdown`, which the theme's script uses to
  open the menu from the keyboard and to close it with Escape, wherever the menu sits on the page.
