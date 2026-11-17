# Options

The theme options a site sets in `html_theme_options` in `conf.py`. Each is described the same
way: its type, its default and what it does.

A component list is a Python list of names, and a name may be written with or without `.html`.
These are the same:

```python
html_theme_options = {
    "footer_start": ["copyright", "sphinx-version"],
}
html_theme_options = {
    "footer_start": ["copyright.html", "sphinx-version.html"],
}
```

Each name is a template. The theme looks for it in its own `components/` directory first, then in
the site's `templates_path`. A name that no template has draws nothing and raises no warning.
[Components](components.md) lists the ones the theme provides.

## Layout

### `layout`

- **Type:** string
- **Default:** `"hHh LpR lff"`
- **Meaning:** The layout code. It places the header, the primary sidebar, the page, the
  secondary sidebar and the footer, and sets which of them stay in view while the page scrolls.
  An empty value means the default. A value that is not a layout code stops the build with a
  message naming the option. [The layout code](layout-code.md) explains each letter.

## Brand

The brand is the logo and name at the start of the navbar. When `layout` gives the top-left
corner to the primary sidebar, the brand heads that sidebar on wide screens and stays in the
navbar on narrow ones. A logo is a full address, a path starting `_static/`, or a path relative
to `_static`. Sphinx's `html_logo` is used for both modes when `logo` gives no image.

### `logo`

- **Type:** dict
- **Default:** empty
- **Meaning:** The brand as a whole. Every key is optional:
  - `text`: the name beside the logo. Without it the site's title is shown, unless the dict
    gives an image, and then no name is shown.
  - `image_light` and `image_dark`: the logos for light and dark mode. The light logo is also
    shown in dark mode when `image_dark` is not set.
  - `alt_text`: the logo's `alt` text. The default is the project name.
  - `link`: where the brand leads. The default is the site's home page.

## Modes and themes

A reader sees the site in a mode: light, dark, or the one their system asks for. Each mode draws
one daisyUI theme. The [theme-switcher](components.md) component lets a reader choose.
[Choose the themes](../developer/choose-the-themes.md) shows the steps.

### `light_theme`

- **Type:** string
- **Default:** `"light"`
- **Meaning:** The theme the light mode draws. The name is used as given, so a theme of the
  site's own works as well as one of daisyUI's.

### `dark_theme`

- **Type:** string
- **Default:** `"dark"`
- **Meaning:** The theme the dark mode draws. The name is used as given.

### `default_mode`

- **Type:** string
- **Default:** `"auto"`
- **Meaning:** The mode a reader sees before they have chosen one. The values are `"auto"`, which
  follows the system's setting, `"light"` and `"dark"`. Any other value builds with a warning and
  means `"auto"`. A reader's own choice replaces it, and the browser remembers that choice.

### `theme_picker`

- **Type:** boolean, string or list of strings
- **Default:** empty, which offers no theme by name
- **Meaning:** The themes the theme menu lists besides the three modes. `True` or `"all"` lists
  every theme the stylesheet holds. A list of names, or one string with the names separated by
  commas, lists those in the order given, each once. An empty value, `False` or `"false"` lists
  none. A name is accepted as given, so a site's own theme can be named.

## Moving between pages

### `show_prev_next`

- **Type:** boolean
- **Default:** `True`
- **Meaning:** Whether each page ends with links to the previous and the next page in the
  site's table of contents. A page with neither, and the search and index pages, show none.

### `navigation_with_keys`

- **Type:** boolean
- **Default:** `False`
- **Meaning:** Whether the left and right arrow keys move to the previous and the next page.
  Sphinx's own script does the moving, and it ignores the keys while the reader types in a field
  or holds a modifier key. The meaning is the one Sphinx's `basic` theme gives the option.

### `back_to_top_button`

- **Type:** boolean
- **Default:** `True`
- **Meaning:** Whether a button appears while the reader scrolls up, far down a page, that scrolls
  back to the top.

### `announcement`

- **Type:** text
- **Default:** empty
- **Meaning:** A banner across the top of every page. Text, including HTML of your own, is
  printed as written and is not escaped. Text that starts with `http://` or `https://` is an
  address instead: the page script fetches it and puts the HTML it returns in the banner. The
  banner is removed when the address cannot be fetched, answers with an error or returns nothing,
  which includes a site opened from the file system. An empty value shows no banner.

### `sticky_banners`

- **Type:** boolean
- **Default:** `False`
- **Meaning:** Whether the banner sits inside the header, so that it stays with the header when
  the layout code keeps the header in place. When off, the banner is the first thing on the page
  and scrolls away.

## Search

The theme draws a search button and a search dialog that list results from the index Sphinx
writes. [Set up search](../developer/set-up-search-and-versions.md) shows the steps.

### `search_bar_text`

