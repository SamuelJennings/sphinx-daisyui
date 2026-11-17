import re
from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp
from test_templates.page import Page

STYLESHEET = "styles/pygments-modes.css"
SCHEME_ONLY = "html:not([data-mode]) .daisy-sphinx-content .highlight"
DARK_QUERY = "@media (prefers-color-scheme: dark)"
LIGHT_QUERY = "@media not (prefers-color-scheme: dark)"
OPTION = "pygments_{}_style"


def options(**styles: str) -> dict[str, Any]:
    """Build the confoverrides that set the Pygments options by mode."""
    return {
        "html_theme_options": {OPTION.format(mode): s for mode, s in styles.items()}
    }


def selector(mode: str) -> str:
    """Write the selector a mode's rules sit under."""
    return f'html[data-mode="{mode}"] .daisy-sphinx-content .highlight'


def built(app: SphinxTestApp) -> tuple[Page, str | None]:
    """Build the site and read its home page and the Pygments stylesheet."""
    app.build()
    page = Page.read(Path(app.outdir) / "index.html")
    sheet = Path(app.outdir) / "_static" / STYLESHEET
    return page, sheet.read_text(encoding="utf-8") if sheet.exists() else None


def linked(page: Page) -> bool:
    """Tell whether the page links the Pygments stylesheet."""
    return any(STYLESHEET in (link.get("href") or "") for link in page.find("link"))


def media_block(sheet: str, query: str) -> str:
    """Return the text of the first block of a media query."""
    start = sheet.index(query)
    depth = 0
    for position in range(sheet.index("{", start), len(sheet)):
        depth += {"{": 1, "}": -1}.get(sheet[position], 0)
        if depth == 0:
            return sheet[start : position + 1]
    raise AssertionError(query)


class TestBothStyles:
    @pytest.mark.sphinx(
        "html",
        testroot="pygments",
        confoverrides=options(light="friendly", dark="monokai"),
    )
    def test_the_page_links_a_stylesheet_with_rules_under_each_mode(
        self, app: SphinxTestApp
    ) -> None:
        page, sheet = built(app)

        assert linked(page)
        assert sheet is not None
        assert selector("light") in sheet
        assert selector("dark") in sheet
        assert not app.warning.getvalue()

    @pytest.mark.sphinx(
        "html",
        testroot="pygments",
        confoverrides=options(light="friendly", dark="monokai"),
    )
    def test_each_mode_resets_the_token_highlighting_first(
        self, app: SphinxTestApp
    ) -> None:
        _, sheet = built(app)

        assert sheet is not None
        for mode in ("light", "dark"):
            reset = re.search(
                rf"{re.escape(selector(mode))} span\s*\{{(.*?)\}}", sheet, re.DOTALL
            )
            assert reset is not None
            body = reset.group(1)
            for declaration in (
                "color: inherit",
                "background-color: transparent",
                "font-weight: inherit",
                "font-style: inherit",
                "text-decoration: inherit",
            ):
                assert declaration in body
            assert sheet.index(reset.group(0)) < sheet.index(f"{selector(mode)} .k")

    @pytest.mark.sphinx(
        "html",
        testroot="pygments",
        confoverrides=options(light="friendly", dark="monokai"),
    )
    def test_without_a_mode_attribute_the_system_colour_scheme_decides(
        self, app: SphinxTestApp
    ) -> None:
        _, sheet = built(app)

        assert sheet is not None
        dark = media_block(sheet, DARK_QUERY)
        light = media_block(sheet, LIGHT_QUERY)
        assert SCHEME_ONLY in dark
        assert SCHEME_ONLY in light
        assert selector("dark") not in dark
        assert "monokai" not in light  # the styles' own rules stay in their query

    @pytest.mark.sphinx(
        "html",
        testroot="pygments",
        confoverrides=options(light="friendly", dark="monokai"),
    )
    def test_sphinxs_own_pygments_stylesheet_is_not_linked(
        self, app: SphinxTestApp
    ) -> None:
        page, _ = built(app)

        assert not [
            link
            for link in page.find("link")
            if (link.get("href") or "").split("?")[0].endswith("/pygments.css")
        ]


class TestOneStyle:
    @pytest.mark.sphinx(
        "html", testroot="pygments", confoverrides=options(dark="monokai")
    )
    def test_only_the_set_mode_has_rules(self, app: SphinxTestApp) -> None:
        page, sheet = built(app)

        assert linked(page)
        assert sheet is not None
        assert selector("dark") in sheet
        assert selector("light") not in sheet
        assert LIGHT_QUERY not in sheet

    @pytest.mark.sphinx(
        "html", testroot="pygments", confoverrides=options(light="friendly")
    )
    def test_only_the_light_mode_can_be_set(self, app: SphinxTestApp) -> None:
        _, sheet = built(app)

        assert sheet is not None
        assert selector("light") in sheet
        assert selector("dark") not in sheet
        assert DARK_QUERY not in sheet


class TestUnknownStyle:
    @pytest.mark.sphinx(
        "html",
        testroot="pygments",
        confoverrides=options(light="friendly", dark="no-such-style"),
    )
    def test_one_warning_names_the_option_and_the_value(
        self, app: SphinxTestApp
    ) -> None:
        _, sheet = built(app)

        warnings = app.warning.getvalue().splitlines()
        assert len(warnings) == 1
        assert "pygments_dark_style" in warnings[0]
        assert "'no-such-style'" in warnings[0]
        assert sheet is not None
        assert selector("light") in sheet
        assert selector("dark") not in sheet

    @pytest.mark.sphinx(
        "html",
        testroot="pygments",
        srcdir="pygments-none-valid",
        confoverrides=options(light="nope", dark="also-nope"),
    )
    def test_no_valid_style_links_no_stylesheet(self, app: SphinxTestApp) -> None:
        page, sheet = built(app)

        assert len(app.warning.getvalue().splitlines()) == 2
        assert sheet is None
        assert not linked(page)

    @pytest.mark.sphinx(
        "html",
        testroot="pygments",
        confoverrides={
            **options(dark="no-such-style"),
            "suppress_warnings": ["daisyui.pygments"],
        },
    )
    def test_the_warning_can_be_suppressed(self, app: SphinxTestApp) -> None:
        built(app)

        assert not app.warning.getvalue()


class TestNoStyle:
    @pytest.mark.sphinx("html", testroot="pygments", srcdir="pygments-none")
    def test_neither_option_writes_or_links_a_stylesheet(
        self, app: SphinxTestApp
    ) -> None:
        page, sheet = built(app)

        assert sheet is None
        assert not linked(page)
        assert not app.warning.getvalue()
