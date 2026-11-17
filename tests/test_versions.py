import json
from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.options import ThemeOptions
from sphinx_daisyui.versions import VersionSwitcher

UNREACHABLE = "http://127.0.0.1:9/switcher.json"


def options(**values: Any) -> dict[str, Any]:
    return {"html_theme_options": values}


def warnings_of(app: SphinxTestApp) -> str:
    return app.warning.getvalue()


class TestVersionSwitcher:
    def test_a_site_setting_nothing_has_no_switcher(self) -> None:
        switcher = VersionSwitcher.from_options(ThemeOptions({}))

        assert switcher.shown is False
        assert switcher.json_url == ""
        assert switcher.version_match == ""
        assert switcher.banner is False
        assert switcher.check is True

    def test_a_json_url_shows_the_switcher_and_both_values_are_trimmed(self) -> None:
        values = {"switcher": {"json_url": " /v.json ", "version_match": 2.0}}

        switcher = VersionSwitcher.from_options(ThemeOptions(values))

        assert switcher.shown is True
        assert switcher.json_url == "/v.json"
        assert switcher.version_match == "2.0"

    def test_a_switcher_with_no_json_url_is_not_shown(self) -> None:
        values = {"switcher": {"version_match": "dev"}}

        assert VersionSwitcher.from_options(ThemeOptions(values)).shown is False

    def test_the_switcher_may_be_written_as_a_json_string(self) -> None:
        text = json.dumps({"json_url": "v.json", "version_match": "dev"})

        switcher = VersionSwitcher.from_options(ThemeOptions({"switcher": text}))

        assert (switcher.json_url, switcher.version_match) == ("v.json", "dev")

    def test_the_banner_and_the_check_read_their_flags(self) -> None:
        values = {"show_version_warning_banner": "true", "check_switcher": "false"}

        switcher = VersionSwitcher.from_options(ThemeOptions(values))

        assert switcher.banner is True
        assert switcher.check is False

    def test_a_full_address_is_told_from_a_path(self) -> None:
        for url, remote in (
            ("https://x.org/s.json", True),
            ("http://x.org/s.json", True),
            ("//x.org/s.json", True),
            ("/s.json", False),
            ("_static/s.json", False),
        ):
            switcher = VersionSwitcher("dev", url, False, True)

            assert switcher.remote is remote, url


class TestCheckSwitcher:
    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": "_static/switcher.json", "version_match": "dev"}
        ),
    )
    def test_a_valid_file_builds_without_a_warning(self, app: SphinxTestApp) -> None:
        app.build()

        assert "switcher" not in warnings_of(app)
        assert (Path(app.outdir) / "index.html").exists()

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": "/_static/switcher.json", "version_match": "dev"}
        ),
    )
    def test_a_path_from_the_servers_root_is_read_from_the_sites_root(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert "switcher" not in warnings_of(app)

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": "_static/missing.json", "version_match": "dev"}
        ),
    )
    def test_a_missing_file_warns_once_naming_the_address_and_builds(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert warnings_of(app).count("_static/missing.json") == 1
        assert (Path(app.outdir) / "index.html").exists()

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": "_static/wrong.json", "version_match": "dev"}
        ),
    )
    def test_a_file_of_the_wrong_shape_warns_once_naming_the_address(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert warnings_of(app).count("_static/wrong.json") == 1

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": UNREACHABLE, "version_match": "dev"}
        ),
    )
    def test_an_unreachable_address_warns_once_naming_it_and_builds(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert warnings_of(app).count(UNREACHABLE) == 1
        assert (Path(app.outdir) / "index.html").exists()

    @pytest.mark.sphinx(
        "html",
        testroot="versions",
        freshenv=True,
        confoverrides=options(
            switcher={"json_url": "_static/missing.json", "version_match": "dev"},
            check_switcher=False,
        ),
    )
    def test_with_the_check_off_a_missing_file_does_not_warn(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert "missing.json" not in warnings_of(app)

    @pytest.mark.sphinx("html", testroot="versions", freshenv=True)
    def test_a_site_with_no_switcher_builds_with_no_warnings(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert warnings_of(app) == ""
