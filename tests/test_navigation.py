import posixpath
from html.parser import HTMLParser
from typing import Any

import pytest
from docutils import nodes
from markupsafe import Markup
from sphinx import addnodes
from sphinx.testing.util import SphinxTestApp
from test_templates.page import Page

from sphinx_daisyui.navigation import (
    HeaderLink,
    HeaderLinks,
    PageContents,
    SiteNavigation,
    translate,
)

NAV = pytest.mark.sphinx("html", testroot="nav", freshenv=True)
BASIC = pytest.mark.sphinx("html", testroot="basic", freshenv=True, srcdir="no-toctree")
SINGLE = pytest.mark.sphinx("singlehtml", testroot="nav", freshenv=True)

TOP_PAGES = [
    "guide/index.html",
    "guide/one/index.html",
    "guide/one/two/index.html",
    "guide/one/two/three/index.html",
    "guide/other.html",
    "reference/index.html",
    "reference/item.html",
    "https://example.com/",
    "hidden.html",
]


def navigation(
    app: SphinxTestApp, docname: str = "index", **options: Any
) -> SiteNavigation:
    app.build()
    values: dict[str, Any] = {
        "maxdepth": 4,
        "collapse": False,
        "includehidden": True,
    }
    values.update(options)
    return SiteNavigation(app.env, docname, app.builder, **values)


def classes(link: dict[str, str | None]) -> list[str]:
    return (link.get("class") or "").split()


def hrefs(menu: Markup) -> list[str | None]:
    return Page(str(menu)).order("href")


def resolved(docname: str, hrefs: list[str | None]) -> list[str]:
    """Express hrefs written from one page as from the site's root."""
    folder = posixpath.dirname(docname)
    return [
        href if "://" in href else posixpath.normpath(posixpath.join(folder, href))
        for href in map(str, hrefs)
    ]


class TestSiteNavigation:
    @NAV
    def test_menu_lists_every_entry_in_toctree_order(self, app: SphinxTestApp) -> None:
        menu = navigation(app).menu(1)

        assert hrefs(menu) == TOP_PAGES

    @NAV
    def test_menu_wraps_each_toctree_in_a_list_the_theme_styles(
        self, app: SphinxTestApp
    ) -> None:
        page = Page(str(navigation(app).menu(1)))

        assert page.find("ul", **{"class": "daisy-nav-list"})
        assert all(
            classes(ul)[0] == "daisy-nav-list" for _, ul in page.tags if _ == "ul"
        )
        assert all(
            classes(li)[0] == "daisy-nav-item" for t, li in page.tags if t == "li"
        )

    @NAV
    def test_every_link_carries_the_link_class(self, app: SphinxTestApp) -> None:
        page = Page(str(navigation(app).menu(1)))

        links = [attrs for tag, attrs in page.tags if tag == "a"]
        assert len(links) == len(TOP_PAGES)
        assert all("daisy-nav-link" in classes(link) for link in links)

    @NAV
    def test_a_caption_labels_its_group(self, app: SphinxTestApp) -> None:
        page = Page(str(navigation(app).menu(1)))

        captions = [
            attrs
            for tag, attrs in page.tags
            if tag == "p" and "caption" in classes(attrs)
        ]
        assert len(captions) == 1
        assert "daisy-nav-caption" in classes(captions[0])
        assert "daisy-section-label" in classes(captions[0])

    @NAV
    def test_the_current_page_is_the_only_entry_marked_current(
        self, app: SphinxTestApp
    ) -> None:
        menu = navigation(app, "guide/one/index").menu(1)
        page = Page(str(menu))

        current = page.find("a", **{"aria-current": "page"})
        assert len(current) == 1
        assert current[0]["href"] == "#"
        assert "menu-active" in classes(current[0])
        assert len(page.having("aria-current")) == 1

    @NAV
    def test_the_entries_on_the_path_are_marked_on_the_path(
        self, app: SphinxTestApp
    ) -> None:
        page = Page(str(navigation(app, "guide/one/index").menu(1)))

        on_path = [
            a["href"]
            for t, a in page.tags
            if t == "a" and "daisy-on-path" in classes(a)
        ]
        assert on_path == ["../index.html"]

    @NAV
    def test_a_page_in_no_toctree_has_the_menu_and_no_current_entry(
        self, app: SphinxTestApp
    ) -> None:
        menu = navigation(app, "orphan").menu(1)

        assert hrefs(menu) == resolved("orphan", TOP_PAGES)
        assert not Page(str(menu)).having("aria-current")

    @NAV
    def test_menu_does_not_change_the_tree_it_reads_from(
        self, app: SphinxTestApp
    ) -> None:
        site = navigation(app, "guide/one/index")

        first = site.menu(1)
        second = site.menu(2)

        assert first == site.menu(1)
        assert first != second
        assert not any(
            isinstance(n, nodes.reference)
            and n.get("classes")
            and "menu-active" in n["classes"]
            for n in site.tree.findall(nodes.reference)
        )


