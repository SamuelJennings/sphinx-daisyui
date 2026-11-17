# All options

Set these in `html_theme_options` in `conf.py`.

## daisyUI

| Option | Default | What it does |
|---|---|---|
| `light_theme` | `"light"` | The daisyUI theme for light mode |
| `dark_theme` | `"dark"` | The daisyUI theme for dark mode |
| `default_mode` | `"auto"` | `"auto"` follows the reader's system. `"light"` or `"dark"` fixes the starting mode |
| `theme_picker` | off | `True` lists every daisyUI theme in the theme menu. A list names the ones to offer |

## Layout

| Option | Default | What it does |
|---|---|---|
| `navbar_start` | `["navbar-logo"]` | Components at the start of the navbar |
| `navbar_center` | `[]` | Components in the middle. `["navbar-nav"]` adds the top-level pages |
| `navbar_end` | `["version-switcher", "theme-switcher", "navbar-icon-links"]` | Components at the end |
| `navbar_persistent` | `["search-button-field"]` | Components that stay in the navbar on a phone |
| `article_header_start` | `["breadcrumbs"]` | Above the page title |
| `secondary_sidebar_items` | `["page-toc"]` | The column on the right |
| `footer_start`, `footer_center`, `footer_end` | copyright, Sphinx version, theme version | The footer |
| `show_prev_next` | `True` | Links to the previous and next page |
| `back_to_top_button` | `True` | A button that appears when you scroll back up a long page |

## Navigation

| Option | Default | What it does |
|---|---|---|
| `navigation_depth` | `4` | How many levels the sidebar holds |
| `show_nav_level` | `1` | How many levels start open |
| `collapse_navigation` | `False` | Leave out the pages that aren't on the way to the current one |
| `show_toc_level` | `2` | How many levels of the page's headings the right-hand column shows |
| `navigation_with_keys` | `False` | Arrow keys move to the previous and next page |
