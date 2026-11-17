# Research: 002-navigation

## Assumptions checked

Run on 2026-11-17 against `main` at `0ffa3a3` with Sphinx 9.2.0, on a three-page test site
(`index` → `a/index` → `a/b/leaf`, the first toctree with a caption) built with
`html_theme = "daisyui"` and an `html-page-context` handler.

| Assumption | Result |
|---|---|
| The page context's `toctree()` takes `maxdepth`, `collapse`, `includehidden` and `titles_only`, which the site navigation and header links need | Holds. Called with all four on `a/b/leaf`, it returns the toctree with the current page's entries marked `current` |
| The page context carries `parents`, which the breadcrumbs need | Holds. On `a/b/leaf` it lists `A` |
| The page context carries `toc`, the page's headings, which On this page needs | Holds. It holds the page's section heading |
| The page's doctree reaches the `html-page-context` handler, for reading headings without parsing HTML | Holds. The handler's `doctree` argument is a docutils `document` |
| Sphinx builds the site toctree as docutils nodes before rendering it, for reading the menu without parsing HTML | Holds on 9.2: `StandaloneHTMLBuilder._get_local_toctree` calls `sphinx.environment.adapters.toctree.global_toctree_for_doc`, which returns nodes, and renders them with `render_partial` afterwards. Not yet checked on Sphinx 7.4 |
| `beautifulsoup4` is available to the theme on `main` | Does not hold. `main` declares `sphinx>=7.4` only, and `bs4` is not installed. Keeping it is a new runtime dependency under Article VII |

## pydata-sphinx-theme's defaults

Read from pydata-sphinx-theme's `theme.conf` (tag `v0.16.1` and `main`): `navigation_depth = 4`,
`show_nav_level = 1`, `collapse_navigation = False`, `sidebar_includehidden = True`,
`external_links` empty, `header_links_before_dropdown = 5`, `header_dropdown_text = More`,
`navbar_align = content`, `show_toc_level = 1`, `navbar_center = navbar-nav`,
`sidebars = sidebar-nav-bs.html`. The spec keeps all but `show_toc_level`, which keeps the
prototype's 2 (decision D3), and `navbar_center`, whose default is #4's.

## The doctree route, confirmed on Sphinx 7.4

Run on 2026-11-17 against Sphinx 7.4.7 and 9.2.0 with a three-page site and an
`html-page-context` handler. `sphinx.environment.adapters.toctree.global_toctree_for_doc(env,
docname, builder, collapse, includehidden, maxdepth, titles_only)` and `document_toc(env,
docname, tags)` have the same signature on both. The handler can change the nodes the first
returns and render them once with `builder.render_partial(node)["fragment"]`:

- A `raw` HTML node appended to an entry's compact paragraph renders straight after the entry's
  link and before its child list, with no wrapper, so the toggle needs no extra element.
- A node class registered with `app.add_node(..., html=(visit, depart))` and swapped in for the
  current page's `reference` renders its own `<a>` with `aria-current="page"`, and the title's
  markup (`<em>`, `<code>`) inside it is rendered by Sphinx as before.
- Classes added to `list_item`, `bullet_list` and `reference` nodes reach the HTML.
- The current page's `refuri` is empty, so the link's address is written as `#`, as Sphinx's own
  toctree writes it.

`StandaloneHTMLBuilder._get_local_toctree`, behind the context's `toctree()`, is the same call
followed by `render_partial`, so the theme does the same work Sphinx does for `toctree()` and no
more.

## Planning notes, answered

- **The prototype.** Adopted. Features 2, 13 and 4 of `PROTOTYPE.md` are the design. Their
  components, the navigation and On this page sections of `frame.css`, and the page script's
  navigation and On this page sections are ported. Python is rebuilt test-first.
- **No design review at the plan stage.** Adopted.
- **The look: ported, never redrawn.** Adopted, with one change of markup that keeps the look:
  the prototype wraps a branch's link and toggle in a `div.daisy-nav-row`. Sphinx renders the
  toggle straight after the link (above), so the row is the entry's own grid: the link and the
  toggle share the first row and the child list takes the second. The rules for
  `.daisy-nav-row` move onto `.daisy-nav-branch`, with the same spacing.
- **A branch that opens and closes.** Adopted. One method, `SiteNavigation.add_toggle`, one rule
  set and one script module, `navigation.js`. daisyUI's collapsible `menu` uses `<details>`,
  which cannot keep the entry a link, so the button beside the link stays. Its state lives once,
  on the button's `aria-expanded`: the stylesheet hides the list of a closed branch with `:has()`,
  so no `hidden` attribute has to be kept in step with it. A toctree in a page (#6) reuses
  `add_toggle`.
- **Reading Sphinx's toctree output.** Adopted, through the doctree: one class,
  `SiteNavigation`, calls `global_toctree_for_doc` once per page and gives the menu, the section
  menu and the top-level links from it. `PageContents` reads `document_toc` for On this page.
  Nothing is parsed from HTML.
- **The site-navigation component, one name.** Adopted: `sidebar-nav` only.
- **Section label.** Adopted: `.daisy-section-label`, used by the navigation's captions and On
  this page's label, reading the dimmed text property from #4.
- **From #4.** Adopted: `ThemeOptions` gains `number` and `records` readers, components are
  placed by the `components` macro, icons come from `Icons`, and dimmed text reads
  `--daisy-text-muted`.
- **The navbar dropdown macro.** Adopted as noted: the header links' menu uses daisyUI's
  `dropdown` directly. #7 folds it into its macro.
- **`navbar_align`.** Adopted. Read from `daisy.navbar_align`. `content` puts the header's
  centre slot in the main column at wide widths and gives it the article's own box, so the first
  header link starts where the article does.
- **`beautifulsoup4`.** Not adopted. The doctree route above reaches everything on Sphinx 7.4
  and 9.2, so the theme adds no runtime dependency.
- **Escaping.** Adopted. Header link titles are the entry's plain text, escaped by the template.
  Toggle names are built with `markupsafe.Markup.format`, which escapes the title.
- **Translation.** Adopted. Python's fixed text uses `sphinx.locale.get_translation("sphinx")`
  under the name `translate`, and `scripts/messages.ini` extracts it from the theme's Python.
- **`show_toc_level`.** Adopted, as FR-016.
- **The heading being read, for a screen reader.** Adopted: `aria-current="location"` on its
  link, set and cleared by the script. External entries carry a visually hidden "(leads outside
  the site)".
- **The disclosure's script.** Adopted, ported into `page-toc.js`.

## What already exists

| Piece | Where the search stopped |
|---|---|
| Reading the site toctree | Sphinx: `global_toctree_for_doc` |
| Reading the page's headings | Sphinx: `document_toc` |
| Rendering nodes to HTML | Sphinx: `builder.render_partial` |
| An `<a>` with `aria-current` | new code: one node class and its visitor, because the HTML writer's `reference` takes no extra attributes |
| Numbers and lists of links from options | this repo: `ThemeOptions`, two new readers beside `flag` and `mapping` |
| Icons | this repo: `Icons` |
| The header links' menu | daisyUI: `dropdown` |
| Breadcrumbs | Sphinx's `parents` and `title` in the page context, and daisyUI's `breadcrumbs` |
| Marking the heading being read | the browser: `IntersectionObserver` and scroll position, ported from the prototype |
| Opening and closing a branch | new code: the button and `navigation.js`, because daisyUI's menu collapses only with `<details>` |
