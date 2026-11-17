"""The links a site shows beside its pages: its accounts and its sources."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

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


@dataclass(frozen=True)
class SourceHost:
    """The address forms of one host that holds a site's source files.

    Attributes:
        edit: Where a page's source is edited, a ``str.format`` template taking
            ``repo``, ``branch`` and ``path``.
        view: Where a page's source is read, a template taking the same names.
    """

    edit: str
    view: str

    @classmethod
    def for_repository(cls, address: str) -> "SourceHost | None":
        """Find the host a repository lives on.

        Args:
            address: The repository's address.

        Returns:
            The host's address forms, or ``None`` when the address is not on a
            host in ``HOSTS``. A leading ``www.`` and the case of the name are
            ignored.
        """
        host = (urlsplit(address).hostname or "").removeprefix("www.")
        return HOSTS.get(host)


HOSTS = {
    "github.com": SourceHost(
        "{repo}/edit/{branch}/{path}", "{repo}/blob/{branch}/{path}"
    ),
    "gitlab.com": SourceHost(
        "{repo}/-/edit/{branch}/{path}", "{repo}/-/blob/{branch}/{path}"
    ),
    "bitbucket.org": SourceHost(
        "{repo}/src/{branch}/{path}?mode=edit", "{repo}/src/{branch}/{path}"
    ),
}
BUTTONS = ("edit", "view")


@dataclass(frozen=True)
class SourceLinks:
    """The addresses of one page's source, each empty when unknown.

    Attributes:
        edit: Where the page's source file is edited in its repository.
        view: Where the page's source file is read in its repository.
        source: Where Sphinx's copy of the page's source is.
    """

    edit: str
    view: str
    source: str

    @classmethod
    def from_options(
        cls, options: ThemeOptions, context: Mapping[str, Any]
    ) -> "SourceLinks":
        """Read the source addresses of one page.

        Args:
            options: The site's theme options.
            context: The page's template context.

        Returns:
            The page's edit and view addresses on its repository's host, and
            the address of Sphinx's copy of the source. A page with no source
            file, which Sphinx gives no ``page_source_suffix``, has none of
            them, and a repository on another host no edit or view address.
            Sphinx's copy is linked only when Sphinx shows and copies it.
        """
        suffix = context.get("page_source_suffix")
        if not suffix:
            return cls("", "", "")
        sourcename = context.get("sourcename")
        source = ""
        if sourcename and context.get("show_source") and context.get("has_source"):
            source = context["pathto"]("_sources/" + sourcename, 1)
        repository = options.text("source_repository").rstrip("/")
        repository = repository.removesuffix(".git").rstrip("/")
        host = SourceHost.for_repository(repository)
        if host is None:
            return cls("", "", source)
        directory = options.text("source_directory").strip("/")
        name = context["pagename"] + suffix
        found = {
            "repo": repository,
            "branch": options.text("source_branch", "main"),
            "path": "/".join([directory, name] if directory else [name]),
        }
        return cls(host.edit.format(**found), host.view.format(**found), source)

    def buttons(self, names: list[str]) -> list[str]:
        """Pick the buttons to draw above a page.

        Args:
            names: The names in ``top_of_page_buttons``.

        Returns:
            The names that are ``edit`` or ``view`` and have an address, in the
            order given.
        """
        return [name for name in names if name in BUTTONS and getattr(self, name)]


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
