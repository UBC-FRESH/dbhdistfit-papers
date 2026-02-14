"""Compile the manuscript and prepend an EarthArXiv cover page."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

try:
    from .common import project_path
except ImportError:  # pragma: no cover
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.common import project_path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"
PREPRINT_DIR = PROJECT_ROOT / "preprint"
PREPRINT_TEX = PREPRINT_DIR / "preprint.tex"
OUTPUT_PDF = PREPRINT_DIR / "eartharxiv-preprint.pdf"


def run_latexmk(tex: Path) -> None:
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", "-f", tex.name]
    subprocess.run(cmd, cwd=tex.parent, check=True)


def clean_aux(directory: Path, stem: str) -> None:
    for ext in [".aux", ".log", ".out", ".fdb_latexmk", ".fls", ".synctex.gz"]:
        path = directory / f"{stem}{ext}"
        if path.exists():
            path.unlink()


def main() -> None:
    PREPRINT_DIR.mkdir(parents=True, exist_ok=True)
    # Ensure manuscript PDF is current
    run_latexmk(MANUSCRIPT_DIR / "main.tex")
    clean_aux(MANUSCRIPT_DIR, "main")

    if not PREPRINT_TEX.exists():
        raise FileNotFoundError("preprint/preprint.tex template missing")

    run_latexmk(PREPRINT_TEX)
    preprint_pdf = PREPRINT_DIR / "preprint.pdf"
    if not preprint_pdf.exists():
        raise FileNotFoundError("preprint.pdf was not generated")

    shutil.copy2(preprint_pdf, OUTPUT_PDF)
    clean_aux(PREPRINT_DIR, "preprint")
    print(f"[preprint] wrote {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
