from sphinx_daisyui.options import ThemeOptions
from sphinx_daisyui.search import SearchSettings


class TestSearchSettings:
    def test_a_site_setting_nothing_gets_search_with_results_as_you_type(self) -> None:
        settings = SearchSettings.from_options(ThemeOptions({}))

        assert settings.enabled is True
        assert settings.as_you_type is True
        assert settings.text

    def test_the_text_comes_from_search_bar_text(self) -> None:
        options = ThemeOptions({"search_bar_text": "Find"})

        assert SearchSettings.from_options(options).text == "Find"

    def test_an_empty_text_falls_back_to_the_default(self) -> None:
        empty = SearchSettings.from_options(ThemeOptions({"search_bar_text": ""}))
        unset = SearchSettings.from_options(ThemeOptions({}))

        assert empty.text == unset.text

    def test_disable_search_turns_search_off_as_a_flag_or_a_word(self) -> None:
        for value in (True, "true"):
            options = ThemeOptions({"disable_search": value})

            assert SearchSettings.from_options(options).enabled is False

    def test_search_as_you_type_turns_off_as_a_flag_or_a_word(self) -> None:
        for value in (False, "false"):
            options = ThemeOptions({"search_as_you_type": value})

            assert SearchSettings.from_options(options).as_you_type is False
