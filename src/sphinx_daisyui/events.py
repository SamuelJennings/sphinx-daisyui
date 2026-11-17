"""The theme's event handlers: the layout check and the page context."""

from importlib.metadata import metadata, version
from typing import Any

from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

from .brand import Brand
from .icons import Icons
from .layout import LayoutCodeError
from .options import ThemeOptions

LOGGER = logging.getLogger(__name__)
ICONS = Icons()
VERSION = version("sphinx-daisyui")
COMPONENT_OPTIONS = (
    "navbar_start",
    "navbar_center",
    "navbar_end",
    "navbar_persistent",
    "article_header_start",
    "article_header_end",
    "article_footer_items",
    "content_footer_items",
    "primary_sidebar_end",
    "footer_start",
    "footer_center",
    "footer_end",
)


def project_url(label: str) -> str:
    """Find one of the package's project URLs by its label.

    Args:
        label: The label the URL has under ``[project.urls]``.

    Returns:
        The URL, or an empty string when the package has none by that label.
    """
    for entry in metadata("sphinx-daisyui").get_all("Project-URL") or []:
        name, _, url = entry.partition(", ")
        if name.lower() == label:
            return str(url)
    return ""


REPOSITORY = project_url("repository")


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


def add_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: object,
) -> None:
    """Give the templates the ``daisy`` context they all read.

    Args:
        app: The Sphinx application building the site.
        pagename: The page being rendered.
        templatename: The template rendering it.
        context: The page's template context, changed in place.
        doctree: The page's document tree, which this does not read.
    """
    if app.config.html_theme != "daisyui":
        return
    options = ThemeOptions.from_context(context)
    context["daisy"] = {
        "layout": options.layout(),
        "brand": Brand.from_options(options, context),
        "icon": ICONS.svg,
        "version": VERSION,
        "repository": REPOSITORY,
        **{name: options.components(name) for name in COMPONENT_OPTIONS},
        "secondary": options.components("secondary_sidebar_items"),
    }
