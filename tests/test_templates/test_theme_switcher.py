from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.events import COMPONENT_OPTIONS
from sphinx_daisyui.modes import THEMES

from .page import Page

MARKUP_NAME = 'x"><b>y</b>'


def options(**values: Any) -> dict[str, Any]:
    return {"html_theme_options": values}


def built(app: SphinxTestApp) -> Page:
    app.build()
    return Page.read(Path(app.outdir) / "index.html")


def themes_of(page: Page) -> list[str | None]:
    return page.order("data-daisy-set-theme")


class TestThemeSwitcher:
    @pytest.mark.sphinx("html", testroot="modes", freshenv=True)
    def test_the_menu_is_drawn_in_the_navbar_end_slot_by_default(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        slot = Page(page.text[page.text.index("data-daisy-navbar-end") :])
        assert slot.find("button", **{"data-daisy-set-mode": "auto"})
        assert page.having("data-daisy-mode-icon")
        assert page.having("data-daisy-mode-current")

    @pytest.mark.sphinx("html", testroot="modes", freshenv=True)
    def test_there_are_three_mode_buttons_and_no_theme_buttons_by_default(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert page.order("data-daisy-set-mode") == ["auto", "light", "dark"]
        assert themes_of(page) == []

    @pytest.mark.sphinx("html", testroot="modes", freshenv=True)
    def test_the_root_is_a_navbar_dropdown(self, app: SphinxTestApp) -> None:
        page = built(app)

        roots = page.classed("div", "daisy-dropdown")
        assert any("data-daisy-mode-names" in root for root in roots)

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides=options(theme_picker=True),
    )
    def test_true_offers_every_bundled_theme_in_order(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert themes_of(page) == THEMES
        assert [t["data-theme"] for t in page.having("data-theme")][-len(THEMES) :] == (
            THEMES
        )

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides=options(theme_picker=["nord", "cupcake", "nord"]),
    )
    def test_a_list_offers_its_names_in_order_and_a_repeat_once(
        self, app: SphinxTestApp
    ) -> None:
        assert themes_of(built(app)) == ["nord", "cupcake"]

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides=options(theme_picker="nord, cupcake,nord"),
    )
    def test_a_comma_separated_string_offers_the_same_names(
        self, app: SphinxTestApp
    ) -> None:
        assert themes_of(built(app)) == ["nord", "cupcake"]

    @pytest.mark.sphinx(
        "html", testroot="modes", freshenv=True, confoverrides=options(theme_picker="")
    )
    def test_an_empty_picker_offers_no_theme(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert themes_of(page) == []
        assert page.order("data-daisy-set-mode") == ["auto", "light", "dark"]

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides=options(
            theme_picker=True,
            **{name: [] for name in COMPONENT_OPTIONS},
        ),
    )
    def test_left_out_of_every_list_no_menu_is_drawn_and_the_modes_still_apply(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert not page.having("data-daisy-set-mode")
        assert not page.having("data-daisy-mode-icon")
        assert page.having("data-light-theme")

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides=options(theme_picker=[MARKUP_NAME]),
    )
    def test_a_name_with_markup_characters_is_escaped(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert "<b>y</b>" not in page.text
        assert themes_of(page) == [MARKUP_NAME]
        assert [
            t["data-theme"]
            for t in page.having("data-theme")
            if t["data-theme"] == MARKUP_NAME
        ]


class TestThemeMenuScript:
    @pytest.mark.sphinx("html", testroot="modes", freshenv=True)
    def test_the_page_loads_the_menu_script_deferred(self, app: SphinxTestApp) -> None:
        page = built(app)

        found = [
            tag
            for tag in page.find("script")
            if (tag["src"] or "").endswith("_static/scripts/theme-menu.js")
        ]
        assert len(found) == 1
        assert "defer" in found[0]
