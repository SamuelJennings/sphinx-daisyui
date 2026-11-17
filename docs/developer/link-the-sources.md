# Link the sources

A site links its repository, its package index and its other accounts as icons, in the navbar
or in the footer.

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
