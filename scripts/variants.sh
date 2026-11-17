#!/bin/bash
# The same documentation built with each layout code, side by side, in parallel.
OUT="$1"
build() { uv run sphinx-build -q -a -b html docs "$OUT/$1" -d "docs/_build/doctrees-${1//\//-}"; }
for code in "lHh LpR lff" "hHh LpR fff" "hhh lpr fff" "hHr LpR lfr"; do
  DAISY_LAYOUT="$code" build "layouts/${code// /-}" &
done
wait
