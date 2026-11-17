# Switching from pydata-sphinx-theme

Change `html_theme` and keep the rest of `conf.py`, including `html_context`.

## What carries over

`logo`
: The `text`, `image_light`, `image_dark`, `alt_text` and `link` keys.

`navbar_start`, `navbar_center`, `navbar_end`, `navbar_persistent`
: The same component names. Put `navbar-nav` in `navbar_center` and the top-level pages move
  into the header, with the sidebar showing only the section you are in, as pydata-sphinx-theme
  does.

`header_links_before_dropdown`, `header_dropdown_text`, `external_links`
: The header links and the menu that holds the rest.

`icon_links`, `github_url`, `gitlab_url`, `bitbucket_url`, `twitter_url`
: Font Awesome names such as `fa-brands fa-github` are matched to bundled icons, so there is no
  icon font to load.

`switcher`
: The same `switcher.json`. Choosing a version opens the same page in it when it exists.

`use_edit_page_button` with `github_user`, `github_repo`, `github_version` and `doc_path`
: The edit link, for GitHub, GitLab or Bitbucket.

`secondary_sidebar_items`, `article_header_start`, `article_footer_items`, `footer_start`, `footer_center`, `footer_end`
: The same component names, including templates of your own from `templates_path`.

`show_toc_level`, `show_nav_level`, `navigation_depth`, `collapse_navigation`, `show_prev_next`, `back_to_top_button`, `search_bar_text`, `announcement`, `pygments_light_style`, `pygments_dark_style`
: As in pydata-sphinx-theme.

## What is different

- pydata-sphinx-theme's own CSS variables (`--pst-color-primary` and the rest) have no effect.
  Use a daisyUI theme, or set daisyUI's variables, as [](../configure/themes.md) shows.
- `analytics` is accepted and ignored for now.

```{seealso}
<a href="/as-pydata/">This site, built with a configuration written for pydata-sphinx-theme</a>
```
