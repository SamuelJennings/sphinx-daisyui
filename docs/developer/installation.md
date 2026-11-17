# Installation

The theme is a Python package. Installing it is all a site needs: the stylesheet is compiled
into the package, so Node and Tailwind are never needed to use it.

## Install the package

Add `sphinx-daisyui` to the dependencies your documentation builds with, such as a `docs`
dependency group or a `requirements.txt`, and install it:

```bash
pip install sphinx-daisyui
```

## Choose the theme

Set the theme in your site's `conf.py`:

```python
html_theme = "daisyui"
```

The theme registers itself with Sphinx when the package is installed, so nothing needs adding to
`extensions`. The next build uses it.
