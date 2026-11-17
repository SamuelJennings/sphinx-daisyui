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

## D2. The interpretation was written, not grilled

The issue, the prototype and its recorded decisions leave nothing open about what the feature
does, and the maintainer handed the work over. The interpretation below was treated as confirmed.

> A reader finds their way around the site and the page. The primary sidebar holds the whole
> site as a menu with open and close toggles, the current page marked and scrolled into view,
> captions labelling sections, and breadcrumbs above the page. A site author sets how deep it
> goes and how much starts open with pydata-sphinx-theme's options. Placing `navbar-nav` in
> `navbar_center` moves the top-level sections into the navbar, with a menu for the rest and
> external links, the primary sidebar then showing only the current section and the drawer
> listing the sections at its head. The secondary sidebar lists the page's headings and marks
> the one being read, or a disclosure above the page does on a narrower screen. Out of scope: the
> page frame (#4), a toctree in a page body (#6), the shared navbar menu (#7), edit and source
> links and the Furo and pydata-sphinx-theme template names (#8).

## D3. `show_toc_level` defaults to 2

pydata-sphinx-theme defaults it to 1. The accepted prototype defaults it to 2, and its screens,
which are agreed, show two levels. A pydata-sphinx-theme configuration that sets the option keeps
its meaning, and one that leaves it unset gets one more level listed, which builds and warns about
nothing (Article X asks for the same name, type and meaning, not the same default). The maintainer
may prefer pydata-sphinx-theme's default: it is one value in `theme.toml`.

## D4. `show_toc_level` takes pydata-sphinx-theme's full meaning

The prototype only tells level 1 from the rest. pydata-sphinx-theme lists headings down to the
level at all times and shows deeper ones while the reader is in their section. Article X asks for
the borrowed meaning, so the spec asks for it (FR-016), and research confirms the detail before
it is built.

## D5. Only `navbar_center` switches the primary sidebar to the current section

The prototype's recorded decision says putting `navbar-nav` in `navbar_center` switches to the
sectioned layout. Placed in another list, it draws the header links and leaves the site
navigation whole, so a site that wants both can have them.

## D6. A page in no section shows no site navigation with header links on

With header links in the navbar, the home page belongs to no section, and the prototype draws no
menu there. pydata-sphinx-theme does the same. Whether the frame then leaves the empty primary
sidebar out is #4's behaviour, not this feature's.

## D7. The current entry and the heading being read are marked for assistive technology

The prototype marks the heading being read and external entries by class only. Article XIV asks
for the theme's controls and states to be named for a screen reader, so the spec asks for a mark
assistive technology reads (FR-006, FR-015).

## D8. `beautifulsoup4` is decided at planning, against the doctree

The prototype carries it with no stated reason. The spec asks only that any runtime dependency
has a stated reason and `deptry` passes (FR-021). Whether to keep it or read docutils' doctree is
how, and research decides it from the check in `research.md`.

## D9. The default of `header_dropdown_text` is translated

Its default is the theme's own text, so Article VIII asks for it to be translatable. A value the
site author sets is theirs and is never translated.

## D10. No goal id

The repository has no `GOALS.md` yet, so the spec cites no goal and the issue carries no goal
footer.
