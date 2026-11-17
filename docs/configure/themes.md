# Themes and colours

Every daisyUI 5 theme is built into the stylesheet. Choose one for each mode:

```python
html_theme_options = {
    "light_theme": "corporate",
    "dark_theme": "business",
}
```

## Let readers choose

```python
html_theme_options = {"theme_picker": ["light", "dark", "nord", "dracula", "retro"]}
```

`True` offers all of them. The reader's choice is remembered on their device. Open the theme
menu in the navbar of this site to try it: every page, code block and component follows.

## Your own colours

daisyUI themes are CSS variables, so a theme of your own is a stylesheet in `html_static_path`.
No Tailwind build is needed.

```{code-block} css
:caption: _static/brand.css

[data-theme="light"] {
  --color-primary: oklch(55% 0.2 280);
  --color-primary-content: oklch(98% 0.01 280);
  --radius-box: 0.75rem;
}
```

```python
html_css_files = ["brand.css"]
```

## Code colours

Code blocks take their colours from the theme, so they match whichever theme is showing. To
use Pygments styles instead, set them as in pydata-sphinx-theme:

```python
html_theme_options = {
    "pygments_light_style": "github-light",
    "pygments_dark_style": "github-dark",
}
```
