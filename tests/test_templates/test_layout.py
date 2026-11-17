from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

TEST_MARKER = "data-test"


def built(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


class TestFrame:
    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_default_code_arranges_the_page(self, app: SphinxTestApp) -> None:
        page = built(app)

        frame = page.find("div", **{"data-layout": "hHh LpR lff"})[0]
        assert "data-header-fixed" in frame
        assert "data-primary-fixed" in frame
        assert "data-secondary-fixed" in frame
        assert "data-footer-fixed" not in frame
        style = frame["style"] or ""
        assert '--daisy-areas-xl: "header header header"' in style
        assert '"primary main secondary"' in style
        assert '--daisy-areas-lg: "header header header"' in style
        assert '"primary main main"' in style

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        freshenv=True,
        confoverrides={"html_theme_options": {"layout": "hhh lpr fff"}},
    )
    def test_a_code_in_lower_case_fixes_nothing(self, app: SphinxTestApp) -> None:
        page = built(app)

        frame = page.find("div", **{"data-layout": "hhh lpr fff"})[0]
        assert not [name for name in frame if name.endswith("-fixed")]

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        freshenv=True,
        confoverrides={"html_theme_options": {"layout": "hHh lpr fFf"}},
    )
    def test_an_upper_case_footer_is_fixed(self, app: SphinxTestApp) -> None:
        page = built(app)

        frame = page.find("div", **{"data-layout": "hHh lpr fFf"})[0]
        assert "data-footer-fixed" in frame
        assert "data-primary-fixed" not in frame

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_article_has_no_main_role(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert page.find("article", role="main") == []
        assert len(page.find("article")) == 1

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_secondary_sidebar_is_drawn_when_it_has_components(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len(page.find("aside", **{"aria-label": "Page tools"})) == 1

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        freshenv=True,
        confoverrides={"html_theme_options": {"secondary_sidebar_items": ""}},
    )
    def test_the_secondary_sidebar_is_left_out_when_empty(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert page.find("aside", **{"aria-label": "Page tools"}) == []

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_brand_is_drawn_in_the_navbar_and_the_sidebar(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len(page.find("a", **{"class": page_class(page, "daisy-brand")})) == 2

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        freshenv=True,
        confoverrides={"html_theme_options": {"layout": "lHh LpR lff"}},
    )
    def test_a_code_giving_the_sidebar_the_corner_still_draws_the_brand_twice(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len(page.find("a", **{"class": page_class(page, "daisy-brand")})) == 2

    @pytest.mark.sphinx("singlehtml", testroot="basic", freshenv=True)
    def test_the_singlehtml_builder_builds_the_site(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert page.find("div", **{"data-layout": "hHh LpR lff"})


def page_class(page: Page, name: str) -> str | None:
    """Find the full class attribute of the first tag whose classes include one."""
    for _, attrs in page.tags:
        if name in (attrs.get("class") or "").split():
            return attrs["class"]
    return None


class TestComponentLists:
    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={
            "html_theme_options": {"footer_start": "second, first", "footer_end": ""}
        },
    )
    def test_components_are_drawn_in_the_order_listed(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert page.order(TEST_MARKER) == ["second", "first"]

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={"html_theme_options": {"footer_start": ["first.html"]}},
    )
    def test_a_site_template_is_drawn_from_a_python_list(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert page.order(TEST_MARKER) == ["first"]

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={"html_theme_options": {"footer_start": "no-such-component"}},
    )
    def test_an_unknown_name_draws_nothing_and_warns_of_nothing(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert app.warning.getvalue() == ""
        assert page.having(TEST_MARKER) == []

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={
            "html_theme_options": {
                "navbar_start": "",
                "footer_start": "",
                "footer_end": "",
                "secondary_sidebar_items": "",
                "article_header_start": "",
            }
        },
    )
    def test_empty_lists_draw_no_header_and_no_secondary_sidebar(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert app.warning.getvalue() == ""
        assert page.find("aside", **{"aria-label": "Page tools"}) == []
        assert not [
            attrs
            for _, attrs in page.tags
            if "daisy-article-header" in (attrs.get("class") or "").split()
        ]

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={
            "html_theme_options": {
                "navbar_center": "first",
                "footer_start": "first",
                "primary_sidebar_end": "first",
            }
        },
    )
    def test_a_component_in_two_lists_is_drawn_in_both(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert page.order(TEST_MARKER) == ["first", "first", "first"]

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={"html_theme_options": {"navbar_end": "second"}},
    )
    def test_navbar_end_components_appear_once_in_the_page(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert page.order(TEST_MARKER) == ["second"]
        assert len(page.having("data-daisy-navbar-end")) == 1
        assert len(page.having("data-daisy-navbar-end-slot")) == 1

    @pytest.mark.sphinx(
        "html",
        testroot="components",
        freshenv=True,
        confoverrides={"html_theme_options": {"footer_start": "button"}},
    )
    def test_the_icon_button_labels_and_escapes_its_text(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        buttons = page.find("button", **{"aria-label": "Do it <now>"})
        assert len(buttons) == 1
        assert buttons[0]["data-tip"] == 'Tip "this"'
        assert "Do it <now>" not in page.text
