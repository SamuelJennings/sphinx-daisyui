#!/bin/bash
# The same documentation built with each layout code, side by side, in parallel.
OUT="$1"
build() { uv run --group docs sphinx-build -q -a -b html docs "$OUT/$1" -d "docs/_build/doctrees-${1//\//-}"; }
for code in "lHh LpR lff" "hHh LpR fff" "hhh lpr fff" "hHr LpR lfr"; do
  DAISY_LAYOUT="$code" build "layouts/${code// /-}" &
done
DAISY_NAVBAR_CENTER=navbar-nav build "header-links" &
DAISY_SOURCE_SIDEBAR=1 build "source-sidebar" &
DAISY_FOOTER_ICONS=1 build "footer-icons" &
wait
