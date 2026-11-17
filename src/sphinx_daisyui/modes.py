"""The colour modes a site offers and the themes they draw."""

import json
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

from .options import FALSE_WORDS, ThemeOptions

LOGGER = logging.getLogger(__name__)
MODES = ("auto", "light", "dark")
THEMES: list[str] = json.loads(
    (Path(__file__).parent / "themes.json").read_text(encoding="utf-8")
)
PICKER_ALL = {"true", "all"}


class Modes:
    """The themes a site draws and the choices its readers are offered.

    Theme names are taken as given, so a site's own theme works as well as one
    of daisyUI's.

    Args:
        light: The theme the light mode draws.
        dark: The theme the dark mode draws.
        default: The mode a reader sees before choosing: one of ``MODES``.
        picker: The themes a reader may pick by name, empty for none.
    """

    def __init__(self, light: str, dark: str, default: str, picker: list[str]) -> None:
        self.light = light
        self.dark = dark
        self.default = default
        self.picker = picker

    @classmethod
    def from_options(cls, options: ThemeOptions) -> "Modes":
        """Read the modes from a site's theme options.

        Args:
            options: The site's theme options.

        Returns:
            The modes, with ``auto`` as the starting mode when the option is
            unset or not one of ``MODES``.
        """
        default = options.text("default_mode").strip().lower()
        return cls(
            light=options.text("light_theme", "light"),
            dark=options.text("dark_theme", "dark"),
            default=default if default in MODES else "auto",
            picker=cls.picked(options.values.get("theme_picker"), options),
        )

    @staticmethod
    def picked(value: Any, options: ThemeOptions) -> list[str]:
        """Work out which themes the picker offers.

        Args:
            value: The raw ``theme_picker`` option.
            options: The site's theme options, which read a list of names.

        Returns:
            Every bundled theme for ``True``, ``"all"`` or ``"true"``, the
            names given for a list or a comma-separated string, none for
            ``False`` or ``"false"``.
        """
        word = str(value).strip().lower()
        if value is True or word in PICKER_ALL:
            return list(THEMES)
        if word in FALSE_WORDS:
            return []
        return options.names("theme_picker")


def check_modes(app: Sphinx) -> None:
    """Warn once when the starting mode is not one of the three modes.

    Args:
        app: The Sphinx application building the site.
    """
    builder = app.builder
    if not isinstance(builder, StandaloneHTMLBuilder):
        return
    if app.config.html_theme != "daisyui":
        return
    options = ThemeOptions(builder.theme.get_options(app.config.html_theme_options))
    word = options.text("default_mode")
    if word and word.strip().lower() not in MODES:
        LOGGER.warning(
            "The theme option default_mode is %r. Use one of: %s. "
            "The page starts in auto.",
            word,
            ", ".join(MODES),
            type="daisyui",
            subtype="modes",
        )
