"""The ``timeline`` and ``timeline-item`` directives, drawn as a daisyUI timeline.

A page lists events in order::

    ```{timeline}
    :::{timeline-item} PhD, Geophysics
    :date: 2017 – 2021
    :place: University of Adelaide

    What the thesis was about.
    :::
    ```

Each item has a title, an optional date, place and badge, and a body of ordinary content.
The items alternate sides of the line on a wide screen. With ``:compact:`` they all
sit on one side, and on a narrow screen they always do.
"""

from typing import Any, ClassVar

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx.writers.html5 import HTML5Translator

DOT = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"'
    ' class="h-5 w-5 text-primary" aria-hidden="true"><circle cx="10" cy="10" r="6"/>'
    "</svg>"
)


class timeline(nodes.General, nodes.Element):  # noqa: N801 - docutils names nodes in lower case
    """A list of events along a line."""


class timeline_item(nodes.General, nodes.Element):  # noqa: N801
    """One event on a timeline: its date, title, place and body."""


class TimelineDirective(SphinxDirective):
    """Draw the ``timeline-item`` directives inside it as one timeline."""

    has_content = True
    option_spec: ClassVar[dict[str, Any]] = {"compact": directives.flag}

    def run(self) -> list[nodes.Node]:
        """Parse the items and wrap them in a timeline node.

        Returns:
            The timeline node.
        """
        node = timeline(compact="compact" in self.options)
        self.set_source_info(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        items = [child for child in node.children if isinstance(child, timeline_item)]
        node.children = items
        for item in items:
            item.parent = node
        return [node]


class TimelineItemDirective(SphinxDirective):
    """One event on a timeline. The argument is its title."""

    has_content = True
    required_arguments = 1
    final_argument_whitespace = True
    option_spec: ClassVar[dict[str, Any]] = {
        "date": directives.unchanged,
        "place": directives.unchanged,
        "badge": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        """Build the item from its title, date, place and body.

        Returns:
            The item node.
        """
        item = timeline_item(
            title=self.arguments[0],
            date=self.options.get("date", ""),
            place=self.options.get("place", ""),
            badge=self.options.get("badge", ""),
        )
        self.set_source_info(item)
        self.state.nested_parse(self.content, self.content_offset, item)
        return [item]


def visit_timeline(translator: HTML5Translator, node: timeline) -> None:
    """Open the timeline's list.

    Args:
        translator: The HTML translator writing the page.
        node: The timeline.
    """
    side = "timeline-compact" if node["compact"] else "max-md:timeline-compact"
    translator.body.append(
        f'<div class="daisy-sphinx-escape daisy-timeline">'
        f'<ul class="timeline timeline-snap-icon timeline-vertical {side}">'
    )


def depart_timeline(translator: HTML5Translator, node: timeline) -> None:
    """Close the timeline's list.

    Args:
        translator: The HTML translator writing the page.
        node: The timeline.
    """
    translator.body.append("</ul></div>")


def visit_timeline_item(translator: HTML5Translator, node: timeline_item) -> None:
    """Open one event: the line above it, its dot, and the start of its box.

    Args:
        translator: The HTML translator writing the page.
        node: The event.
    """
    parent = node.parent
    index = parent.index(node)
    start = not parent["compact"] and index % 2 == 0
    box = "timeline-start md:text-end" if start else "timeline-end"
    escape = translator.encode
    head = [
        "<li>",
        "<hr>" if index else "",
        f'<div class="timeline-middle">{DOT}</div>',
        f'<div class="{box} mb-10 daisy-timeline-box">',
    ]
    if node["date"]:
        head.append(
            f'<p class="font-mono text-sm text-base-content/70">{escape(node["date"])}</p>'
        )
    badge = (
        f' <span class="badge badge-accent badge-sm align-middle">{escape(node["badge"])}</span>'
        if node["badge"]
        else ""
    )
    head.append(f'<p class="text-lg font-bold">{escape(node["title"])}{badge}</p>')
    if node["place"]:
        head.append(f'<p class="text-base-content/80">{escape(node["place"])}</p>')
    head.append('<div class="daisy-timeline-body mt-2">')
    translator.body.append("".join(head))


def depart_timeline_item(translator: HTML5Translator, node: timeline_item) -> None:
    """Close one event, and draw the line below it unless it is the last.

    Args:
        translator: The HTML translator writing the page.
        node: The event.
    """
    last = node.parent.index(node) == len(node.parent.children) - 1
    translator.body.append("</div></div>" + ("" if last else "<hr>") + "</li>")
