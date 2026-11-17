from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.navigation import translate

from .page import Page

SECTION_COUNT = 6
EXTERNALS = [
    {"name": "Example & <Co>", "url": "https://example.com/?a=1&b=2"},
    {"name": "No address"},
    {"name": "Second", "url": "https://example.org/"},
]
LINK_COUNT = SECTION_COUNT + 2
SECTION_HREFS = [
    "one/index.html",
    "two/index.html",
    "three/index.html",
    "four/index.html",
    "five/index.html",
    "six/index.html",
]


def header(**options: Any) -> pytest.MarkDecorator:
    """Build the sections root with ``navbar-nav`` in the centre, plus options."""
    values = {"navbar_center": ["navbar-nav"], "external_links": EXTERNALS, **options}
    return pytest.mark.sphinx(
        "html",
        testroot="sections",
        freshenv=True,
        confoverrides={"html_theme_options": values},
    )


def menu_links(page: Page) -> list[dict[str, str | None]]:
    """Find the links of the site's menus, not those of a toctree in the article."""
    links = page.classed("a", "daisy-nav-link")
    return links[
        : len(links) - len(page.inside("article").classed("a", "daisy-nav-link"))
    ]


def built(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def header_nav(page: Page) -> tuple[Page, Page]:
    """Split the header's Sections landmark into the links shown and the menu."""
    nav = page.inside("header").inside("nav")
    shown, _, menu = nav.text.partition("dropdown-content")
    return Page(shown), Page(menu)


def anchors(page: Page) -> list[dict[str, str | None]]:
    return [attrs for tag, attrs in page.tags if tag == "a"]


class TestSectionLinks:
    @header()
    def test_there_is_a_link_for_each_section_in_toctree_order(
        self, app: SphinxTestApp
    ) -> None:
        shown, menu = header_nav(built(app))

        hrefs = [a["href"] for a in anchors(shown) + anchors(menu)]
        assert hrefs[:SECTION_COUNT] == SECTION_HREFS

    @header()
    def test_the_current_sections_link_is_marked_and_no_other(
        self, app: SphinxTestApp
    ) -> None:
        shown, menu = header_nav(built(app, "one/page.html"))

        current = [a for a in anchors(shown) + anchors(menu) if a.get("aria-current")]
        assert [a["href"] for a in current] == ["index.html"]
        assert current[0]["aria-current"] == "true"

    @header()
    def test_the_home_page_marks_no_link(self, app: SphinxTestApp) -> None:
        shown, menu = header_nav(built(app))

        assert not (shown.having("aria-current") or menu.having("aria-current"))

    @header()
    def test_the_links_are_one_landmark_named_sections(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app).inside("header")

        assert len(page.find("nav", **{"aria-label": translate("Sections")})) == 1


class TestExternalLinks:
    @header()
    def test_they_follow_the_sections_in_order_and_skip_one_without_an_address(
        self, app: SphinxTestApp
    ) -> None:
        shown, menu = header_nav(built(app))

        hrefs = [a["href"] for a in anchors(shown) + anchors(menu)]
        assert hrefs[SECTION_COUNT:] == [
            "https://example.com/?a=1&b=2",
            "https://example.org/",
        ]

    @header(header_links_before_dropdown=99)
    def test_each_says_that_it_leads_outside_the_site(self, app: SphinxTestApp) -> None:
        page = built(app).inside("header")

        assert page.text.count(translate("(leads outside the site)")) == 2

    @header()
    def test_their_name_and_address_reach_the_page_escaped(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert "<Co>" not in page.text
        assert "Example &amp; &lt;Co&gt;" in page.text
        assert "?a=1&amp;b=2" in page.text

    @header(header_links_before_dropdown=10)
    def test_they_reach_the_navbar_escaped_when_shown_there(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app).inside("header")

        assert "<Co>" not in page.text
        assert "Example &amp; &lt;Co&gt;" in page.text


class TestMenu:
    @header()
    def test_five_links_are_shown_and_the_rest_are_in_the_menu(
        self, app: SphinxTestApp
    ) -> None:
        shown, menu = header_nav(built(app))

        assert len(anchors(shown)) == 5
        assert len(anchors(menu)) == LINK_COUNT - 5

    @header(header_links_before_dropdown=2)
    def test_the_limit_is_an_option(self, app: SphinxTestApp) -> None:
        shown, menu = header_nav(built(app))

        assert len(anchors(shown)) == 2
        assert len(anchors(menu)) == LINK_COUNT - 2

    @header(header_links_before_dropdown="3")
    def test_a_limit_given_as_a_string_is_read(self, app: SphinxTestApp) -> None:
        shown, _ = header_nav(built(app))

        assert len(anchors(shown)) == 3

    @header(header_links_before_dropdown=0)
    def test_a_limit_of_zero_puts_every_link_in_the_menu(
        self, app: SphinxTestApp
    ) -> None:
        shown, menu = header_nav(built(app))

        assert anchors(shown) == []
        assert len(anchors(menu)) == LINK_COUNT

    @header(header_links_before_dropdown=LINK_COUNT)
    def test_a_limit_at_the_count_draws_no_menu(self, app: SphinxTestApp) -> None:
        page = built(app).inside("header")

        assert "dropdown-content" not in page.text
        assert not page.find("div", role="button")

    @header()
    def test_the_label_is_the_translated_more_by_default(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app).inside("header")

        assert f">{translate('More')}<" in page.text.replace(" ", "")

    @header(header_dropdown_text="<Other> & more")
    def test_a_given_label_is_used_and_escaped(self, app: SphinxTestApp) -> None:
        page = built(app).inside("header")

        assert "<Other>" not in page.text
        assert "&lt;Other&gt; &amp; more" in page.text
        assert translate("More") not in page.text

    @header()
    def test_the_control_can_be_reached_and_announces_a_menu(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app).inside("header")

        control = page.find("div", role="button", **{"aria-haspopup": "menu"})
        assert len(control) == 1
        assert control[0]["tabindex"] == "0"

    @header()
    def test_the_control_is_not_current_when_no_link_in_it_is(
        self, app: SphinxTestApp
    ) -> None:
        control = (
            built(app, "one/page.html").inside("header").find("div", role="button")
        )

        assert "aria-current" not in control[0]
        assert "btn-active" not in (control[0]["class"] or "").split()

    @header()
    def test_a_current_link_in_the_menu_marks_the_control_too(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app, "six/page.html").inside("header")
        _, menu = header_nav(built(app, "six/page.html"))

        control = page.find("div", role="button")[0]
        assert control["aria-current"] == "true"
        assert "btn-active" in (control["class"] or "").split()
        assert [a["aria-current"] for a in anchors(menu) if a.get("aria-current")] == [
            "true"
        ]


class TestDrawer:
    @header()
    def test_the_drawer_lists_every_link_including_the_menus(
        self, app: SphinxTestApp
    ) -> None:
        aside = built(app, "six/page.html").inside("aside")

        nav = Page(aside.text[aside.text.index("<nav") :])
        sections = nav.find("nav", **{"aria-label": translate("Sections")})
        assert len(sections) == 1
        listed = [
            a for a in anchors(nav) if "daisy-nav-link" not in (a.get("class") or "")
        ]
        assert [a["href"] for a in listed][:LINK_COUNT][:SECTION_COUNT] == [
            "../" + h for h in SECTION_HREFS[:-1]
        ] + ["index.html"]
        assert len(listed) >= LINK_COUNT
        assert [a["aria-current"] for a in listed if a.get("aria-current")] == ["true"]

    @header(navbar_center=[], navbar_end=["navbar-nav"])
    def test_a_header_elsewhere_leaves_the_drawer_without_sections(
        self, app: SphinxTestApp
    ) -> None:
        aside = built(app).inside("aside")

        assert not aside.find("nav", **{"aria-label": translate("Sections")})


class TestSidebar:
    @header()
    def test_a_page_in_a_section_has_only_that_sections_pages(
        self, app: SphinxTestApp
    ) -> None:
        aside = built(app, "one/page.html").inside("aside")

        entries = aside.classed("a", "daisy-nav-link")
        assert [a["href"] for a in entries] == ["#"]
        assert entries[0]["aria-current"] == "page"

    @header()
    def test_the_home_page_has_no_site_navigation(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert page.classed("nav", "daisy-nav") == []

    @header(navbar_center=[], navbar_end=["navbar-nav"])
    def test_a_header_elsewhere_draws_the_links_and_keeps_the_whole_site(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len(anchors(page.inside("header"))) >= LINK_COUNT
        assert len(menu_links(page)) == 2 * SECTION_COUNT

    @header(navbar_center=[], external_links=[])
    def test_no_navbar_nav_anywhere_draws_no_sections_and_keeps_the_whole_site(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert not page.find("nav", **{"aria-label": translate("Sections")})
        assert len(menu_links(page)) == 2 * SECTION_COUNT


class TestAlignment:
    @header()
    def test_the_centre_slot_carries_the_default_alignment(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert list(page.order("data-navbar-align")) == ["content"]

    @header(navbar_align="right")
    def test_a_given_alignment_is_carried(self, app: SphinxTestApp) -> None:
        assert built(app).order("data-navbar-align") == ["right"]

    @header(navbar_align="bogus")
    def test_an_unknown_alignment_is_the_default(self, app: SphinxTestApp) -> None:
        assert built(app).order("data-navbar-align") == ["content"]


class TestSectionMenuLevels:
    @pytest.mark.sphinx(
        "html",
        testroot="nav",
        freshenv=True,
        confoverrides={
            "html_theme_options": {"navbar_center": ["navbar-nav"], "show_nav_level": 2}
        },
    )
    def test_the_section_menus_first_level_counts_as_the_sidebars_first(
        self, app: SphinxTestApp
    ) -> None:
        aside = built(app, "guide/other.html").inside("aside")

        toggles = aside.find("button", type="button")
        assert [t["aria-expanded"] for t in toggles if t.get("aria-label")] == [
            "true",
            "false",
        ]
