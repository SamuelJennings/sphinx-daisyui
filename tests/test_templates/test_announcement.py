from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

ADDRESS = "https://example.org/banner.html?a=1&b=2"
SCRIPT = "announcement.js"


def options(**values: str) -> dict[str, dict[str, str]]:
    return {"html_theme_options": values}


def read(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def banners(page: Page) -> list[dict[str, str | None]]:
    return page.find("div", role="region")


def pages(**values: str) -> pytest.MarkDecorator:
    return pytest.mark.sphinx(
        "html", testroot="pages", freshenv=True, confoverrides=options(**values)
    )


class TestAnnouncement:
    @pytest.mark.sphinx("html", testroot="pages", freshenv=True)
    def test_no_announcement_gives_no_banner(self, app: SphinxTestApp) -> None:
        assert banners(read(app)) == []

    @pages(announcement="Version 2 is out")
    def test_a_text_announcement_appears_on_every_page(
        self, app: SphinxTestApp
    ) -> None:
        for name in ("index.html", "second.html", "sub/third.html", "search.html"):
            page = read(app, name)

            assert len(banners(page)) == 1, name
            assert "Version 2 is out" in page.text, name
            assert page.having("data-daisy-announcement") == [], name

    @pages(announcement="<em>New</em> release")
    def test_the_site_authors_html_is_kept_as_markup(self, app: SphinxTestApp) -> None:
        page = read(app)

        assert "<em>New</em> release" in page.text
        assert "&lt;em&gt;" not in page.text

    @pages(announcement=ADDRESS)
    def test_a_url_gives_an_empty_banner_carrying_the_escaped_address(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        assert len(banners(page)) == 1
        assert page.order("data-daisy-announcement") == [ADDRESS]
        assert "a=1&amp;b=2" in page.text
        assert len(page.having("data-daisy-announcement-body")) == 1
        start = page.text.index("data-daisy-announcement-body")
        assert page.text[start:].split(">", 1)[1].startswith("</span>")

    @pages(announcement="Version 2 is out")
    def test_the_banner_is_a_labelled_region_before_the_header(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        assert banners(page)[0].get("aria-label")
        assert page.text.index('role="region"') < page.text.index("<header")

    @pages(announcement=ADDRESS)
    def test_the_page_links_the_script_from_the_right_depth(
        self, app: SphinxTestApp
    ) -> None:
        sources = [tag.get("src") for tag in read(app, "sub/third.html").find("script")]

        assert f"../_static/scripts/{SCRIPT}" in sources


class TestStickyBanners:
    @pages(announcement="Version 2 is out", sticky_banners="false")
    def test_off_the_banner_comes_before_the_header(self, app: SphinxTestApp) -> None:
        page = read(app)

        assert len(banners(page)) == 1
        assert banners(page.inside("header")) == []

    @pages(announcement="Version 2 is out", sticky_banners="true")
    def test_on_the_banner_is_inside_the_header_and_still_one(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        assert len(banners(page)) == 1
        assert len(banners(page.inside("header"))) == 1
