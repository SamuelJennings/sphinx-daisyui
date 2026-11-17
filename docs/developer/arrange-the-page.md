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
