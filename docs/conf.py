"""Sphinx configuration for the sphinx-daisyui documentation.

The documentation is built with the theme itself.

Set DAISY_LAYOUT to build these pages with another layout code, and
DAISY_NAVBAR_CENTER to build them with a component in the middle of the navbar,
and DAISY_FOOTER_ICONS to build them with the icon links in the footer, to compare
them.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project = "sphinx-daisyui"
author = "Sam Jennings"
copyright = "2026, Sam Jennings"

extensions = [
    "layout_playground",
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
myst_heading_anchors = 3
# The kitchen sink links one name into the Python documentation.
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "dollarmath",
    "fieldlist",
    "substitution",
]
todo_include_todos = True
autodoc_member_order = "bysource"

html_theme = "daisyui"
html_title = "sphinx-daisyui"
html_last_updated_fmt = "%d %B %Y"
html_static_path = ["_static"]
html_favicon = "_static/logo-light.svg"
html_theme_options = {
    "logo": {
        "text": "sphinx-daisyui",
        "image_light": "logo-light.svg",
        "image_dark": "logo-dark.svg",
    },
    "footer_start": ["copyright", "last-updated"],
    "footer_end": ["sphinx-version", "theme-version"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/SamuelJennings/sphinx-daisyui",
            "icon": "github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/sphinx-daisyui",
            "icon": "pypi",
        },
    ],
    "source_repository": "https://github.com/SamuelJennings/sphinx-daisyui",
    "source_branch": "main",
    "source_directory": "docs/",
    "top_of_page_buttons": ["edit"],
    "secondary_sidebar_items": ["page-toc", "sourcelink"],
    "navigation_with_keys": True,
    "theme_picker": True,
    "switcher": {"json_url": "_static/switcher.json", "version_match": "dev"},
}

if os.environ.get("DAISY_LAYOUT"):
    html_theme_options["layout"] = os.environ["DAISY_LAYOUT"]
    html_theme_options["announcement"] = (
        f'This build uses <code>layout = "{os.environ["DAISY_LAYOUT"]}"</code>. '
        '<a class="link" href="/reference/layout-code.html">Compare the layouts</a>'
    )

if os.environ.get("DAISY_NAVBAR_CENTER"):
    html_theme_options["navbar_center"] = [os.environ["DAISY_NAVBAR_CENTER"]]

if os.environ.get("DAISY_FOOTER_ICONS"):
    html_theme_options["footer_end"] = [
        *html_theme_options.get("footer_end", []),
        "navbar-icon-links",
    ]

if os.environ.get("DAISY_SOURCE_SIDEBAR"):
    html_theme_options["secondary_sidebar_items"] = [
        "page-toc",
        "edit-this-page",
        "sourcelink",
    ]

# docs/agents/ and the brainstorm are notes for maintainers, not part of the site.
exclude_patterns = ["_build", "adr", "agents", "brainstorm.md"]
