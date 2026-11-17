from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.modes import MODES, THEMES, Modes
from sphinx_daisyui.options import ThemeOptions


def modes(**values: Any) -> Modes:
    return Modes.from_options(ThemeOptions(values))


class TestThemes:
    def test_the_bundled_list_has_each_theme_once(self) -> None:
        assert THEMES
        assert len(set(THEMES)) == len(THEMES)

    def test_the_modes_are_auto_light_and_dark(self) -> None:
        assert MODES == ("auto", "light", "dark")


class TestModes:
    def test_a_site_setting_nothing_gets_the_defaults(self) -> None:
        result = modes()

        assert (result.light, result.dark, result.default) == ("light", "dark", "auto")
        assert result.picker == []

    def test_both_themes_are_taken_as_given(self) -> None:
        result = modes(light_theme="cupcake", dark_theme="dracula")

        assert (result.light, result.dark) == ("cupcake", "dracula")

    def test_empty_theme_options_give_the_defaults(self) -> None:
        result = modes(light_theme="", dark_theme="")

        assert (result.light, result.dark) == ("light", "dark")

    @pytest.mark.parametrize("word", ["light", "dark", "auto", " Dark ", "LIGHT"])
    def test_a_known_starting_mode_is_kept_lower_cased(self, word: str) -> None:
        assert modes(default_mode=word).default == word.strip().lower()

    @pytest.mark.parametrize("word", ["sepia", "system", "cupcake"])
    def test_an_unknown_starting_mode_is_auto(self, word: str) -> None:
        assert modes(default_mode=word).default == "auto"

    @pytest.mark.parametrize("value", [True, "all", "All", "true", "True", " TRUE "])
    def test_true_and_all_offer_every_theme(self, value: Any) -> None:
        assert modes(theme_picker=value).picker == list(THEMES)

    @pytest.mark.parametrize("value", [None, "", False, "false"])
    def test_an_unset_or_false_picker_offers_none(self, value: Any) -> None:
        assert modes(theme_picker=value).picker == []

    def test_a_list_is_offered_in_its_order(self) -> None:
        assert modes(theme_picker=["dracula", "cupcake"]).picker == [
            "dracula",
            "cupcake",
        ]

    def test_a_comma_separated_string_is_offered_in_its_order(self) -> None:
        assert modes(theme_picker="dracula, cupcake").picker == ["dracula", "cupcake"]

    def test_a_repeated_name_is_offered_once(self) -> None:
        assert modes(theme_picker=["cupcake", "dracula", "cupcake"]).picker == [
            "cupcake",
            "dracula",
        ]

    def test_a_sites_own_theme_name_is_kept(self) -> None:
        assert modes(theme_picker=["brand", "light"]).picker == ["brand", "light"]


class TestCheckModes:
    @pytest.mark.sphinx("html", testroot="modes", freshenv=True)
    def test_a_site_setting_none_of_the_options_builds_without_a_warning(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert app.warning.getvalue() == ""

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides={"html_theme_options": {"default_mode": "sepia"}},
    )
    def test_an_unknown_starting_mode_warns_once_naming_the_option(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        warnings = app.warning.getvalue().splitlines()
        assert len(warnings) == 1
        assert "default_mode" in warnings[0]

    @pytest.mark.sphinx(
        "html",
        testroot="modes",
        freshenv=True,
        confoverrides={"html_theme_options": {"default_mode": "Dark"}},
    )
    def test_a_known_starting_mode_in_any_case_does_not_warn(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert app.warning.getvalue() == ""
