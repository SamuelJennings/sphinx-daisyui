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

## Try it

Type a code or pick a recipe. Scroll inside the window to see which areas stay in place.

```{raw} html
<div class="daisy-sphinx-escape lp" data-layout-playground data-screen="xl">
  <form class="lp-form" aria-label="Layout code">
    <label class="lp-field">
      <span class="lp-label">Layout code</span>
      <input class="input input-sm lp-code" value="hHh LpR lff" spellcheck="false" autocomplete="off" aria-describedby="lp-msg">
    </label>
    <div class="lp-group">
      <span class="lp-label">Recipes</span>
      <div class="join">
        <button type="button" class="btn btn-sm join-item" data-code="hHh LpR lff">Default</button>
        <button type="button" class="btn btn-sm join-item" data-code="lHh LpR lff">Furo</button>
        <button type="button" class="btn btn-sm join-item" data-code="hHh LpR fff">pydata</button>
        <button type="button" class="btn btn-sm join-item" data-code="hhh lpr fff">Static</button>
        <button type="button" class="btn btn-sm join-item" data-code="hHr LpR lfr">Tall right</button>
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
        <div class="lp-area lp-primary" data-area="primary"><div class="lp-inner"><span class="lp-title">Left sidebar <span class="lp-pin" data-pin="primary">stays</span></span><div class="lp-lines"><span></span><span></span><span></span><span></span><span></span><span></span></div></div></div>
        <div class="lp-area lp-main" data-area="main"><span class="lp-title">Page</span><div class="lp-lines"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></div>
        <div class="lp-area lp-secondary" data-area="secondary"><div class="lp-inner"><span class="lp-title">Right sidebar <span class="lp-pin" data-pin="secondary">stays</span></span><div class="lp-lines"><span></span><span></span><span></span><span></span></div></div></div>
        <div class="lp-area lp-footer" data-area="footer"><span class="lp-title">Footer <span class="lp-pin" data-pin="footer">stays</span></span></div>
      </div>
    </div>
  </div>
  <ul class="lp-explain"></ul>
  <pre class="lp-snippet"><code></code></pre>
</div>
```

## Compare them

Each of these is this documentation built with one code, to see a layout on real pages. The banner at the top of each says
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
