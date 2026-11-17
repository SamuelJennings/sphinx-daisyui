"""A Sphinx theme drawn with daisyUI.

Sphinx finds the theme through the ``sphinx.html_themes`` entry point, so a site
selects it with ``html_theme = "daisyui"`` and nothing in ``extensions``.
"""

from pathlib import Path

from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging
from sphinx.util.typing import ExtensionMetadata

from .layout import LayoutCodeError
from .options import ThemeOptions

LOGGER = logging.getLogger(__name__)
THEME_DIR = Path(__file__).parent / "theme" / "daisyui"


def setup(app: Sphinx) -> ExtensionMetadata:
    """Register the ``daisyui`` HTML theme.

    Args:
        app: The Sphinx application building the site.

    Returns:
        The extension's metadata, declaring it safe for parallel builds.
    """
    app.add_html_theme("daisyui", str(THEME_DIR))
    app.connect("builder-inited", check_layout)
    return {"parallel_read_safe": True, "parallel_write_safe": True}


def check_layout(app: Sphinx) -> None:
    """Stop the build, with the reason alone, when the layout code is wrong.

    Sphinx prints a crash report with a traceback for every exception that
    leaves a build, and ``SystemExit`` is the one it lets through.

    Args:
        app: The Sphinx application building the site.

    Raises:
        SystemExit: With code 2, after logging the error, when the layout code
            is wrong.
    """
    builder = app.builder
    if not isinstance(builder, StandaloneHTMLBuilder):
        return
    if app.config.html_theme != "daisyui":
        return
    options = ThemeOptions(builder.theme.get_options(app.config.html_theme_options))
    try:
        options.layout()
    except LayoutCodeError as error:
        LOGGER.error(str(error))  # noqa: TRY400
        raise SystemExit(2) from None
