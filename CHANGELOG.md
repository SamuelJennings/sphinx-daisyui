# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[semantic versioning](https://semver.org/).

## [Unreleased]

### Added

- Edit and view links: the `source_repository`, `source_branch`, `source_directory` and
  `top_of_page_buttons` options, which draw edit and view buttons beside the breadcrumbs for
  GitHub, GitLab and Bitbucket repositories, and the `edit-this-page` component.
- Icon links: the `icon_links` and `icon_links_label` options and the `navbar-icon-links`
  component, which link a site's accounts as bundled icons or images in the navbar or the
  footer, and a build-time warning for an unknown icon name.
- A version switcher, drawn by the `version-switcher` component from a `switcher.json` file, the
  `switcher`, `check_switcher` and `show_version_warning_banner` options, and a build-time
  warning when the file cannot be used.
- A search dialog, opened by the `search-button-field` component or by Ctrl+K, ⌘K or `/`,
  that lists pages, sections and API names as the reader types, and the `search_bar_text`,
  `disable_search` and `search_as_you_type` options.
- The `light_theme`, `dark_theme`, `default_mode` and `theme_picker` options, and the
  `theme-switcher` component, which lets a reader choose light, dark, the system's setting or a
  theme by name.
- The `daisyui` HTML theme, registered with Sphinx, with its stylesheet compiled from Tailwind
  CSS 4 and daisyUI 5 and shipped in the package.
- The `layout` option, which arranges the header, sidebars, page and footer with one code, and
  thirteen component lists that fill them, with the `copyright`, `sphinx-version`,
  `theme-version`, `last-updated` and `navbar-logo` components.
- The reader's page: a drawer for the navigation on narrow windows, a sticky header, a skip link,
  and text that translates with Sphinx's `language` setting.
- The brand: a logo for each colour mode and an optional name, set with the `logo` option
  or Sphinx's `html_logo`.
- Previous and next links at the end of each page, the `show_prev_next` option, a back to top
  button, the `back_to_top_button` option, and the `navigation_with_keys` option, which turns on
  Sphinx's arrow-key navigation.
- An announcement banner across every page, set with the `announcement` option as text, HTML or
  an address to fetch, and the `sticky_banners` option, which keeps it with the header.
- The site navigation in the primary sidebar, with a toggle for each entry that has children and
  the current page marked, and breadcrumbs above each page that lead from the front page to it.
- The `navbar-nav` component, which draws the site's top-level sections and the `external_links`
  as header links, with a menu for those past `header_links_before_dropdown` named by
  `header_dropdown_text`, the `navbar_align` option, the sections at the head of the drawer, and a
  primary sidebar that lists only the current section when it is in `navbar_center`.
- The page body's styles: headings, text, lists, quotes, admonitions and version notes with
  their icons, code, tables, figures, equations, API entries and the sphinx-design and
  sphinx-copybutton markup, drawn from daisyUI's tokens in every theme and mode, with wide tables
  and display equations in focusable scroll regions.
- The `page-toc` component, which lists the headings of the page under On this page and marks
  the one being read, a closed disclosure with the same list above the page on narrow windows,
  and the `show_toc_level` option.
- The `pygments_light_style` and `pygments_dark_style` options, which give code a Pygments style for each
  colour mode, and documentation of the `daisy-sphinx-escape` class, which leaves raw HTML to daisyUI's
  own styles, and of the daisyUI components compiled in for it.
