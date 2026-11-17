# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[semantic versioning](https://semver.org/).

## [Unreleased]

### Added

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
- The `page-toc` component, which lists the headings of the page under On this page and marks
  the one being read, a closed disclosure with the same list above the page on narrow windows,
  and the `show_toc_level` option.
