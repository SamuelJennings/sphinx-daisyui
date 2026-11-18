"""The ``wordmark`` directive: a logo that takes the place of the page's title.

Placed straight after the title::

    # FairDM

    ```{wordmark} _static/fairdm-logo.svg
    :dark: _static/fairdm-logo-dark.svg
    :height: 4rem
    ```

The title stays in the page for its tab, the table of contents and screen readers,
but is hidden from view. The wordmark is drawn in its place, and the paragraph under
it reads as the page's introduction. ``:dark:`` names a version drawn in dark mode.
"""

from typing import Any, ClassVar

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx.util.osutil import relative_uri
from sphinx.writers.html5 import HTML5Translator


class wordmark(nodes.General, nodes.Element):  # noqa: N801 - docutils names nodes in lower case
    """A logo drawn in place of the page's title."""


class WordmarkDirective(SphinxDirective):
    """Draw the image named in the argument in place of the page's title."""

    required_arguments = 1
    option_spec: ClassVar[dict[str, Any]] = {
        "dark": directives.unchanged,
        "height": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        """Record the images and their height.

        Returns:
            The wordmark node.
        """
        node = wordmark(
            uri=self.arguments[0],
            dark=self.options.get("dark", ""),
            height=self.options.get("height", "4rem"),
        )
        self.set_source_info(node)
        return [node]


def visit_wordmark(translator: HTML5Translator, node: wordmark) -> None:
    """Write the wordmark. Its images are decorative: the hidden title names the page.

    Args:
        translator: The HTML translator writing the page.
        node: The wordmark.

    Raises:
        SkipNode: Always, since the wordmark has no children.
    """
    builder = translator.builder
    here = builder.get_target_uri(builder.current_docname)
    escape = translator.attval

    def image(uri: str, css: str) -> str:
        src = uri if "://" in uri else relative_uri(here, uri.lstrip("/"))
        style = f"height: {escape(node['height'])}"
        return f'<img class="{css}" src="{escape(src)}" alt="" style="{style}">'

    if node["dark"]:
        images = image(node["uri"], "daisy-logo-light") + image(node["dark"], "daisy-logo-dark")
    else:
        images = image(node["uri"], "")
    translator.body.append(f'<div class="daisy-sphinx-escape daisy-wordmark">{images}</div>')
    raise nodes.SkipNode
