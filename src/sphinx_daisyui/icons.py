"""The inline SVG icons the theme draws, read from the bundled ``icons.json``."""

import json
from functools import cached_property
from pathlib import Path

from markupsafe import Markup, escape

FALLBACK = "link"


class Icons:
    """The icons bundled with the theme, by name."""

    @cached_property
    def by_name(self) -> dict[str, str]:
        """The SVG source of every bundled icon, read from disk once.

        Returns:
            A mapping from icon name to its SVG markup.
        """
        path = Path(__file__).parent / "icons.json"
        icons: dict[str, str] = json.loads(path.read_text(encoding="utf-8"))
        return icons

    def svg(self, name: str, classes: str = "size-5") -> Markup:
        """Return an icon as inline SVG, hidden from assistive technology.

        Args:
            name: The bundled icon's name. An unknown name gives the link icon.
            classes: Tailwind classes to put on the ``<svg>`` element.

        Returns:
            The SVG markup, safe to place in a template unescaped.
        """
        source = self.by_name.get(name) or self.by_name[FALLBACK]
        attributes = f'class="{escape(classes)}" aria-hidden="true" focusable="false" '
        # The source is the bundled file and the classes are escaped above.
        return Markup(source.replace("<svg ", f"<svg {attributes}", 1))  # noqa: S704


ICONS = Icons()
