from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

SCRIPT = "back-to-top.js"


def read(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def buttons(page: Page) -> list[dict[str, str | None]]:
    return [
        tag
        for name, tag in page.tags
        if name == "button" and "daisy-back-to-top" in (tag.get("class") or "").split()
    ]


def scripts(page: Page) -> list[str]:
    return [tag["src"] or "" for tag in page.find("script") if "src" in tag]


class TestBackToTop:
    @pytest.mark.sphinx("html", testroot="pages", freshenv=True)
    def test_every_page_carries_a_button_that_starts_hidden(
        self, app: SphinxTestApp
    ) -> None:
        for name in ("index.html", "second.html", "sub/third.html", "search.html"):
            found = buttons(read(app, name))

            assert len(found) == 1, name
            assert "hidden" in found[0], name

    @pytest.mark.sphinx(
        "html",
        testroot="pages",
        freshenv=True,
        confoverrides={"html_theme_options": {"back_to_top_button": False}},
    )
    def test_the_option_removes_the_button(self, app: SphinxTestApp) -> None:
        assert buttons(read(app)) == []

    @pytest.mark.sphinx("html", testroot="pages", freshenv=True)
    def test_the_page_links_the_script_from_the_right_depth(
        self, app: SphinxTestApp
    ) -> None:
        assert f"_static/scripts/{SCRIPT}" in scripts(read(app))
        assert f"../_static/scripts/{SCRIPT}" in scripts(read(app, "sub/third.html"))
