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
- The brand: a logo for each colour mode and an optional name, set with Furo's `light_logo`,
  `dark_logo` and `sidebar_hide_name`, pydata-sphinx-theme's `logo` and `logo_link`, or Sphinx's
  `html_logo`.
