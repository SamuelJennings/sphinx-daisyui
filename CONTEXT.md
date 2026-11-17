# sphinx-daisyui — Context

The words this repository uses, what each one means here, and the words it avoids. Issues, pull
requests, code and tests use these terms.

## Glossary

**Site**
A Sphinx project that sets `html_theme = "daisyui"`. Its author configures it in `conf.py`.
_Avoid_: project, docs (both mean other things).

**Theme**
This package's Sphinx HTML theme, named `daisyui`. On its own, "theme" always means this.
_Avoid_: skin, template.

**daisyUI theme**
One of daisyUI's named colour sets, such as `light`, `dark` or `nord`. A site picks one for each
mode. _Avoid_: colour scheme, palette, theme on its own.

**Mode**
Light, dark or auto (follow the reader's system setting). The reader switches it in the navbar.
A mode selects a daisyUI theme. _Avoid_: dark theme, appearance.

**Token**
A daisyUI colour variable, such as `base-100`, `primary` or `base-content`, and the Tailwind
utilities built on it. Every colour the theme draws is a token. _Avoid_: colour variable, CSS var.

**Theme option**
A key of `html_theme_options`. A **borrowed option** is one Furo or pydata-sphinx-theme defines
and the theme accepts under the same name. An **own option** is one only this theme defines, such
as `layout`. _Avoid_: setting (Sphinx's word for a `conf.py` value), config key.

**Component**
A template under `components/` that a site places by name in a component list such as
`navbar_end` or `footer_start`, as pydata-sphinx-theme does. Furo's sidebar templates named in
`html_sidebars` are components too. _Avoid_: partial, widget, snippet.

**Area**
One of the five regions of a page: header, primary sidebar, main, secondary sidebar and footer.
The page is one CSS grid with these named areas. _Avoid_: region, panel, column.

**Primary sidebar**
The left area, holding the site navigation. "Left sidebar" in text for readers. _Avoid_: nav
panel, drawer (the drawer is how it shows on a phone).

**Secondary sidebar**
The right area, holding "On this page" and page tools. "Right sidebar" in text for readers.
_Avoid_: TOC column.

**Drawer**
The primary sidebar on a narrow screen, opened from the navbar's menu button over the page.
_Avoid_: off-canvas, mobile menu.

**Layout code**
The value of the `layout` option: three groups of three letters in Quasar's notation, such as
`hHh LpR lff`. Each letter names the area in that cell of the grid, and upper case means the area
stays in place as the page scrolls. _Avoid_: layout string, view code.

**Sticky**
Staying in place while the page scrolls, written as an upper-case letter in the layout code.
_Avoid_: fixed (except in Quasar's own documentation), pinned.

**Site navigation**
The toctree of the whole site, drawn as a menu with open and close toggles, in the primary
sidebar. _Avoid_: sidebar tree, global TOC.

**On this page**
The headings of the page being read, in the secondary sidebar, or above the page on a narrow
screen. _Avoid_: local TOC, page TOC, outline.

**Header links**
Top-level sections of the site shown across the navbar, as pydata-sphinx-theme does when a site
places `navbar-nav`. _Avoid_: tabs, top nav.

**Page body**
The HTML Sphinx writes for a page's content. The page-body styles draw it: headings, admonitions,
code, tables, lists and the markup of the extensions the theme supports. _Avoid_: article content,
prose.

**Admonition**
A block written with one of the admonition directives (`note`, `warning`, `tip` and the rest).
Named after the directive. _Avoid_: notice, callout, alert.

**Escape class**
`daisy-sphinx-escape`. Raw HTML inside an element with this class is left out of the page-body
styles and keeps daisyUI's own look. _Avoid_: raw block, unstyled block.

**Announcement**
A banner across the top of every page, from text or from a URL that returns HTML. _Avoid_:
banner on its own, notice.

**Version switcher**
The navbar menu that lists the site's published versions from a `switcher.json` file, as
pydata-sphinx-theme defines it. _Avoid_: version picker, version dropdown.

**Icon link**
A link shown as an icon in the navbar or footer, such as the site's repository or its chat.
Icons are inline SVG bundled in the package. _Avoid_: social link, badge.

**Search dialog**
The dialog opened with Ctrl+K, ⌘K or `/`, which lists results from Sphinx's own search index as
the reader types. Sphinx's full search page stays, restyled. _Avoid_: search modal, quick search.

## Relationships

- A **site** chooses the **theme**, and a **daisyUI theme** for each **mode**.
- The **layout code** places the five **areas**. The **primary sidebar** becomes the **drawer**
  on a narrow screen.
- **Components** fill the header, sidebars and footer, in the order the site's component lists
  give.
- Every colour on a page is a **token**, so changing the daisyUI theme recolours everything.
