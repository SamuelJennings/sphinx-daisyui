import re
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


CONTENT_STYLESHEET = "sphinx-daisyui-content.css"
# The custom properties a page that loads daisyUI 5 already has: daisyUI's theme
# tokens, Tailwind's fonts, and sphinx-design's own.
HOST_PROPERTIES = ("--color-", "--radius-", "--border", "--size-", "--font-", "--sd-")


class TestSetup:
    @pytest.mark.sphinx("html", testroot="basic")
    def test_a_site_choosing_the_theme_builds_without_warnings(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert app.builder.theme.name == "daisyui"
        assert app.warning.getvalue() == ""

    @pytest.mark.sphinx("html", testroot="basic")
    def test_each_page_links_the_compiled_stylesheet(self, app: SphinxTestApp) -> None:
        app.build()

        page = (app.outdir / "index.html").read_text(encoding="utf-8")
        stylesheet = app.outdir / "_static" / "styles" / "sphinx-daisyui.css"
        assert 'href="_static/styles/sphinx-daisyui.css' in page
        assert stylesheet.stat().st_size > 0

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_theme_asks_for_neither_sphinx_design_nor_sphinx_copybutton(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert app.warning.getvalue() == ""
        assert "sphinx_design" not in app.extensions
        assert "sphinx_copybutton" not in app.extensions


class TestContentStylesheet:
    @pytest.mark.sphinx("html", testroot="basic")
    def test_an_html_build_writes_the_page_body_styles_on_their_own(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert (app.outdir / "_static" / "styles" / CONTENT_STYLESHEET).stat().st_size

    @pytest.mark.sphinx("json", testroot="basic")
    def test_a_json_build_writes_both_stylesheets(self, app: SphinxTestApp) -> None:
        app.build()

        styles = app.outdir / "_static" / "styles"
        assert app.warning.getvalue() == ""
        assert (styles / "sphinx-daisyui.css").stat().st_size
        assert (styles / CONTENT_STYLESHEET).stat().st_size

    @pytest.mark.sphinx("html", testroot="basic")
    def test_the_page_body_styles_read_only_what_a_daisyui_page_has(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        css = (app.outdir / "_static" / "styles" / CONTENT_STYLESHEET).read_text("utf-8")
        declared = set(re.findall(r"(--[\w-]+):", css))
        read = set(re.findall(r"var\((--[\w-]+)", css))
        missing = {
            name
            for name in read - declared
            if not name.startswith(HOST_PROPERTIES)
            and not name.startswith("--daisy-sphinx-")
        }
        assert missing == set()
        assert "tailwindcss" not in css
