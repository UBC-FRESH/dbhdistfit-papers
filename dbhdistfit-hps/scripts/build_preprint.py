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
PREPRINT_DIR = PROJECT_ROOT / "preprint"
PREPRINT_TEX = PREPRINT_DIR / "preprint.tex"
FINAL_PDF = PREPRINT_DIR / "eartharxiv-preprint.pdf"


def run_latexmk(tex_path: Path) -> None:
    """Compile a LaTeX document with latexmk."""
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", tex_path.name]
    try:
        subprocess.run(cmd, cwd=tex_path.parent, check=True)
    except FileNotFoundError as exc:
        raise RuntimeError("latexmk is required to build the preprint PDF.") from exc


def clean_auxiliary_files(directory: Path, stem: str) -> None:
    """Remove common LaTeX auxiliary files for the given stem."""
    extensions = [".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".synctex.gz"]
    for ext in extensions:
        candidate = directory / f"{stem}{ext}"
        if candidate.exists():
            candidate.unlink()


def main() -> None:
    PREPRINT_DIR.mkdir(parents=True, exist_ok=True)

    # Ensure the manuscript PDF is up to date.
    run_latexmk(MANUSCRIPT_DIR / "main.tex")
    clean_auxiliary_files(MANUSCRIPT_DIR, "main")

    if not PREPRINT_TEX.exists():
        raise FileNotFoundError(f"Preprint template not found: {PREPRINT_TEX}")

    run_latexmk(PREPRINT_TEX)
    preprint_pdf = PREPRINT_DIR / "preprint.pdf"
    if not preprint_pdf.exists():
        raise FileNotFoundError("Failed to produce preprint.pdf")

    shutil.copy2(preprint_pdf, FINAL_PDF)
    clean_auxiliary_files(PREPRINT_DIR, "preprint")
    print(f"[preprint] Wrote {FINAL_PDF}")


if __name__ == "__main__":
    main()
