#!/bin/bash
# Serve the documentation with live rebuilds: the stylesheet first, then the site,
# then the same pages built with a Furo and a pydata-sphinx-theme configuration.
set -e
cd "$(dirname "$0")/.."
PORT="${PORT:-8062}"
OUT=docs/_build/site
presets() {
  DAISY_PRESET=furo uv run sphinx-build -q -a -b html docs "$OUT/as-furo" -d docs/_build/doctrees-furo
  DAISY_PRESET=pydata uv run sphinx-build -q -a -b html docs "$OUT/as-pydata" -d docs/_build/doctrees-pydata
}
npm run -s build
uv run sphinx-build -q -a -b html docs "$OUT" -d docs/_build/doctrees
presets
exec uv run sphinx-autobuild docs "$OUT" -d docs/_build/doctrees -a --host 0.0.0.0 --port "$PORT" \
  --watch src --watch assets --ignore "*/static/styles/*" --ignore "*/_build/*" \
  --pre-build "bash -c 'npm run -s build; rm -rf $OUT/_modules $OUT/as-furo/_modules $OUT/as-pydata/_modules'" \
  --post-build "bash -c 'DAISY_PRESET=furo uv run sphinx-build -q -a -b html docs $OUT/as-furo -d docs/_build/doctrees-furo; DAISY_PRESET=pydata uv run sphinx-build -q -a -b html docs $OUT/as-pydata -d docs/_build/doctrees-pydata'" \
  -q
