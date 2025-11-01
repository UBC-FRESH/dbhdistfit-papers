#!/usr/bin/env bash
set -euo pipefail

TEXCOUNT=${TEXCOUNT:-texcount}
DOC=main.tex

if ! command -v "$TEXCOUNT" >/dev/null 2>&1; then
  echo "texcount not found on PATH" >&2
  exit 1
fi

echo "Truncated-Distribution Manuscript Word Count"
echo "-------------------------------------------"
$TEXCOUNT -inc -incbib -total -sum "$DOC" | sed '1,5p'
