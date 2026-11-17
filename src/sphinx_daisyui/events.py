"""The theme's event handlers: the layout check and the page context."""

from importlib.metadata import metadata, version
from typing import Any

from markupsafe import Markup
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

from .brand import Brand
from .icons import ICONS
from .layout import LayoutCodeError
from .navigation import HeaderLinks, PageContents, SiteNavigation
from .options import ThemeOptions

LOGGER = logging.getLogger(__name__)
VERSION = version("sphinx-daisyui")
NAVBAR_NAV = "navbar-nav.html"
NAVBAR_ALIGNMENTS = ("content", "left", "right")
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
    "secondary_sidebar_items",
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


def is_index_page(templatename: str) -> bool:
    """Tell whether Sphinx renders a page with one of its index templates.

    Args:
        templatename: The template rendering the page.

    Returns:
        Whether the page is the search page, a domain index or a general index,
        whole or split.
    """
    return templatename in ("search.html", "domainindex.html") or (
        templatename.startswith("genindex")
    )


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
    announcement = options.text("announcement").strip()
    is_url = announcement.startswith(("http://", "https://"))
    index_page = is_index_page(templatename)
    site = SiteNavigation(
        app.env,
        pagename,
        app.builder,
        maxdepth=options.number("navigation_depth", 4),
        collapse=options.flag("collapse_navigation"),
        includehidden=options.flag("sidebar_includehidden", True),
    )
    show_nav_level = options.number("show_nav_level", 1)
    sectioned = NAVBAR_NAV in options.components("navbar_center")
    placed = any(NAVBAR_NAV in options.components(n) for n in COMPONENT_OPTIONS)
    align = options.text("navbar_align", "content")
    context["daisy"] = {
        "layout": options.layout(),
        "brand": Brand.from_options(options, context),
        "icon": ICONS.svg,
        "version": VERSION,
        "repository": REPOSITORY,
        **{name: options.components(name) for name in COMPONENT_OPTIONS},
        "show_prev_next": options.flag("show_prev_next", True),
        "back_to_top": options.flag("back_to_top_button", True),
        "sticky_banners": options.flag("sticky_banners"),
        "announcement": "" if is_url else Markup(announcement),  # noqa: S704
        "announcement_url": announcement if is_url else "",
        "sectioned": sectioned,
        "navigation": (
            site.section_menu(show_nav_level)
            if sectioned
            else site.menu(show_nav_level)
        ),
        "header": (
            HeaderLinks(
                site.top_level(),
                options.records("external_links"),
                options.number("header_links_before_dropdown", 5),
                options.text("header_dropdown_text"),
            )
            if placed
            else None
        ),
        "navbar_align": align if align in NAVBAR_ALIGNMENTS else "content",
    }
    show_toc_level = options.number("show_toc_level", 2)
    contents = PageContents(app.env, pagename, app.builder)
    context["daisy"].update(
        page_toc=Markup() if index_page else contents.markup(show_toc_level),
        page_toc_count=0 if index_page else contents.count,
        show_toc_level=show_toc_level,
    )
    if index_page:
        context["daisy"]["secondary_sidebar_items"] = []