- **Type:** string
- **Default:** `""`, which shows the words Search the docs in the reader's language
- **Meaning:** The words on the search button and in the dialog's field. The text is shown as
  written, so markup in it appears as characters and is never read as HTML.

### `disable_search`

- **Type:** boolean
- **Default:** `False`
- **Meaning:** When `True`, no page draws the search button or the dialog, and the keyboard
  shortcuts that open the dialog do nothing. Sphinx's own search page is still built.

### `search_as_you_type`

- **Type:** boolean
- **Default:** `True`
- **Meaning:** Whether results are listed while the reader types. When `False`, nothing is
  listed as they type, and Enter opens Sphinx's full search page with their words.

## Versions

The theme draws a version menu in the header when a site names the file that lists its
versions. [Set up versions](../developer/set-up-search-and-versions.md) shows the steps.

### `switcher`

- **Type:** dictionary with `json_url` and `version_match`
- **Default:** `{}`, which draws no menu and no banner
- **Meaning:** `json_url` is where the file listing every version is. `version_match` is the
  version this build documents. It labels the menu and picks the entry the reader is on.
  The menu is drawn on every page only when `json_url` is set.

`json_url` takes three forms:

- A full address, such as `https://example.org/switcher.json`, or one starting with `//`, which
  is read as `https:`.
- A path from the server's root, such as `/switcher.json`.
- Any other path, such as `_static/switcher.json`, which is read from the site's root.

A version's `url` in the file takes the same three forms. A path from the server's root is
used as given, and any other path is read from the site's root, so one file serves a page at any
depth. The check described under `check_switcher` reads a path in `json_url` from the build's
output, where a path from the server's root is read as from the site's root.

### `check_switcher`

- **Type:** boolean
- **Default:** `True`
- **Meaning:** Whether the build reads the file at `json_url` once, at the end of the build,
  and warns when it cannot be read or is not a list of versions each with a `version` and a
  `url`. The build still succeeds. A path is read from the built site, so a file in a static
  directory is found after the build copies it. When `False`, the file is never read.

### `show_version_warning_banner`

- **Type:** boolean
- **Default:** `False`
- **Meaning:** When `True` and `json_url` is set, every page carries a banner before the header
  that appears on any version other than the preferred one and links to the preferred one.

## Site navigation

The navigation in the primary sidebar is the site's table of contents, drawn from its `toctree`
directives.

### `navigation_depth`

- **Type:** integer
- **Default:** `4`
- **Meaning:** How many levels of entries the navigation lists. Deeper entries are left out. Zero lists them all.

### `show_nav_level`

- **Type:** integer
- **Default:** `1`
- **Meaning:** How many levels of entries are open before the reader opens any. The entries on
  the way to the current page are always open.

### `collapse_navigation`

- **Type:** boolean
- **Default:** `False`
- **Meaning:** Whether the navigation leaves out the children of every entry that is not on the
  way to the current page.

### `sidebar_includehidden`

- **Type:** boolean
- **Default:** `True`
- **Meaning:** Whether the navigation lists the pages of a `toctree` marked `:hidden:`.

## Header links

The `navbar-nav` component draws a link to each top-level page of the site's table of contents,
and to each of `external_links`, in the header.

### `external_links`

- **Type:** list of dicts
- **Default:** empty
- **Meaning:** Links to other sites, drawn by `navbar-nav` after the site's own sections. Each dict
  has a `name`, which is the link's text, and a `url`. A dict with no `url` is left out. Each link
  is marked as leading outside the site.

### `header_links_before_dropdown`

- **Type:** integer
- **Default:** `5`
- **Meaning:** How many header links are shown before the rest go into a menu. Zero puts every
  link in the menu, and a number at or above the number of links draws no menu.

### `header_dropdown_text`

- **Type:** text
- **Default:** empty, which shows "More" in the site's language
- **Meaning:** The label of the menu that holds the links past `header_links_before_dropdown`.

### `navbar_align`

- **Type:** text, one of `content`, `left` or `right`
- **Default:** `"content"`
- **Meaning:** Where the header links sit in the navbar, on screens 64rem wide and up. `content`
  starts the first link where the page's text starts, `left` starts it at the start of the
  navbar's free space and `right` ends the links at the end of that space. Any other value is
  read as `content`.

## Icon links

The `navbar-icon-links` component draws a link for each entry of `icon_links`, as an icon.

### `icon_links`

- **Type:** list of dicts
- **Default:** empty
- **Meaning:** The accounts and sites to link as icons. Each dict has these keys:
  - `url`: where the link leads. A dict with no `url` is left out.
  - `name`: the link's accessible name and its tooltip. Without one, the `url` is the name.
  - `icon`: the icon the link is drawn with. With no `type`, it is the name of one of the
    icons listed below. With `type` set to `url`, it is the address of an image. With `type`
    set to `local`, it is the address of an image, a path starting `_static/`, or a path
    relative to `_static`, and every page points at the file from its own depth.
  - `type`: `url` or `local` when `icon` is an image. Any other value, or none, makes `icon`
    a bundled icon's name.
