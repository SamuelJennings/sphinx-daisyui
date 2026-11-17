from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from .page import Page

DEEP = "a/b/c/page.html"
REPOSITORIES = {
    "github.com": ("https://github.com/owner/project", "edit/main", "blob/main"),
    "gitlab.com": ("https://gitlab.com/owner/project", "-/edit/main", "-/blob/main"),
    "bitbucket.org": ("https://bitbucket.org/owner/project", "src/main", "src/main"),
}
GITHUB = REPOSITORIES["github.com"][0]


def options(repository: str | None = GITHUB, **more: Any) -> dict[str, Any]:
    values = dict(more)
    if repository is not None:
        values["source_repository"] = repository
    return {"html_theme_options": values}


def site(repository: str | None = GITHUB, **more: Any) -> pytest.MarkDecorator:
    return pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(repository, **more),
    )


def built(app: SphinxTestApp, name: str = "index.html") -> Page:
    app.build()
    return Page.read(Path(app.outdir) / name)


def leading_to(page: Page, repository: str) -> list[str]:
    """List the addresses on the repository that the page links to, in order."""
    return [
        str(tag["href"])
        for tag in page.having("href")
        if str(tag["href"]).startswith(repository)
    ]


class TestTopOfPageButtons:
    @pytest.mark.parametrize(
        ("repository", "edit", "suffix"),
        [
            pytest.param(
                repo,
                edit,
                "?mode=edit" if host == "bitbucket.org" else "",
                marks=site(repo),
                id=host,
            )
            for host, (repo, edit, _) in REPOSITORIES.items()
        ],
    )
    @pytest.mark.parametrize(
        ("name", "path"), [("index.html", "index.rst"), (DEEP, "a/b/c/page.rst")]
    )
    def test_the_edit_button_leads_to_the_hosts_edit_address(
        self,
        app: SphinxTestApp,
        repository: str,
        edit: str,
        suffix: str,
        name: str,
        path: str,
    ) -> None:
        page = built(app, name)

        assert leading_to(page, repository) == [f"{repository}/{edit}/{path}{suffix}"]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(top_of_page_buttons=["view", "edit"]),
    )
    def test_the_buttons_follow_the_order_listed(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert leading_to(page, GITHUB) == [
            f"{GITHUB}/blob/main/index.rst",
            f"{GITHUB}/edit/main/index.rst",
        ]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(top_of_page_buttons=["edit", "view"]),
    )
    def test_the_buttons_follow_the_other_order_too(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert leading_to(page, GITHUB) == [
            f"{GITHUB}/edit/main/index.rst",
            f"{GITHUB}/blob/main/index.rst",
        ]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(top_of_page_buttons=["edit", "view"]),
    )
    def test_each_button_has_an_accessible_name(self, app: SphinxTestApp) -> None:
        page = built(app)

        buttons = [t for t in page.having("href") if t["href"].startswith(GITHUB)]  # type: ignore[union-attr]
        assert len(buttons) == 2
        assert all(tag.get("aria-label") for tag in buttons)
        assert buttons[0]["aria-label"] != buttons[1]["aria-label"]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(top_of_page_buttons=[]),
    )
    def test_an_empty_list_shows_no_button(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert leading_to(page, GITHUB) == []

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(top_of_page_buttons=[], article_header_start=[]),
    )
    def test_an_empty_list_and_empty_header_lists_draw_no_header(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert not page.classed("div", "daisy-article-header")

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(article_header_start=[], article_header_end=[]),
    )
    def test_the_buttons_alone_draw_the_header(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert page.classed("div", "daisy-article-header")
        assert leading_to(page, GITHUB) == [f"{GITHUB}/edit/main/index.rst"]

    @pytest.mark.sphinx(
        "html", testroot="links", freshenv=True, confoverrides=options()
    )
    def test_the_branch_is_main_by_default(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert leading_to(page, GITHUB) == [f"{GITHUB}/edit/main/index.rst"]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(source_branch="develop"),
    )
    def test_the_branch_set_is_the_one_linked(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert leading_to(page, GITHUB) == [f"{GITHUB}/edit/develop/index.rst"]

    @pytest.mark.sphinx(
        "html", testroot="links", freshenv=True, confoverrides=options()
    )
    def test_a_page_with_another_suffix_links_to_its_own_file(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app, "plain.html")

        assert leading_to(page, GITHUB) == [f"{GITHUB}/edit/main/plain.txt"]

    @pytest.mark.parametrize(
        "directory",
        [
            pytest.param(d, marks=site(source_directory=d), id=d)
            for d in ("docs", "docs/", "/docs/")
        ],
    )
    def test_a_directory_gives_the_same_address_with_or_without_slashes(
        self, app: SphinxTestApp, directory: str
    ) -> None:
        page = built(app)

        assert leading_to(page, GITHUB) == [f"{GITHUB}/edit/main/docs/index.rst"]


class TestEscaping:
    BRANCH = 'a" data-injected="1"><b id=injected>&'
    DIRECTORY = 'd"<i id=injected>'

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            source_branch=BRANCH,
            source_directory=DIRECTORY,
            top_of_page_buttons=["edit", "view"],
        ),
    )
    def test_a_branch_and_a_directory_reach_the_address_escaped(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert not page.find("b", id="injected")
        assert not page.find("i", id="injected")
        assert not page.having("data-injected")
        assert leading_to(page, GITHUB) == [
            f"{GITHUB}/edit/{self.BRANCH}/{self.DIRECTORY}/index.rst",
            f"{GITHUB}/blob/{self.BRANCH}/{self.DIRECTORY}/index.rst",
        ]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            source_branch=BRANCH,
            source_directory=DIRECTORY,
            top_of_page_buttons=[],
            secondary_sidebar_items=["edit-this-page"],
        ),
    )
    def test_the_component_escapes_the_address_too(self, app: SphinxTestApp) -> None:
        page = built(app)

        assert not page.find("b", id="injected")
        assert not page.having("data-injected")
        assert leading_to(page, GITHUB) == [
            f"{GITHUB}/edit/{self.BRANCH}/{self.DIRECTORY}/index.rst"
        ]


