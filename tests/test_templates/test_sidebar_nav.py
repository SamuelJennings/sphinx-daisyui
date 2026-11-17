from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.navigation import translate

from .page import Page

PAGES = [
    "guide/index.html",
    "guide/one/index.html",
    "guide/one/two/index.html",
    "guide/one/two/three/index.html",
    "guide/other.html",
    "reference/index.html",
    "reference/item.html",
    "https://example.com/",
    "hidden.html",
]
FOUR = "guide/one/two/three/four.html"


def nav(builder: str = "html", **options: Any) -> pytest.MarkDecorator:
    return pytest.mark.sphinx(
        builder,
        testroot="nav",
        freshenv=True,
        confoverrides={"html_theme_options": options},
    )


def menu(app: SphinxTestApp, name: str = "index.html") -> Page:
    """Read the site navigation of a built page."""
    app.build()
    text = (Path(app.outdir) / name).read_text(encoding="utf-8")
    start = text.index('<nav class="daisy-nav"')
    return Page(text[start : text.index("</nav>", start)])


def classes(link: dict[str, str | None]) -> list[str]:
    return (link.get("class") or "").split()


def links(page: Page) -> list[dict[str, str | None]]:
    return [attrs for tag, attrs in page.tags if tag == "a"]


class TestEveryToctreeIsDrawn:
    @nav()
    def test_the_menu_lists_the_toctrees_pages_in_order(
        self, app: SphinxTestApp
    ) -> None:
        assert menu(app).order("href") == PAGES

    @nav()
    def test_the_deepest_page_is_left_out_at_the_default_depth(
        self, app: SphinxTestApp
    ) -> None:
        assert FOUR not in menu(app).order("href")

    @nav()
    def test_the_menu_is_one_labelled_landmark(self, app: SphinxTestApp) -> None:
        app.build()
        text = (Path(app.outdir) / "index.html").read_text(encoding="utf-8")

        assert text.count('<nav class="daisy-nav"') == 1
        assert Page(text).find(
            "nav", **{"class": "daisy-nav", "aria-label": translate("Documentation")}
        )


class TestCaptions:
    @nav()
    def test_a_caption_comes_before_its_groups_list(self, app: SphinxTestApp) -> None:
        text = str(menu(app).text)

        caption = text.index("daisy-nav-caption")
        assert text.index("<ul", caption) > caption
        assert text.index("<ul") > caption


class TestToggles:
    @nav()
    def test_a_branch_has_its_link_and_a_toggle_named_for_it(
        self, app: SphinxTestApp
    ) -> None:
        page = menu(app)

        buttons = page.find("button", type="button")
        assert len(buttons) == 4
        assert all("aria-expanded" in button for button in buttons)
        assert buttons[0]["aria-label"] == translate("Show the pages in %(title)s") % {
            "title": "Guide"
        }

    @nav()
    def test_a_page_without_children_has_no_toggle(self, app: SphinxTestApp) -> None:
        page = menu(app)

        assert len(page.find("button", type="button")) < len(links(page))


class TestCurrentPage:
    @nav()
    def test_the_current_page_is_marked_once(self, app: SphinxTestApp) -> None:
        page = menu(app, "guide/one/index.html")

        current = page.find("a", **{"aria-current": "page"})
        assert len(current) == 1
        assert current[0]["href"] == "#"
        assert len(page.having("aria-current")) == 1

    @nav()
    def test_the_entries_above_it_are_on_its_path_and_open(
        self, app: SphinxTestApp
    ) -> None:
        page = menu(app, "guide/one/index.html")

        on_path = [a for a in links(page) if "daisy-on-path" in classes(a)]
        assert [a["href"] for a in on_path] == ["../index.html"]
        assert page.order("aria-expanded")[:2] == ["true", "true"]

    @nav()
    def test_a_page_in_no_toctree_has_the_menu_and_nothing_current(
        self, app: SphinxTestApp
    ) -> None:
        page = menu(app, "orphan.html")

        assert page.order("href") == PAGES
        assert not page.having("aria-current")