- **Warnings:** The build warns once, with the warning type `daisyui.icon_links`, when the option
  is given as text rather than a list, and once for each entry whose `icon` is not a bundled
  icon. The warning names the entry and the icon, and the link is drawn with the `link` icon.
- **Bundled icons:** `anaconda`, `arrow-left`, `arrow-right`, `arrow-up`, `bitbucket`, `bluesky`, `book-open`, `check`, `chevron-down`, `chevron-right`, `circle-plus`, `circle-x`, `codeberg`, `condaforge`, `copy`, `discord`, `discourse`, `docker`, `external-link`, `file-code`, `github`, `gitlab`, `history`, `info`, `jupyter`, `languages`, `lightbulb`, `link`, `list`, `mastodon`, `matrix`, `megaphone`, `menu`, `moon`, `npm`, `octagon-x`, `orcid`, `palette`, `pencil`, `pypi`, `python`, `readthedocs`, `search`, `square-arrow-out-up-right`, `square-plus`, `stackoverflow`, `star`, `sun`, `sun-moon`, `triangle-alert`, `x`, `x-twitter`, `youtube`, `zenodo`, `zulip`.

### `icon_links_label`

- **Type:** text
- **Default:** empty, which names the list "Icon links" in the site's language
- **Meaning:** The name of the list of icon links, which a screen reader announces before the
  links.

## On this page

The `page-toc` component lists the headings of the page being read.

### `show_toc_level`

- **Type:** integer
- **Default:** `2`
- **Meaning:** How many levels of headings are shown before the reader reaches them. Headings
  under that depth stay hidden until the section above them is being read. A level of `1`
  shows only the headings directly under the page's title, and a level larger than the page's
  deepest heading shows them all.

## Component lists

### `navbar_start`

- **Type:** list of component names
- **Default:** `"navbar-logo"`
- **Meaning:** The components at the start of the navbar, after the button that opens the
  navigation on a narrow screen.

### `navbar_center`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components in the middle of the navbar. They are hidden below 64rem.

### `navbar_end`

- **Type:** list of component names
- **Default:** `"version-switcher, theme-switcher, navbar-icon-links"`
- **Meaning:** The components at the end of the navbar. They are written once in the page and
  hidden on the narrowest screens.

### `navbar_persistent`

- **Type:** list of component names
- **Default:** `"search-button-field"`
- **Meaning:** The components at the end of the navbar that stay on every screen width.

### `article_header_start`

- **Type:** list of component names
- **Default:** `"breadcrumbs"`
- **Meaning:** The components at the start of the line above the page's content. The line is
  left out when this list and `article_header_end` are both empty.

### `article_header_end`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components at the end of the line above the page's content.

### `article_footer_items`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components directly below the page's content.

### `content_footer_items`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components at the very end of the content column, below
  `article_footer_items`.

### `primary_sidebar_end`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components at the end of the primary sidebar, after Sphinx's own sidebar
  templates.

### `secondary_sidebar_items`

- **Type:** list of component names
- **Default:** `"page-toc"`
- **Meaning:** The components in the secondary sidebar. The sidebar is left out when the list is
  empty, and on the search page and every index page.

### `footer_start`

- **Type:** list of component names
- **Default:** `"copyright, sphinx-version"`
- **Meaning:** The components at the start of the footer.

### `footer_center`

- **Type:** list of component names
- **Default:** empty
- **Meaning:** The components in the middle of the footer.

### `footer_end`

- **Type:** list of component names
- **Default:** `"theme-version"`
- **Meaning:** The components at the end of the footer.

## Pygments styles

By default code is drawn with the theme's token colours. These two options give a mode a
Pygments style instead. Sphinx's own `pygments_style` setting is not used: the theme drops
Sphinx's Pygments stylesheet from every page.

### `pygments_light_style`

- **Type:** string
- **Default:** empty, which keeps the theme's token highlighting
- **Meaning:** The name of the Pygments style code uses in light mode, such as `"friendly"`.
  The style follows the mode the page shows, and the system's colour scheme until the page
  has a mode. A name that is not a Pygments style is reported as a warning of type `daisyui`
  and subtype `pygments`, and the mode keeps the theme's token highlighting.

### `pygments_dark_style`

- **Type:** string
- **Default:** empty, which keeps the theme's token highlighting
- **Meaning:** The name of the Pygments style code uses in dark mode, such as `"monokai"`. It
  follows the mode the page shows in the same way as `pygments_light_style`, and an unknown name
  is handled in the same way.

```python
html_theme_options = {
    "pygments_light_style": "friendly",
    "pygments_dark_style": "monokai",
}
```
