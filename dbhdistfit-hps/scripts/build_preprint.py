#!/usr/bin/env python3
"""
Build an EarthArXiv-ready PDF preprint.

This script compiles the main manuscript with author metadata intact and copies
the resulting PDF into ``preprint/eartharxiv-preprint.pdf`` for upload. The
source manuscript remains the authoritative LaTeX project under ``manuscript/``.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"
OUTPUT_DIR = PROJECT_ROOT / "preprint"
PDF_NAME = "eartharxiv-preprint.pdf"


def run_latexmk() -> Path:
    """Compile the manuscript with latexmk and return the PDF path."""
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", "main.tex"]
    try:
        subprocess.run(cmd, cwd=MANUSCRIPT_DIR, check=True)
    except FileNotFoundError as exc:
        raise RuntimeError("latexmk is required to build the preprint PDF.") from exc
    return MANUSCRIPT_DIR / "main.pdf"


def copy_preprint(pdf_path: Path) -> Path:
    """Copy the compiled PDF into the preprint directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_DIR / PDF_NAME
    shutil.copy2(pdf_path, destination)
    return destination


def main() -> None:
    pdf = run_latexmk()
    destination = copy_preprint(pdf)
    print(f"[preprint] Wrote {destination}")


if __name__ == "__main__":
    main()