class TestToggles:
    @NAV
    def test_only_entries_with_pages_under_them_have_a_toggle(
        self, app: SphinxTestApp
    ) -> None:
        page = Page(str(navigation(app).menu(1)))

        buttons = page.find("button", type="button")
        # Guide, One, Two and Reference. Three's only child is cut by the depth.
        assert len(buttons) == 4
        assert all("daisy-nav-toggle" in classes(button) for button in buttons)
        assert all(button.get("aria-label") for button in buttons)

    @NAV
    def test_a_branch_stays_a_link_beside_its_toggle(self, app: SphinxTestApp) -> None:
        text = str(navigation(app).menu(1))

        branch = text[text.index("daisy-nav-branch") :]
        assert branch.index("<a ") < branch.index("<button")

    @NAV
    def test_at_level_one_only_the_path_is_open(self, app: SphinxTestApp) -> None:
        page = Page(str(navigation(app, "guide/one/index").menu(1)))

        assert page.order("aria-expanded") == ["true", "true", "false", "false"]

    @NAV
    def test_at_level_one_nothing_is_open_off_the_path(
        self, app: SphinxTestApp
    ) -> None:
        page = Page(str(navigation(app).menu(1)))

        assert set(page.order("aria-expanded")) == {"false"}

    @NAV
    def test_level_two_opens_the_top_level_entries(self, app: SphinxTestApp) -> None:
        page = Page(str(navigation(app).menu(2)))

        assert page.order("aria-expanded") == ["true", "false", "false", "true"]

    @NAV
    def test_the_toggle_is_named_for_its_entry(self, app: SphinxTestApp) -> None:
        page = Page(str(navigation(app).menu(1)))

        labels = page.order("aria-label")
        assert labels[0] == translate("Show the pages in %(title)s") % {
            "title": "Guide"
        }

    def test_add_toggle_escapes_the_title(self) -> None:
        item = nodes.list_item()
        item += addnodes.compact_paragraph()

        SiteNavigation.add_toggle(item, '<b>"x" & y', is_open=False)

        html = item[0][0]
        assert isinstance(html, nodes.raw)
        assert "<b>" not in html.astext()
        assert "&lt;b&gt;&#34;x&#34; &amp; y" in html.astext()
        assert 'aria-expanded="false"' in html.astext()

    def test_add_toggle_reports_an_open_branch(self) -> None:
        item = nodes.list_item()
        item += addnodes.compact_paragraph()

        SiteNavigation.add_toggle(item, "Title", is_open=True)

        assert 'aria-expanded="true"' in item[0][0].astext()


class TestOptions:
    @NAV
    def test_maxdepth_drops_the_deeper_entries(self, app: SphinxTestApp) -> None:
        menu = navigation(app, maxdepth=2).menu(1)

        assert hrefs(menu) == [
            "guide/index.html",
            "guide/one/index.html",
            "guide/other.html",
            "reference/index.html",
            "reference/item.html",
            "https://example.com/",
            "hidden.html",
        ]

    @NAV
    def test_collapse_leaves_no_child_lists_off_the_path(
        self, app: SphinxTestApp
    ) -> None:
        page = Page(str(navigation(app, collapse=True).menu(2)))

        assert [a["href"] for t, a in page.tags if t == "a"] == [
            "guide/index.html",
            "reference/index.html",
            "https://example.com/",
            "hidden.html",
        ]
        assert not page.find("button", type="button")

    @NAV
    def test_collapse_keeps_the_children_on_the_path(self, app: SphinxTestApp) -> None:
        menu = navigation(app, "guide/other", collapse=True).menu(1)

        found = hrefs(menu)
        assert found[2] == "#"
        assert resolved("guide/other", found[:2] + found[3:]) == [
            "guide/index.html",
            "guide/one/index.html",
            "reference/index.html",
            "https://example.com/",
            "hidden.html",
        ]
        assert len(Page(str(menu)).find("button", type="button")) == 1

    @NAV
    def test_includehidden_false_drops_the_hidden_toctree(
        self, app: SphinxTestApp
    ) -> None:
        menu = navigation(app, includehidden=False).menu(1)

        assert "hidden.html" not in hrefs(menu)
        assert hrefs(menu) == TOP_PAGES[:-1]


