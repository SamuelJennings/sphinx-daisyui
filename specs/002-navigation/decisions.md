# Decisions: 002-navigation

Decisions made while specifying, with the reason each is defensible. Each stands until the
maintainer changes it.

## D1. Three stories, one per feature of the prototype

The prototype's hand-over names three features for this issue: site navigation, header links and
On this page. Site navigation has a reader's part (moving through the menu and the breadcrumbs)
and a site author's part (how deep it goes and how much starts open). The site author's options
only vary what the reader's menu holds, and nobody sets out to change `show_nav_level` on its
own, so they are scenarios of the reader's story rather than a story of their own. Header links
stay the site author's story: placing `navbar-nav` is a choice a site author makes, and what the
reader then gets is its scenarios.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D2. The interpretation was written, not grilled

The issue, the prototype and its recorded decisions leave nothing open about what the feature
does, and the maintainer handed the work over. The interpretation below was treated as confirmed.

> A reader finds their way around the site and the page. The primary sidebar holds the whole
> site as a menu with open and close toggles, the current page marked and scrolled into view,
> captions labelling sections, and breadcrumbs above the page. A site author sets how deep it
> goes and how much starts open. Placing `navbar-nav` in
> `navbar_center` moves the top-level sections into the navbar, with a menu for the rest and
> external links, the primary sidebar then showing only the current section and the drawer
> listing the sections at its head. The secondary sidebar lists the page's headings and marks
> the one being read, or a disclosure above the page does on a narrower screen. Out of scope: the
> page frame (#4), a toctree in a page body (#6), the shared navbar menu (#7), edit and source
> links (#8).

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D3. `show_toc_level` defaults to 2

The accepted prototype defaults it to 2, and its screens, which are agreed, show two levels. The
option is the theme's own, so its default is the theme's choice. It is one value in `theme.toml`.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D4. `show_toc_level` lists levels at all times and shows deeper ones in their section

The prototype only tells level 1 from the rest, which leaves every value above 1 meaning the same.
The spec gives each value a meaning: headings down to the level are listed at all times, and
deeper ones are shown while the reader is in their section (FR-016).

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D5. Only `navbar_center` switches the primary sidebar to the current section

The prototype's recorded decision says putting `navbar-nav` in `navbar_center` switches to the
sectioned layout. Placed in another list, it draws the header links and leaves the site
navigation whole, so a site that wants both can have them.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D6. A page in no section shows no site navigation with header links on

With header links in the navbar, the home page belongs to no section, and the prototype draws no
menu there. Whether the frame then leaves the empty primary
sidebar out is #4's behaviour, not this feature's.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D7. The current entry and the heading being read are marked for assistive technology

The prototype marks the heading being read and external entries by class only. Article XIV asks
for the theme's controls and states to be named for a screen reader, so the spec asks for a mark
assistive technology reads (FR-006, FR-015).

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D8. `beautifulsoup4` is decided at planning, against the doctree

The prototype carries it with no stated reason. The spec asks only that any runtime dependency
has a stated reason and `deptry` passes (FR-021). Whether to keep it or read docutils' doctree is
how, and research decides it from the check in `research.md`.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D9. The default of `header_dropdown_text` is translated

Its default is the theme's own text, so Article VIII asks for it to be translatable. A value the
site author sets is theirs and is never translated.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D10. No goal id

The repository has no `GOALS.md` yet, so the spec cites no goal and the issue carries no goal
footer.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D11. The theme's own configuration, with no compatibility layer

The maintainer ruled on 2026-11-17 that the theme has its own configuration: nothing accepts,
maps or aliases another theme's options or template names, and a site coming from another theme
reconfigures. The options this feature uses keep pydata-sphinx-theme's names and shapes, because
they are good names for the same settings, but they are the theme's own. The site navigation is
the `sidebar-nav` component under that one name.

**ADR:** none — the rule is the constitution's; this records how this feature follows it.

## D12. Sphinx's toctree is read as nodes, with no new dependency

The theme reads the site toctree with `global_toctree_for_doc` and the page's headings with
`document_toc`, changes the nodes and renders them once. Both are on Sphinx 7.4 and 9.2 with the
same signature (`research.md`). `beautifulsoup4` is not added, so no page is parsed back from
HTML and the theme adds no runtime dependency.

**ADR:** docs/adr/0001-read-toctrees-as-document-nodes.md

## D13. A branch's open state lives on its toggle

The toggle's `aria-expanded` is the one record of whether a branch is open. The stylesheet hides
the list of a closed branch, so the script changes one attribute and nothing can disagree with
it.

**ADR:** none — how one control keeps its state, local to the site navigation.

## D14. Header link titles are plain text

A header link shows its page's title as text, escaped by the template. Markup in a title, such
as code, would need styles in the navbar that nothing else there has, and the prototype shows
plain text.

**ADR:** none — local to the header links' template.

## D15. The heading being read is marked with `aria-current="location"`

WAI-ARIA's `location` value is for the current item within a set of links to parts of the page.
The site navigation's current page keeps `aria-current="page"`.

**ADR:** none — follows WAI-ARIA's meaning of the value, nothing to decide again.

## D16. Domain indices count as index pages

A domain index such as `py-modindex` is a list of entries with no headings of its own, like
`genindex`, so the secondary sidebar and the On this page disclosure are left out there too. The
pages are told apart by the template Sphinx renders them with (`genindex*.html`,
`domainindex.html`, `search.html`), which holds for every split and every domain.

**ADR:** none — a reading of the specification for this feature, nothing downstream inherits it.

## D17. Header links aligned to the article are placed by a measuring script

`navbar_align = "content"` must start the first header link at the article's left edge for every
layout code and window width. The edge depends on the primary column's width, the page column's
width, the centring of the article inside it and where the header starts in the grid, which differ
between layout codes. A stylesheet-only rule would repeat the grid's arithmetic for each layout
code. `navigation.js` measures the article's and the first link's positions and sets the margin
on wide screens, and `left` and `right` are stylesheet rules. Without the script the links start
at the start of the navbar's free space.

Revisit if the layout code gives the header a fixed column, which would let the stylesheet place
the links on the same grid columns.

**ADR:** none — local to the header links' alignment, inside one script.

## D18. A header link marks its section with `aria-current="true"`

A header link leads to a section's first page, and it is marked while the reader is anywhere in
that section. `aria-current="page"` would tell a screen reader the link is the page being read,
which holds only on the section's first page, so the mark is `true`. The site navigation's
entry for the page being read keeps `page`.

**ADR:** none — follows WAI-ARIA's meaning of the value, nothing to decide again.