class TestShowNavLevel:
    @nav()
    def test_by_default_only_the_path_is_open(self, app: SphinxTestApp) -> None:
        assert set(menu(app).order("aria-expanded")) == {"false"}

    @nav(show_nav_level=2)
    def test_level_two_opens_the_top_level_entries(self, app: SphinxTestApp) -> None:
        assert menu(app).order("aria-expanded") == ["true", "false", "false", "true"]

    @nav(show_nav_level="2")
    def test_a_level_given_as_digits_is_read(self, app: SphinxTestApp) -> None:
        assert menu(app).order("aria-expanded") == ["true", "false", "false", "true"]


class TestNavigationDepth:
    @nav(navigation_depth=2)
    def test_deeper_entries_are_left_out(self, app: SphinxTestApp) -> None:
        assert menu(app).order("href") == [
            "guide/index.html",
            "guide/one/index.html",
            "guide/other.html",
            "reference/index.html",
            "reference/item.html",
            "https://example.com/",
            "hidden.html",
        ]

    @nav(navigation_depth="2")
    def test_a_depth_given_as_digits_is_read(self, app: SphinxTestApp) -> None:
        assert "guide/one/two/index.html" not in menu(app).order("href")


class TestCollapseNavigation:
    @nav(collapse_navigation=True)
    def test_no_child_lists_are_drawn_off_the_path(self, app: SphinxTestApp) -> None:
        page = menu(app)

        assert page.order("href") == [
            "guide/index.html",
            "reference/index.html",
            "https://example.com/",
            "hidden.html",
        ]
        assert not page.find("button", type="button")


class TestIncludeHidden:
    @nav()
    def test_a_hidden_toctree_is_drawn_by_default(self, app: SphinxTestApp) -> None:
        assert "hidden.html" in menu(app).order("href")

    @nav(sidebar_includehidden=False)
    def test_a_hidden_toctree_can_be_left_out(self, app: SphinxTestApp) -> None:
        assert "hidden.html" not in menu(app).order("href")


class TestExternalEntries:
    @nav()
    def test_an_external_entry_says_it_leads_outside_the_site(
        self, app: SphinxTestApp
    ) -> None:
        page = menu(app)

        external = [a for a in links(page) if "daisy-external" in classes(a)]
        assert [a["href"] for a in external] == ["https://example.com/"]
        assert len(page.find("span", **{"class": "sr-only"})) == 1
        assert translate("(leads outside the site)") in page.text


class TestTitles:
    @nav()
    def test_a_title_with_markup_reaches_the_page_as_sphinx_wrote_it(
        self, app: SphinxTestApp
    ) -> None:
        text = menu(app).text

        assert "Fish &amp; <em>chips</em> <code" in text


class TestNoToctree:
    @pytest.mark.sphinx("html", testroot="basic", freshenv=True, srcdir="no-toctree")
    def test_a_site_without_a_toctree_draws_no_menu(self, app: SphinxTestApp) -> None:
        app.build()
        text = (Path(app.outdir) / "index.html").read_text(encoding="utf-8")

        assert 'class="daisy-nav"' not in text


class TestBuilders:
    @nav("dirhtml")
    @pytest.mark.parametrize("name", ["guide/other/index.html", "index.html"])
    def test_every_link_reaches_a_built_page(
        self, app: SphinxTestApp, name: str
    ) -> None:
        page = menu(app, name)

        folder = (Path(app.outdir) / name).parent
        internal = [
            str(href)
            for href in page.order("href")
            if "://" not in str(href) and href != "#"
        ]
        assert internal
        for href in internal:
            target = (folder / href).resolve()
            assert target.is_file() or (target / "index.html").is_file(), href

    @nav("singlehtml")
    def test_a_site_built_as_one_page_builds_without_a_menu(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert (Path(app.outdir) / "index.html").exists()
        assert not app.warning.getvalue().strip()
