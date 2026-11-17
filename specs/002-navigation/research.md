# Research: 002-navigation

## Assumptions checked

Run on 2026-11-17 against `main` at `0ffa3a3` with Sphinx 9.2.0, on a three-page test site
(`index` → `a/index` → `a/b/leaf`, the first toctree with a caption) built with
`html_theme = "daisyui"` and an `html-page-context` handler.

| Assumption | Result |
|---|---|
| The page context's `toctree()` takes `maxdepth`, `collapse`, `includehidden` and `titles_only`, which the site navigation and header links need | Holds. Called with all four on `a/b/leaf`, it returns the toctree with the current page's entries marked `current` |
| The page context carries `parents`, which the breadcrumbs need | Holds. On `a/b/leaf` it lists `A` |
| The page context carries `toc`, the page's headings, which On this page needs | Holds. It holds the page's section heading |
| The page's doctree reaches the `html-page-context` handler, for reading headings without parsing HTML | Holds. The handler's `doctree` argument is a docutils `document` |
| Sphinx builds the site toctree as docutils nodes before rendering it, for reading the menu without parsing HTML | Holds on 9.2: `StandaloneHTMLBuilder._get_local_toctree` calls `sphinx.environment.adapters.toctree.global_toctree_for_doc`, which returns nodes, and renders them with `render_partial` afterwards. Not yet checked on Sphinx 7.4 |
| `beautifulsoup4` is available to the theme on `main` | Does not hold. `main` declares `sphinx>=7.4` only, and `bs4` is not installed. Keeping it is a new runtime dependency under Article VII |

## pydata-sphinx-theme's defaults

Read from pydata-sphinx-theme's `theme.conf` (tag `v0.16.1` and `main`): `navigation_depth = 4`,
`show_nav_level = 1`, `collapse_navigation = False`, `sidebar_includehidden = True`,
`external_links` empty, `header_links_before_dropdown = 5`, `header_dropdown_text = More`,
`navbar_align = content`, `show_toc_level = 1`, `navbar_center = navbar-nav`,
`sidebars = sidebar-nav-bs.html`. The spec keeps all but `show_toc_level`, which keeps the
prototype's 2 (decision D3), and `navbar_center`, whose default is #4's.
