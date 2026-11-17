import re
from pathlib import Path

import pytest
from babel.messages import Catalog
from babel.messages.extract import extract_from_dir
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
from sphinx.testing.util import SphinxTestApp

import sphinx_daisyui

from .page import Page

SKIP_LINK = "Skip to content"
BREADCRUMB = "Breadcrumb"
TOGGLE = "Show the pages in %(title)s"
TABLE = "Table"
EQUATION = "Equation"
CHOOSE_THEME = "Choose the colour theme"
SYSTEM_MODE = "Match the system"
THEME = Path(sphinx_daisyui.__file__).parent
SHIPPED = THEME / "locale" / "sphinx.pot"


@pytest.fixture
def catalogue(app_params: object) -> Catalog:
    """Compile a German catalogue into the test site before Sphinx loads it."""
    catalogue = Catalog(locale="de")
    catalogue.add(SKIP_LINK, "Zum Inhalt springen")
    catalogue.add(BREADCRUMB, "Brotkrumen")
    catalogue.add(TOGGLE, "Seiten in %(title)s anzeigen")
    catalogue.add(TABLE, "Tabelle")
    catalogue.add(EQUATION, "Gleichung")
    catalogue.add(CHOOSE_THEME, "Farbschema wählen")
    catalogue.add(SYSTEM_MODE, "Wie das System")
    srcdir = Path(app_params.kwargs["srcdir"])  # type: ignore[attr-defined]
    folder = srcdir / "locale" / "de" / "LC_MESSAGES"
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / "sphinx.mo").open("wb") as stream:
        write_mo(stream, catalogue)
    return catalogue


class TestTranslation:
    @pytest.mark.sphinx("html", testroot="locale", freshenv=True)
    def test_the_skip_link_is_translated_by_the_sites_catalogue(
        self, catalogue: Catalog, app: SphinxTestApp
    ) -> None:
        app.build()

        text = (Path(app.outdir) / "index.html").read_text(encoding="utf-8")
        link = re.search(r'<a href="#main-content"[^>]*>(.*?)</a>', text)
        assert link is not None
        message = catalogue.get(SKIP_LINK)
        assert message is not None
        assert link.group(1) == message.string

    @pytest.mark.sphinx("html", testroot="locale", freshenv=True)
    def test_a_toggles_name_and_the_breadcrumb_landmark_are_translated(
        self, catalogue: Catalog, app: SphinxTestApp
    ) -> None:
        app.build()

        toggle = catalogue.get(TOGGLE)
        landmark = catalogue.get(BREADCRUMB)
        assert toggle is not None
        assert landmark is not None
        home = Page.read(Path(app.outdir) / "index.html")
        section = Page.read(Path(app.outdir) / "section.html")
        labels = [t.get("aria-label") for t in home.find("button", type="button")]
        assert toggle.string % {"title": "Section"} in labels
        assert landmark.string in [nav.get("aria-label") for nav in section.find("nav")]

    @pytest.mark.sphinx("html", testroot="locale", freshenv=True)
    def test_the_names_of_an_uncaptioned_table_and_equation_are_translated(
        self, catalogue: Catalog, app: SphinxTestApp
    ) -> None:
        app.build()

        table = catalogue.get(TABLE)
        equation = catalogue.get(EQUATION)
        assert table is not None
        assert equation is not None
        page = Page.read(Path(app.outdir) / "index.html")
        names = [
            r.get("aria-label") for r in page.classed("div", "daisy-sphinx-scroll")
        ]
        assert names == [table.string, equation.string]

    @pytest.mark.sphinx("html", testroot="locale", freshenv=True)
    def test_the_theme_menus_name_and_a_mode_button_are_translated(
        self, catalogue: Catalog, app: SphinxTestApp
    ) -> None:
        app.build()

        name = catalogue.get(CHOOSE_THEME)
        system = catalogue.get(SYSTEM_MODE)
        assert name is not None
        assert system is not None
        text = (Path(app.outdir) / "index.html").read_text(encoding="utf-8")
        page = Page(text)
        assert name.string in [b.get("aria-label") for b in page.find("div")]
        assert re.search(
            r'data-daisy-set-mode="auto"[^>]*>.*?' + re.escape(system.string), text
        )

    def test_every_message_the_templates_mark_is_in_the_shipped_template(self) -> None:
        marked = {
            message
            for _, _, message, _, _ in [
                *extract_from_dir(
                    str(THEME / "theme"),
                    method_map=[("**.html", "jinja2.ext.babel_extract")],
                    options_map={"**.html": {"extensions": "jinja2.ext.i18n"}},
                ),
                *extract_from_dir(
                    str(THEME),
                    method_map=[("**.py", "python")],
                    keywords={"translate": None},
                ),
            ]
        }
        with SHIPPED.open("rb") as stream:
            shipped = {message.id for message in read_po(stream) if message.id}

        assert marked
        assert marked <= shipped
