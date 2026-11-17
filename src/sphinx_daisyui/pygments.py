"""The Pygments styles a site picks for each colour mode."""

from pathlib import Path

from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

from .options import ThemeOptions

LOGGER = logging.getLogger(__name__)
STYLESHEET = "styles/pygments-modes.css"
STYLESHEET_PRIORITY = 900  # after the theme's own stylesheet
CODE = ".daisy-sphinx-content .highlight"
UNSTYLED = "html:not([data-mode]) " + CODE
SCHEME_QUERIES = {
    "light": "@media not (prefers-color-scheme: dark)",
    "dark": "@media (prefers-color-scheme: dark)",
}
RESET = """\
{selector} span {{
  color: inherit;
  background-color: transparent;
  font-weight: inherit;
  font-style: inherit;
  text-decoration: inherit;
}}
"""


class PygmentsStyles:
    """The Pygments style a site sets for each colour mode.

    ``styles`` maps each mode that has a valid style to the style's name.

    Args:
        options: The theme's option values.
    """

    def __init__(self, options: ThemeOptions) -> None:
        self.styles: dict[str, str] = {}
        for mode in SCHEME_QUERIES:
            name = options.text(f"pygments_{mode}_style")
            if not name:
                continue
            try:
                get_style_by_name(name)
            except ClassNotFound:
                LOGGER.warning(
                    "The option pygments_%s_style names no Pygments style: %r. "
                    "The %s mode keeps the theme's token highlighting.",
                    mode,
                    name,
                    mode,
                    type="daisyui",
                    subtype="pygments",
                )
                continue
            self.styles[mode] = name

    def rules(self, mode: str) -> str:
        """Write one mode's rules: a reset, then the style under the mode's selectors.

        Args:
            mode: ``"light"`` or ``"dark"``.

        Returns:
            The CSS that applies the mode's style when the page shows that mode,
            and, until the page has a mode attribute, when the system's colour
            scheme matches.
        """
        formatter = HtmlFormatter(style=self.styles[mode])

        def block(selector: str) -> str:
            reset = RESET.format(selector=selector)
            return reset + str(formatter.get_style_defs(selector)) + "\n"

        scheme = block(UNSTYLED)
        indented = "".join(f"  {line}\n" for line in scheme.splitlines())
        return (
            block(f'html[data-mode="{mode}"] {CODE}')
            + f"{SCHEME_QUERIES[mode]} {{\n{indented}}}\n"
        )

    def css(self) -> str:
        """Write the stylesheet for every mode that has a valid style.

        Returns:
            The CSS, empty when no mode has one.
        """
        return "".join(self.rules(mode) for mode in self.styles)


def write_pygments_styles(app: Sphinx) -> None:
    """Write and link the Pygments styles the site sets, once per build.

    Args:
        app: The Sphinx application building the site.
    """
    builder = app.builder
    if not isinstance(builder, StandaloneHTMLBuilder):
        return
    if app.config.html_theme != "daisyui":
        return
    options = ThemeOptions(builder.theme.get_options(app.config.html_theme_options))
    css = PygmentsStyles(options).css()
    if not css:
        return
    target = Path(app.outdir) / "_static" / STYLESHEET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(css, encoding="utf-8")
    app.add_css_file(STYLESHEET, priority=STYLESHEET_PRIORITY)
