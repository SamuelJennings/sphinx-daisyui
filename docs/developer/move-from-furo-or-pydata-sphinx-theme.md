# Move from Furo or pydata-sphinx-theme

This theme has its own options and does not read another theme's. An option written for Furo or
pydata-sphinx-theme does nothing here, so a site moving across changes its `conf.py` once. This
page lists which option of this theme does the job each of theirs did. The options themselves are
described in the [options reference](../reference/options.md).

Change the theme first:

```python
html_theme = "daisyui"
```

## From Furo

| Furo | This theme |
|---|---|
| `light_logo` and `dark_logo` | `logo`, with `image_light` and `image_dark` |
| `sidebar_hide_name` | `logo` with an image and no `text`, which shows no name |
| `announcement` | `announcement`, with the same meaning |
| `navigation_with_keys` | `navigation_with_keys`, with the same meaning |
| `top_of_page_buttons` | `top_of_page_buttons`, with the same meaning |
| `source_repository`, `source_branch` and `source_directory` | The same three options, with the same meaning |
| `source_edit_link` and `source_view_link` | Not read. The links are built from the three options above |
| `light_css_variables` and `dark_css_variables` | Not read. Choose a daisyUI theme with `light_theme` and `dark_theme` |
| `footer_icons` | `icon_links`, with `navbar-icon-links` in `footer_end` |
| The sidebar templates in `html_sidebars` | Not read. `primary_sidebar_end` adds components to the sidebar |
| `pygments_style` and `pygments_dark_style` | `pygments_light_style` and `pygments_dark_style` |

The `layout` option arranges the page, and [the layout code](../reference/layout-code.md) explains
how to write one.

## From pydata-sphinx-theme

| pydata-sphinx-theme | This theme |
|---|---|
| `logo` | `logo`, with the same keys |
| `github_url`, `gitlab_url`, `bitbucket_url` and `twitter_url` | An entry of `icon_links` for each |
| `icon_links` with a Font Awesome name such as `fa-brands fa-github` | `icon_links` with the name of a bundled icon, such as `github` |
| `external_links`, `header_links_before_dropdown` and `header_dropdown_text` | The same three options |
| `navbar_start`, `navbar_center`, `navbar_end` and `navbar_persistent` | The same four options, with this theme's component names |
| `article_header_start`, `article_header_end`, `article_footer_items` and `content_footer_items` | The same four options |
| `primary_sidebar_end` and `secondary_sidebar_items` | The same two options |
| `footer_start`, `footer_center` and `footer_end` | The same three options |
| `switcher`, `check_switcher` and `show_version_warning_banner` | The same three options |
| `use_edit_page_button` with `html_context` | `top_of_page_buttons`, with `source_repository`, `source_branch` and `source_directory` |
| `show_toc_level`, `show_nav_level`, `navigation_depth` and `collapse_navigation` | The same four options |
| `show_prev_next`, `back_to_top_button` and `navigation_with_keys` | The same three options |
| `search_bar_text` and `search_as_you_type` | The same two options |
| `announcement` | `announcement` |
| `pygment_light_style` and `pygment_dark_style` | `pygments_light_style` and `pygments_dark_style` |
| `default_mode` in `html_context` | `default_mode` in `html_theme_options` |
| `analytics`, `shorten_urls`, `surface_warnings` and `templates_skip_empty_check` | Not read |
| Colour variables such as `--pst-color-primary` | Not read. Choose a daisyUI theme |

`navbar-nav`, `navbar-icon-links`, `theme-switcher` and `version-switcher` are components of
this theme under those names. [Components](../reference/components.md) lists every component.
