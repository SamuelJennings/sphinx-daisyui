import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

from sphinx_daisyui.layout import LayoutCode, LayoutCodeError

EXTENSION = Path(__file__).parents[2] / "docs" / "_ext" / "layout_playground.py"


def load_extension() -> ModuleType:
    spec = importlib.util.spec_from_file_location("layout_playground", EXTENSION)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def extension() -> ModuleType:
    return load_extension()


@pytest.fixture(scope="module")
def rules(extension: ModuleType) -> dict:
    return extension.read_rules()


class TestReadRules:
    def test_every_code_it_lists_is_a_layout_code(
        self, extension: ModuleType, rules: dict
    ) -> None:
        for code, facts in rules["layouts"].items():
            layout = LayoutCode.parse(code)

            assert layout.code == code
            assert facts == extension.facts(layout)

    def test_each_position_takes_the_letters_the_layout_code_accepts(
        self, rules: dict
    ) -> None:
        letters = "hhh lpr fff".replace(" ", "")
        for index, taken in enumerate(rules["positions"]):
            for letter in "hlprf":
                swapped = letters[:index] + letter + letters[index + 1 :]
                code = " ".join(swapped[i : i + 3] for i in range(0, 9, 3))

                if letter in taken:
                    LayoutCode.parse(code)
                else:
                    with pytest.raises(LayoutCodeError):
                        LayoutCode.parse(code)

    def test_only_the_positions_where_case_changes_the_layout_are_listed(
        self, extension: ModuleType, rules: dict
    ) -> None:
        letters = "hhhlprfff"
        lower = extension.facts(LayoutCode.parse(extension.spaced(letters)))
        for index in range(9):
            capital = letters[:index] + letters[index].upper() + letters[index + 1 :]

            changed = extension.facts(LayoutCode.parse(extension.spaced(capital)))

            assert (changed != lower) == (index in rules["case"])


class TestLayoutRulesDirective:
    def test_it_writes_the_rules_into_the_page_as_json(
        self, extension: ModuleType, rules: dict
    ) -> None:
        directive = extension.LayoutRules.__new__(extension.LayoutRules)

        (node,) = directive.run()
        html = node.astext()
        body = html.split(">", 1)[1].rsplit("</script", 1)[0]

        assert 'id="layout-rules"' in html
        assert json.loads(body) == rules
