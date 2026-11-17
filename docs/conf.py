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
html_static_path = ["_static"]
html_favicon = "_static/logo-light.svg"
html_theme_options = {
    "logo": {"image_light": "logo-light.svg", "image_dark": "logo-dark.svg"},
    "footer_start": ["copyright", "last-updated"],
    "footer_end": ["sphinx-version", "theme-version"],
    "navigation_with_keys": True,
}

if os.environ.get("DAISY_LAYOUT"):
    html_theme_options["layout"] = os.environ["DAISY_LAYOUT"]
    html_theme_options["announcement"] = (
        f'This build uses <code>layout = "{os.environ["DAISY_LAYOUT"]}"</code>. '
        '<a class="link" href="/reference/layout-code.html">Compare the layouts</a>'
    )

# docs/agents/ and the brainstorm are notes for maintainers, not part of the site.
exclude_patterns = ["_build", "agents", "brainstorm.md"]
