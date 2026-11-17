# Link the sources

A site links its repository, its package index and its other accounts as icons, in the navbar
or in the footer. It also links each page to its source file, with edit and view buttons above
the page and a link in the page tools.

## Link the repository and other accounts

1. Set `icon_links` in `html_theme_options` in `conf.py`, one dict for each link:

   ```python
   html_theme_options = {
       "icon_links": [
           {
               "name": "GitHub",
               "url": "https://github.com/SamuelJennings/sphinx-daisyui",
               "icon": "github",
           },
           {
               "name": "PyPI",
               "url": "https://pypi.org/project/sphinx-daisyui",
               "icon": "pypi",
           },
       ],
   }
   ```

   The `icon` is the name of one of the icons the theme bundles. [Options](../reference/options.md)
   lists them. An unknown name makes the build warn, naming the entry and the icon, and the
   link is drawn with a generic link icon.

2. To draw an image instead, set `type` and give the image as `icon`:

   ```python
   {
       "name": "Chat",
       "url": "https://chat.example.org",
       "icon": "chat.svg",
       "type": "local",
   }
   ```

   With `"type": "local"`, the `icon` is a file in a directory listed in `html_static_path`,
   written relative to `_static` or starting `_static/`. With `"type": "url"`, it is the
   address of an image.

3. Name the list for screen readers with `icon_links_label`:

   ```python
   html_theme_options = {
       "icon_links_label": "Project accounts",
   }
   ```

The default navbar now shows each link as an icon, and the list is named for screen readers.

## Show the links in the footer

1. Name `navbar-icon-links` in `footer_end`, or in any other component list:

   ```python
   html_theme_options = {
       "footer_end": ["navbar-icon-links", "theme-version"],
   }
   ```

2. Build the site.

The footer now carries the same links. [Components](../reference/components.md) describes the
component.

## Set up the edit and view buttons

1. Set the repository, the branch and the folder holding the source in `html_theme_options`:

   ```python
   html_theme_options = {
       "source_repository": "https://github.com/SamuelJennings/sphinx-daisyui",
       "source_branch": "main",
       "source_directory": "docs/",
   }
   ```

   The theme builds each page's address from the host named in `source_repository`: GitHub,
   GitLab or Bitbucket. On any other host the pages get no edit or view link, and the build
   does not warn.

2. Choose the buttons with `top_of_page_buttons`. The default is `["edit"]`. List `view` as
   well to add a button to the file as the host shows it, in the order you want them:

   ```python
   html_theme_options = {
       "top_of_page_buttons": ["edit", "view"],
   }
   ```

   An empty list shows no button.

3. Build the site.

Each page now has the buttons beside its breadcrumbs, and each links to that page's own source
file, whatever its suffix and however deep it is. [Options](../reference/options.md) describes
each value.

## Link the edit address in the sidebar

1. Name `edit-this-page` in `secondary_sidebar_items`, after the page's contents:

   ```python
   html_theme_options = {
       "secondary_sidebar_items": ["page-toc", "edit-this-page"],
   }
   ```

2. Build the site.

The sidebar now carries an Edit this page link to the same address as the edit button.
[Components](../reference/components.md) describes the component.

## Link Sphinx's copy of the source

1. Name `sourcelink` in `secondary_sidebar_items`:

   ```python
   html_theme_options = {
       "secondary_sidebar_items": ["page-toc", "sourcelink"],
   }
   ```

2. Leave `html_show_sourcelink` and `html_copy_source` on. Their default is on.
3. Build the site.

Each page now carries a Show source link to Sphinx's copy of its source under `_sources`.
With either setting off, nothing is drawn. [Components](../reference/components.md) describes
the component.
