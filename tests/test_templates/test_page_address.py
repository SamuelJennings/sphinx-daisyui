import re
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

SEARCH_ORDER = ("keys", "page-address", "search")


def sources(page: Page) -> list[str]:
    return [
        attrs["src"] or ""
        for tag, attrs in page.tags
        if tag == "script" and "src" in attrs and "defer" in attrs
    ]


class TestPageAddressScript:
    @pytest.mark.sphinx("html", testroot="pages", freshenv=True)
    @pytest.mark.parametrize(
        ("name", "prefix"),
        [("index.html", "_static/"), ("sub/third.html", "../_static/")],
    )
    def test_each_page_links_it_deferred_after_the_key_script(
        self, app: SphinxTestApp, name: str, prefix: str
    ) -> None:
        app.build()

        found = sources(Page.read(Path(app.outdir) / name))
        keys = f"{prefix}scripts/keys.js"
        address = f"{prefix}scripts/page-address.js"
        assert address in found
        assert found.index(keys) < found.index(address)

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_script_is_in_the_output(self, app: SphinxTestApp) -> None:
        app.build()

        script = Path(app.outdir) / "_static" / "scripts" / "page-address.js"
        assert script.is_file()


class TestSphinxSearchShortcuts:
    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_sphinxs_own_slash_listener_is_off(self, app: SphinxTestApp) -> None:
        app.build()

        options = Path(app.outdir) / "_static" / "documentation_options.js"
        text = options.read_text(encoding="utf-8")
        found = re.search(r"ENABLE_SEARCH_SHORTCUTS:\s*(\w+)", text)
        assert found is not None
        assert found.group(1) == "false"


class TestSearchScript:
    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    @pytest.mark.parametrize(
        ("name", "prefix"),
        [("index.html", "_static/"), ("nested/deep.html", "../_static/")],
    )
    def test_each_page_links_it_deferred_after_the_key_and_address_scripts(
        self, app: SphinxTestApp, name: str, prefix: str
    ) -> None:
        app.build()

        found = sources(Page.read(Path(app.outdir) / name))
        wanted = [f"{prefix}scripts/{script}.js" for script in SEARCH_ORDER]
        assert [source for source in found if source in wanted] == wanted

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_script_is_in_the_output(self, app: SphinxTestApp) -> None:
        app.build()

        assert (Path(app.outdir) / "_static" / "scripts" / "search.js").is_file()