class TestExternalEntries:
    @NAV
    def test_an_external_entry_is_marked_and_says_so(self, app: SphinxTestApp) -> None:
        menu = navigation(app).menu(1)
        page = Page(str(menu))

        external = [
            a for t, a in page.tags if t == "a" and "daisy-external" in classes(a)
        ]
        assert [a["href"] for a in external] == ["https://example.com/"]
        assert len(page.find("span", **{"class": "sr-only"})) == 1
        assert translate("(leads outside the site)") in menu
        assert "<svg" in str(menu)[str(menu).index("example.com") :]


class TestTitles:
    @NAV
    def test_a_title_with_markup_keeps_it_and_escapes_the_ampersand(
        self, app: SphinxTestApp
    ) -> None:
        menu = str(navigation(app).menu(1))

        assert "Fish &amp; <em>chips</em> <code" in menu
        assert "Fish & " not in menu

    @NAV
    def test_a_toggle_label_holds_the_plain_title_escaped(
        self, app: SphinxTestApp
    ) -> None:
        page = Page(str(navigation(app, "reference/index").menu(1)))

        assert translate("Show the pages in %(title)s") % {"title": "Reference"} in (
            page.order("aria-label")
        )


class TestNoToctree:
    @BASIC
    def test_a_site_without_a_toctree_has_no_menu(self, app: SphinxTestApp) -> None:
        assert navigation(app).menu(1) == ""

    @SINGLE
    def test_a_site_built_as_one_page_has_no_menu(self, app: SphinxTestApp) -> None:
        site = navigation(app)

        assert site.menu(1) == ""


TOC = pytest.mark.sphinx("html", testroot="toc", freshenv=True)


