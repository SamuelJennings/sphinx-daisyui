# Layout

The `layout` option arranges the page with a code of three groups of three letters, in the
notation the Quasar framework uses for its layouts.

```python
html_theme_options = {"layout": "hHh LpR lff"}
```

## Reading a code

The three groups are the top, middle and bottom rows of the page, each read left, centre and
right.

| Letter | Area |
|---|---|
| `h` | The header: the logo, search and menus |
| `l` | The left sidebar: the documentation's contents |
| `p` | The page |
| `r` | The right sidebar: the page's own headings |
| `f` | The footer |

- **A corner says which area reaches it.** `l` in the top-left corner runs the sidebar up to the
  top of the window, and the header starts beside it. `h` there runs the header across above
  the sidebar.
- **Upper case stays in place.** `H` is a header that stays at the top as you scroll. `L` and `R`
  are sidebars that stay beside the page and scroll on their own. In lower case they scroll away
  with the page.

The middle row is always `l`, `p`, `r`, and the centre of the top and bottom rows is always `h`
and `f`. A code of any other shape stops the build with a message saying what it needs.

## Compare them

Each of these is this documentation built with one code. The banner at the top of each says
which.

| Code | What it gives | See it |
|---|---|---|
| `hHh LpR lff` | The default. The header runs across the top and stays there. The sidebar runs from under it to the bottom. | <a href="/">This site</a> |
| `lHh LpR lff` | As Furo lays a page out: the sidebar runs to the top with the logo at its head, and the header sits beside it. | <a href="/layouts/lHh-LpR-lff/">Open</a> |
| `hHh LpR fff` | As pydata-sphinx-theme lays a page out: the footer runs the whole width. | <a href="/layouts/hHh-LpR-fff/">Open</a> |
| `hhh lpr fff` | Nothing stays in place. The whole page scrolls as one. | <a href="/layouts/hhh-lpr-fff/">Open</a> |
| `hHr LpR lfr` | The page's headings run the full height on the right, beside the header and the footer. | <a href="/layouts/hHr-LpR-lfr/">Open</a> |

## On a narrower screen

- Below 1280 pixels there's no room for the right sidebar. Its cells go to the area on their
  left, and the page's headings move to an "On this page" list above the page.
- Below 1024 pixels the page is one column (header, page, footer), and the left sidebar opens
  from the menu button.

## Column widths

The widths are CSS variables. Set them in a stylesheet of your own:

```css
.daisy-layout {
  --daisy-primary-width: 20rem;
  --daisy-main-width: 56rem;
  --daisy-secondary-width: 16rem;
}
```
