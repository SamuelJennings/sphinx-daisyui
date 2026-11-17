"""The site navigation: the toctrees drawn as one menu, read from the doctree."""

import copy
import inspect
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property
from typing import Any

from docutils import nodes
from markupsafe import Markup
from sphinx.builders import Builder
from sphinx.environment import BuildEnvironment
from sphinx.environment.adapters.toctree import document_toc, global_toctree_for_doc
from sphinx.locale import get_translation
from sphinx.writers.html5 import HTML5Translator

from .icons import ICONS

translate = get_translation("sphinx")

# Sphinx 7.4 takes no ``tags``; later versions warn when they are left out.
TAGS_ACCEPTED = "tags" in inspect.signature(global_toctree_for_doc).parameters
EXTERNAL_SCHEMES = ("http://", "https://")
TOGGLE_HTML = (
    '<button type="button" class="daisy-nav-toggle btn btn-ghost btn-xs btn-square" '
    'aria-expanded="{expanded}" aria-label="{label}">{icon}</button>'
)


@dataclass(frozen=True)
class HeaderLink:
    """One link of the header: a top-level section or a link to another site.

    Attributes:
        title: The link's text.
        href: Where it leads.
        current: Whether it leads to the section holding the page being read.
        external: Whether it leads outside the site.
    """

    title: str
    href: str
    current: bool
    external: bool


class HeaderLinks:
    """The header's links, split into those shown and those in a menu.

    Args:
        links: The site's top-level sections.
        external_links: Records with a ``name`` and a ``url``, drawn after the
            sections; a record with no ``url`` is left out.
        before_dropdown: How many links are shown before the rest go in the
            menu.
        dropdown_text: The menu's label, empty for the translated "More".

    Attributes:
        shown: The links drawn in the header.
        more: The links in the menu.
        more_text: The menu's label.
        more_current: Whether a link in the menu is the current one.
    """

    shown: list[HeaderLink]
    more: list[HeaderLink]
    more_text: str
    more_current: bool

    def __init__(
        self,
        links: Sequence[HeaderLink],
        external_links: Sequence[dict[str, Any]],
        before_dropdown: int,
        dropdown_text: str,
    ) -> None:
        externals = [
            HeaderLink(
                str(record.get("name", record["url"])), str(record["url"]), False, True
            )
            for record in external_links
            if record.get("url")
        ]
        everything = [*links, *externals]
        limit = max(before_dropdown, 0)
        self.shown = everything[:limit]
        self.more = everything[limit:]
        self.more_text = dropdown_text or translate("More")
        self.more_current = any(link.current for link in self.more)


class CurrentLink(nodes.reference):
    """The link to the page being read, which carries ``aria-current="page"``."""


def visit_current_link(translator: HTML5Translator, node: CurrentLink) -> None:
    """Write the opening tag of the current page's link.

    Args:
        translator: The HTML translator writing the page.
        node: The link to the current page.
    """
    attributes: dict[str, Any] = {
        "href": node.get("refuri") or "#",
        "CLASS": "reference internal",
        "aria-current": "page",
    }
    translator.body.append(translator.starttag(node, "a", "", **attributes))


def depart_current_link(translator: HTML5Translator, node: CurrentLink) -> None:
    """Write the closing tag of the current page's link.

    Args:
        translator: The HTML translator writing the page.
        node: The link to the current page.
    """
    translator.body.append("</a>")


