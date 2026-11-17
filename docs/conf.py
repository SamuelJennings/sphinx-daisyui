"""Sphinx configuration for the sphinx-daisyui documentation, built with the theme itself.

Set DAISY_LAYOUT to build these pages with another layout code, to compare them.
"""

import os

project = "sphinx-daisyui"
author = "Sam Jennings"
copyright = "2026, Sam Jennings"

extensions = ["myst_parser"]
myst_heading_anchors = 3

html_theme = "daisyui"
html_title = "sphinx-daisyui"
html_last_updated_fmt = "%d %B %Y"
html_theme_options = {
    "footer_start": ["copyright", "last-updated"],
    "footer_end": ["sphinx-version", "theme-version"],
}

if os.environ.get("DAISY_LAYOUT"):
    html_theme_options["layout"] = os.environ["DAISY_LAYOUT"]

# docs/agents/ and the brainstorm are notes for maintainers, not part of the site.
exclude_patterns = ["_build", "agents", "brainstorm.md"]
