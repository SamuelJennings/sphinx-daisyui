from typing import Any

import pytest

from sphinx_daisyui.layout import LayoutCode, LayoutCodeError
from sphinx_daisyui.options import ThemeOptions


class TestThemeOptions:
    def test_from_context_reads_every_theme_value(self) -> None:
        context = {"theme_layout": "hhh lpr fff", "theme_logo": "a.svg", "title": "x"}

        options = ThemeOptions.from_context(context)

        assert options.text("layout") == "hhh lpr fff"
        assert options.text("logo") == "a.svg"
        assert options.text("title", "none") == "none"

    @pytest.mark.parametrize(
        ("value", "expected"),
        [("abc", "abc"), (None, "fallback"), ("", "fallback"), (5, "5")],
    )
    def test_text_gives_the_default_for_an_empty_value(
        self, value: Any, expected: str
    ) -> None:
        assert ThemeOptions({"name": value}).text("name", "fallback") == expected

    def test_text_of_a_missing_option_is_the_default(self) -> None:
        assert ThemeOptions({}).text("name") == ""
        assert ThemeOptions({}).text("name", "fallback") == "fallback"

    @pytest.mark.parametrize(
        "value", [True, "true", "True", "1", "yes", "on", " true "]
    )
    def test_flag_reads_true_values(self, value: Any) -> None:
        assert ThemeOptions({"name": value}).flag("name") is True

    @pytest.mark.parametrize("value", [False, "false", "False", "0", "no", "off"])
    def test_flag_reads_false_values(self, value: Any) -> None:
        assert ThemeOptions({"name": value}).flag("name", default=True) is False

    @pytest.mark.parametrize("default", [True, False])
    def test_flag_gives_the_default_for_an_empty_value(self, default: bool) -> None:
        assert ThemeOptions({"name": ""}).flag("name", default) is default
        assert ThemeOptions({"name": None}).flag("name", default) is default
        assert ThemeOptions({}).flag("name", default) is default

    def test_mapping_reads_a_dict(self) -> None:
        assert ThemeOptions({"name": {"a": 1}}).mapping("name") == {"a": 1}

    def test_mapping_reads_a_json_string(self) -> None:
        assert ThemeOptions({"name": '{"a": 1}'}).mapping("name") == {"a": 1}

    @pytest.mark.parametrize("value", ["not json", "[1, 2]", "", None, 5])
    def test_mapping_of_anything_else_is_empty(self, value: Any) -> None:
        assert ThemeOptions({"name": value}).mapping("name") == {}

    def test_components_reads_a_list(self) -> None:
        options = ThemeOptions({"name": ["navbar-logo", "search.html"]})

        assert options.components("name") == ["navbar-logo.html", "search.html"]

    def test_components_reads_a_tuple(self) -> None:
        assert ThemeOptions({"name": ("a", "b")}).components("name") == [
            "a.html",
            "b.html",
        ]

    @pytest.mark.parametrize("value", ["navbar-logo, search.html", "navbar-logo"])
    def test_components_of_a_string_is_empty(self, value: str) -> None:
        assert ThemeOptions({"name": value}).components("name") == []

    @pytest.mark.parametrize("value", ["", [], None, "  , "])
    def test_components_of_nothing_is_empty(self, value: Any) -> None:
        assert ThemeOptions({"name": value}).components("name") == []

    def test_components_of_a_missing_option_is_empty(self) -> None:
        assert ThemeOptions({}).components("name") == []

    def test_layout_reads_the_layout_option(self) -> None:
        assert ThemeOptions({"layout": "hhh lpr fff"}).layout() == LayoutCode.parse(
            "hhh lpr fff"
        )

    @pytest.mark.parametrize("value", ["", None])
    def test_layout_without_a_code_is_the_default(self, value: Any) -> None:
        assert ThemeOptions({"layout": value}).layout() == LayoutCode.parse(None)
        assert ThemeOptions({}).layout() == LayoutCode.parse(None)

    def test_layout_refuses_a_wrong_code(self) -> None:
        with pytest.raises(LayoutCodeError):
            ThemeOptions({"layout": "xxx"}).layout()


class TestNumber:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [(2, 2), (0, 0), ("3", 3), (" 4 ", 4), ("-1", -1), ("007", 7)],
    )
    def test_number_reads_an_int_or_a_string_of_digits(
        self, value: Any, expected: int
    ) -> None:
        assert ThemeOptions({"name": value}).number("name", 9) == expected

    @pytest.mark.parametrize("value", [True, False, None, "", "abc", "1.5", [3]])
    def test_number_of_anything_else_is_the_default(self, value: Any) -> None:
        assert ThemeOptions({"name": value}).number("name", 9) == 9

    def test_number_of_a_missing_option_is_the_default(self) -> None:
        assert ThemeOptions({}).number("name", 9) == 9


class TestRecords:
    def test_records_reads_a_list_of_dicts(self) -> None:
        records = [{"name": "a", "url": "x"}, {"name": "b", "url": "y"}]

        assert ThemeOptions({"name": records}).records("name") == records

    def test_records_reads_a_tuple_of_dicts(self) -> None:
        assert ThemeOptions({"name": ({"a": 1},)}).records("name") == [{"a": 1}]

    def test_records_keeps_only_the_dicts_of_a_list(self) -> None:
        options = ThemeOptions({"name": [{"a": 1}, "text", 3, None, {"b": 2}]})

        assert options.records("name") == [{"a": 1}, {"b": 2}]

    def test_records_of_a_json_string_is_empty(self) -> None:
        options = ThemeOptions({"name": '[{"name": "a"}, {"name": "b"}]'})

        assert options.records("name") == []

    @pytest.mark.parametrize(
        "value", ["not json", '{"a": 1}', "", None, 5, {"a": 1}]
    )
    def test_records_of_anything_else_is_empty(self, value: Any) -> None:
        assert ThemeOptions({"name": value}).records("name") == []

    def test_records_of_a_missing_option_is_empty(self) -> None:
        assert ThemeOptions({}).records("name") == []


class TestStaticUrl:
    @staticmethod
    def pathto(path: str, resource: int = 0) -> str:
        return f"../{path}"

    @pytest.mark.parametrize(
        ("path", "expected"),
        [
            ("", ""),
            ("logo.svg", "../_static/logo.svg"),
            ("img/logo.svg", "../_static/img/logo.svg"),
            ("_static/logo.svg", "../_static/logo.svg"),
            ("https://example.org/logo.svg", "https://example.org/logo.svg"),
            ("//example.org/logo.svg", "//example.org/logo.svg"),
            ("data:image/svg+xml;base64,AAAA", "data:image/svg+xml;base64,AAAA"),
        ],
    )
    def test_each_form_of_path_resolves_from_the_page(
        self, path: str, expected: str
    ) -> None:
        assert ThemeOptions({}).static_url(path, self.pathto) == expected
