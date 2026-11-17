# The layout code

The `layout` option arranges the page with a code of three groups of three letters, such as
`hHh LpR lff`.

## The letters

The three groups are the top, middle and bottom rows of the page. Each group is read left,
centre and right.

| Letter | Area |
|---|---|
| `h` | The header |
| `l` | The primary sidebar, on the left |
| `p` | The page |
| `r` | The secondary sidebar, on the right |
| `f` | The footer |

Each position takes only some letters:

| Position | Letters |
|---|---|
| Top row, left | `h` or `l` |
| Top row, centre | `h` |
| Top row, right | `h` or `r` |
| Middle row | `l`, `p`, `r` |
| Bottom row, left | `f` or `l` |
| Bottom row, centre | `f` |
| Bottom row, right | `f` or `r` |

A corner holding `l` or `r` gives that corner to the sidebar, so the sidebar runs the full height
of the page on that side.

## Upper case

An upper-case header, sidebar or footer letter keeps that area in place while the page scrolls.
`hHh` keeps the header in view. The same holds for `L`, which keeps the
primary sidebar, and `R`, which keeps the secondary sidebar.

## The medium arrangement

Below 80rem wide, the secondary sidebar is hidden and its cells go to the area on their left.
Below 64rem the page is one column and the primary sidebar becomes a drawer that the reader opens
with a button in the navbar.

## Examples

- `hHh LpR lff`: the default. A header above everything that stays in view, both sidebars in
  place, and a footer under the page and the primary sidebar.
- `lHh LpR lff`: the primary sidebar reaches the top-left corner and holds the site's brand.
- `hHh LpR fff`: the footer runs the full width under both sidebars.
- `hhh lpr fff`: nothing stays in place while the page scrolls.
- `hHr LpR lfr`: both sidebars reach the corners on their side.
