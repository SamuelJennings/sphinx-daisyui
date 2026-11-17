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
- **Options modelled on pydata-sphinx-theme's.** One name and one shape for each setting, with
  no layer that accepts another theme's configuration. A site coming from Furo or
  pydata-sphinx-theme reconfigures.
- **A layout code.** The five areas of the page can be rearranged with one option, in Quasar's
  notation, which no Sphinx theme offers.

## Why build it rather than restyle Furo

Furo's markup and stylesheet are written together, and its colours are its own variables. A
daisyUI look on Furo would mean overriding most of its stylesheet and still not reaching
daisyUI's components, so the result would be harder to maintain than a theme drawn with daisyUI
from the start.

## Viability

The prototype on the branch `prototype-theme` builds the documentation with the theme's own
options and shows the page layouts of Furo and of pydata-sphinx-theme, which the layout option
reproduces.
