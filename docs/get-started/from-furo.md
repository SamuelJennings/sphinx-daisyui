# Switching from Furo

Change `html_theme` and keep the rest of `conf.py`. Every Furo option is read:

| Furo option | What sphinx-daisyui does with it |
|---|---|
| `light_logo`, `dark_logo` | The logo in the navbar, swapped with the mode |
| `sidebar_hide_name` | Hides the project name beside the logo |
| `announcement` | A banner above the navbar |
| `light_css_variables`, `dark_css_variables` | Mapped onto daisyUI's tokens: `color-brand-primary` becomes `--color-primary`, `font-stack` becomes `--font-sans`. Others are set as written |
| `footer_icons` | Icons at the end of the footer |
| `top_of_page_buttons` | Edit and view buttons beside the breadcrumbs |
| `source_repository`, `source_branch`, `source_directory` | Build the edit and view links |
| `source_edit_link`, `source_view_link` | Used as written, with `{filename}` filled in |
| `navigation_with_keys` | {kbd}`←` and {kbd}`→` move to the previous and next page |

Furo's `html_sidebars` templates (`sidebar/brand.html`, `sidebar/search.html`,
`sidebar/navigation.html` and the rest) are recognised, so a Furo sidebar configuration builds.
The brand and search are drawn in the navbar instead.

```{seealso}
<a href="/as-furo/">This site, built with the configuration from Furo's own documentation</a>
```
