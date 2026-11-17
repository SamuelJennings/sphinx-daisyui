from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

DEEP = "a/b/c/page.html"
GITHUB = {"name": "Code", "url": "https://example.org/code", "icon": "github"}


def options(*entries: dict[str, Any], **more: Any) -> dict[str, Any]:
    return {"html_theme_options": {"icon_links": list(entries), **more}}


def built(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def lists(page: Page) -> list[dict[str, str | None]]:
    return [
        tag
        for name, tag in page.tags
        if name == "ul" and "aria-label" in tag and "flex" in (tag["class"] or "")
    ]


def holding(page: Page) -> Page:
    """Read what the first icon links list holds."""
    start = page.text.index('<ul class="flex items-center" aria-label=')
    return Page(page.text[start : page.text.index("</ul>", start)])


def link(page: Page, url: str) -> dict[str, str | None]:
    [found] = page.find("a", href=url)
    return found


class TestIconLinks:
    @pytest.mark.sphinx(
        "html", testroot="links", freshenv=True, confoverrides=options(GITHUB)
    )
    def test_a_link_leads_to_the_address_and_is_named(self, app: SphinxTestApp) -> None:
        found = link(built(app), "https://example.org/code")

        assert found["aria-label"] == "Code"

    @pytest.mark.sphinx(
        "html", testroot="links", freshenv=True, confoverrides=options(GITHUB)
    )
    def test_a_bundled_icon_is_drawn_inline(self, app: SphinxTestApp) -> None:
        page = built(app)

        links = holding(page)
        assert links.find("svg")
        assert not links.find("img")

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            {"name": "A", "url": "https://a", "icon": "img.svg", "type": "local"},
            {
                "name": "B",
                "url": "https://b",
                "icon": "_static/img.svg",
                "type": "local",
            },
            {
                "name": "C",
                "url": "https://c",
                "icon": "https://cdn.example/i.png",
                "type": "local",
            },
            {
                "name": "D",
                "url": "https://d",
                "icon": "https://cdn.example/d.png",
                "type": "url",
            },
        ),
    )
    @pytest.mark.parametrize(
        ("name", "prefix"), [("index.html", ""), (DEEP, "../../../")]
    )
    def test_images_point_at_the_right_file_at_any_depth(
        self, app: SphinxTestApp, name: str, prefix: str
    ) -> None:
        app.build()
        page = Page.read(Path(app.outdir) / name)

        sources = [tag["src"] for tag in holding(page).find("img")]
        assert sources == [
            f"{prefix}_static/img.svg",
            f"{prefix}_static/img.svg",
            "https://cdn.example/i.png",
            "https://cdn.example/d.png",
        ]
        assert all(tag["alt"] == "" for tag in holding(page).find("img"))

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            GITHUB, footer_end=["navbar-icon-links"], navbar_end=["navbar-icon-links"]
        ),
    )
    def test_the_list_appears_in_the_navbar_and_in_the_footer(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len(lists(page)) == 2
        assert len(page.find("a", href="https://example.org/code")) == 2
        footer = Page(page.text[page.text.index("<footer") :])
        assert len(lists(footer)) == 1

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(GITHUB, icon_links_label="Our accounts"),
    )
    def test_the_option_names_the_list(self, app: SphinxTestApp) -> None:
        [found] = lists(built(app))

        assert found["aria-label"] == "Our accounts"

    @pytest.mark.sphinx(
        "html", testroot="links", freshenv=True, confoverrides=options(GITHUB)
    )
    def test_without_the_option_the_list_is_still_named(
        self, app: SphinxTestApp
    ) -> None:
        [found] = lists(built(app))

        assert found["aria-label"]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            {
                "name": 'N"><b id="n">',
                "url": 'https://x/?a=1&b="2"><i id="u">',
                "icon": 'p"><u id="p">&',
                "type": "local",
            },
            icon_links_label='L"><s id="l">',
        ),
    )
    def test_text_from_the_site_reaches_the_page_escaped(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        for injected in ("n", "u", "p", "l"):
            assert page.find("b", id=injected) == []
            assert page.find("i", id=injected) == []
            assert page.find("u", id=injected) == []
            assert page.find("s", id=injected) == []
        [found] = lists(page)
        assert found["aria-label"] == 'L"><s id="l">'

    @pytest.mark.sphinx("html", testroot="links", freshenv=True)
    def test_no_links_leave_no_list(self, app: SphinxTestApp) -> None:
        assert lists(built(app)) == []

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            {"name": "Nowhere", "icon": "github"}, {"name": "Empty", "url": ""}
        ),
    )
    def test_entries_with_no_address_leave_no_list(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert lists(page) == []
        assert page.find("a", **{"aria-label": "Nowhere"}) == []
