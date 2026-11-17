import posixpath
import re
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.navigation import translate

from .page import Page

NAV = re.compile(r'<nav class="breadcrumbs.*?</nav>', re.DOTALL)
HOME = "index.html"


def breadcrumbs(app: SphinxTestApp, name: str) -> Page | None:
    """Build the site and read the breadcrumb landmark of one page, if drawn."""
    app.build()
    text = (Path(app.outdir) / name).read_text(encoding="utf-8")
    found = NAV.search(text)
    return Page(found.group(0)) if found else None


def targets(page: Page, name: str) -> list[str]:
    """Resolve each link of the landmark from the page that holds it."""
    folder = posixpath.dirname(name)
    return [
        posixpath.normpath(posixpath.join(folder, link["href"] or ""))
        for link in page.find("a")
    ]


@pytest.mark.sphinx("html", testroot="nav", freshenv=True)
class TestBreadcrumbs:
    def test_a_deep_page_leads_from_home_through_each_parent_to_itself(
        self, app: SphinxTestApp
    ) -> None:
        name = "guide/one/two/index.html"

        page = breadcrumbs(app, name)

        assert page is not None
        assert targets(page, name) == [HOME, "guide/index.html", "guide/one/index.html"]
        current = page.find("li", **{"aria-current": "page"})
        assert len(current) == 1
        assert page.tags[-1][0] != "a"
        assert len(page.find("a")) == 3

    def test_the_root_page_has_no_breadcrumbs(self, app: SphinxTestApp) -> None:
        assert breadcrumbs(app, HOME) is None

    def test_a_page_in_no_toctree_has_home_then_itself(
        self, app: SphinxTestApp
    ) -> None:
        name = "orphan.html"

        page = breadcrumbs(app, name)

        assert page is not None
        assert targets(page, name) == [HOME]
        assert len(page.find("li", **{"aria-current": "page"})) == 1

    def test_the_current_title_is_escaped_once_and_carries_no_markup(
        self, app: SphinxTestApp
    ) -> None:
        name = "reference/item.html"

        page = breadcrumbs(app, name)

        assert page is not None
        assert "&lt;" not in page.text
        assert "&amp;amp;" not in page.text
        assert page.text.count("&amp;") == 1
        assert "code" not in [tag for tag, _ in page.tags]

    def test_the_landmark_is_labelled_in_the_sites_language(
        self, app: SphinxTestApp
    ) -> None:
        page = breadcrumbs(app, "guide/index.html")

        assert page is not None
        assert page.find("nav")[0]["aria-label"] == translate("Breadcrumb")


@pytest.mark.sphinx("html", testroot="crumbs", freshenv=True)
def test_a_parents_title_reaches_the_page_as_sphinx_wrote_it(
    app: SphinxTestApp,
) -> None:
    page = breadcrumbs(app, "child.html")

    assert page is not None
    assert [tag for tag, _ in page.tags].count("code") == 1
    assert "&lt;" not in page.text
    assert "&amp;amp;" not in page.text
