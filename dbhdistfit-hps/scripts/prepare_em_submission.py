#!/usr/bin/env python3
"""Create a flat Editorial Manager submission package."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"
FIGURES_DIR = PROJECT_ROOT / "figures"
TABLES_DIR = PROJECT_ROOT / "tables"
DEST_DIR = PROJECT_ROOT / "em-submission"
ARCHIVE_PATH = PROJECT_ROOT / "em-submission.zip"


def _copy_file(src: Path, dest_name: str | None = None) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Required submission file missing: {src}")
    dest = DEST_DIR / (dest_name or src.name)
    shutil.copy2(src, dest)


def flatten_main_tex() -> None:
    """Inline section files and rewrite asset paths."""
    main_path = MANUSCRIPT_DIR / "main.tex"
    text = main_path.read_text(encoding="utf-8")

    input_pattern = re.compile(r"\\input\{([^}]+)\}")

    def expand(match: re.Match[str]) -> str:
        rel = match.group(1)
        section_path = (MANUSCRIPT_DIR / f"{rel}.tex").resolve()
        if not section_path.exists():
            raise FileNotFoundError(f"Missing section for inclusion: {section_path}")
        section_text = section_path.read_text(encoding="utf-8")
        banner = f"% >>> BEGIN {rel}\n{section_text}\n% <<< END {rel}"
        return banner

    flattened = input_pattern.sub(expand, text)
    flattened = flattened.replace("../figures/", "")
    flattened = flattened.replace("../tables/", "")
    (DEST_DIR / "main.tex").write_text(flattened, encoding="utf-8")


def populate_destination() -> None:
    if DEST_DIR.exists():
        shutil.rmtree(DEST_DIR)
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    # Flatten manuscript source
    flatten_main_tex()

    # Copy manuscript artefacts
    artefacts = [
        MANUSCRIPT_DIR / "main.pdf",
        MANUSCRIPT_DIR / "main.bbl",
        MANUSCRIPT_DIR / "references.bib",
        MANUSCRIPT_DIR / "title-page.pdf",
        MANUSCRIPT_DIR / "title-page.tex",
        MANUSCRIPT_DIR / "cover-letter.pdf",
        MANUSCRIPT_DIR / "cover-letter.tex",
    ]
    for path in artefacts:
        if path.exists():
            _copy_file(path)

    # Copy figure exports (only Fig1.*)
    for suffix in (".pdf", ".eps", ".png", ".tif"):
        figure_file = FIGURES_DIR / f"Fig1{suffix}"
        if figure_file.exists():
            _copy_file(figure_file)

    # Copy table exports
    for table_name in ("method_comparison.csv", "method_comparison.tex"):
        table_path = TABLES_DIR / table_name
        if table_path.exists():
            _copy_file(table_path)


def make_archive() -> None:
    if ARCHIVE_PATH.exists():
        ARCHIVE_PATH.unlink()
    shutil.make_archive(ARCHIVE_PATH.with_suffix(""), "zip", DEST_DIR)


def main() -> None:
    populate_destination()
    make_archive()
    print(f"[em-submission] Created flat archive at {ARCHIVE_PATH}")


if __name__ == "__main__":
    main()
