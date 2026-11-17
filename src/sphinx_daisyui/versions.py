"""The version switcher's settings and the check of the file it reads."""

import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen

from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging

from .options import ThemeOptions

LOGGER = logging.getLogger(__name__)
REMOTE_PREFIXES = ("http://", "https://", "//")
TIMEOUT = 10


class VersionSwitcher:
    """How the version switcher and its warning banner behave on a page.

    Args:
        version_match: The version this build documents.
        json_url: The address of the file listing every version, empty for none.
        banner: Whether a banner warns on a version other than the preferred one.
        check: Whether the build reads the file and warns when it is wrong.
    """

    def __init__(
        self, version_match: str, json_url: str, banner: bool, check: bool
    ) -> None:
        self.version_match = version_match
        self.json_url = json_url
        self.banner = banner
        self.check = check

    @classmethod
    def from_options(cls, options: ThemeOptions) -> "VersionSwitcher":
        """Read the switcher's settings from a site's theme options.

        Args:
            options: The site's theme options.

        Returns:
            The settings, with ``json_url`` and ``version_match`` read from the
            ``switcher`` option and empty when it does not give them.
        """
        switcher = options.mapping("switcher")
        return cls(
            version_match=str(switcher.get("version_match", "")).strip(),
            json_url=str(switcher.get("json_url", "")).strip(),
            banner=options.flag("show_version_warning_banner"),
            check=options.flag("check_switcher", True),
        )

    @property
    def shown(self) -> bool:
        """Whether pages draw the switcher: it has a file to read."""
        return bool(self.json_url)

    @property
    def remote(self) -> bool:
        """Whether the file is at a full address rather than in the build."""
        return self.json_url.startswith(REMOTE_PREFIXES)

    def read(self, outdir: Path) -> Any:
        """Read the file the switcher lists its versions in.

        Args:
            outdir: The build's output directory, where a path is read from.

        Returns:
            The file's parsed JSON. An unreadable file, an address that cannot
            be reached or text that is not JSON raises ``OSError`` or
            ``ValueError``, which the caller handles.
        """
        if self.remote:
            url = "https:" + self.json_url if self.json_url[0] == "/" else self.json_url
            with urlopen(url, timeout=TIMEOUT) as response:  # noqa: S310
                return json.load(response)
        path = self.json_url.lstrip("/")
        path = path.removeprefix("./")
        return json.loads((outdir / path).read_text(encoding="utf-8"))

    @staticmethod
    def problem(versions: Any) -> str:
        """Say what is wrong with the versions a file holds.

        Args:
            versions: The file's parsed JSON.

        Returns:
            The fault, or an empty string when every entry has a version and a url.
        """
        if not isinstance(versions, list):
            return "it is not a list of versions"
        for entry in versions:
            if not isinstance(entry, dict):
                return "an entry is not an object"
            for key in ("version", "url"):
                value = entry.get(key)
                if not isinstance(value, str) or not value:
                    return f"an entry has no {key}"
        return ""


def check_switcher(app: Sphinx, exception: Exception | None) -> None:
    """Warn once when the file the version switcher reads cannot be used.

    Args:
        app: The Sphinx application that built the site.
        exception: The error that ended the build, if one did.
    """
    builder = app.builder
    if exception is not None or not isinstance(builder, StandaloneHTMLBuilder):
        return
    if app.config.html_theme != "daisyui":
        return
    options = ThemeOptions(builder.theme.get_options(app.config.html_theme_options))
    switcher = VersionSwitcher.from_options(options)
    if not switcher.shown or not switcher.check:
        return
    try:
        fault = VersionSwitcher.problem(switcher.read(Path(app.outdir)))
    except (OSError, ValueError) as error:
        reason = getattr(error, "strerror", None) or error
        fault = f"it could not be read ({reason})"
    if fault:
        LOGGER.warning(
            "The version switcher file %s cannot be used: %s.",
            switcher.json_url,
            fault,
            type="daisyui",
            subtype="switcher",
        )
