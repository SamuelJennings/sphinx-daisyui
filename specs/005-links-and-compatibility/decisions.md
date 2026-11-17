# Decisions: 005-links-and-compatibility

Decisions made while specifying, with the reason each is defensible. Each stands until the
maintainer changes it.

## D1. The reading of issue #8, taken as agreed

A site author links out from the site as icons and points each page at its source, and a reader
opens that source. A site author switches from Furo or pydata-sphinx-theme by changing
`html_theme` only. The design is the prototype's features 10, 11, 14 and 15, whose screens and
decisions are agreed. Everything else the prototype holds belongs to issues #4 to #7. No goal id
is cited because the repository has no `GOALS.md` yet.

## D2. Five stories

Icon links, the Furo configurations and the pydata-sphinx-theme configurations are each one
thing a site author sets out to do. Edit and view source links have two people: the site author
who says where the sources live, and the reader who opens them. A site author's and a reader's
stories are never merged, so that feature is two stories and the spec has five.

## D3. Footer icon markup is the site author's own

Furo's `footer_icons` entries carry their icon as raw SVG in `html`. Escaping it would print the
SVG as text, so every Furo configuration that sets it would lose its icons, against Article X.
It is printed as markup, on the same reasoning Article V already gives the announcement: it is
the site author's own HTML, and both themes treat it that way. Article V names only the
announcement, so the article needs the same exception added before the build. Every other value
in this feature is escaped.

## D4. `edit-this-page` keeps pydata-sphinx-theme's meaning

The prototype drew the component whenever an edit address existed. pydata-sphinx-theme draws it
only when `use_edit_page_button` is on. A borrowed component keeps its source theme's meaning
(Article X), so it follows pydata-sphinx-theme. The prototype's own rule, that turning the option
on adds the component to the secondary sidebar when no list names it, stays, because this
theme's default `secondary_sidebar_items` does not list it as pydata-sphinx-theme's does.

## D5. Every component name pydata-sphinx-theme ships resolves

Read from the pydata-sphinx-theme 0.24 wheel (`research.md`): it ships `icon-links`, `indices`,
`prev-next` and `searchbox`, which the prototype has no template for. A configuration naming
them builds already, because an unknown name draws nothing, but the issue promises every
component name is accepted. `icon-links` draws the icon links, its meaning there. `prev-next`,
`indices` and `searchbox` draw nothing: the frame draws previous and next from `show_prev_next`,
the theme has no index list, and `searchbox` is an empty container for Sphinx's highlight button.

## D6. An empty `top_of_page_buttons` shows no buttons

In Furo an empty list means no buttons. The prototype fell back to `top_of_page_button` and drew
the edit button. The spec follows Furo.

## D7. A missing host never stops the build

pydata-sphinx-theme raises an error when `use_edit_page_button` is on and `html_context` names no
host. Article X says an option the theme can't honour is never an error, so the build succeeds
and draws no edit link.

## D8. pydata-sphinx-theme's self-hosted hosts and `edit_page_url_template` are in

Its edit link reads a self-hosted `github_url`, `gitlab_url` or `bitbucket_url` and an
`edit_page_url_template` from `html_context`, and the prototype read neither. Both are part of
the edit link's meaning there, and a configuration that sets them would otherwise lose its edit
link, so the spec includes them.

## D9. `analytics` stays ignored

pydata-sphinx-theme's `analytics` loads a script from another host. Article XII says the theme
loads nothing from another host, so it is accepted and ignored for good, and the reference says
a site adds its own analytics script. `shorten_urls`, `surface_warnings` and
`templates_skip_empty_check` are accepted and ignored too, as the issue allows, and the
reference says so for each.

## D10. Furo's CSS variables: map every counterpart, set the rest as written

The prototype mapped eight of Furo's 107 variables. The spec asks for every variable with a
daisyUI counterpart to be mapped, and the rest set as written so a site's own stylesheet that
reads them still works. Which variables have a counterpart is research.

## D11. Versions promised

Furo 2025.12 and pydata-sphinx-theme 0.24, the versions the prototype read. Options those themes
removed in earlier versions are not promised.
