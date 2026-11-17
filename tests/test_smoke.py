import pytest
from sphinx.testing.util import SphinxTestApp


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
