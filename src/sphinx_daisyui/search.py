"""The search dialog's settings."""

from sphinx.locale import get_translation

from .options import ThemeOptions

translate = get_translation("sphinx")


class SearchSettings:
    """How the search dialog behaves on a page.

    Args:
        enabled: Whether the page draws the search button and the dialog.
        text: The words the search button and the dialog's field show.
        as_you_type: Whether results appear while the reader types.
    """

    def __init__(self, enabled: bool, text: str, as_you_type: bool) -> None:
        self.enabled = enabled
        self.text = text
        self.as_you_type = as_you_type

    @classmethod
    def from_options(cls, options: ThemeOptions) -> "SearchSettings":
        """Read the search settings from a site's theme options.

        Args:
            options: The site's theme options.

        Returns:
            The settings: search on unless ``disable_search`` is set, the text
            from ``search_bar_text`` or the default, and results as the reader
            types unless ``search_as_you_type`` is off.
        """
        return cls(
            enabled=not options.flag("disable_search"),
            text=options.text("search_bar_text", translate("Search the docs")),
            as_you_type=options.flag("search_as_you_type", True),
        )
