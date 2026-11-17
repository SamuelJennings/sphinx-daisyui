from sphinx_daisyui.options import ThemeOptions
from sphinx_daisyui.search import SearchSettings


class TestSearchSettings:
    def test_a_site_setting_nothing_gets_search_with_results_as_you_type(self) -> None:
        settings = SearchSettings.from_options(ThemeOptions({}))

        assert settings.enabled is True
        assert settings.as_you_type is True
        assert settings.text
