#!/usr/bin/env bash
set -euo pipefail
MANUSCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$MANUSCRIPT_DIR"
if ! command -v texcount >/dev/null 2>&1; then
  echo "texcount not found in PATH" >&2
  exit 1
fi
TOTAL=$(texcount -inc -incbib -total -sum main.tex | awk '/Sum count:/ {print $3}')
EXCL=$(texcount -inc -total -sum main.tex | awk '/Sum count:/ {print $3}')
ABSTRACT=$(texcount sections/abstract.tex | awk '/Words in text:/ {print $4}')
SUPP=0
cat <<REPORT
Word Count Summary
------------------
Total number of words (including references): $TOTAL
Total number of words (excluding references): $EXCL
Abstract number of words: $ABSTRACT
Number of words in Supplementary Information: $SUPP
REPORT
