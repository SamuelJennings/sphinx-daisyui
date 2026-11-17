# Brainstorm

Working notes from setting the project up. Nothing here is a ratified decision: decisions go in
`docs/adr/`, and the rules in `CONSTITUTION.md`.

## What overlaps

- **Furo** is the theme most modern Sphinx sites use, with a stylesheet of its own, a left
  navigation, a right "On this page" and light and dark modes.
- **pydata-sphinx-theme** is drawn with Bootstrap 5. It has header links, a version switcher,
  component lists for every area, and an announcement banner. sphinx-book-theme builds on it.
- **Shibuya** and **sphinxawesome-theme** are modern themes with options of their own.
  sphinxawesome-theme is built on Tailwind.

## What is new

- **daisyUI.** None of the above uses it. With it come daisyUI's 35 colour themes in light and
  dark from one stylesheet, and documentation that looks like a site already built with daisyUI.
- **Reading another theme's options.** No theme accepts Furo's or pydata-sphinx-theme's options,
  so changing theme means rewriting `conf.py`. Accepting both lowers the cost of trying this one
  to a single line.
- **A layout code.** The five areas of the page can be rearranged with one option, in Quasar's
  notation, which no Sphinx theme offers.

## Why build it rather than restyle Furo

Furo's markup and stylesheet are written together, and its colours are its own variables. A
daisyUI look on Furo would mean overriding most of its stylesheet and still not reaching
daisyUI's components, so the result would be harder to maintain than a theme drawn with daisyUI
from the start.

## Viability

The prototype on the branch `prototype-theme` builds the documentation three times: with the
theme's own options, with a Furo configuration and with a pydata-sphinx-theme configuration. It
answers the open question, whether one theme can honour both sets of options, for the options
those two configurations use.
