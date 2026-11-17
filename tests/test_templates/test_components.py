import datetime
from importlib.metadata import metadata, version
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

HOSTILE = '<b>&"'


def footer(app: SphinxTestApp) -> Page:
    """Build the site with one component in the footer and read the footer."""
    app.build()
    return Page.read(Path(app.outdir) / "index.html").inside("footer")


def only(name: str) -> dict[str, object]:
    return {
        "html_theme_options": {
            "footer_start": [name],
            "footer_center": [],
            "footer_end": [],
        }
    }


def repository() -> str:
    for entry in metadata("sphinx-daisyui").get_all("Project-URL") or []:
        label, _, url = entry.partition(", ")
        if label.lower() == "repository":
            return url
    raise LookupError("the package has no repository URL")


class TestCopyright:
    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={**only("copyright"), "html_show_copyright": False},
    )
    def test_it_draws_nothing_when_the_site_hides_the_copyright(
        self, app: SphinxTestApp
    ) -> None:
        page = footer(app)

        assert page.find("p") == []

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={**only("copyright"), "html_show_copyright": True},
    )
    def test_it_draws_the_copyright_when_shown(self, app: SphinxTestApp) -> None:
        page = footer(app)

        assert len(page.find("p")) == 1
        assert "2026, Test" in page.text

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={
            **only("copyright"),
            "html_show_copyright": True,
            "copyright": HOSTILE,
        },
    )
    def test_it_escapes_the_copyright(self, app: SphinxTestApp) -> None:
        page = footer(app)

        assert "&lt;b&gt;&amp;" in page.text
        assert "<b>" not in page.text


class TestSphinxVersion:
    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={**only("sphinx-version"), "html_show_sphinx": False},
    )
    def test_it_draws_nothing_when_the_site_hides_sphinx(
        self, app: SphinxTestApp
    ) -> None:
        page = footer(app)

        assert page.find("a") == []

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={**only("sphinx-version"), "html_show_sphinx": True},
    )
    def test_it_links_sphinx_and_shows_its_version(self, app: SphinxTestApp) -> None:
        page = footer(app)

        assert len(page.find("a", href="https://www.sphinx-doc.org/")) == 1
        assert version("sphinx") in page.text


class TestThemeVersion:
    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides=only("theme-version"),
    )
    def test_it_links_the_repository_and_shows_the_version(
        self, app: SphinxTestApp
    ) -> None:
        page = footer(app)

        assert len(page.find("a", href=repository())) == 1
        assert version("sphinx-daisyui") in page.text


class TestLastUpdated:
    @pytest.mark.sphinx(
        "html", testroot="components", freshenv=True, confoverrides=only("last-updated")
    )
    def test_it_draws_nothing_without_a_date_format(self, app: SphinxTestApp) -> None:
        page = footer(app)

        assert page.find("p") == []

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={**only("last-updated"), "html_last_updated_fmt": "%Y"},
    )
    def test_it_draws_the_date_when_a_format_is_set(self, app: SphinxTestApp) -> None:
        page = footer(app)

        assert len(page.find("p")) == 1
        assert str(datetime.date.today().year) in page.text


class TestNavbarLogo:
    @pytest.mark.sphinx("html", testroot="pages", freshenv=True)
    def test_the_default_lists_link_the_title_to_the_front_page(
        self, app: SphinxTestApp
    ) -> None:
        app.build()
        page = Page.read(Path(app.outdir) / "sub" / "third.html")

        brands = [
            attrs
            for _, attrs in page.tags
            if "daisy-brand" in (attrs.get("class") or "").split()
        ]
        assert brands
        assert {attrs["href"] for attrs in brands} == {"../index.html"}
        assert "Pages" in page.inside("header").text

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={"project": HOSTILE, "html_title": HOSTILE},
    )
    def test_it_escapes_the_title(self, app: SphinxTestApp) -> None:
        app.build()
        text = (Path(app.outdir) / "index.html").read_text(encoding="utf-8")
        brand = Page(text).inside("header").text

        assert "&lt;b&gt;&amp;" in brand
        assert "<b>" not in brand
