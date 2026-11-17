import dataclasses

import pytest
from markupsafe import Markup

from sphinx_daisyui.layout import LayoutCode, LayoutCodeError

HEADER_HEIGHT = "var(--daisy-header-height)"


class TestLayoutCode:
    def test_the_default_code_has_a_sticky_header_and_sidebars(self) -> None:
        layout = LayoutCode.parse(None)

        assert LayoutCode.DEFAULT == "hHh LpR lff"
        assert layout.code == "hHh LpR lff"
        assert layout.areas_wide == Markup(
            '"header header header" "primary main secondary" "primary footer footer"'
        )
        assert layout.header_sticky
        assert layout.primary_sticky
        assert layout.secondary_sticky
        assert not layout.footer_sticky
        assert layout.primary_top == HEADER_HEIGHT
        assert layout.secondary_top == HEADER_HEIGHT
        assert not layout.brand_in_sidebar

    def test_an_empty_value_means_the_default(self) -> None:
        assert LayoutCode.parse("") == LayoutCode.parse(None)
        assert LayoutCode.parse("  ") == LayoutCode.parse(None)

    def test_the_areas_are_markup(self) -> None:
        layout = LayoutCode.parse(None)

        assert isinstance(layout.areas_wide, Markup)
        assert isinstance(layout.areas_medium, Markup)

    def test_a_sidebar_in_the_top_left_corner_holds_the_brand(self) -> None:
        layout = LayoutCode.parse("lHh LpR lff")

        assert layout.brand_in_sidebar
        assert layout.areas_wide == Markup(
            '"primary header header" "primary main secondary" "primary footer footer"'
        )

    def test_an_all_lower_case_code_has_no_sticky_areas(self) -> None:
        layout = LayoutCode.parse("hhh lpr fff")

        assert not layout.header_sticky
        assert not layout.primary_sticky
        assert not layout.secondary_sticky
        assert not layout.footer_sticky

    def test_exactly_the_upper_case_areas_are_sticky(self) -> None:
        layout = LayoutCode.parse("hhh lpR fFf")

        assert not layout.header_sticky
        assert not layout.primary_sticky
        assert layout.secondary_sticky
        assert layout.footer_sticky

    def test_the_medium_arrangement_gives_the_secondary_cells_to_the_left(
        self,
    ) -> None:
        layout = LayoutCode.parse("hHr LpR lfr")

        assert layout.areas_wide == Markup(
            '"header header secondary" "primary main secondary" "primary footer secondary"'
        )
        assert layout.areas_medium == Markup(
            '"header header header" "primary main main" "primary footer footer"'
        )

    @pytest.mark.parametrize(
        ("code", "primary_top", "secondary_top"),
        [
            ("hHh LpR lff", HEADER_HEIGHT, HEADER_HEIGHT),
            ("lHh LpR lff", "0px", HEADER_HEIGHT),
            ("hHr LpR lff", HEADER_HEIGHT, "0px"),
            ("hhh LpR lff", "0px", "0px"),
        ],
    )
    def test_the_sidebars_offset_follows_the_header(
        self, code: str, primary_top: str, secondary_top: str
    ) -> None:
        layout = LayoutCode.parse(code)

        assert layout.primary_top == primary_top
        assert layout.secondary_top == secondary_top

    def test_extra_spaces_and_mixed_case_read_the_same_code(self) -> None:
        tidy = LayoutCode.parse("hHh LpR lff")

        assert LayoutCode.parse("  hHh   LpR\tlff ") == tidy
        assert LayoutCode.parse("HHH lpr LFF").code == "HHH lpr LFF"
        assert LayoutCode.parse("HHH lpr LFF").areas_wide == (
            LayoutCode.parse("hhh lpr lff").areas_wide
        )

    def test_the_code_is_frozen(self) -> None:
        with pytest.raises(dataclasses.FrozenInstanceError):
            LayoutCode.parse(None).code = "hhh lpr fff"  # type: ignore[misc]

    @pytest.mark.parametrize(
        "code",
        [
            "xHh LpR lff",
            "hxh LpR lff",
            "hHx LpR lff",
            "hHh xpR lff",
            "hHh LxR lff",
            "hHh Lpx lff",
            "hHh LpR xff",
            "hHh LpR lxf",
            "hHh LpR lfx",
            "hHh LpR",
            "hHh LpR lff hHh",
            "hHhLpRlff",
            "hHh LpR lf",
        ],
    )
    def test_a_code_of_the_wrong_shape_is_refused(self, code: str) -> None:
        with pytest.raises(LayoutCodeError) as error:
            LayoutCode.parse(code)

        assert "layout" in str(error.value)
        assert repr(code) in str(error.value)
        assert "Traceback" not in str(error.value)

    @pytest.mark.parametrize("value", [5, ["hHh", "LpR", "lff"], True])
    def test_a_value_that_is_not_a_string_is_refused(self, value: object) -> None:
        with pytest.raises(LayoutCodeError) as error:
            LayoutCode.parse(value)

        assert "layout" in str(error.value)
        assert repr(value) in str(error.value)

    def test_the_error_is_a_value_error(self) -> None:
        assert issubclass(LayoutCodeError, ValueError)