class ListReader(HTMLParser):
    """The lists of a page's contents: each one's classes and first link's text."""

    def __init__(self, text: str) -> None:
        super().__init__()
        self.lists: list[tuple[list[str], str]] = []
        self.links: list[dict[str, str | None]] = []
        self.anchor = False
        self.feed(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        found = dict(attrs)
        if tag == "ul":
            self.lists.append(((found.get("class") or "").split(), ""))
        if tag == "a":
            self.links.append(found)
            self.anchor = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            self.anchor = False

    def handle_data(self, data: str) -> None:
        if not self.anchor:
            return
        # The first link after a list opens is that list's own first entry.
        for index in reversed(range(len(self.lists))):
            names, text = self.lists[index]
            if not text:
                self.lists[index] = (names, data)
            if not text or index == 0:
                return

    def deep(self) -> list[str]:
        """The first link's text of each list marked deep, in order."""
        return [text for names, text in self.lists if "daisy-toc-deep" in names]


def contents(app: SphinxTestApp, docname: str) -> PageContents:
    app.build()
    return PageContents(app.env, docname, app.builder)


class TestPageContents:
    @TOC
    def test_the_headings_are_nested_in_order_without_the_title(
        self, app: SphinxTestApp
    ) -> None:
        reader = ListReader(str(contents(app, "levels").markup(2)))

        assert [link["href"] for link in reader.links] == [
            "#first",
            "#under-first",
            "#second",
            "#naive-cafe",
        ]
        assert len(reader.lists) == 2

    @TOC
    def test_every_list_and_link_is_marked_for_the_script(
        self, app: SphinxTestApp
    ) -> None:
        reader = ListReader(str(contents(app, "levels").markup(2)))

        assert all("daisy-toc-list" in names for names, _ in reader.lists)
        assert all(
            "daisy-toc-link" in (link.get("class") or "").split()
            for link in reader.links
        )

    @TOC
    def test_the_count_is_the_number_of_headings_below_the_title(
        self, app: SphinxTestApp
    ) -> None:
        assert contents(app, "levels").count == 4

    @TOC
    def test_a_page_with_no_headings_has_none(self, app: SphinxTestApp) -> None:
        page = contents(app, "flat")

        assert page.count == 0
        assert page.markup(2) == ""

    @TOC
    @pytest.mark.parametrize(
        ("level", "deep"),
        [(1, ["First", "Under first"]), (2, ["Under first"]), (3, [])],
    )
    def test_lists_at_or_below_the_level_are_marked_deep(
        self, app: SphinxTestApp, level: int, deep: list[str]
    ) -> None:
        # The list of the page's first headings is depth 1, the lists under it 2.
        reader = ListReader(str(contents(app, "levels").markup(level)))

        assert reader.deep() == deep

    @TOC
    def test_a_heading_keeps_its_markup(self, app: SphinxTestApp) -> None:
        markup = str(contents(app, "markup").markup(2))

        assert "<code" in markup
        assert "<em>emphasis</em>" in markup

    @TOC
    def test_the_markup_is_not_escaped_again(self, app: SphinxTestApp) -> None:
        assert isinstance(contents(app, "levels").markup(2), Markup)


SECTIONS = pytest.mark.sphinx("html", testroot="sections", freshenv=True)
SECTION_NAMES = ["one", "two", "three", "four", "five", "six"]
EXTERNALS = [
    {"name": "Example & <Co>", "url": "https://example.com/?a=1&b=2"},
    {"name": "No address"},
    {"name": "Second", "url": "https://example.org/"},
]


class TestTopLevel:
    @SECTIONS
    def test_one_link_for_each_top_level_entry_in_toctree_order(
        self, app: SphinxTestApp
    ) -> None:
        links = navigation(app, "index").top_level()

        assert [link.href for link in links] == [
            f"{n}/index.html" for n in SECTION_NAMES
        ]
        assert [link.title for link in links] == [f"Section {n}" for n in SECTION_NAMES]
        assert not any(link.current or link.external for link in links)

    @SECTIONS
    def test_the_section_holding_the_page_is_current(self, app: SphinxTestApp) -> None:
        links = navigation(app, "one/page").top_level()

        assert [link.current for link in links] == [True] + [False] * 5

    @NAV
    def test_a_bare_address_has_its_address_as_the_link(
        self, app: SphinxTestApp
    ) -> None:
        links = navigation(app).top_level()

        assert "https://example.com/" in [link.href for link in links]

    @BASIC
    def test_a_site_with_no_toctree_has_no_links(self, app: SphinxTestApp) -> None:
        assert navigation(app).top_level() == []

    @SINGLE
    def test_the_single_page_builder_has_no_links(self, app: SphinxTestApp) -> None:
        assert navigation(app).top_level() == []


class TestSectionMenu:
    @SECTIONS
    def test_the_menu_holds_the_pages_of_the_current_section_only(
        self, app: SphinxTestApp
    ) -> None:
        menu = navigation(app, "one/page").section_menu(1)

        assert hrefs(menu) == ["#"]
        assert Page(str(menu)).find("a", **{"aria-current": "page"})

    @SECTIONS
    def test_it_is_decorated_as_the_whole_menu_is(self, app: SphinxTestApp) -> None:
        menu = Page(str(navigation(app, "one/page").section_menu(1)))

        assert menu.classed("ul", "daisy-nav-list")
        assert menu.classed("a", "daisy-nav-link")

    @SECTIONS
    def test_the_home_page_has_no_menu(self, app: SphinxTestApp) -> None:
        assert navigation(app, "index").section_menu(1) == Markup()

    @NAV
    def test_a_section_without_children_has_no_menu(self, app: SphinxTestApp) -> None:
        assert navigation(app, "hidden").section_menu(1) == Markup()

    @BASIC
    def test_a_site_with_no_toctree_has_no_menu(self, app: SphinxTestApp) -> None:
        assert navigation(app).section_menu(1) == Markup()


def link(title: str, current: bool = False) -> HeaderLink:
    return HeaderLink(title, f"{title}.html", current, False)


class TestHeaderLinks:
    def test_external_links_follow_the_sections_and_are_marked(self) -> None:
        header = HeaderLinks([link("a")], EXTERNALS, 9, "")

        assert [(x.title, x.external) for x in header.shown] == [
            ("a", False),
            ("Example & <Co>", True),
            ("Second", True),
        ]
        assert not any(x.current for x in header.shown if x.external)

    def test_the_links_past_the_limit_are_in_the_menu(self) -> None:
        links = [link(str(n)) for n in range(7)]

        header = HeaderLinks(links, [], 5, "")

        assert [x.title for x in header.shown] == ["0", "1", "2", "3", "4"]
        assert [x.title for x in header.more] == ["5", "6"]

    def test_a_limit_of_zero_puts_every_link_in_the_menu(self) -> None:
        header = HeaderLinks([link("a"), link("b")], [], 0, "")

        assert header.shown == []
        assert len(header.more) == 2

    def test_a_limit_at_or_above_the_count_draws_no_menu(self) -> None:
        links = [link("a"), link("b")]

        assert HeaderLinks(links, [], 2, "").more == []
        assert HeaderLinks(links, [], 9, "").more == []

    def test_the_menu_is_named_by_the_text_or_by_the_translated_default(
        self,
    ) -> None:
        assert HeaderLinks([], [], 5, "").more_text == translate("More")
        assert HeaderLinks([], [], 5, "Other").more_text == "Other"

    def test_the_menu_is_current_when_a_link_in_it_is(self) -> None:
        links = [link("a"), link("b", current=True)]

        assert HeaderLinks(links, [], 1, "").more_current
        assert not HeaderLinks(links, [], 2, "").more_current
