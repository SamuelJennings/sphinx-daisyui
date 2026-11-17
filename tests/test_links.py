from typing import Any

import pytest
from markupsafe import Markup
from sphinx.testing.util import SphinxTestApp

from sphinx_daisyui.icons import ICONS
from sphinx_daisyui.links import HOSTS, IconLink, IconLinks, SourceHost, SourceLinks
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


REPOSITORY = "https://{host}/owner/project"
ADDRESSES = {
    "github.com": (
        "https://github.com/owner/project/edit/main/{path}",
        "https://github.com/owner/project/blob/main/{path}",
    ),
    "gitlab.com": (
        "https://gitlab.com/owner/project/-/edit/main/{path}",
        "https://gitlab.com/owner/project/-/blob/main/{path}",
    ),
    "bitbucket.org": (
        "https://bitbucket.org/owner/project/src/main/{path}?mode=edit",
        "https://bitbucket.org/owner/project/src/main/{path}",
    ),
}


def sources(options: dict[str, Any] | None = None, **context: Any) -> SourceLinks:
    page = {
        "pagename": "index",
        "sourcename": "index.rst.txt",
        "page_source_suffix": ".rst",
        "pathto": pathto,
        **context,
    }
    return SourceLinks.from_options(ThemeOptions(options or {}), page)


class TestSourceHost:
    @pytest.mark.parametrize(
        "address",
        [
            "https://github.com/o/p",
            "https://GitHub.com/o/p",
            "https://www.github.com/o/p",
            "https://github.com:443/o/p",
        ],
    )
    def test_a_known_host_is_read_from_the_address(self, address: str) -> None:
        assert SourceHost.for_repository(address) is HOSTS["github.com"]

    @pytest.mark.parametrize(
        "address", ["https://example.org/o/p", "not an address", "", "github.com/o/p"]
    )
    def test_any_other_address_has_no_host(self, address: str) -> None:
        assert SourceHost.for_repository(address) is None

    def test_the_three_hosts_are_known(self) -> None:
        assert set(HOSTS) == {"github.com", "gitlab.com", "bitbucket.org"}


class TestSourceLinksAddresses:
    @pytest.mark.parametrize("host", list(ADDRESSES))
    @pytest.mark.parametrize(
        ("pagename", "path"),
        [("index", "index.rst"), ("a/b/c/page", "a/b/c/page.rst")],
    )
    def test_each_host_has_its_own_edit_and_view_address(
        self, host: str, pagename: str, path: str
    ) -> None:
        links = sources(
            {"source_repository": REPOSITORY.format(host=host)}, pagename=pagename
        )

        edit, view = ADDRESSES[host]
        assert (links.edit, links.view) == (
            edit.format(path=path),
            view.format(path=path),
        )

    def test_the_branch_is_main_unless_one_is_given(self) -> None:
        repository = REPOSITORY.format(host="github.com")

        default = sources({"source_repository": repository})
        named = sources({"source_repository": repository, "source_branch": "dev"})
        empty = sources({"source_repository": repository, "source_branch": ""})

        assert "/blob/main/" in default.view
        assert "/blob/dev/" in named.view
        assert "/blob/main/" in empty.view

    @pytest.mark.parametrize(
        "repository",
        [
            "https://github.com/owner/project/",
            "https://github.com/owner/project.git",
            "https://github.com/owner/project.git/",
        ],
    )
    def test_a_trailing_slash_or_dot_git_is_dropped(self, repository: str) -> None:
        links = sources({"source_repository": repository})

        assert links.view == "https://github.com/owner/project/blob/main/index.rst"

    @pytest.mark.parametrize("directory", ["docs", "docs/", "/docs", "/docs/"])
    def test_a_directory_is_joined_whatever_its_slashes(self, directory: str) -> None:
        links = sources(
            {
                "source_repository": REPOSITORY.format(host="github.com"),
                "source_directory": directory,
            }
        )

        assert links.view.endswith("/blob/main/docs/index.rst")

    @pytest.mark.parametrize("suffix", [".md", ".txt"])
    def test_the_address_ends_with_the_pages_own_suffix(self, suffix: str) -> None:
        links = sources(
            {"source_repository": REPOSITORY.format(host="github.com")},
            page_source_suffix=suffix,
        )

        assert links.view.endswith(f"/index{suffix}")

    def test_a_page_with_no_suffix_in_its_context_is_an_rst_file(self) -> None:
        context = {"pagename": "index", "sourcename": "index.rst.txt"}
        options = ThemeOptions({"source_repository": "https://github.com/o/p"})

        links = SourceLinks.from_options(options, context)

        assert links.view.endswith("/index.rst")

    @pytest.mark.parametrize("repository", ["https://example.org/o/p", "", None])
    def test_an_unknown_host_or_no_repository_has_no_edit_or_view_address(
        self, repository: str | None
    ) -> None:
        options = {} if repository is None else {"source_repository": repository}

        links = sources(options)

        assert (links.edit, links.view) == ("", "")

    def test_a_page_with_no_source_has_no_addresses_at_all(self) -> None:
        options = {"source_repository": REPOSITORY.format(host="github.com")}

        links = sources(options, sourcename="", show_source=True, has_source=True)

        assert links == SourceLinks("", "", "")

    def test_a_page_with_no_sourcename_in_its_context_has_none(self) -> None:
        context = {"pagename": "genindex", "pathto": pathto}
        options = ThemeOptions({"source_repository": "https://github.com/o/p"})

        assert SourceLinks.from_options(options, context) == SourceLinks("", "", "")


class TestSourceLinksCopy:
    def test_the_copy_of_the_source_is_linked_when_shown_and_copied(self) -> None:
        links = sources(show_source=True, has_source=True)

        assert links.source == "../../_sources/index.rst.txt"

    @pytest.mark.parametrize(
        "flags",
        [
            {"show_source": False, "has_source": True},
            {"show_source": True, "has_source": False},
            {},
        ],
    )
    def test_there_is_no_link_unless_both_are_on(self, flags: dict[str, bool]) -> None:
        assert sources(**flags).source == ""


class TestSourceLinksButtons:
    LINKS = SourceLinks("https://e", "https://v", "")

    def test_the_names_given_are_kept_in_order(self) -> None:
        assert self.LINKS.buttons(["view", "edit"]) == ["view", "edit"]
        assert self.LINKS.buttons(["edit", "view"]) == ["edit", "view"]

    def test_an_unknown_name_is_left_out(self) -> None:
        assert self.LINKS.buttons(["edit", "print", "source"]) == ["edit"]

    def test_an_empty_list_gives_none(self) -> None:
        assert self.LINKS.buttons([]) == []

    def test_a_button_with_no_address_is_left_out(self) -> None:
        links = SourceLinks("https://e", "", "")

        assert links.buttons(["view", "edit"]) == ["edit"]
