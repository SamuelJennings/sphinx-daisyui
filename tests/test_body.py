import re
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp
from test_templates.page import Page

REGION = "daisy-sphinx-scroll"
TABLE_REGION = re.compile(rf'<div[^>]*class="{REGION}"[^>]*>\s*<table')
OUTER_TABLES = 4
DISPLAY_EQUATIONS = 2
ATTRIBUTION = re.compile(r'<p class="attribution">(.*?)</p>', re.DOTALL)
NAMES = ["Ada", "Grace", "Alan"]
ADMONITIONS = 13
VERSION_NOTES = 4


def built(app: SphinxTestApp) -> tuple[str, Page]:
    """Build the site and read its home page, as written and as parsed."""
    app.build()
    text = (Path(app.outdir) / "index.html").read_text(encoding="utf-8")
    return text, Page(text)


def regions(page: Page) -> list[dict[str, str | None]]:
    """Find the scroll regions of a page."""
    return page.classed("div", REGION)


def link_names(page: Page) -> list[str]:
    """List the accessible names of a page's permalinks."""
    return [
        str(link["aria-label"])
        for link in page.classed("a", "headerlink")
        if link.get("aria-label")
    ]


class TestScrollRegions:
    @pytest.mark.sphinx("html", testroot="body")
    def test_every_outermost_table_and_display_equation_is_a_named_region(
        self, app: SphinxTestApp
    ) -> None:
        _, page = built(app)

        found = regions(page)
        assert len(found) == OUTER_TABLES + DISPLAY_EQUATIONS
        for region in found:
            assert region["role"] == "region"
            assert region["tabindex"] == "0"
            assert (region["aria-label"] or "").strip()

    @pytest.mark.sphinx("html", testroot="body")
    def test_a_table_inside_a_table_is_not_wrapped_again(
        self, app: SphinxTestApp
    ) -> None:
        text, _ = built(app)

        assert text.count("<table") == OUTER_TABLES + 1
        assert len(TABLE_REGION.findall(text)) == OUTER_TABLES

    @pytest.mark.sphinx("html", testroot="body")
    def test_a_table_is_named_by_its_caption_without_the_permalink(
        self, app: SphinxTestApp
    ) -> None:
        _, page = built(app)

        names = [region["aria-label"] or "" for region in regions(page)]
        assert any(name.endswith("Fish & <chips> one") for name in names)
        assert any(name.endswith("Only markup") for name in names)
        assert not any("¶" in name for name in names)

    @pytest.mark.sphinx("html", testroot="body")
    def test_markup_characters_in_a_caption_arrive_escaped(
        self, app: SphinxTestApp
    ) -> None:
        text, _ = built(app)

        assert re.search(r'aria-label="[^"]*Fish &amp; &lt;chips&gt; one"', text)
        assert "<chips>" not in text

    @pytest.mark.sphinx("html", testroot="body")
    def test_an_equations_number_and_id_stay_outside_its_region(
        self, app: SphinxTestApp
    ) -> None:
        text, _ = built(app)

        numbered = re.search(
            rf'id="equation-eq-one".*?<span class="eqno">\(1\).*?</span>\s*'
            rf'<div[^>]*class="{REGION}"',
            text,
            re.DOTALL,
        )
        assert numbered is not None

    @pytest.mark.sphinx("html", testroot="body")
    def test_an_equation_still_holds_its_notation_for_mathjax(
        self, app: SphinxTestApp
    ) -> None:
        text, _ = built(app)

        assert re.search(rf'class="{REGION}".*?a\^2 \+ b\^2 = c\^2', text, re.DOTALL)

    @pytest.mark.sphinx("html", testroot="body")
    def test_inline_math_is_not_wrapped(self, app: SphinxTestApp) -> None:
        text, _ = built(app)

        assert r"\(x\)" in text
        assert not re.search(rf'class="{REGION}"[^>]*>\s*<span class="math', text)

    @pytest.mark.sphinx("html", testroot="body")
    def test_the_build_is_clean(self, app: SphinxTestApp) -> None:
        app.build()

        assert app.warning.getvalue() == ""

    @pytest.mark.sphinx("dirhtml", testroot="body")
    def test_the_regions_are_written_by_the_dirhtml_builder(
        self, app: SphinxTestApp
    ) -> None:
        _, page = built(app)

        assert len(regions(page)) == OUTER_TABLES + DISPLAY_EQUATIONS

    @pytest.mark.sphinx("singlehtml", testroot="body")
    def test_the_regions_are_written_by_the_singlehtml_builder(
        self, app: SphinxTestApp
    ) -> None:
        _, page = built(app)

        found = regions(page)
        assert len(found) == OUTER_TABLES + DISPLAY_EQUATIONS
        assert all((region["aria-label"] or "").strip() for region in found)

    @pytest.mark.sphinx("html", testroot="body", confoverrides={"html_theme": "basic"})
    def test_a_site_on_another_theme_is_left_alone(self, app: SphinxTestApp) -> None:
        text, page = built(app)

        assert regions(page) == []
        assert link_names(page) == []
        assert "\u2014\u2009" not in text


