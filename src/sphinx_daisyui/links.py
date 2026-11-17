"""The links a site shows beside its pages: its accounts as icons."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from markupsafe import Markup
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

from .icons import ICONS
from .options import ThemeOptions

LOGGER = logging.getLogger(__name__)
IMAGE_TYPES = ("url", "local")


@dataclass(frozen=True)
class IconLink:
    """One link drawn as an icon.

    Attributes:
        name: The link's accessible name and tooltip.
        url: Where the link leads.
        image: The markup drawn inside the link, safe to print unescaped.
    """

    name: str
    url: str
    image: Markup


class IconLinks:
    """The links a site lists in its ``icon_links`` option."""

    @staticmethod
    def entries(options: ThemeOptions) -> list[dict[str, Any]]:
        """Read the entries that have an address.

        Args:
            options: The site's theme options.

        Returns:
            The dicts of ``icon_links`` whose ``url`` is not empty, in order.
        """
        return [entry for entry in options.records("icon_links") if entry.get("url")]

    @classmethod
    def from_options(
        cls, options: ThemeOptions, pathto: Callable[..., str]
    ) -> list[IconLink]:
        """Read the links to draw on one page.

        Args:
            options: The site's theme options.
            pathto: Sphinx's ``pathto`` for the page, which resolves a local image.

        Returns:
            One link for each entry with an address, named by its ``name`` or
            else its address. An entry of type ``url`` or ``local`` carries an
            image, any other entry the bundled icon it names.
        """
        found = []
        for entry in cls.entries(options):
            url = str(entry["url"])
            icon = str(entry.get("icon") or "")
            kind = entry.get("type")
            if kind == "url":
                image = cls.image(icon)
            elif kind == "local":
                image = cls.image(options.static_url(icon, pathto))
            else:
                image = ICONS.svg(icon)
            found.append(IconLink(str(entry.get("name") or url), url, image))
        return found

    @staticmethod
    def image(address: str) -> Markup:
        """Draw an image icon.

        Args:
            address: Where the image is.

        Returns:
            One ``<img>`` element, with the address escaped.
        """
        return Markup('<img alt="" class="size-5 rounded-sm" src="{}">').format(address)

    @classmethod
    def problems(cls, options: ThemeOptions) -> list[str]:
        """Find what is wrong with the ``icon_links`` option.

        Args:
            options: The site's theme options.

        Returns:
            One message when the option is a string, and one for each entry with
            an address whose bundled icon does not exist.
        """
        if isinstance(options.values.get("icon_links"), str):
            return ["The theme option icon_links is text. Give it a list of dicts."]
        return [
            f"The icon_links entry {entry.get('name') or entry['url']!r} names the "
            f"icon {entry.get('icon')!r}, which the theme does not bundle. "
            "It is drawn with the link icon."
            for entry in cls.entries(options)
            if entry.get("type") not in IMAGE_TYPES
            and entry.get("icon") not in ICONS.by_name
        ]


def check_icon_links(app: Sphinx) -> None:
    """Warn about each fault in the ``icon_links`` option.

    Args:
        app: The Sphinx application building the site.
    """
    builder = app.builder
    if not isinstance(builder, StandaloneHTMLBuilder):
        return
    if app.config.html_theme != "daisyui":
        return
    options = ThemeOptions(builder.theme.get_options(app.config.html_theme_options))
    for problem in IconLinks.problems(options):
        LOGGER.warning(problem, type="daisyui", subtype="icon_links")
