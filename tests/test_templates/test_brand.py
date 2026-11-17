from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

HOSTILE = '<b>&"'
ESCAPED = "&lt;b&gt;&amp;&#34;"
WIDE_HIDDEN = "lg:hidden"
SIDEBAR_CODE = "lHh LpR lff"
BOTH = {"image_light": "light.svg", "image_dark": "dark.svg"}


def options(**values: Any) -> dict[str, Any]:
    return {"html_theme_options": values}


def read(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def sources(page: Page) -> list[str | None]:
    return [tag["src"] for tag in page.find("img")]


def navbar_wrapper_hidden_on_wide_screens(page: Page) -> bool:
    return bool(page.inside("header").find("div", **{"class": WIDE_HIDDEN}))


def sidebar_head_hidden_on_wide_screens(page: Page) -> bool:
    head = page.inside("aside").find("div")[1]
    return WIDE_HIDDEN in (head["class"] or "").split()


class TestBrandOnThePage:
    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides=options(light_logo="light.svg", dark_logo="dark.svg"),
    )
    def test_the_images_are_addressed_from_a_page_at_the_root(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        assert sources(page) == ["_static/light.svg", "_static/dark.svg"] * 2

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides=options(light_logo="light.svg", dark_logo="dark.svg"),
    )
    def test_the_images_are_addressed_from_a_page_one_level_down(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app, "sub/page.html")

        assert (
            sources(page)
            == [
                "../_static/light.svg",
                "../_static/dark.svg",
            ]
            * 2
        )

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides=options(logo={"text": HOSTILE, "link": f"/a?b=1&c={HOSTILE}"}),
    )
    def test_the_text_and_link_reach_the_page_escaped(self, app: SphinxTestApp) -> None:
        page = read(app)

        assert f'<span class="truncate text-base">{ESCAPED}</span>' in page.text
        assert HOSTILE not in page.text.replace(f"c={HOSTILE}", "")
        links = [
            tag["href"]
            for tag in page.find("a")
            if "daisy-brand" in (tag["class"] or "")
        ]
        assert links == [f"/a?b=1&c={HOSTILE}"] * 2

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides=options(logo={**BOTH, "alt_text": HOSTILE}),
    )
    def test_the_alt_text_reaches_the_page_escaped(self, app: SphinxTestApp) -> None:
        page = read(app)

        assert [tag["alt"] for tag in page.find("img")] == [HOSTILE] * 4
        assert f'alt="{ESCAPED}"' in page.text

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides=options(logo={**BOTH, "text": "My site"}),
    )
    def test_the_images_say_nothing_when_the_text_is_shown(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        assert [tag["alt"] for tag in page.find("img")] == [""] * 4

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides=options(layout=SIDEBAR_CODE, light_logo="light.svg"),
    )
    def test_the_brand_is_written_twice_and_the_navbar_copy_yields_to_the_sidebar(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        assert len(sources(page)) == 4
        assert len(page.inside("header").find("img")) == 2
        assert len(page.inside("aside").find("img")) == 2
        assert navbar_wrapper_hidden_on_wide_screens(page)
        assert not sidebar_head_hidden_on_wide_screens(page)

    @pytest.mark.sphinx(
        "html",
        testroot="logo",
        freshenv=True,
        confoverrides=options(light_logo="light.svg"),
    )
    def test_the_sidebar_copy_yields_to_the_navbar_under_the_default_code(
        self, app: SphinxTestApp
    ) -> None:
        page = read(app)

        assert len(sources(page)) == 4
        assert not navbar_wrapper_hidden_on_wide_screens(page)
        assert sidebar_head_hidden_on_wide_screens(page)
