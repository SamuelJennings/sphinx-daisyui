import shutil
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

import pytest
from markupsafe import Markup
from sphinx.testing.util import SphinxTestApp

BAD_CODE = "xHh LpR lff"
LATE = 900  # after the theme's own handler, which runs at the default 500


@pytest.fixture
def contexts(app: SphinxTestApp) -> dict[str, dict[str, Any]]:
    """Collect each page's template context as the build produces it."""
    seen: dict[str, dict[str, Any]] = {}

    def collect(
        app: SphinxTestApp,
        pagename: str,
        templatename: str,
        context: dict[str, Any],
        doctree: object,
    ) -> None:
        seen[pagename] = context

    app.connect("html-page-context", collect, priority=LATE)
    return seen


class TestCheckLayout:
    @pytest.mark.sphinx("html", testroot="basic")
    def test_a_wrong_code_stops_the_build_with_one_error(
        self, app: SphinxTestApp
    ) -> None:
        # A SystemExit raised while the application is constructed skips the
        # fixture's cleanup and leaks Sphinx's global state into later tests, so
        # the wrong code is set on a finished set-up and the event fired again.
        app.config.html_theme_options = {"layout": BAD_CODE}

        with pytest.raises(SystemExit) as stop:
            app.events.emit("builder-inited")

        errors = app.warning.getvalue().splitlines()
        assert stop.value.code == 2
        assert len(errors) == 1
        assert "ERROR" in errors[0]
        assert "layout" in errors[0]
        assert repr(BAD_CODE) in errors[0]
        assert not (app.outdir / "index.html").exists()

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        confoverrides={"html_theme_options": {"layout": "lHh lpr fFf"}},
    )
    def test_a_valid_code_other_than_the_default_builds_cleanly(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert app.warning.getvalue() == ""
        assert (app.outdir / "index.html").exists()

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        confoverrides={
            "html_theme": "basic",
            "html_theme_options": {"layout": BAD_CODE},
        },
    )
    def test_another_theme_is_not_checked(self, app: SphinxTestApp) -> None:
        app.build()

        assert (app.outdir / "index.html").exists()

    def test_the_command_line_shows_the_message_without_a_traceback(
        self, tmp_path: Path, rootdir: Path
    ) -> None:
        source = tmp_path / "source"
        shutil.copytree(rootdir / "test-basic", source)
        (source / "conf.py").write_text(
            'project = "Basic"\n'
            'html_theme = "daisyui"\n'
            f'html_theme_options = {{"layout": "{BAD_CODE}"}}\n',
            encoding="utf-8",
        )
        command = [sys.executable, "-m", "sphinx", "-b", "html"]

        result = subprocess.run(  # noqa: S603
            [*command, str(source), str(tmp_path / "out")],
            capture_output=True,
            text=True,
            check=False,
        )

        output = result.stdout + result.stderr
        assert result.returncode == 2
        assert "Traceback" not in output
        assert "layout" in output
        assert repr(BAD_CODE) in output
        assert not (tmp_path / "out" / "index.html").exists()


class TestPageContext:
    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_default_components_are_listed_as_template_names(
        self, app: SphinxTestApp, contexts: dict[str, dict[str, Any]]
    ) -> None:
        app.build()

        daisy = contexts["index"]["daisy"]
        assert daisy["navbar_start"] == ["navbar-logo.html"]
        assert daisy["footer_start"] == ["copyright.html", "sphinx-version.html"]
        assert daisy["footer_end"] == ["theme-version.html"]
        assert daisy["secondary"] == ["page-toc.html"]
        assert daisy["navbar_center"] == []

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        freshenv=True,
        confoverrides={
            "html_theme_options": {
                "navbar_end": ["search-button-field", "theme-switcher.html"],
                "footer_center": ["copyright", "sphinx-version.html"],
            }
        },
    )
    def test_a_site_sets_components_as_a_list(
        self, app: SphinxTestApp, contexts: dict[str, dict[str, Any]]
    ) -> None:
        app.build()

        daisy = contexts["index"]["daisy"]
        assert daisy["navbar_end"] == [
            "search-button-field.html",
            "theme-switcher.html",
        ]
        assert daisy["footer_center"] == ["copyright.html", "sphinx-version.html"]

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_layout_is_read_from_the_options(
        self, app: SphinxTestApp, contexts: dict[str, dict[str, Any]]
    ) -> None:
        app.build()

        assert contexts["index"]["daisy"]["layout"].code == "hHh LpR lff"

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_icon_function_returns_markup(
        self, app: SphinxTestApp, contexts: dict[str, dict[str, Any]]
    ) -> None:
        app.build()

        svg = contexts["index"]["daisy"]["icon"]("search", "size-4")

        assert isinstance(svg, Markup)
        assert svg.startswith('<svg class="size-4"')

    @pytest.mark.sphinx("html", testroot="basic", freshenv=True)
    def test_the_version_and_repository_come_from_the_package_metadata(
        self, app: SphinxTestApp, contexts: dict[str, dict[str, Any]]
    ) -> None:
        app.build()

        daisy = contexts["index"]["daisy"]
        assert daisy["version"] == version("sphinx-daisyui")
        assert daisy["repository"] == "https://github.com/SamuelJennings/sphinx-daisyui"

    @pytest.mark.sphinx(
        "html",
        testroot="basic",
        freshenv=True,
        confoverrides={"html_theme": "basic"},
    )
    def test_another_theme_gets_no_context(
        self, app: SphinxTestApp, contexts: dict[str, dict[str, Any]]
    ) -> None:
        app.build()

        assert "daisy" not in contexts["index"]
