"""Hands the layout code's rules to the layout playground on the Layout page.

The playground in ``_static/layout-playground.js`` holds no copy of the rules. This
extension reads them from :class:`sphinx_daisyui.layout.LayoutCode` by parsing codes,
and writes them into the page for the script to read.

Nothing here is part of the theme.
"""

from __future__ import annotations

import itertools
import json
from typing import TYPE_CHECKING, Any

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from sphinx_daisyui.layout import AREA_NAMES, LayoutCode

if TYPE_CHECKING:
    from sphinx.application import Sphinx

# The shortest code, with every letter in lower case.
PROBE = "hhh lpr fff"


def facts(layout: LayoutCode) -> dict[str, Any]:
    """Pick out what the playground draws from a parsed code."""
    return {
        "wide": str(layout.areas_wide),
        "medium": str(layout.areas_medium),
        "header_fixed": layout.header_sticky,
        "primary_fixed": layout.primary_sticky,
        "secondary_fixed": layout.secondary_sticky,
        "footer_fixed": layout.footer_sticky,
        "primary_below_header": layout.primary_top != "0px",
        "secondary_below_header": layout.secondary_top != "0px",
    }


def read_rules() -> dict[str, Any]:
    """Read the layout code's rules by parsing codes.

    Returns:
        ``positions``: the letters each of the nine positions takes. ``case``: the
        positions where upper case changes the layout. ``areas``: each letter's
        area. ``layouts``: what the code draws, for every code the rules allow,
        keyed by the code with only those positions in upper case.
    """
    letters = PROBE.replace(" ", "")
    positions = []
    for index in range(len(letters)):
        taken = []
        for letter in sorted(AREA_NAMES):
            candidate = letters[:index] + letter + letters[index + 1 :]
            try:
                LayoutCode.parse(spaced(candidate))
            except ValueError:
                continue
            taken.append(letter)
        positions.append("".join(taken))

    base = facts(LayoutCode.parse(PROBE))
    case = [
        index
        for index in range(len(letters))
        if facts(LayoutCode.parse(spaced(capitalise(letters, index)))) != base
    ]

    layouts = {}
    for shape in itertools.product(*positions):
        for upper in itertools.product([False, True], repeat=len(case)):
            written = list(shape)
            for index, up in zip(case, upper, strict=True):
                if up:
                    written[index] = written[index].upper()
            code = spaced("".join(written))
            layouts[code] = facts(LayoutCode.parse(code))
    return {
        "positions": positions,
        "case": case,
        "areas": AREA_NAMES,
        "layouts": layouts,
    }


def capitalise(letters: str, index: int) -> str:
    return letters[:index] + letters[index].upper() + letters[index + 1 :]


def spaced(letters: str) -> str:
    return " ".join(letters[i : i + 3] for i in range(0, len(letters), 3))


class LayoutRules(SphinxDirective):
    """Write the layout code's rules into the page for the playground."""

    def run(self) -> list[nodes.Node]:
        data = json.dumps(read_rules(), separators=(",", ":")).replace("</", "<\\/")
        html = f'<script type="application/json" id="layout-rules">{data}</script>'
        return [nodes.raw("", html, format="html")]


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_directive("layout-rules", LayoutRules)
    app.add_css_file("layout-playground.css")
    app.add_js_file("layout-playground.js", defer="defer")
    return {"parallel_read_safe": True, "parallel_write_safe": True}