class TestEditThisPage:
    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            top_of_page_buttons=[], secondary_sidebar_items=["edit-this-page"]
        ),
    )
    def test_the_component_links_to_the_edit_address(self, app: SphinxTestApp) -> None:
        page = built(app, DEEP)

        assert leading_to(page, GITHUB) == [f"{GITHUB}/edit/main/a/b/c/page.rst"]

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            top_of_page_buttons=[], secondary_sidebar_items=["edit-this-page"]
        ),
    )
    def test_the_component_draws_even_when_the_buttons_are_off(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert len(leading_to(page, GITHUB)) == 1

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            "https://example.org/owner/project",
            secondary_sidebar_items=["edit-this-page"],
        ),
    )
    def test_an_unknown_host_draws_nothing_and_does_not_warn(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert leading_to(page, "https://example.org") == []
        assert "WARNING" not in app.warning.getvalue()


class TestWithoutAnAddress:
    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            "https://example.org/owner/project",
            top_of_page_buttons=["edit", "view"],
            secondary_sidebar_items=["edit-this-page"],
        ),
    )
    def test_an_unknown_host_has_no_button_and_no_warning(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert leading_to(page, "https://example.org") == []
        assert "WARNING" not in app.warning.getvalue()

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            None,
            top_of_page_buttons=["edit", "view"],
            secondary_sidebar_items=["edit-this-page"],
        ),
    )
    def test_no_repository_means_no_button_and_no_warning(
        self, app: SphinxTestApp
    ) -> None:
        page = built(app)

        assert not [t for t in page.having("href") if "/edit/" in str(t["href"])]
        assert "WARNING" not in app.warning.getvalue()

    @pytest.mark.sphinx(
        "html",
        testroot="links",
        freshenv=True,
        confoverrides=options(
            top_of_page_buttons=["edit", "view"],
            secondary_sidebar_items=["edit-this-page"],
        ),
    )
    @pytest.mark.parametrize("name", ["search.html", "genindex.html"])
    def test_the_search_and_index_pages_carry_none(
        self, app: SphinxTestApp, name: str
    ) -> None:
        page = built(app, name)

        assert leading_to(page, GITHUB) == []
