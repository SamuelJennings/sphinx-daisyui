from collections.abc import Callable
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.brand import Brand
from sphinx_daisyui.options import ThemeOptions

LATE = 900  # after the theme's own handler, which runs at the default 500
BOTH = {"image_light": "light.svg", "image_dark": "dark.svg"}


def pathto(path: str, resource: int = 0) -> str:
    """Stand in for Sphinx's pathto on a page one level down."""
    return f"../{path}" if resource else f"../{path or 'index'}.html"


def make(options: dict[str, Any], **context: Any) -> Brand:
    context = {
        "pathto": pathto,
        "docstitle": "Docs title",
        "project": "Project",
        "root_doc": "index",
        **context,
    }
    return Brand.from_options(ThemeOptions(options), context)


@pytest.fixture
def brands(app: SphinxTestApp) -> Callable[[str], Brand]:
    """Collect each page's brand as the build produces it."""
    seen: dict[str, Brand] = {}

    def collect(
        app: SphinxTestApp,
        pagename: str,
        templatename: str,
        context: dict[str, Any],
        doctree: object,
    ) -> None:
        seen[pagename] = context["daisy"]["brand"]

    app.connect("html-page-context", collect, priority=LATE)
    app.build()
    return seen.__getitem__


class TestBrand:
    def test_a_site_with_no_logo_shows_its_title_only(self) -> None:
        brand = make({})

        assert (brand.light, brand.dark) == ("", "")
        assert brand.text == "Docs title"

    def test_the_project_name_stands_in_for_a_missing_title(self) -> None:
        assert make({}, docstitle="").text == "Project"

    def test_the_homepage_is_the_default_link(self) -> None:
        assert make({}).href == "../index.html"

    def test_the_html_logo_serves_both_modes(self) -> None:
        brand = make({}, logo_url="../_static/site.svg")

        assert brand.light == brand.dark == "../_static/site.svg"

    def test_a_full_html_logo_address_passes_through(self) -> None:
        brand = make({}, logo_url="https://example.org/site.svg")

        assert brand.light == brand.dark == "https://example.org/site.svg"

    def test_the_logo_option_gives_each_mode_its_image(self) -> None:
        brand = make({"logo": BOTH})

        assert brand.light == "../_static/light.svg"
        assert brand.dark == "../_static/dark.svg"

    def test_a_light_image_alone_serves_the_dark_mode(self) -> None:
        brand = make({"logo": {"image_light": "light.svg"}})

        assert brand.light == brand.dark == "../_static/light.svg"

    def test_a_logo_image_wins_over_the_html_logo(self) -> None:
        brand = make(
            {"logo": {"image_light": "light.svg"}}, logo_url="../_static/site.svg"
        )

        assert brand.light == "../_static/light.svg"

    @pytest.mark.parametrize(
        "image", ["light.svg", "_static/light.svg", "https://example.org/light.svg"]
    )
    def test_a_logo_resolves_in_each_form_it_is_given(self, image: str) -> None:
        expected = {
            "light.svg": "../_static/light.svg",
            "_static/light.svg": "../_static/light.svg",
            "https://example.org/light.svg": "https://example.org/light.svg",
        }[image]

        assert make({"logo": {"image_light": image}}).light == expected

    def test_a_logo_that_carries_the_name_is_drawn_without_the_text(self) -> None:
        brand = make({"logo": BOTH})

        assert brand.text == ""
        assert brand.alt == "Project"

    def test_the_logo_text_is_shown_beside_the_images(self) -> None:
        brand = make({"logo": {**BOTH, "text": "My site"}})

        assert brand.text == "My site"

    def test_the_alt_text_is_read_from_the_logo_option(self) -> None:
        assert make({"logo": {**BOTH, "alt_text": "Our mark"}}).alt == "Our mark"

    def test_the_link_in_the_logo_option_is_followed(self) -> None:
        brand = make({"logo": {"link": "https://example.org/"}})

        assert brand.href == "https://example.org/"


class TestBrandInABuild:
    @pytest.mark.sphinx("html", testroot="logo", freshenv=True)
    def test_a_site_with_no_logo_shows_its_title_only(
        self, brands: Callable[[str], Brand]
    ) -> None:
        brand = brands("index")

        assert brand.light == ""
        assert brand.text.startswith("Logo")

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides={"html_logo": "_static/light.svg"},
    )
    def test_the_html_logo_serves_both_modes_from_each_depth(
        self, brands: Callable[[str], Brand]
    ) -> None:
        assert brands("index").light == brands("index").dark == "_static/light.svg"
        assert brands("sub/page").light == "../_static/light.svg"
        assert brands("sub/page").dark == "../_static/light.svg"

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides={"html_theme_options": {"logo": BOTH}},
    )
    def test_the_logo_option_gives_both_images_from_each_depth(
        self, brands: Callable[[str], Brand]
    ) -> None:
        assert brands("index").dark == "_static/dark.svg"
        assert brands("sub/page").light == "../_static/light.svg"

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides={"html_theme_options": {"logo": {"image_light": "light.svg"}}},
    )
    def test_a_light_image_alone_serves_the_dark_mode(
        self, brands: Callable[[str], Brand]
    ) -> None:
        assert brands("sub/page").dark == "../_static/light.svg"

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides={
            "html_theme_options": {
                "logo": {
                    "image_light": "_static/light.svg",
                    "link": "https://example.org/",
                },
            }
        },
    )
    def test_a_static_path_and_a_link_resolve_from_each_depth(
        self, brands: Callable[[str], Brand]
    ) -> None:
        assert brands("index").light == "_static/light.svg"
        assert brands("sub/page").light == "../_static/light.svg"
        assert brands("sub/page").href == "https://example.org/"

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides={
            "html_theme_options": {
                "logo": {"image_light": "https://example.org/light.svg"}
            }
        },
    )
    def test_a_full_address_resolves_from_each_depth(
        self, brands: Callable[[str], Brand]
    ) -> None:
        assert brands("sub/page").light == "https://example.org/light.svg"

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides={"html_theme_options": {"logo": BOTH}},
    )
    def test_a_logo_without_text_gives_empty_text_and_an_alt_naming_the_site(
        self, brands: Callable[[str], Brand]
    ) -> None:
        brand = brands("index")

        assert brand.text == ""
        assert brand.alt == "Logo"
