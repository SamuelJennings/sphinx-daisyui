from pathlib import Path
from urllib.parse import unquote

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page


def options(**values: bool) -> dict[str, dict[str, bool]]:
    return {"html_theme_options": values}


def read(app: SphinxTestApp, name: str) -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def article_footer(page: Page) -> Page:
    start = page.text.index("</article>")
    return Page(page.text[start:])


def links(page: Page) -> dict[str, dict[str, str | None]]:
    """Find the previous and next links written after the article."""
    after = article_footer(page)
    return {
        rel: found[0] for rel in ("prev", "next") if (found := after.find("a", rel=rel))
    }


def titled(page: Page, rel: str) -> str:
    """Read the text of the link with this rel, tags and all."""
    after = page.text[page.text.index("</article>") :]
    start = after.index(f'rel="{rel}"')
    return after[start : after.index("</a>", start)]


PAGES = pytest.mark.sphinx("html", testroot="pages", freshenv=True)
MARKUP = pytest.mark.sphinx("html", testroot="markup", freshenv=True)


class TestPrevNext:
    @PAGES
    def test_the_middle_page_links_both_neighbours(self, app: SphinxTestApp) -> None:
        page = read(app, "second.html")

        found = links(page)
        assert found["prev"]["href"] == "first.html"
        assert found["next"]["href"] == "sub/third.html"
        assert (Path(app.outdir) / "first.html").exists()
        assert (Path(app.outdir) / "sub/third.html").exists()

    @PAGES
    def test_each_link_carries_its_pages_title(self, app: SphinxTestApp) -> None:
        page = read(app, "second.html")

        assert "First" in titled(page, "prev")
        assert "Third" in titled(page, "next")

    @PAGES
    def test_the_first_page_has_only_a_next_link(self, app: SphinxTestApp) -> None:
        page = read(app, "index.html")

        assert set(links(page)) == {"next"}

    @PAGES
    def test_the_last_page_has_only_a_previous_link(self, app: SphinxTestApp) -> None:
        page = read(app, "sub/third.html")

        found = links(page)
        assert set(found) == {"prev"}
        assert found["prev"]["href"] == "../second.html"

    @pytest.mark.sphinx(
        "html",
        testroot="pages",
        freshenv=True,
        confoverrides=options(show_prev_next=False),
    )
    def test_the_option_turns_the_links_off(self, app: SphinxTestApp) -> None:
        page = read(app, "second.html")

        assert links(page) == {}

    @PAGES
    def test_the_search_page_has_none(self, app: SphinxTestApp) -> None:
        page = read(app, "search.html")

        assert links(page) == {}

    @PAGES
    def test_the_index_page_has_none(self, app: SphinxTestApp) -> None:
        page = read(app, "genindex.html")

        assert links(page) == {}


class TestMarkupInTitles:
    @MARKUP
    def test_the_title_is_printed_as_sphinx_wrote_it(self, app: SphinxTestApp) -> None:
        page = read(app, "index.html")

        assert "Fish &amp; <code" in titled(page, "next")

    @MARKUP
    def test_the_href_leads_to_the_page_whose_name_holds_an_ampersand(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app, "index.html")

        href = links(page)["next"]["href"] or ""
        assert "&" not in href.replace("&amp;", "")
        assert (Path(app.outdir) / unquote(href)).exists()


def head_links(page: Page, rel: str) -> list[dict[str, str | None]]:
    return page.inside("head").find("link", rel=rel)


def keys_option(app: SphinxTestApp) -> str:
    script = (Path(app.outdir) / "_static" / "documentation_options.js").read_text()
    return next(
        line.split(":", 1)[1].strip(" ,\n")
        for line in script.splitlines()
        if "NAVIGATION_WITH_KEYS" in line
    )


class TestArrowKeys:
    @pytest.mark.sphinx(
        "html",
        testroot="pages",
        freshenv=True,
        confoverrides=options(navigation_with_keys=True),
    )
    def test_the_option_switches_sphinxs_handler_on(self, app: SphinxTestApp) -> None:
        read(app, "second.html")

        assert keys_option(app) == "true"

    @PAGES
    def test_the_handler_is_off_by_default(self, app: SphinxTestApp) -> None:
        read(app, "second.html")

        assert keys_option(app) == "false"

    @PAGES
    def test_the_middle_page_names_its_neighbours_in_the_head(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app, "second.html")

        assert [tag["href"] for tag in head_links(page, "prev")] == ["first.html"]
        assert [tag["href"] for tag in head_links(page, "next")] == ["sub/third.html"]
