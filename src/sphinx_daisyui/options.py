"""The theme options a site sets."""

import json
from collections.abc import Callable, Mapping
from typing import Any

from .layout import LayoutCode

TRUE_WORDS = {"true", "1", "yes", "on"}
FALSE_WORDS = {"false", "0", "no", "off"}


class ThemeOptions:
    """The values of a theme's options, with a reader for each form they take.

    Sphinx hands every option over as given in ``conf.py`` or as the string in
    ``theme.toml``, so a list may be a comma-separated string and a flag may be
    the word ``"true"``.

    Args:
        values: The option values by name, without the ``theme_`` prefix.
    """

    def __init__(self, values: Mapping[str, Any]) -> None:
        self.values = values

    @classmethod
    def from_context(cls, context: Mapping[str, Any]) -> "ThemeOptions":
        """Read the options from a page's template context.

        Args:
            context: The context Sphinx builds for a page.

        Returns:
            The options held in its ``theme_<name>`` entries.
        """
        prefix = "theme_"
        return cls(
            {
                key.removeprefix(prefix): value
                for key, value in context.items()
                if key.startswith(prefix)
            }
        )

    def text(self, name: str, default: str = "") -> str:
        """Read an option as text.

        Args:
            name: The option's name.
            default: What to return when the option is unset or empty.

        Returns:
            The option's value as a string, or the default.
        """
        value = self.values.get(name)
        return default if value is None or value == "" else str(value)

    def flag(self, name: str, default: bool = False) -> bool:
        """Read an option as a flag.

        Args:
            name: The option's name.
            default: What to return when the option is unset, empty or not
                a recognised word.

        Returns:
            The flag, reading Sphinx's and pydata-sphinx-theme's boolean strings.
        """
        value = self.values.get(name)
        if isinstance(value, bool):
            return value
        word = str(value).strip().lower() if value is not None else ""
        if word in TRUE_WORDS:
            return True
        if word in FALSE_WORDS:
            return False
        return default

    def number(self, name: str, default: int) -> int:
        """Read an option as a whole number.

        Args:
            name: The option's name.
            default: What to return when the option is unset, empty or not a
                whole number. A flag is not a number.

        Returns:
            The number, reading ``"2"`` from ``-D name=2`` as 2.
        """
        value = self.values.get(name)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        if isinstance(value, str):
            try:
                return int(value.strip())
            except ValueError:
                return default
        return default

    def records(self, name: str) -> list[dict[str, Any]]:
        """Read an option as a list of dicts.

        Args:
            name: The option's name.

        Returns:
            The dicts of the option's list or tuple, or of the list a JSON
            string holds, otherwise empty.
        """
        value = self.values.get(name)
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                return []
        if not isinstance(value, list | tuple):
            return []
        return [dict(item) for item in value if isinstance(item, dict)]

    def mapping(self, name: str) -> dict[str, Any]:
        """Read an option as a dict.

        Args:
            name: The option's name.

        Returns:
            The option's dict, or the dict a JSON string holds, otherwise empty.
        """
        value = self.values.get(name)
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                return {}
        return dict(value) if isinstance(value, dict) else {}

    def static_url(self, path: str, pathto: Callable[..., str]) -> str:
        """Resolve the address of a file the site ships, from the current page.

        Args:
            path: A full address, a path starting ``_static/``, or a path
                relative to ``_static``.
            pathto: Sphinx's ``pathto`` for the page.

        Returns:
            The address to print on the page, empty when the path is empty.
        """
        if not path:
            return ""
        if "://" in path or path.startswith(("//", "data:")):
            return path
        if path.startswith("_static/"):
            return str(pathto(path, 1))
        return str(pathto(f"_static/{path}", 1))

    def components(self, name: str) -> list[str]:
        """Read an option as a list of template names.

        Args:
            name: The option's name.

        Returns:
            The template file for each name in a list or comma-separated string.
        """
        value = self.values.get(name)
        if isinstance(value, str):
            value = value.split(",")
        names = [str(item).strip() for item in value or []]
        return [
            item if item.endswith(".html") else f"{item}.html" for item in names if item
        ]

    def layout(self) -> LayoutCode:
        """Read the ``layout`` option.

        Returns:
            The layout code, or the default when the option is empty. A value
            that is not a layout code raises ``LayoutCodeError``.
        """
        return LayoutCode.parse(self.text("layout") or None)
