"""Sphinx configuration for the sphinx-daisyui documentation, built with the theme itself."""

project = "sphinx-daisyui"
author = "Sam Jennings"
copyright = "2026, Sam Jennings"

extensions = ["myst_parser"]
myst_heading_anchors = 3

html_theme = "daisyui"
html_title = "sphinx-daisyui"

# docs/agents/ and the brainstorm are notes for maintainers, not part of the site.
exclude_patterns = ["_build", "agents", "brainstorm.md"]
