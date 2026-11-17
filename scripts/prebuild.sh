#!/bin/bash
# Rebuild the stylesheet, and drop viewcode pages so they are written again.
OUT="$1"
npm run -s build
rm -rf "$OUT"/_modules "$OUT"/layouts/*/_modules
