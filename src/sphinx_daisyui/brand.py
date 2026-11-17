"""The brand a page shows: a logo for each colour mode, a name and a link."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .options import ThemeOptions


@dataclass(frozen=True)
class Brand:
    """What the brand component prints.

    Attributes:
        light: The address of the logo for light mode, empty when there is none.
        dark: The address of the logo for dark mode.
        text: The name printed beside the logo, empty when none is shown.
        alt: The description of the logo for a reader who cannot see it.
        href: Where the brand leads.
    """

    light: str
    dark: str
    text: str
    alt: str
    href: str

    @classmethod
    def from_options(cls, options: ThemeOptions, context: Mapping[str, Any]) -> "Brand":
        """Read the brand from the theme options and a page's template context.

        Args:
            options: The theme's options.
            context: The context Sphinx builds for a page.

        Returns:
            The brand, with every address resolved from the page.
        """
        pathto = context["pathto"]
        logo = options.mapping("logo")
        light_name = logo.get("image_light")
        dark_name = logo.get("image_dark")
        light = (
            options.static_url(light_name, pathto)
            if light_name
            else context.get("logo_url") or ""
        )
        dark = options.static_url(dark_name, pathto) if dark_name else light
        if "text" in logo:
            text = str(logo["text"])
        elif light and (light_name or dark_name):
            text = ""
        else:
            text = context.get("docstitle") or context.get("project") or ""
        return cls(
            light=light,
            dark=dark,
            text=text,
            alt=str(logo.get("alt_text") or context.get("project") or ""),
            href=str(logo.get("link") or pathto(context.get("root_doc", "index"))),
        )
