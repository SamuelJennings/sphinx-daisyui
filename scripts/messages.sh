#!/usr/bin/env bash
# Regenerate the message catalogue template from the theme's templates and Python.
set -euo pipefail
cd "$(dirname "$0")/.."

uv run pybabel extract \
  --mapping-file scripts/messages.ini \
  --project sphinx-daisyui \
  --no-location \
  --keyword=translate \
  --sort-output \
  --output-file src/sphinx_daisyui/locale/sphinx.pot \
  src/sphinx_daisyui

# Babel ends the file with a blank line, which the repo's end-of-file check removes.
sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' src/sphinx_daisyui/locale/sphinx.pot
