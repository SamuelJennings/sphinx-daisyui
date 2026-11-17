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

## Try it

Type a code or pick an example, and the page below is drawn with it. Scroll inside the window to
see which areas stay in place. Each position takes only its own letters, so the field refuses
any other. The line under the window is the setting to copy into `conf.py`.

```{layout-rules}
```

```{raw} html
<div class="daisy-sphinx-escape lp" data-layout-playground data-screen="xl">
  <form class="lp-form" aria-label="Layout code">
    <label class="lp-field">
      <span class="lp-label">Layout code</span>
      <input class="input input-sm validator lp-code" value="hHh LpR lff" spellcheck="false" autocomplete="off" autocapitalize="off" required aria-describedby="lp-msg">
    </label>
    <div class="lp-group">
      <span class="lp-label">Examples</span>
      <div class="join">
        <button type="button" class="btn btn-sm join-item" data-code="hHh LpR lff">Default</button>
        <button type="button" class="btn btn-sm join-item" data-code="lHh LpR lff">Brand in the sidebar</button>
        <button type="button" class="btn btn-sm join-item" data-code="hHh LpR fff">Full-width footer</button>
        <button type="button" class="btn btn-sm join-item" data-code="hhh lpr fff">Nothing stays</button>
        <button type="button" class="btn btn-sm join-item" data-code="hHr LpR lfr">Tall sidebars</button>
      </div>
    </div>
    <div class="lp-group">
      <span class="lp-label">Screen</span>
      <div class="join">
        <button type="button" class="btn btn-sm join-item btn-primary" data-screen-choice="xl" aria-pressed="true">Wide</button>
        <button type="button" class="btn btn-sm join-item" data-screen-choice="lg" aria-pressed="false">Medium</button>
        <button type="button" class="btn btn-sm join-item" data-screen-choice="sm" aria-pressed="false">Phone</button>
      </div>
    </div>
  </form>
  <p id="lp-msg" class="lp-msg" aria-live="polite"></p>
  <div class="lp-chips" aria-hidden="true"></div>
  <div class="mockup-browser">
    <div class="mockup-browser-toolbar"><div class="input lp-address">docs.example.org</div></div>
    <div class="lp-viewport" tabindex="0" aria-label="A page drawn with this layout. Scroll it to see which areas stay in place.">
      <div class="lp-grid">
        <div class="lp-area lp-header" data-area="header"><span class="lp-title"><span class="lp-menu" aria-hidden="true">&#9776;</span>Header <span class="lp-pin" data-pin="header">stays</span></span></div>
        <div class="lp-area lp-primary" data-area="primary"><div class="lp-inner"><span class="lp-title">Primary sidebar <span class="lp-pin" data-pin="primary">stays</span></span><div class="lp-lines"><span></span><span></span><span></span><span></span><span></span><span></span></div></div></div>
        <div class="lp-area lp-main" data-area="main"><span class="lp-title">Page</span><div class="lp-lines"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></div>
        <div class="lp-area lp-secondary" data-area="secondary"><div class="lp-inner"><span class="lp-title">Secondary sidebar <span class="lp-pin" data-pin="secondary">stays</span></span><div class="lp-lines"><span></span><span></span><span></span><span></span></div></div></div>
        <div class="lp-area lp-footer" data-area="footer"><span class="lp-title">Footer <span class="lp-pin" data-pin="footer">stays</span></span></div>
      </div>
    </div>
  </div>
  <ul class="lp-explain"></ul>
  <pre class="lp-snippet"><code></code></pre>
</div>
```

## Examples

- `hHh LpR lff`: the default. A header above everything that stays in view, both sidebars in
  place, and a footer under the page and the primary sidebar.
- `lHh LpR lff`: the primary sidebar reaches the top-left corner and holds the site's brand.
- `hHh LpR fff`: the footer runs the full width under both sidebars.
- `hhh lpr fff`: nothing stays in place while the page scrolls.
- `hHr LpR lfr`: both sidebars reach the corners on their side.
