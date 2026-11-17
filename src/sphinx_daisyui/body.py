"""The page body: what the theme changes while Sphinx writes a page's content."""

import types
from typing import Any

from docutils import nodes
from markupsafe import escape
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.locale import _, get_translation
from sphinx.util.math import get_node_equation_number
from sphinx.writers.html5 import HTML5Translator

translate = get_translation("sphinx")

REGION_CLASS = "daisy-sphinx-scroll"
ATTRIBUTION_SPACE = "\N{THIN SPACE}"


class PageBodyTranslator(HTML5Translator):
    """Changes to the HTML Sphinx writes for a page's content.

    ``install_translator`` puts this class in front of the translator the
    builder already uses, so an extension's own translator keeps working.

    Attributes:
        table_depth: How many tables the one being written is inside.
    """

    table_depth = 0

    def region(self, name: str) -> str:
        """Write the opening tag of a focusable scroll region.

        Args:
            name: The region's accessible name.

        Returns:
            The opening tag, with its attribute values escaped.
        """
        return self.starttag(
            nodes.Element(),
            "div",
            "",
            CLASS=REGION_CLASS,
            role="region",
            tabindex="0",
            **{"aria-label": name},  # type: ignore[arg-type]
        )

    def visit_table(self, node: nodes.table) -> None:
        """Put an outermost table in a scroll region named by its caption.

        Args:
            node: The table.
        """
        if self.table_depth == 0:
            captions = [child for child in node if isinstance(child, nodes.title)]
            name = captions[0].astext().strip() if captions else ""
            self.body.append(self.region(name or translate("Table")))
        self.table_depth += 1
        super().visit_table(node)

    def depart_table(self, node: nodes.table) -> None:
        """Close the table, and the region it sits in when it is outermost.

        Args:
            node: The table.
        """
        super().depart_table(node)
        self.table_depth -= 1
        if self.table_depth == 0:
            self.body.append("</div>\n")

    def visit_math_block(self, node: nodes.math_block, math_env: str = "") -> None:
        """Put a display equation's notation in a scroll region.

        The id and the number stay outside the region, so the number does not
        scroll away from the equation it belongs to.

        Args:
            node: The display equation.
            math_env: The math environment, for the renderers that take one.

        Raises:
            SkipNode: Always, as the renderers do, once the equation is written.
        """
        if node.get("no-wrap", node.get("nowrap", False)):
            super().visit_math_block(node, math_env)
            return
        number = get_node_equation_number(self, node) if node.get("number") else ""
        self.body.append(
            self.starttag(node, "div", CLASS="math notranslate nohighlight")
        )
        if number:
            self.body.append(f'<span class="eqno">({number})')
            self.add_permalink_ref(node, _("Link to this equation"))
            self.body.append("</span>")
            name = translate("Equation %(number)s") % {"number": f"({number})"}
        else:
            name = translate("Equation")
        self.body.append(self.region(name))
        notation = node.deepcopy()
        notation["number"] = None
        notation["ids"] = []
        try:
            super().visit_math_block(notation, math_env)
        except nodes.SkipNode:
            pass
        else:
            super().depart_math_block(notation, math_env)
        self.body.append("</div></div>\n")
        raise nodes.SkipNode

    def permalink_text(self, node: Any) -> str:
        """Find the text of what a permalink belongs to.

        Args:
            node: The node the permalink is written for.

        Returns:
            The signature's name, the equation's number, or the text of the
            title or caption, whichever the node has.
        """
        if isinstance(node, addnodes.desc_signature):
            parts = [
                child
                for child in node.children
                if isinstance(child, (addnodes.desc_addname, addnodes.desc_name))
            ]
            return "".join(part.astext() for part in parts).strip()
        if isinstance(node, nodes.math_block):
            return f"({get_node_equation_number(self, node)})"
        for child in node.children:
            if isinstance(child, (nodes.title, nodes.caption)):
                return str(child.astext()).strip()
        return str(node.astext()).strip()

    def add_permalink_ref(self, node: nodes.Element, title: str) -> None:
        """Write Sphinx's permalink, named by the text it belongs to.

        Args:
            node: The node the permalink is written for.
            title: The link's title, such as "Link to this heading".
        """
        written = len(self.body)
        super().add_permalink_ref(node, title)
        if len(self.body) == written:
            return
        label = escape(f"{title}: {self.permalink_text(node)}")
        link = self.body[-1].replace(
            'class="headerlink"', f'class="headerlink" aria-label="{label}"', 1
        )
        self.body[-1] = link

    def visit_attribution(self, node: nodes.Element) -> None:
        """Space a quotation's attribution the same however it was written.

        Args:
            node: The attribution.
        """
        first = node[0] if node.children else None
        if isinstance(first, nodes.Text):
            node.replace(first, nodes.Text(first.astext().lstrip()))
        super().visit_attribution(node)
        if self.settings.attribution == "dash":
            self.body.append(ATTRIBUTION_SPACE)


def install_translator(app: Sphinx) -> None:
    """Put the page-body changes in front of the builder's translator.

    Args:
        app: The Sphinx application building the site.
    """
    builder = app.builder
    if app.config.html_theme != "daisyui" or builder.format != "html":
        return
    base = app.registry.translators.get(builder.name, builder.default_translator_class)
    if base is None or issubclass(base, PageBodyTranslator):
        return
    translator = types.new_class("DaisyHTMLTranslator", (PageBodyTranslator, base), {})
    app.set_translator(builder.name, translator, override=True)
