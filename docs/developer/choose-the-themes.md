# Choose the themes

The theme draws the site in a daisyUI theme for each colour mode. A site chooses which theme each
mode draws, which mode a reader starts in, and which themes a reader may pick by name.

## Set the themes for each mode

1. Set `light_theme` and `dark_theme` in `html_theme_options` in `conf.py`:

   ```python
   html_theme_options = {
       "light_theme": "corporate",
       "dark_theme": "business",
   }
   ```

2. Set `default_mode` to the mode a reader sees first. The values are `"auto"`, which follows
   the reader's system, `"light"` and `"dark"`:

   ```python
   html_theme_options = {
       "default_mode": "dark",
   }
   ```

Every page now draws the light theme in light mode and the dark theme in dark mode. A reader who
chooses a mode from the theme menu keeps that choice on their device. Every daisyUI 5 theme is
built into the stylesheet. [Options](../reference/options.md) describes each option.

## Let readers choose a theme

1. Set `theme_picker` to the themes to offer:

   ```python
   html_theme_options = {
       "theme_picker": ["light", "dark", "nord", "dracula", "retro"],
   }
   ```

   `True` offers every theme. A string with the names separated by commas works too.

2. Check that the theme menu is in a component list. The theme puts the `theme-switcher`
   component in `navbar_end`.

The theme menu now lists the three modes, then the themes, each once and in the order given.
Every page, code block and component follows the reader's choice, and the browser remembers it.

## Use your own colours

A daisyUI theme is a set of CSS variables, so a theme of your own is a stylesheet. No Tailwind
build is needed.

1. Write the stylesheet in a directory listed in `html_static_path`:

   ```{code-block} css
   :caption: _static/brand.css

   [data-theme="light"] {
     --color-primary: oklch(55% 0.2 280);
     --color-primary-content: oklch(98% 0.01 280);
     --radius-box: 0.75rem;
   }
   ```

2. Name it in `html_css_files` in `conf.py`:

   ```python
   html_css_files = ["brand.css"]
   ```

The rule above changes the colours of the light theme. To add a theme under a new name, write
the rule for `[data-theme="brand"]`, set `color-scheme` in it, and name it in `light_theme`,
`dark_theme` or `theme_picker`. A name is used as given, so it need not be one of daisyUI's.

## Read the mode in your own styles

The theme sets six attributes on the root element before the page is drawn.
[The page](../reference/page.md) lists them. Key a rule on them to style something differently in
dark mode:

```css
html[data-mode="dark"] .diagram {
  filter: invert(1);
}
```
