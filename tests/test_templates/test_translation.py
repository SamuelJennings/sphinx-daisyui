import re
from pathlib import Path

import pytest
from babel.messages import Catalog
from babel.messages.extract import extract_from_dir
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
from sphinx.testing.util import SphinxTestApp

import sphinx_daisyui

SKIP_LINK = "Skip to content"
THEME = Path(sphinx_daisyui.__file__).parent
SHIPPED = THEME / "locale" / "sphinx.pot"


@pytest.fixture
def catalogue(app_params: object) -> Catalog:
    """Compile a German catalogue into the test site before Sphinx loads it."""
    catalogue = Catalog(locale="de")
    catalogue.add(SKIP_LINK, "Zum Inhalt springen")
    srcdir = Path(app_params.kwargs["srcdir"])  # type: ignore[attr-defined]
    folder = srcdir / "locale" / "de" / "LC_MESSAGES"
    folder.mkdir(parents=True)
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

    def test_every_message_the_templates_mark_is_in_the_shipped_template(self) -> None:
        marked = {
            message
            for _, _, message, _, _ in extract_from_dir(
                str(THEME / "theme"),
                method_map=[("**.html", "jinja2.ext.babel_extract")],
                options_map={"**.html": {"extensions": "jinja2.ext.i18n"}},
            )
        }
        with SHIPPED.open("rb") as stream:
            shipped = {message.id for message in read_po(stream) if message.id}

        assert marked
        assert marked <= shipped
