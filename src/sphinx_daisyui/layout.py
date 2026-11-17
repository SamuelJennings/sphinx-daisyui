"""The layout code that arranges the page, such as ``hHh LpR lff``."""

import re
from dataclasses import dataclass
from typing import ClassVar

from markupsafe import Markup

AREA_NAMES = {
    "h": "header",
    "l": "primary",
    "p": "main",
    "r": "secondary",
    "f": "footer",
}
SHAPE = re.compile(r"^[hl]h[hr] lpr [fl]f[fr]$")
HEADER_HEIGHT = "var(--daisy-header-height)"


class LayoutCodeError(ValueError):
    """A ``layout`` option that is not a layout code."""


@dataclass(frozen=True)
class LayoutCode:
    """A layout code read into the facts the templates and styles need.

    Three groups of three letters are the top, middle and bottom rows of the
    page, each read left, centre and right: ``h`` header, ``l`` primary sidebar,
    ``p`` main, ``r`` secondary sidebar, ``f`` footer. A corner names the area
    that reaches it. An upper-case header, sidebar or footer letter keeps the
    area in view while the page scrolls.

    Attributes:
        DEFAULT: The code used when the option is empty.
        code: The code with its spaces normalised and its case kept.
        areas_wide: The ``grid-template-areas`` value for wide screens.
        areas_medium: The value for medium screens, where the secondary
            sidebar's cells go to the area on their left.
        header_sticky: Whether the header stays in view.
        primary_sticky: Whether the primary sidebar stays in view.
        secondary_sticky: Whether the secondary sidebar stays in view.
        footer_sticky: Whether the footer stays in view.
        primary_top: The offset a sticky primary sidebar starts at.
        secondary_top: The offset a sticky secondary sidebar starts at.
        brand_in_sidebar: Whether the primary sidebar holds the brand, because
            it reaches the top-left corner.
    """

    DEFAULT: ClassVar[str] = "hHh LpR lff"

    code: str
    areas_wide: Markup
    areas_medium: Markup
    header_sticky: bool
    primary_sticky: bool
    secondary_sticky: bool
    footer_sticky: bool
    primary_top: str
    secondary_top: str
    brand_in_sidebar: bool

    @classmethod
    def parse(cls, value: object) -> "LayoutCode":
        """Read a layout code.

        Args:
            value: The ``layout`` option. ``None`` or an empty string means
                the default code.

        Returns:
            The code read into its facts.

        Raises:
            LayoutCodeError: If the value is not a string, or is a string of
                the wrong shape.
        """
        if value is None:
            value = cls.DEFAULT
        if not isinstance(value, str):
            raise LayoutCodeError(cls.refusal(value))
        code = " ".join(value.split()) or cls.DEFAULT
        if not SHAPE.match(code.lower()):
            raise LayoutCodeError(cls.refusal(value))

        rows = code.split(" ")
        lower = [row.lower() for row in rows]
        header_sticky = rows[0][1] == "H"
        return cls(
            code=code,
            areas_wide=cls.areas(lower),
            areas_medium=cls.areas(
                [
                    "".join(
                        row[i - 1] if letter == "r" else letter
                        for i, letter in enumerate(row)
                    )
                    for row in lower
                ]
            ),
            header_sticky=header_sticky,
            primary_sticky=rows[1][0] == "L",
            secondary_sticky=rows[1][2] == "R",
            footer_sticky=rows[2][1] == "F",
            primary_top=HEADER_HEIGHT
            if header_sticky and lower[0][0] == "h"
            else "0px",
            secondary_top=(
                HEADER_HEIGHT if header_sticky and lower[0][2] == "h" else "0px"
            ),
            brand_in_sidebar=lower[0][0] == "l",
        )

    @staticmethod
    def areas(rows: list[str]) -> Markup:
        """Write rows of area letters as a ``grid-template-areas`` value.

        Args:
            rows: Three strings of three lower-case area letters.

        Returns:
            One quoted string of area names for each row.
        """
        quoted = (
            '"' + " ".join(AREA_NAMES[letter] for letter in row) + '"' for row in rows
        )
        return Markup(" ".join(quoted))  # noqa: S704

    @staticmethod
    def refusal(value: object) -> str:
        """Build the message for a value that is not a layout code.

        Args:
            value: The value as the site gave it.

        Returns:
            A message naming the option, quoting the value and stating the rules.
        """
        return (
            f"The theme option 'layout' is {value!r}, which is not a layout code. "
            "It needs three groups of three letters separated by spaces, such as "
            "'hHh LpR lff': the top row is h or l, then h, then h or r; the middle "
            "row is l, p, r; the bottom row is f or l, then f, then f or r. "
            "Upper case keeps a header, sidebar or footer in view while the page scrolls."
        )