class SiteNavigation:
    """The site's toctrees, read once for a page and drawn as a menu.

    Args:
        env: The build environment holding the toctrees.
        docname: The page being built.
        builder: The HTML builder, which renders the nodes.
        maxdepth: How many levels of entries to keep; zero keeps them all.
        collapse: Whether to leave out the children of entries off the
            current page's path.
        includehidden: Whether to include the toctrees marked ``:hidden:``.
    """

    def __init__(
        self,
        env: BuildEnvironment,
        docname: str,
        builder: Builder,
        maxdepth: int,
        collapse: bool,
        includehidden: bool,
    ) -> None:
        self.env = env
        self.docname = docname
        self.builder = builder
        self.maxdepth = maxdepth
        self.collapse = collapse
        self.includehidden = includehidden

    @cached_property
    def tree(self) -> nodes.Element | None:
        """The site's toctrees as Sphinx builds them for the page.

        Returns:
            The nodes, or ``None`` when the site has no toctree or the builder
            gives the page no menu.
        """
        if self.builder.name == "singlehtml":
            return None
        extra = {"tags": self.builder.tags} if TAGS_ACCEPTED else {}
        return global_toctree_for_doc(
            self.env,
            self.docname,
            self.builder,
            **extra,
            collapse=self.collapse,
            includehidden=self.includehidden,
            maxdepth=self.maxdepth,
            titles_only=True,
        )

    def menu(self, show_nav_level: int) -> Markup:
        """Draw the site's toctrees as the menu of the primary sidebar.

        Args:
            show_nav_level: How many levels of entries are open on a page off
                the current path.

        Returns:
            The menu's markup, empty when there is nothing to draw.
        """
        if self.tree is None:
            return Markup()
        tree = copy.deepcopy(self.tree)
        for bullets in tree.children:
            if isinstance(bullets, nodes.bullet_list):
                self.decorate_list(bullets, 0, show_nav_level)
        captions: list[nodes.Element] = [
            *tree.findall(nodes.title),
            *tree.findall(nodes.caption),
        ]
        for caption in captions:
            caption["classes"] += ["daisy-section-label", "daisy-nav-caption"]
        # Sphinx wrote the titles and Docutils escaped them when rendering.
        return Markup(self.builder.render_partial(tree)["fragment"])  # type: ignore[attr-defined]  # noqa: S704

    def top_level(self) -> list[HeaderLink]:
        """List the site's top-level pages as header links.

        Returns:
            One link for each entry at the first level of the toctrees, in
            order; empty when there is nothing to draw.
        """
        return [
            HeaderLink(
                title=link.astext(),
                href=str(link.get("refuri") or "#"),
                current="current" in item["classes"],
                external=False,
            )
            for item in self.top_items()
            if (link := next(item.findall(nodes.reference), None)) is not None
        ]

    def section_menu(self, show_nav_level: int) -> Markup:
        """Draw the pages of the current top-level section as the menu.

        Args:
            show_nav_level: How many levels of entries are open on a page off
                the current path.

        Returns:
            The menu's markup, empty when the page is in no section or the
            section has no pages below it.
        """
        for item in self.top_items():
            if "current" not in item["classes"]:
                continue
            bullets = next(
                (c for c in item.children if isinstance(c, nodes.bullet_list)), None
            )
            if bullets is None:
                return Markup()
            bullets = copy.deepcopy(bullets)
            self.decorate_list(bullets, 0, show_nav_level)
            # Sphinx wrote the titles and Docutils escaped them when rendering.
            return Markup(self.builder.render_partial(bullets)["fragment"])  # type: ignore[attr-defined]  # noqa: S704
        return Markup()

    def top_items(self) -> list[nodes.list_item]:
        """List the entries at the first level of the toctrees.

        Returns:
            The entries in order, empty when the site has no toctree.
        """
        if self.tree is None:
            return []
        return [
            item
            for bullets in self.tree.children
            if isinstance(bullets, nodes.bullet_list)
            for item in bullets.children
            if isinstance(item, nodes.list_item)
        ]

    def decorate_list(
        self, bullets: nodes.bullet_list, depth: int, show_nav_level: int
    ) -> None:
        """Mark a list of entries, and the lists under them, for the stylesheet.

        Args:
            bullets: The list to mark, changed in place.
            depth: How many lists enclose it; zero for a top-level list.
            show_nav_level: How many levels of entries are open off the path.
        """
        bullets["classes"] = ["daisy-nav-list"]
        for item in bullets.children:
            if isinstance(item, nodes.list_item):
                self.decorate_item(item, depth, show_nav_level)

    def decorate_item(
        self, item: nodes.list_item, depth: int, show_nav_level: int
    ) -> None:
        """Mark one entry: its link, its place on the path and its toggle.

        Args:
            item: The entry to mark, changed in place.
            depth: How many lists enclose it, less one.
            show_nav_level: How many levels of entries are open off the path.
        """
        on_path = "current" in item["classes"]
        children = [c for c in item.children if isinstance(c, nodes.bullet_list)]
        item["classes"] = ["daisy-nav-item"]
        link = next(item[0].findall(nodes.reference), None) if item.children else None
        if link is not None:
            link["classes"] += ["daisy-nav-link"]
            # Sphinx marks the current page's own link; an entry whose pages lie
            # below the depth limit is only on the path.
            if "current" in link["classes"]:
                self.replace_with_current_link(link)
            elif on_path:
                link["classes"] += ["daisy-on-path"]
            if str(link.get("refuri", "")).startswith(EXTERNAL_SCHEMES):
                self.mark_external(link)
        for bullets in children:
            self.decorate_list(bullets, depth + 1, show_nav_level)
        if children:
            item["classes"] += ["daisy-nav-branch"]
            title = link.astext() if link is not None else ""
            self.add_toggle(item, title, on_path or depth < show_nav_level - 1)

    @staticmethod
    def replace_with_current_link(link: nodes.reference) -> None:
        """Swap a link for the one that marks the current page.

        Args:
            link: The link to the current page, replaced in its entry.
        """
        current = CurrentLink("", "", *link.children, **link.attributes)
        current["classes"] += ["menu-active"]
        link.replace_self(current)

    @staticmethod
    def mark_external(link: nodes.reference) -> None:
        """Mark a link that leads outside the site, for sight and for readers.

        Args:
            link: The external link, changed in place.
        """
        link["classes"] += ["daisy-external"]
        link += nodes.raw(
            "",
            str(ICONS.svg("external-link", "size-3.5 opacity-60 shrink-0")),
            format="html",
        )
        link += nodes.inline(
            "", translate("(leads outside the site)"), classes=["sr-only"]
        )

    @staticmethod
    def add_toggle(item: nodes.list_item, title: str, is_open: bool) -> None:
        """Put the button that opens and closes an entry beside its link.

        Args:
            item: The entry, whose first child is the paragraph holding its
                link, changed in place.
            title: The entry's title, which names the button.
            is_open: Whether the entry's pages are shown to begin with.
        """
        # The template is this module's own; format() escapes every value given.
        html = Markup(TOGGLE_HTML).format(  # noqa: S704
            expanded="true" if is_open else "false",
            label=translate("Show the pages in %(title)s") % {"title": title},
            icon=ICONS.svg("chevron-right", "size-4"),
        )
        paragraph = item.children[0]
        if isinstance(paragraph, nodes.Element):
            paragraph += nodes.raw("", str(html), format="html")


