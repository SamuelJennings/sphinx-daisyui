from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

MARKUP = 'x"><b>y</b>&'
PAGES = ("index.html", "deep/er/page.html")


def options(**values: Any) -> dict[str, Any]:
    return {"html_theme_options": values}


def switcher(url: str = "_static/switcher.json", match: str = "dev") -> dict[str, Any]:
    return options(switcher={"json_url": url, "version_match": match})


def unchecked(url: str) -> dict[str, Any]:
    return options(
        switcher={"json_url": url, "version_match": "dev"}, check_switcher=False
    )


def assert_address_on_every_page(app: SphinxTestApp, url: str) -> None:
    for name in PAGES:
        page = Page.read(Path(app.outdir) / name)
        assert root_of(page)["data-daisy-json-url"] == url


def read(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def root_of(page: Page) -> dict[str, str | None]:
    return next(
        found
        for found in page.having("data-daisy-json-url")
        if "data-daisy-version-banner" not in found
    )


class TestVersionSwitcherComponent:
    @pytest.mark.sphinx("html", testroot="versions", freshenv=True)
    def test_no_switcher_draws_nothing_and_no_banner(self, app: SphinxTestApp) -> None:
        page = read(app)

        assert page.having("data-daisy-json-url") == []
        assert page.having("data-daisy-version-banner") == []

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"version_match": "dev"}, show_version_warning_banner=True
        ),
    )
    def test_a_switcher_with_no_json_url_draws_nothing_and_no_banner(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        assert page.having("data-daisy-json-url") == []
        assert page.having("data-daisy-version-banner") == []

    @pytest.mark.sphinx(
        "html", testroot="versions", freshenv=True, confoverrides=switcher(match="1.0")
    )
    def test_every_page_carries_the_component_labelled_with_the_version_built(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        for name in PAGES:
            page = Page.read(Path(app.outdir) / name)
            root = root_of(page)
            assert root["data-daisy-version-match"] == "1.0"
            assert "daisy-dropdown" in (root["class"] or "").split()
            assert page.having("data-daisy-version-label")
            assert "data-daisy-version-label>1.0<" in page.text.replace(" ", "")
            assert page.having("data-daisy-version-list")

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=unchecked("https://x.org/s.json"),
    )
    def test_a_full_address_reaches_every_page_as_given(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert_address_on_every_page(app, "https://x.org/s.json")

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=unchecked("/switcher.json"),
    )
    def test_a_path_from_the_servers_root_reaches_every_page_as_given(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert_address_on_every_page(app, "/switcher.json")

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=unchecked("_static/switcher.json"),
    )
    def test_a_path_from_the_sites_root_reaches_every_page_as_given(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert_address_on_every_page(app, "_static/switcher.json")

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": MARKUP, "version_match": MARKUP},
            check_switcher=False,
        ),
    )
    def test_the_address_and_version_are_escaped(self, app: SphinxTestApp) -> None:
        page = read(app)

        root = root_of(page)
        assert root["data-daisy-json-url"] == MARKUP
        assert root["data-daisy-version-match"] == MARKUP
        assert "<b>y</b>" not in page.text


class TestVersionBanner:
    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": "_static/switcher.json", "version_match": "dev"},
            show_version_warning_banner=True,
        ),
    )
    def test_the_banners_place_is_hidden_and_carries_what_the_script_reads(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        banner = page.having("data-daisy-version-banner")[0]
        assert "hidden" in banner
        assert banner["data-daisy-json-url"] == "_static/switcher.json"
        assert banner["data-daisy-version-match"] == "dev"
        assert banner["data-text-message"]
        assert banner["data-text-link"]
        assert banner["role"] == "region"

    @pytest.mark.sphinx(
        "html", testroot="versions", freshenv=True, confoverrides=switcher()
    )
    def test_the_banner_is_absent_unless_switched_on(self, app: SphinxTestApp) -> None:
        assert read(app).having("data-daisy-version-banner") == []

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": MARKUP, "version_match": MARKUP},
            show_version_warning_banner=True,
            check_switcher=False,
        ),
    )
    def test_the_banners_values_are_escaped(self, app: SphinxTestApp) -> None:
        page = read(app)

        banner = page.having("data-daisy-version-banner")[0]
        assert banner["data-daisy-version-match"] == MARKUP
        assert "<b>y</b>" not in page.text
