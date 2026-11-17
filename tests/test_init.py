import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

BAD_CODE = "xHh LpR lff"


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
