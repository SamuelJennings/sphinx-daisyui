# Put the sections in the header

By default the primary sidebar lists the whole site. A site with several large sections can move
its top-level pages into the header, and leave the sidebar to the section being read.

## Place the sections in the header

1. Name `navbar-nav` in `navbar_center` in `html_theme_options` in `conf.py`:

   ```python
   html_theme_options = {
       "navbar_center": ["navbar-nav"],
   }
   ```

2. Build the site.

The header now holds a link to each top-level page of the site's table of contents, and the link
to the section being read is marked. The primary sidebar lists only the pages of that section,
with the same toggles and marks as before, and nothing on a page that is in no section, such as
the front page. On a narrow window, the drawer lists every header link above the sidebar's pages.

Named in another list, such as `navbar_end`, `navbar-nav` draws the links there and the sidebar
keeps the whole site.

## Link to other sites

1. List each link with a `name` and a `url` in `external_links`:

   ```python
   html_theme_options = {
       "external_links": [
           {"name": "Source", "url": "https://github.com/example/project"},
       ],
   }
   ```

The links follow the site's sections, in the order given, and are marked as leading outside the
site.

## Choose how many links are shown

1. Set `header_links_before_dropdown` to the number of links to show:

   ```python
   html_theme_options = {
       "header_links_before_dropdown": 3,
       "header_dropdown_text": "More pages",
   }
   ```

2. Optionally name the menu with `header_dropdown_text`. Without it the menu is labelled "More"
   in the site's language.

The rest of the links are in a menu. A reader opens it from the keyboard by focusing its control,
moves through its links with Tab and Shift+Tab, and closes it with Escape. When the current
section is one of the links in the menu, the menu's control is marked as well.

## Line the links up

1. Set `navbar_align` to `content`, `left` or `right`:

   ```python
   html_theme_options = {
       "navbar_align": "left",
   }
   ```

With `content`, the default, the first link starts where the page's text starts. `left` starts the
links at the start of the navbar's free space, and `right` ends them at its end. The setting
applies on screens 64rem wide and up. [Options](../reference/options.md) lists each option.

## Why the sidebar changes

Header links and the sidebar share one table of contents. When the top level is in the header, the
sidebar would repeat it, so it shows what is below the current section. A site that wants the
header links and a whole-site sidebar names `navbar-nav` in a list other than `navbar_center`.