class PageContents:
    """The headings of a page, drawn as the list of its On this page.

    Args:
        env: The build environment holding the page's table of contents.
        docname: The page being built.
        builder: The HTML builder, which renders the nodes.
    """

    def __init__(self, env: BuildEnvironment, docname: str, builder: Builder) -> None:
        self.env = env
        self.docname = docname
        self.builder = builder

    @cached_property
    def headings(self) -> nodes.bullet_list | None:
        """The list of the page's headings, without the page's own title.

        Returns:
            The list under the title, or ``None`` when the page has none.
        """
        toc = document_toc(self.env, self.docname, self.builder.tags)
        title = next(toc.findall(nodes.list_item), None)
        if title is None:
            return None
        return next(
            (c for c in title.children if isinstance(c, nodes.bullet_list)), None
        )

    @property
    def count(self) -> int:
        """How many headings the page has below its title."""
        if self.headings is None:
            return 0
        return len(list(self.headings.findall(nodes.list_item)))

    def markup(self, show_toc_level: int) -> Markup:
        """Draw the headings as nested lists the stylesheet and script mark.

        Args:
            show_toc_level: The depth at which a list is left closed until
                its section is read, where the page's first headings are in a
                list of depth one.

        Returns:
            The lists' markup, empty when the page has no headings.
        """
        if self.headings is None:
            return Markup()
        headings = self.headings.deepcopy()
        for bullets in headings.findall(nodes.bullet_list):
            depth = 1 + sum(
                isinstance(parent, nodes.bullet_list)
                for parent in self.parents(bullets)
            )
            bullets["classes"] = ["daisy-toc-list"]
            if depth >= show_toc_level:
                bullets["classes"] += ["daisy-toc-deep"]
        for link in headings.findall(nodes.reference):
            link["classes"] += ["daisy-toc-link"]
        # Sphinx wrote the titles and Docutils escaped them when rendering.
        return Markup(self.builder.render_partial(headings)["fragment"])  # type: ignore[attr-defined]  # noqa: S704

    @staticmethod
    def parents(node: nodes.Node) -> list[nodes.Element]:
        """List the nodes that enclose one, within its own tree.

        Args:
            node: The node to start from.

        Returns:
            Its parents, nearest first.
        """
        found: list[nodes.Element] = []
        while node.parent is not None:
            found.append(node.parent)
            node = node.parent
        return found
