"""Documentation for sphinx-daisyui, which is also the theme's test site.

Set DAISY_PRESET=furo or DAISY_PRESET=pydata to build these pages with a
configuration written for that theme, unchanged, to see how a switch looks.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project = "sphinx-daisyui"
author = "Sam Jennings"
copyright = "2026, Sam Jennings"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
myst_enable_extensions = ["colon_fence", "deflist", "tasklist", "dollarmath", "fieldlist", "substitution"]
todo_include_todos = True
html_theme = "daisyui"
html_title = "sphinx-daisyui"
html_static_path = ["_static"]
html_favicon = "_static/logo-light.svg"
html_css_files = ["layout-playground.css"]
html_js_files = [("layout-playground.js", {"defer": "defer"})]
html_last_updated_fmt = "%d %B %Y"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
autodoc_member_order = "bysource"

preset = os.environ.get("DAISY_PRESET", "daisyui")

if preset == "furo":
    # Options as Furo's own documentation sets them.
    html_theme_options = {
        "light_logo": "logo-light.svg",
        "dark_logo": "logo-dark.svg",
        "sidebar_hide_name": False,
        "navigation_with_keys": True,
        "announcement": "This build uses a configuration written for <em>Furo</em>, unchanged.",
        "source_repository": "https://github.com/SamuelJennings/sphinx-daisyui/",
        "source_branch": "main",
        "source_directory": "docs/",
        "top_of_page_buttons": ["view", "edit"],
        "light_css_variables": {"color-brand-primary": "#7C4DFF", "color-brand-content": "#7C4DFF"},
        "dark_css_variables": {"color-brand-primary": "#B39DDB", "color-brand-content": "#B39DDB"},
        "footer_icons": [
            {
                "name": "GitHub",
                "url": "https://github.com/SamuelJennings/sphinx-daisyui",
                "html": '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path></svg>',
                "class": "",
            },
        ],
    }
elif preset == "pydata":
    # Options as pydata-sphinx-theme's documentation sets them.
    html_theme_options = {
        "logo": {"text": "sphinx-daisyui", "image_light": "logo-light.svg", "image_dark": "logo-dark.svg"},
        "github_url": "https://github.com/SamuelJennings/sphinx-daisyui",
        "icon_links": [
            {"name": "PyPI", "url": "https://pypi.org/project/sphinx-daisyui", "icon": "fa-custom fa-pypi"},
            {"name": "Mastodon", "url": "https://fosstodon.org/", "icon": "fa-brands fa-mastodon"},
        ],
        "external_links": [{"name": "daisyUI", "url": "https://daisyui.com"}],
        "header_links_before_dropdown": 3,
        "navbar_center": ["navbar-nav"],
        "navbar_end": ["version-switcher", "theme-switcher", "navbar-icon-links"],
        "use_edit_page_button": True,
        "show_toc_level": 2,
        "show_nav_level": 2,
        "navigation_depth": 3,
        "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
        "footer_start": ["copyright"],
        "footer_end": ["sphinx-version", "theme-version"],
        "switcher": {"json_url": "_static/switcher.json", "version_match": "0.1"},
        "announcement": "This build uses a configuration written for <em>pydata-sphinx-theme</em>, unchanged.",
    }
    html_context = {
        "github_user": "SamuelJennings",
        "github_repo": "sphinx-daisyui",
        "github_version": "main",
        "doc_path": "docs",
    }
else:
    html_theme_options = {
        "light_logo": "logo-light.svg",
        "dark_logo": "logo-dark.svg",
        "light_theme": "light",
        "dark_theme": "dark",
        "theme_picker": True,
        "source_repository": "https://github.com/SamuelJennings/sphinx-daisyui/",
        "source_branch": "main",
        "source_directory": "docs/",
        "top_of_page_buttons": ["edit"],
        "github_url": "https://github.com/SamuelJennings/sphinx-daisyui",
        "icon_links": [{"name": "PyPI", "url": "https://pypi.org/project/sphinx-daisyui", "icon": "pypi"}],
        "switcher": {"json_url": "_static/switcher.json", "version_match": "0.1"},
        "secondary_sidebar_items": ["page-toc", "sourcelink"],
        "footer_start": ["copyright", "last-updated"],
        "footer_end": ["sphinx-version", "theme-version"],
        "navigation_with_keys": True,
    }

# DAISY_LAYOUT builds these pages with another layout code, to compare them.
if os.environ.get("DAISY_LAYOUT"):
    html_theme_options["layout"] = os.environ["DAISY_LAYOUT"]
    html_theme_options["announcement"] = (
        f'This build uses <code>layout = "{os.environ["DAISY_LAYOUT"]}"</code>. '
        '<a class="link" href="/configure/layout-code.html">Compare the layouts</a>'
    )
