"""Create a flat Editorial Manager submission package for the truncated-data manuscript."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

try:
    from .common import ensure_dir, project_path
except ImportError:  # pragma: no cover
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.common import ensure_dir, project_path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"
FIGURES_DIR = PROJECT_ROOT / "figures"
TABLES_DIR = PROJECT_ROOT / "tables"
DEST_DIR = PROJECT_ROOT / "em-submission"
ARCHIVE_PATH = PROJECT_ROOT / "em-submission.zip"


def run_latexmk(tex: Path) -> None:
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", "-f", tex.name]
    subprocess.run(cmd, cwd=tex.parent, check=True)


def clean_aux(directory: Path, stem: str) -> None:
    for ext in [".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".synctex.gz", ".blg"]:
        path = directory / f"{stem}{ext}"
        if path.exists():
            path.unlink()


def populate_destination() -> None:
    if DEST_DIR.exists():
        shutil.rmtree(DEST_DIR)
    DEST_DIR.mkdir(parents=True)

    run_latexmk(MANUSCRIPT_DIR / "main.tex")
    run_latexmk(MANUSCRIPT_DIR / "title-page.tex")
    run_latexmk(MANUSCRIPT_DIR / "cover-letter.tex")

    clean_aux(MANUSCRIPT_DIR, "main")
    clean_aux(MANUSCRIPT_DIR, "title-page")
    clean_aux(MANUSCRIPT_DIR, "cover-letter")

    assets = [
        MANUSCRIPT_DIR / "main.tex",
        MANUSCRIPT_DIR / "main.pdf",
        MANUSCRIPT_DIR / "main.bbl",
        MANUSCRIPT_DIR / "references.bib",
        MANUSCRIPT_DIR / "title-page.pdf",
        MANUSCRIPT_DIR / "cover-letter.pdf",
        MANUSCRIPT_DIR / "cover-letter.txt",
    ]
    for asset in assets:
        if asset.exists():
            shutil.copy2(asset, DEST_DIR / asset.name)

    for folder in (FIGURES_DIR, TABLES_DIR):
        if folder.exists():
            for path in folder.iterdir():
                if path.is_file():
                    shutil.copy2(path, DEST_DIR / path.name)


def make_archive() -> None:
    if ARCHIVE_PATH.exists():
        ARCHIVE_PATH.unlink()
    shutil.make_archive(ARCHIVE_PATH.with_suffix(""), "zip", DEST_DIR)


def main() -> None:
    populate_destination()
    make_archive()
    print(f"[em-submission] Wrote {ARCHIVE_PATH}")


if __name__ == "__main__":
    main()
