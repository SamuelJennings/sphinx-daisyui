import json
from pathlib import Path

from markupsafe import Markup

from sphinx_daisyui.icons import Icons

ICONS_JSON = Path(__file__).parent.parent / "src" / "sphinx_daisyui" / "icons.json"


class TestIcons:
    def test_a_known_name_returns_its_svg_with_the_classes(self) -> None:
        svg = Icons().svg("search", "size-4 text-primary")

        assert isinstance(svg, Markup)
        assert svg.startswith('<svg class="size-4 text-primary"')
        assert 'aria-hidden="true"' in svg
        assert 'focusable="false"' in svg
        assert json.loads(ICONS_JSON.read_text())["search"].split(" ", 1)[1] in svg

    def test_the_default_size_is_applied(self) -> None:
        assert 'class="size-5"' in Icons().svg("search")

    def test_an_unknown_name_falls_back_to_the_link_icon(self) -> None:
        assert Icons().svg("no-such-icon") == Icons().svg("link")

    def test_classes_are_escaped(self) -> None:
        svg = Icons().svg("search", '"><script>alert(1)</script>')

        assert "<script>" not in svg
        assert "&lt;script&gt;" in svg
