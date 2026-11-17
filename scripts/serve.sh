#!/bin/bash
# Serve the documentation with live rebuilds: the stylesheet first, then the site,
# then the same pages built with each layout code the docs compare.
set -e
cd "$(dirname "$0")/.."
PORT="${PORT:-8000}"
OUT=docs/_build/site
exec uv run sphinx-autobuild docs "$OUT" -d docs/_build/doctrees -a --host 0.0.0.0 --port "$PORT" \
  --watch src --watch assets --ignore "*/static/styles/*" --ignore "*/_build/*" \
  --pre-build "bash scripts/prebuild.sh $OUT" \
  --post-build "bash scripts/variants.sh $OUT" \
  -q
