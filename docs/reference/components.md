# Components

A component is a template that a [component list](options.md) names. The theme provides five.
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

## Your own components

A site adds a component by putting a template in a directory listed in `templates_path`, and
naming it in a [component list](options.md). A template named `status.html` is named `status` or
`status.html`. [Arrange the page](../developer/arrange-the-page.md) shows the steps.

A template has the page's full context, as every Sphinx template does, and the theme's own
values under `daisy`.

A name that matches no template draws nothing and raises no warning.

## Macros

`components/macros.html` holds two macros a component may import:

```jinja
{%- from 'components/macros.html' import components, icon_button with context %}
```

- `components(names)` draws each name in a list, looking in the theme's `components/` directory
  first and then in the site's templates.
- `icon_button(label, icon, tooltip="")` draws a ghost button holding the named icon. The label
  is the button's accessible name. When a tooltip is given, it shows on hover.
