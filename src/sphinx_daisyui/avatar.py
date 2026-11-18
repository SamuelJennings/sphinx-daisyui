"""The ``avatar`` directive: an image drawn as a daisyUI avatar.

A page shows a portrait in a circle::

    ```{avatar} _static/portrait.jpg
    :alt: Portrait of the author
    :size: 10rem
    ```

``:shape:`` is ``circle`` (the default), ``rounded`` or ``square``. ``:dark:`` names a
second image drawn in dark mode instead, for a logo with light and dark versions. ``:size:`` is any CSS
length. With ``:beside-title:`` the avatar sits to the left of the page's title and the
paragraph under it, centred on them, and stacks above them on a narrow screen.
"""

from typing import Any, ClassVar

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx.util.osutil import relative_uri
from sphinx.writers.html5 import HTML5Translator

SHAPES = {"circle": "rounded-full", "rounded": "rounded-box", "square": ""}


class avatar(nodes.General, nodes.Element):  # noqa: N801 - docutils names nodes in lower case
    """A portrait drawn as a daisyUI avatar."""


class AvatarDirective(SphinxDirective):
    """Draw the image named in the argument as an avatar."""

    required_arguments = 1
    option_spec: ClassVar[dict[str, Any]] = {
        "alt": directives.unchanged,
        "dark": directives.unchanged,
        "size": directives.unchanged,
        "shape": lambda value: directives.choice(value, tuple(SHAPES)),
        "beside-title": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        """Record the image, its text alternative, size and shape.

        Returns:
            The avatar node.
        """
        uri = self.arguments[0]
        dark = self.options.get("dark", "")
        node = avatar(
            uri=uri,
            dark=dark,
            alt=self.options.get("alt", ""),
            size=self.options.get("size", "6rem"),
            shape=self.options.get("shape", "circle"),
            beside_title="beside-title" in self.options,
        )
        self.set_source_info(node)
        return [node]


def visit_avatar(translator: HTML5Translator, node: avatar) -> None:
    """Write the avatar.

    Args:
        translator: The HTML translator writing the page.
        node: The avatar.

    Raises:
        SkipNode: Always, since the avatar has no children.
    """
    builder = translator.builder
    here = builder.get_target_uri(builder.current_docname)

    def resolve(uri: str) -> str:
        return uri if "://" in uri else relative_uri(here, uri.lstrip("/"))

    escape = translator.attval
    alt = escape(node["alt"])
    if node["dark"]:
        images = (
            f'<img class="daisy-logo-light" src="{escape(resolve(node["uri"]))}" alt="{alt}">'
            f'<img class="daisy-logo-dark" src="{escape(resolve(node["dark"]))}" alt="{alt}">'
        )
    else:
        images = f'<img src="{escape(resolve(node["uri"]))}" alt="{alt}">'

    classes = "daisy-sphinx-escape avatar daisy-avatar"
    if node["beside_title"]:
        classes += " daisy-avatar-beside-title"
    shape = SHAPES[node["shape"]]
    translator.body.append(
        f'<div class="{classes}">'
        f'<div class="{shape}" style="width: {escape(node["size"])}">'
        f"{images}</div></div>"
    )
    raise nodes.SkipNode
