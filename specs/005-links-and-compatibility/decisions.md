# Decisions: 005-links-and-compatibility

Decisions made while specifying, with the reason each is defensible. Each stands until the
maintainer changes it.

## D1. Scope: icon links and source links

The theme has its own configuration and takes no other theme's options (maintainer, 2026-11-17).
A site coming from Furo or pydata-sphinx-theme reconfigures. This feature is the prototype's
features 10 (icon links) and 11 (edit and view source links). Its features 14 and 15, which made
another theme's configuration build unchanged, are not built. No goal id is cited because the
repository has no `GOALS.md` yet.

**ADR:** none — a scope ruling for this feature, recorded in the specification

## D2. Three stories

Icon links are one thing a site author sets out to do. Source links have two people: the site
author who says where the sources live, and the reader who opens them. A site author's and a
reader's stories are never merged.

**ADR:** none — how this feature's stories are cut, local to it

## D3. `icon_links` names bundled icons

Each entry's `icon` names one of the theme's bundled icons, with `type` `url` or `local` for an
image. pydata-sphinx-theme's shape is kept for the entry (`name`, `url`, `icon`, `type`), since
it is a good shape for the same thing. Its Font Awesome names, its `attributes` key and its
`github_url`, `gitlab_url`, `bitbucket_url` and `twitter_url` shortcuts are not: each is a second
way to write a link, or a mapping onto icons the theme does not use.

**ADR:** none — the shape of one option, documented in the options reference

## D4. An unknown icon name warns

A name that is not bundled draws the generic link icon and warns, naming the entry. A silent
fallback would hide a typo, and a site that builds with warnings as errors learns of it at once.

**ADR:** none — one option's warning, documented in the options reference

## D5. Icon links in the footer go through the component

`navbar-icon-links` is placed in a footer component list like any other component. There is no
second option for footer icons, so the Article V exception for footer HTML is not needed.

**ADR:** none — follows from the component lists FS-001 recorded, nothing new downstream

## D6. One shape for source links

`source_repository`, `source_branch` and `source_directory` say where the sources live, for all
three hosts. `top_of_page_buttons` (a list of `edit` and `view`, default `["edit"]`) says which
buttons sit beside the breadcrumbs, and the `edit-this-page` and `sourcelink` components place
links in a sidebar. The edit-link and view-link templates and every `html_context` key are left
out, because each is a second way to say the same thing.

**ADR:** none — the shape of four options, documented in the options reference

## D7. The host is read from the repository's address

`github.com`, `gitlab.com` and `bitbucket.org` are recognised. Any other host gets no links and no
warning, since a site may name a repository the theme cannot link into. Self-hosted instances
can get an option naming the host later, without changing these options.

**ADR:** none — a rule of one option, documented in the options reference, and a later option for self-hosted instances changes nothing here

## D8. `edit-this-page` draws whenever an edit address exists

With no `use_edit_page_button`, placing the component is the site author's choice to show the
link, as with any other component.

**ADR:** none — one component's behaviour, documented in the components reference

## D9. Versions

There is no other theme's version to track, since nothing is borrowed for compatibility.

**ADR:** none — records an absence, nothing inherits it
