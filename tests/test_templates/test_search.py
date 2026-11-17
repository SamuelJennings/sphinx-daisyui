import re
from pathlib import Path
from urllib.parse import urljoin

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

PAGES = ["index.html", "guide.html", "nested/deep.html", "search.html", "genindex.html"]
DEPTH = {name: name.count("/") for name in PAGES}
STRINGS = ("prompt", "nothing", "unavailable", "page", "section")
SCRIPTS = ("language-data", "searchtools", "searchindex")


def built(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def dialog_of(page: Page) -> dict[str, str | None]:
    found = page.find("dialog", id="daisy-search")
    assert len(found) == 1
    return found[0]


class TestSearchDialog:
    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    def test_every_page_carries_the_dialog_once(self, app: SphinxTestApp) -> None:
        app.build()

        for name in PAGES:
            text = (Path(app.outdir) / name).read_text(encoding="utf-8")

            assert len(re.findall(r'id="daisy-search"', text)) == 1, name

    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    def test_the_form_goes_to_the_search_page_from_any_depth(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        for name in DEPTH:
            page = Page.read(Path(app.outdir) / name)
            form = page.find("form", role="search")

            assert len(form) == 1, name
            assert form[0].get("method") == "get"
            target = urljoin("http://site/" + name, form[0].get("action") or "")
            assert target.split("#")[0] == "http://site/search.html", name

    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    def test_the_hooks_the_script_reads_are_present(self, app: SphinxTestApp) -> None:
        page = built(app)

        field = page.classed("input", "daisy-search-input")
        assert [(f.get("name"), f.get("type")) for f in field] == [("q", "search")]
        assert field[0].get("aria-controls") == "daisy-search-results"
        assert field[0].get("role") == "combobox"
        assert field[0].get("aria-expanded") == "false"
        assert len(page.classed("p", "daisy-search-status")) == 1
        assert page.find("ul", id="daisy-search-results", role="listbox")
        assert page.having("data-daisy-search-close")
        assert page.having("data-daisy-mod")

    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    def test_the_dialog_names_the_files_of_sphinxs_search_from_any_depth(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        for name in PAGES:
            dialog = dialog_of(Page.read(Path(app.outdir) / name))
            folder = (Path(app.outdir) / name).parent
            addresses = [dialog.get(f"data-daisy-{script}") or "" for script in SCRIPTS]

            assert all(addresses), name
            assert all((folder / address).is_file() for address in addresses), name

    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    def test_the_dialog_holds_the_strings_the_script_writes(
        self, app: SphinxTestApp
    ) -> None:
        dialog = dialog_of(built(app))

        assert all(dialog.get(f"data-daisy-{name}") for name in STRINGS)
        assert "%(query)s" in (dialog.get("data-daisy-nothing") or "")
        assert dialog.get("data-daisy-as-you-type") == "true"

    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    def test_the_dialog_comes_after_the_pages_content(self, app: SphinxTestApp) -> None:
        page = built(app, "genindex.html")

        assert page.text.index('id="daisy-search"') > page.text.index("<main")


class TestSearchButton:
    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    def test_the_button_is_in_the_persistent_slot_not_the_end_slot(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        buttons = page.classed("button", "daisy-search-open")
        end = page.text.index("data-daisy-navbar-end")
        button = page.text.index("daisy-search-open")
        assert len(buttons) == 1
        assert buttons[0].get("aria-haspopup") == "dialog"
        assert buttons[0].get("type") == "button"
        assert button < end

    @pytest.mark.sphinx(
        "html",
        testroot="search",
        freshenv=True,
        confoverrides={
            "html_theme_options": {
                "navbar_persistent": [],
                "navbar_end": ["search-button-field"],
            }
        },
    )
    def test_the_button_follows_the_slot_a_site_puts_it_in(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        end = page.text.index("data-daisy-navbar-end")
        assert page.text.index("daisy-search-open") > end


def options(**theme: object) -> dict[str, object]:
    return {"confoverrides": {"html_theme_options": theme}}


class TestSearchOptions:
    @pytest.mark.sphinx(
        "html",
        testroot="search",
        freshenv=True,
        **options(navbar_persistent=[], navbar_start=["search-button-field"]),
    )
    def test_the_button_follows_the_navbar_start_slot(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert len(page.classed("button", "daisy-search-open")) == 1
        assert len(page.find("dialog", id="daisy-search")) == 1
        assert page.text.index("daisy-search-open") < page.text.index(
            "data-daisy-navbar-end"
        )

    @pytest.mark.sphinx(
        "html",
        testroot="search",
        freshenv=True,
        **options(navbar_persistent=[], footer_end=["search-button-field"]),
    )
    def test_the_button_follows_the_footer_slot(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert len(page.classed("button", "daisy-search-open")) == 1
        assert len(page.find("dialog", id="daisy-search")) == 1
        assert page.text.index("daisy-search-open") > page.text.index("<footer")

    @pytest.mark.sphinx(
        "html",
        testroot="search",
        freshenv=True,
        **options(search_bar_text="<b>Find</b> & go"),
    )
    def test_the_text_reaches_the_button_and_the_field_escaped(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        field = page.classed("input", "daisy-search-input")
        assert field[0].get("placeholder") == "<b>Find</b> & go"
        assert "<b>Find</b>" not in page.text
        assert "&lt;b&gt;Find&lt;/b&gt; &amp; go" in page.inside("button").text

    @pytest.mark.sphinx(
        "html", testroot="search", freshenv=True, **options(search_as_you_type=False)
    )
    def test_as_you_type_off_by_a_false_flag(self, app: SphinxTestApp) -> None:
        dialog = dialog_of(built(app))

        assert dialog.get("data-daisy-as-you-type") == "false"

    @pytest.mark.sphinx(
        "html", testroot="search", freshenv=True, **options(search_as_you_type="false")
    )
    def test_as_you_type_off_by_the_word_false(self, app: SphinxTestApp) -> None:
        dialog = dialog_of(built(app))

        assert dialog.get("data-daisy-as-you-type") == "false"

    @pytest.mark.sphinx(
        "html", testroot="search", freshenv=True, **options(disable_search=True)
    )
    def test_search_off_by_a_true_flag_leaves_no_button_or_dialog(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        for name in PAGES:
            page = Page.read(Path(app.outdir) / name)
            assert not page.classed("button", "daisy-search-open"), name
            assert not page.find("dialog", id="daisy-search"), name
            assert not page.having("data-daisy-search-close"), name
        assert (Path(app.outdir) / "search.html").is_file()
        assert Page.read(Path(app.outdir) / "search.html").find("form")

    @pytest.mark.sphinx(
        "html", testroot="search", freshenv=True, **options(disable_search="true")
    )
    def test_search_off_by_the_word_true_leaves_no_button_or_dialog(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        for name in PAGES:
            page = Page.read(Path(app.outdir) / name)
            assert not page.classed("button", "daisy-search-open"), name
            assert not page.find("dialog", id="daisy-search"), name
            assert not page.having("data-daisy-search-close"), name
        assert (Path(app.outdir) / "search.html").is_file()
        assert Page.read(Path(app.outdir) / "search.html").find("form")

    @pytest.mark.sphinx("html", testroot="search", freshenv=True)
    def test_a_site_setting_none_of_them_builds_without_warnings(
        self, app: SphinxTestApp, warning: object
    ) -> None:
        app.build()

        assert str(warning.getvalue()) == ""  # type: ignore[attr-defined]
