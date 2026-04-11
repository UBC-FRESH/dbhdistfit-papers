#!/usr/bin/env bash
set -euo pipefail

MANUSCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$MANUSCRIPT_DIR"

if ! command -v texcount >/dev/null 2>&1; then
  echo "texcount not found in PATH" >&2
  exit 1
fi

DOC=${1:-main.tex}
TOTAL=$(texcount -inc -incbib -total -sum "$DOC" | perl -ne 'print "$1\n" if /^Sum count:\s+(\d+)/')
EXCL=$(texcount -inc -total -sum "$DOC" | perl -ne 'print "$1\n" if /^Sum count:\s+(\d+)/')
ABSTRACT=$(texcount sections/abstract.tex | perl -ne 'print "$1\n" if /^Words in text:\s+(\d+)/')
SUPP=0

cat <<REPORT
Truncated-Distribution Manuscript Word Count
-------------------------------------------
Total number of words (including references): $TOTAL
Total number of words (excluding references): $EXCL
Abstract number of words: $ABSTRACT
Number of words in Supplementary Information: $SUPP
REPORT
