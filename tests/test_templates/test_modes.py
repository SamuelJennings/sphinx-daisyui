from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page


def head_of(app: SphinxTestApp) -> Page:
    app.build()
    return Page.read(Path(app.outdir) / "index.html").inside("head")


def mode_script(head: Page) -> dict[str, str | None]:
    return next(tag for tag in head.find("script") if "data-light-theme" in tag)


def sheet_and_script_order(head: Page) -> list[str]:
    order = []
    for name, attrs in head.tags:
        if name == "link" and attrs.get("rel") == "stylesheet":
            order.append("stylesheet")
        if name == "script" and "data-light-theme" in attrs:
            order.append("mode")
    return order


def options(**values: Any) -> dict[str, Any]:
    return {"html_theme_options": values}


class TestModeScript:
    @pytest.mark.sphinx("html", testroot="modes", freshenv=True)
    def test_the_script_is_in_the_head_without_defer_after_the_stylesheets(
        self, app: SphinxTestApp
    ) -> None:
        head = head_of(app)

        script = mode_script(head)
        assert "defer" not in script
        assert "async" not in script
        assert (script["src"] or "").endswith("_static/scripts/mode.js")
        order = sheet_and_script_order(head)
        assert order[-1] == "mode"
        assert "stylesheet" in order

    @pytest.mark.sphinx("html", testroot="modes", freshenv=True)
    def test_the_defaults_reach_the_script(self, app: SphinxTestApp) -> None:
        script = mode_script(head_of(app))

        assert script["data-light-theme"] == "light"
        assert script["data-dark-theme"] == "dark"
        assert script["data-default-mode"] == "auto"
        assert script["data-themes"] == ""

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides=options(
            light_theme="cupcake",
            dark_theme="dracula",
            default_mode="dark",
            theme_picker=["cupcake", "dracula", "nord"],
        ),
    )
    def test_the_sites_values_reach_the_script(self, app: SphinxTestApp) -> None:
        script = mode_script(head_of(app))

        assert script["data-light-theme"] == "cupcake"
        assert script["data-dark-theme"] == "dracula"
        assert script["data-default-mode"] == "dark"
        assert script["data-themes"] == "cupcake dracula nord"

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides=options(default_mode="sepia"),
    )
    def test_an_unknown_starting_mode_reaches_the_script_as_auto(
        self, app: SphinxTestApp
    ) -> None:
        assert mode_script(head_of(app))["data-default-mode"] == "auto"

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides=options(
            light_theme='"><b>x', dark_theme="a&b", theme_picker=['"><i>y']
        ),
    )
    def test_names_holding_markup_reach_the_attributes_escaped(
        self, app: SphinxTestApp
    ) -> None:
        app.build()
        text = (Path(app.outdir) / "index.html").read_text(encoding="utf-8")
        script = mode_script(Page(text).inside("head"))

        assert script["data-light-theme"] == '"><b>x'
        assert script["data-dark-theme"] == "a&b"
        assert script["data-themes"] == '"><i>y'
        assert "<b>x" not in text
        assert "<i>y" not in text

    @pytest.mark.sphinx("html", testroot="modes", freshenv=True)
    def test_the_page_declares_both_colour_schemes(self, app: SphinxTestApp) -> None:
        head = head_of(app)

        assert head.find("meta", name="color-scheme", content="light dark")
