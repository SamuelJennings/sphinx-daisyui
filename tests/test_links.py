from typing import Any

import pytest
from markupsafe import Markup
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.icons import ICONS
from sphinx_daisyui.links import IconLink, IconLinks
from sphinx_daisyui.options import ThemeOptions


def pathto(name: str, resource: int = 0) -> str:
    return f"../../{name}" if resource else name


def links(*entries: Any, **values: Any) -> list[IconLink]:
    options = ThemeOptions({"icon_links": list(entries), **values})
    return IconLinks.from_options(options, pathto)


def problems(value: Any) -> list[str]:
    return IconLinks.problems(ThemeOptions({"icon_links": value}))


class TestFromOptions:
    def test_an_entry_becomes_a_link_with_its_name_address_and_bundled_icon(
        self,
    ) -> None:
        [link] = links(
            {"name": "Code", "url": "https://example.org/x", "icon": "github"}
        )

        assert (link.name, link.url) == ("Code", "https://example.org/x")
        assert link.image == ICONS.svg("github")

    def test_an_entry_with_no_name_is_named_by_its_address(self) -> None:
        [link] = links({"url": "https://example.org/x", "icon": "github"})

        assert link.name == "https://example.org/x"

    @pytest.mark.parametrize("entry", [{"name": "No address", "icon": "github"}, {}])
    def test_an_entry_with_no_address_leaves_no_link(
        self, entry: dict[str, Any]
    ) -> None:
        assert links(entry, {"url": "", "icon": "github"}) == []

    def test_an_unknown_icon_is_drawn_as_the_link_icon(self) -> None:
        [link] = links({"url": "https://example.org", "icon": "no-such-icon"})

        assert link.image == ICONS.svg("link")

    def test_a_type_that_is_not_url_or_local_draws_the_bundled_icon(self) -> None:
        [link] = links({"url": "https://example.org", "icon": "github", "type": "fa"})

        assert link.image == ICONS.svg("github")

    def test_a_url_image_is_one_img_at_the_address_given(self) -> None:
        [link] = links(
            {
                "url": "https://example.org",
                "icon": "https://cdn.example/i.png",
                "type": "url",
            }
        )

        assert link.image.startswith("<img ")
        assert link.image.count("<") == 1
        assert 'src="https://cdn.example/i.png"' in link.image
        assert 'alt=""' in link.image

    @pytest.mark.parametrize(
        ("icon", "expected"),
        [
            ("img.svg", "../../_static/img.svg"),
            ("_static/img.svg", "../../_static/img.svg"),
            ("https://cdn.example/i.png", "https://cdn.example/i.png"),
        ],
    )
    def test_a_local_image_is_resolved_from_the_page(
        self, icon: str, expected: str
    ) -> None:
        [link] = links({"url": "https://example.org", "icon": icon, "type": "local"})

        assert f'src="{expected}"' in link.image

    @pytest.mark.parametrize("kind", ["url", "local"])
    def test_an_image_address_is_escaped(self, kind: str) -> None:
        [link] = links(
            {"url": "https://example.org", "icon": 'x"><script>&', "type": kind}
        )

        assert isinstance(link.image, Markup)
        assert "<script>" not in link.image
        assert link.image.count("<") == 1

    @pytest.mark.parametrize("value", [None, "", "github", {"url": "x"}, 3, []])
    def test_a_value_that_is_not_a_list_of_entries_gives_no_links(
        self, value: Any
    ) -> None:
        assert IconLinks.from_options(ThemeOptions({"icon_links": value}), pathto) == []

    def test_entries_that_are_not_dicts_are_left_out(self) -> None:
        found = links("github", 3, {"url": "https://example.org", "icon": "github"})

        assert len(found) == 1

    def test_the_links_keep_the_order_of_the_entries(self) -> None:
        found = links(
            {"name": "b", "url": "https://b", "icon": "github"},
            {"name": "a", "url": "https://a", "icon": "github"},
        )

        assert [link.name for link in found] == ["b", "a"]


class TestProblems:
    def test_good_entries_give_none(self) -> None:
        assert problems([{"url": "https://example.org", "icon": "github"}]) == []

    def test_an_unset_option_gives_none(self) -> None:
        assert problems([]) == []

    def test_a_string_names_the_option(self) -> None:
        [message] = problems("github")

        assert "icon_links" in message

    def test_an_unknown_icon_names_the_entry_and_the_icon(self) -> None:
        [message] = problems(
            [{"name": "Chat", "url": "https://example.org", "icon": "no-such-icon"}]
        )

        assert "Chat" in message
        assert "no-such-icon" in message

    def test_an_unnamed_entry_is_named_by_its_address(self) -> None:
        [message] = problems([{"url": "https://example.org/x", "icon": "no-such-icon"}])

        assert "https://example.org/x" in message

    def test_one_message_for_each_unknown_icon(self) -> None:
        found = problems(
            [
                {"name": "A", "url": "https://a", "icon": "nope"},
                {"name": "B", "url": "https://b", "icon": "github"},
                {"name": "C", "url": "https://c", "icon": "nada"},
            ]
        )

        assert len(found) == 2

    @pytest.mark.parametrize("kind", ["url", "local"])
    def test_an_image_entry_is_not_checked_against_the_bundled_icons(
        self, kind: str
    ) -> None:
        entry = {"url": "https://example.org", "icon": "logo.png", "type": kind}

        assert problems([entry]) == []

    def test_an_entry_with_no_address_is_not_checked(self) -> None:
        assert problems([{"name": "None", "icon": "no-such-icon"}]) == []


class TestCheckIconLinks:
    @pytest.mark.sphinx("html", testroot="links", freshenv=True)
    def test_a_site_setting_no_links_builds_without_a_warning(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert app.warning.getvalue() == ""

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides={
            "html_theme_options": {
                "icon_links": [{"name": "Chat", "url": "https://x", "icon": "nope"}]
            }
        },
    )
    def test_an_unknown_icon_warns_once_naming_the_entry_and_the_icon(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        warnings = app.warning.getvalue().splitlines()
        assert len(warnings) == 1
        assert "Chat" in warnings[0]
        assert "nope" in warnings[0]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides={"html_theme_options": {"icon_links": "github"}},
    )
    def test_a_string_option_warns_once_naming_the_option(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        warnings = app.warning.getvalue().splitlines()
        assert len(warnings) == 1
        assert "icon_links" in warnings[0]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides={
            "html_theme_options": {
                "icon_links": [
                    {"name": "Code", "url": "https://x", "icon": "github"},
                    {
                        "name": "Logo",
                        "url": "https://x",
                        "icon": "a.png",
                        "type": "local",
                    },
                ]
            }
        },
    )
    def test_known_icons_and_images_build_without_a_warning(
        self, app: SphinxTestApp
    ) -> None:
        app.build()

        assert app.warning.getvalue() == ""