class TestNamedPermalinks:
    @pytest.mark.sphinx("html", testroot="body")
    def test_a_heading_link_is_named_by_the_heading(self, app: SphinxTestApp) -> None:
        _, page = built(app)

        assert any(name.endswith("Salt & <pepper>") for name in link_names(page))

    @pytest.mark.sphinx("html", testroot="body")
    def test_an_api_link_is_named_by_the_signature(self, app: SphinxTestApp) -> None:
        _, page = built(app)

        names = link_names(page)
        assert any(name.endswith("sample.greet") for name in names)
        assert any(name.endswith("sample.Thing") for name in names)

    @pytest.mark.sphinx("html", testroot="body")
    def test_a_caption_link_is_named_by_the_caption(self, app: SphinxTestApp) -> None:
        _, page = built(app)

        names = link_names(page)
        assert any(name.endswith("Fish & <chips> one") for name in names)
        assert any(name.endswith("A figure & its caption") for name in names)

    @pytest.mark.sphinx("html", testroot="body")
    def test_an_equation_link_is_named_by_its_number(self, app: SphinxTestApp) -> None:
        _, page = built(app)

        assert any(name.endswith("(1)") for name in link_names(page))

    @pytest.mark.sphinx("html", testroot="body")
    def test_the_names_are_escaped_in_the_source(self, app: SphinxTestApp) -> None:
        text, _ = built(app)

        assert re.search(r'aria-label="[^"]*Salt &amp; &lt;pepper&gt;"', text)
        assert "<pepper>" not in text


class TestAttributions:
    @pytest.mark.sphinx("html", testroot="body")
    def test_every_attribution_is_spaced_the_same_however_it_was_written(
        self, app: SphinxTestApp
    ) -> None:
        text, _ = built(app)

        found = [re.sub(r"<[^>]+>", "", match) for match in ATTRIBUTION.findall(text)]
        assert len(found) == len(NAMES)
        prefixes = {item[: -len(name)] for item, name in zip(found, NAMES, strict=True)}
        assert all(item.endswith(name) for item, name in zip(found, NAMES, strict=True))
        assert len(prefixes) == 1
        assert next(iter(prefixes)).endswith("\u2009")


class TestAdmonitionIcons:
    @pytest.mark.sphinx("html", testroot="body")
    def test_every_admonition_title_starts_with_an_icon(
        self, app: SphinxTestApp
    ) -> None:
        text, _ = built(app)

        titles = re.findall(
            r'<(?:p|summary)[^>]*class="admonition-title[^"]*"[^>]*>', text
        )
        iconed = re.findall(r'class="admonition-title[^"]*"[^>]*><svg', text)
        assert len(titles) == ADMONITIONS
        assert len(iconed) == ADMONITIONS

    @pytest.mark.sphinx("html", testroot="body")
    def test_every_version_note_starts_with_an_icon(self, app: SphinxTestApp) -> None:
        text, _ = built(app)

        notes = re.findall(
            r'<div class="(?:versionadded|versionchanged|deprecated|versionremoved)">'
            r"\s*<svg",
            text,
        )
        assert len(notes) == VERSION_NOTES

    @pytest.mark.sphinx("html", testroot="body")
    def test_a_generic_admonition_keeps_its_own_title(self, app: SphinxTestApp) -> None:
        text, _ = built(app)

        assert re.search(
            r'class="admonition-title[^"]*"[^>]*><svg.*?</svg>A custom title</p>',
            text,
            re.DOTALL,
        )


class TestPygmentsStylesheet:
    @pytest.mark.sphinx("html", testroot="body")
    def test_no_page_links_the_sphinx_pygments_stylesheet(
        self, app: SphinxTestApp
    ) -> None:
        _, page = built(app)

        hrefs = [str(link["href"]) for link in page.find("link", rel="stylesheet")]
        assert not any(href.split("?")[0].endswith("pygments.css") for href in hrefs)
        assert any("sphinx-daisyui.css" in href for href in hrefs)

    @pytest.mark.sphinx("html", testroot="body", confoverrides={"html_theme": "basic"})
    def test_a_site_on_another_theme_keeps_it(self, app: SphinxTestApp) -> None:
        _, page = built(app)

        hrefs = [str(link["href"]) for link in page.find("link", rel="stylesheet")]
        assert any(href.split("?")[0].endswith("pygments.css") for href in hrefs)
