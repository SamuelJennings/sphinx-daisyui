import posixpath
from typing import Any

import pytest
from docutils import nodes
from markupsafe import Markup
from sphinx import addnodes
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.navigation import SiteNavigation, translate

from test_templates.page import Page

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
