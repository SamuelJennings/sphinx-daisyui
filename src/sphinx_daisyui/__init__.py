"""A Sphinx theme drawn with daisyUI.

Sphinx finds the theme through the ``sphinx.html_themes`` entry point, so a site
selects it with ``html_theme = "daisyui"`` and nothing in ``extensions``.
"""

from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from .events import add_page_context, check_layout

THEME_DIR = Path(__file__).parent / "theme" / "daisyui"
LOCALE_DIR = Path(__file__).parent / "locale"


def setup(app: Sphinx) -> ExtensionMetadata:
    """Register the ``daisyui`` HTML theme.

    Args:
        app: The Sphinx application building the site.

    Returns:
        The extension's metadata, declaring it safe for parallel builds.
    """
    app.add_html_theme("daisyui", str(THEME_DIR))
    # The theme's text joins Sphinx's own domain, which is the one templates read.
    app.add_message_catalog("sphinx", str(LOCALE_DIR))
    app.connect("builder-inited", check_layout)
    app.connect("html-page-context", add_page_context)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
