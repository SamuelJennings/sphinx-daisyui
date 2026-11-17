from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.navigation import translate

from .page import Page


def toc(**options: Any) -> pytest.MarkDecorator:
    return pytest.mark.sphinx(
        "html",
        testroot="toc",
        freshenv=True,
        confoverrides={"html_theme_options": options},
    )


def built(app: SphinxTestApp, name: str = "levels.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def contents(page: Page) -> Page:
    """Read the On this page list in the secondary sidebar."""
    start = page.text.index('<nav class="daisy-page-toc')
    return Page(page.text[start : page.text.index("</nav>", start)])


def deep(page: Page) -> int:
    return len(contents(page).classed("ul", "daisy-toc-deep"))


class TestPageToc:
    @toc()
    def test_the_sidebar_lists_the_headings_in_order_as_links_to_their_ids(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        links = [a["href"] for a in contents(page).classed("a", "daisy-toc-link")]
        ids = {tag["id"] for tag in page.having("id")}
        assert links == ["#first", "#under-first", "#second", "#naive-cafe"]
        assert {str(href)[1:] for href in links} <= ids
        assert "#levels" not in links

    @toc()
    def test_the_list_is_a_labelled_landmark(self, app: SphinxTestApp) -> None:
        page = built(app)

        nav = page.classed("nav", "daisy-page-toc")[0]
        label = page.find("p", id="daisy-page-toc-label")
        assert nav["aria-labelledby"] == "daisy-page-toc-label"
        assert len(label) == 1
        assert nav["data-toc-level"] == "2"

    @toc()
    def test_a_page_without_headings_draws_neither_list_nor_disclosure(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app, "flat.html")

        assert page.classed("nav", "daisy-page-toc") == []
        assert page.find("details") == []

    @toc(show_toc_level=2)
    def test_with_two_the_lists_under_the_headings_are_deep(
        self, app: SphinxTestApp
    ) -> None:
        assert deep(built(app)) == 1

    @toc(show_toc_level=3)
    def test_with_three_none_are_deep(self, app: SphinxTestApp) -> None:
        assert deep(built(app)) == 0

    @toc(show_toc_level=1)
    def test_with_one_the_first_lists_are_deep_too(self, app: SphinxTestApp) -> None:
        assert deep(built(app)) == 2

    @toc(show_toc_level="3")
    def test_a_string_of_digits_is_a_level(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert deep(page) == 0
        assert contents(page).classed("ul", "daisy-toc-list")
        assert page.classed("nav", "daisy-page-toc")[0]["data-toc-level"] == "3"

    @toc()
    def test_a_heading_keeps_its_markup(self, app: SphinxTestApp) -> None:
        page = built(app, "markup.html")

        assert "<code" in contents(page).text

    @toc()
    def test_the_disclosure_is_closed_and_holds_the_same_links(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        details = page.classed("details", "daisy-toc-mobile")
        assert len(details) == 1
        assert "open" not in details[0]
        start = page.text.index("<details")
        inner = Page(page.text[start : page.text.index("</details>", start)])
        assert [a["href"] for a in inner.classed("a", "daisy-toc-link")] == [
            "#first",
            "#under-first",
            "#second",
            "#naive-cafe",
        ]
        assert inner.find("nav", **{"aria-label": translate("On this page")})

    @toc(secondary_sidebar_items=[])
    def test_with_no_secondary_items_there_is_no_disclosure(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert page.find("details") == []
        assert page.classed("nav", "daisy-page-toc") == []

    @toc()
    @pytest.mark.parametrize("name", ["search.html", "genindex.html"])
    def test_index_pages_have_neither(self, app: SphinxTestApp, name: str) -> None:
        page = built(app, name)

        assert page.classed("nav", "daisy-page-toc") == []
        assert page.find("details") == []
