# Arrange the page

The theme draws a header, a primary sidebar, the page, a secondary sidebar and a footer. A site
chooses where they sit, and what each one holds, with theme options.

## Set the layout

1. Set `layout` in `html_theme_options` in `conf.py`:

   ```python
   html_theme_options = {
       "layout": "lHh LpR lff",
   }
   ```

2. Build the site. A code that is not a layout code stops the build with a message saying what
   a code needs.

The primary sidebar now reaches the top-left corner. [The layout code](../reference/layout-code.md)
describes each letter.

## Fill a component list

1. Choose the list for where the component goes, from [Options](../reference/options.md).
2. Name the components, in the order they should appear:

   ```python
   html_theme_options = {
       "footer_start": ["copyright", "last-updated"],
       "footer_end": ["sphinx-version", "theme-version"],
   }
   ```

3. Set `html_last_updated_fmt`, so that `last-updated` has a date to show:

   ```python
   html_last_updated_fmt = "%d %B %Y"
   ```

The footer now shows the components in that order. A component whose Sphinx setting is off draws
nothing. [Components](../reference/components.md) names the setting for each one.

## Show a logo

1. Put the logo files in a directory listed in `html_static_path` in `conf.py`.
2. Name them in `html_theme_options`, in the shape of the theme you are coming from. Furo's:

   ```python
   html_theme_options = {
       "light_logo": "logo-light.svg",
       "dark_logo": "logo-dark.svg",
   }
   ```

   pydata-sphinx-theme's:

   ```python
   html_theme_options = {
       "logo": {
           "image_light": "logo-light.svg",
           "image_dark": "logo-dark.svg",
           "alt_text": "Project name",
           "link": "https://example.org/",
       },
   }
   ```

   A site with one logo for both modes sets Sphinx's `html_logo` instead:

   ```python
   html_logo = "_static/logo.svg"
   ```

The brand now shows the logo for the reader's colour mode, and the dark logo falls back to the
light one. Add `"text"` to `logo` to print a name beside the images. [Options](../reference/options.md)
describes each option.

## Add your own component

1. Add a directory for your templates to `templates_path` in `conf.py`, if the site has none:

   ```python
   templates_path = ["_templates"]
   ```

2. Write the template as `_templates/status.html`:

   ```html
   <p>Status: stable</p>
   ```

3. Name it in a list:

   ```python
   html_theme_options = {
       "footer_center": "status",
   }
   ```

The footer now shows the template. A name that matches no template draws nothing and raises no
warning, so a misspelt name leaves a gap and no message.

## Moving between pages

Each page ends with links to the previous and the next page in the table of contents. To turn
them off, set `show_prev_next` to `False`.

To let readers move with the left and right arrow keys, set `navigation_with_keys` to `True`:

```python
html_theme_options = {
    "navigation_with_keys": True,
}
```

A button that scrolls back to the top appears while the reader scrolls up, far down a page. Set
`back_to_top_button` to `False` to remove it. All three options are described in
[Options](../reference/options.md).

## Put an announcement across every page

Set `announcement` to the text of a banner that appears at the top of every page:

```python
html_theme_options = {
    "announcement": "Version 2 is out. <a href='/changes.html'>See what changed</a>",
}
```

The text may hold HTML of your own, and the theme prints it as written. To keep the banner in
one file, set `announcement` to an address that starts with `http://` or `https://`. The page
script fetches that address when a reader opens a page and puts the HTML it returns in the banner.
The banner is removed when the address fails, cannot be reached or returns nothing.

To keep the banner in view with the header, set `sticky_banners` to `True`:

```python
html_theme_options = {
    "sticky_banners": True,
}
```

Both options are described in [Options](../reference/options.md).

## How the page behaves for a reader

The browser changes the page as the window changes:

- Below 64rem wide, the primary sidebar becomes a drawer. A button in the header opens it, and a
  link in it, the close button, a press outside it or the Escape key closes it.
- From 80rem wide, the secondary sidebar appears beside the page.
- An area marked with an upper-case letter in the layout code stays in view while the page scrolls,
  and the sticky areas sit below the header, whatever height it has.
- Below 40rem wide, the items in `navbar_end` move into the drawer.
- A skip link is the first thing a keyboard reader reaches, and it jumps to the page.

The search and index pages leave out the secondary sidebar, as they have no headings of their own.
