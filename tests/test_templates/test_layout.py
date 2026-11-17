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
    def test_the_primary_sidebar_holds_none_of_the_basic_themes_sidebars(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert [tag for tag in page.having("id") if tag["id"] == "searchbox"] == []

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
        confoverrides={"html_theme_options": {"secondary_sidebar_items": []}},
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
            "html_theme_options": {
                "footer_start": ["second", "first"],
                "footer_end": [],
            }
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
        confoverrides={"html_theme_options": {"footer_start": ["no-such-component"]}},
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
                "navbar_start": [],
                "footer_start": [],
                "footer_end": [],
                "secondary_sidebar_items": [],
                "article_header_start": [],
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
                "navbar_center": ["first"],
                "footer_start": ["first"],
                "primary_sidebar_end": ["first"],
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
        confoverrides={"html_theme_options": {"navbar_end": ["second"]}},
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
        confoverrides={"html_theme_options": {"footer_start": ["button"]}},
    )
    def test_the_icon_button_labels_and_escapes_its_text(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        buttons = page.find("button", **{"aria-label": "Do it <now>"})
        assert len(buttons) == 1
        assert buttons[0]["data-tip"] == 'Tip "this"'
        assert "Do it <now>" not in page.text


class TestReaderPage:
    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_first_focusable_element_skips_to_the_main_landmark(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        body = [tag for tag in page.tags if tag[0] == "body"]
        assert body
        after_body = page.tags[page.tags.index(body[0]) + 1 :]
        first = next(
            attrs
            for name, attrs in after_body
            if (name == "a" and "href" in attrs)
            or name == "button"
            or (attrs.get("tabindex") or "-1") != "-1"
        )
        assert first["href"] == "#main-content"
        assert len(page.find("main", id="main-content")) == 1

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_drawer_opens_and_closes_from_keyboard_reachable_controls(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        controls = [
            attrs
            for name, attrs in page.tags
            if name == "label" and attrs.get("for") == "daisy-drawer"
        ]
        reachable = [
            attrs
            for attrs in controls
            if attrs.get("role") == "button" and attrs.get("tabindex") == "0"
        ]
        assert len(reachable) == 2

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_page_has_one_main_landmark_and_no_main_role(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len([name for name, _ in page.tags if name == "main"]) == 1
        assert not [attrs for _, attrs in page.tags if attrs.get("role") == "main"]

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_both_sidebars_are_labelled_landmarks(self, app: SphinxTestApp) -> None:
        page = built(app)

        asides = [attrs for name, attrs in page.tags if name == "aside"]
        assert len(asides) == 2
        assert all(attrs.get("aria-label") for attrs in asides)
        assert len({attrs["aria-label"] for attrs in asides}) == 2

    @pytest.mark.sphinx("html", testroot="pages", freshenv=True)
    def test_the_body_carries_the_values_sphinx_gives_for_the_index(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        body = page.find("body")[0]
        assert body["data-daisy-root"] == "./"
        assert body["data-daisy-suffix"] == ".html"
        assert body["data-daisy-link-suffix"] == ".html"
        assert body["data-daisy-builder"] == "html"
        assert body["data-daisy-page"] == "index"

    @pytest.mark.sphinx("html", testroot="pages", freshenv=True)
    def test_the_body_carries_the_root_of_a_page_in_a_subdirectory(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app, "sub/third.html")

        body = page.find("body")[0]
        assert body["data-daisy-root"] == "../"
        assert body["data-daisy-page"] == "sub/third"

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    @pytest.mark.parametrize("name", ["search.html", "genindex.html"])
    def test_the_secondary_sidebar_is_left_out_of_search_and_the_index(
        self, app: SphinxTestApp, name: str
    ) -> None:
        page = built(app, name)

        assert page.find("aside", **{"aria-label": "Page tools"}) == []
        assert page.find("main", id="main-content")

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_secondary_sidebar_is_drawn_on_a_normal_page(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len([name for name, _ in page.tags if name == "aside"]) == 2

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        freshenv=True,
        confoverrides={"html_theme_options": {"secondary_sidebar_items": []}},
    )
    def test_an_empty_secondary_list_leaves_one_sidebar(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len([name for name, _ in page.tags if name == "aside"]) == 1


class TestPageScripts:
    @pytest.mark.sphinx("html", testroot="pages", freshenv=True)
    @pytest.mark.parametrize(
        ("name", "prefix"),
        [("index.html", "_static/"), ("sub/third.html", "../_static/")],
    )
    def test_each_page_links_the_key_script_before_the_frame_script(
        self, app: SphinxTestApp, name: str, prefix: str
    ) -> None:
        page = built(app, name)

        sources = [
            attrs["src"]
            for tag, attrs in page.tags
            if tag == "script" and "src" in attrs
        ]
        wanted = [f"{prefix}scripts/keys.js", f"{prefix}scripts/frame.js"]
        assert [source for source in sources if source in wanted] == wanted
        assert all(
            "defer" in attrs
            for tag, attrs in page.tags
            if tag == "script" and attrs.get("src") in wanted
        )

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_both_scripts_are_in_the_output(self, app: SphinxTestApp) -> None:
        app.build()

        scripts = Path(app.outdir) / "_static" / "scripts"
        assert (scripts / "keys.js").is_file()
        assert (scripts / "frame.js").is_file()

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_hooks_the_frame_script_reads_exist(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert page.find("div", **{"data-layout": "hHh LpR lff"})
        assert len(page.find("input", id="daisy-drawer")) == 1
        assert len(page.having("data-daisy-navbar-end")) == 1
        assert len(page.having("data-daisy-navbar-end-slot")) == 1
        classes = [(attrs.get("class") or "").split() for _, attrs in page.tags]
        for name in ("daisy-layout", "daisy-area-header", "daisy-area-primary"):
            assert any(name in found for found in classes)


class TestIndexPages:
    @pytest.mark.sphinx("html", testroot="indexes", freshenv=True)
    def test_no_index_page_has_a_secondary_sidebar(self, app: SphinxTestApp) -> None:
        app.build()
        index_pages = [
            "genindex.html",
            "genindex-all.html",
            "py-modindex.html",
            "search.html",
            *sorted(p.name for p in Path(app.outdir).glob("genindex-?.html")),
        ]

        assert "genindex-F.html" in index_pages
        for name in index_pages:
            page = Page.read(Path(app.outdir) / name)
            assert page.find("aside", **{"aria-label": "Page tools"}) == [], name
            assert page.find("main", id="main-content"), name

    @pytest.mark.sphinx("html", testroot="indexes", freshenv=True)
    def test_an_ordinary_page_has_it(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert len(page.find("aside", **{"aria-label": "Page tools"})) == 1
