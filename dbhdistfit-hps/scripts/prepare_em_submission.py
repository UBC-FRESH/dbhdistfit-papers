#!/usr/bin/env python3
"""Create a flat Editorial Manager submission package."""

from __future__ import annotations

import re
import shutil
import subprocess
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

    # Remove identifying information for double-blind review.
    def remove_braced_command(source: str, command: str, replacement: str = "") -> str:
        token = f"\\{command}{{"
        while True:
            start = source.find(token)
            if start == -1:
                break
            idx = start + len(token)
            depth = 1
            while idx < len(source) and depth > 0:
                char = source[idx]
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                idx += 1
            source = source[:start] + replacement + source[idx:]
        return source

    flattened = remove_braced_command(flattened, "author")
    flattened = re.sub(r"\\date\{.*?\}", r"\\date{}", flattened, flags=re.DOTALL)
    flattened = re.sub(r"\\noindent\\textbf\{Keywords:}.*", "", flattened)

    statements_pattern = re.compile(
        r"\\section\*{Statements and Declarations}.*?\\appendix",
        flags=re.DOTALL,
    )
    def _replace_statements(_match: re.Match[str]) -> str:
        return (
            "\\section*{Statements and Declarations}\n"
            "This section has been removed for double-blind review; full declarations are provided in the separate title page upload.\n\n"
            "\\appendix"
        )

    flattened = statements_pattern.sub(_replace_statements, flattened)

    def _replace_data_availability(_match: re.Match[str]) -> str:
        return "\\paragraph{Data Availability} Details provided separately for double-blind review.\\\\"

    flattened = re.sub(
        r"\\paragraph\{Data Availability\}.*?\\\\",
        _replace_data_availability,
        flattened,
        flags=re.DOTALL,
    )

    (DEST_DIR / "main.tex").write_text(flattened, encoding="utf-8")


def build_blinded_pdf() -> None:
    """Compile the blinded LaTeX source into a PDF."""
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", "-f", "main.tex"]
    try:
        subprocess.run(cmd, cwd=DEST_DIR, check=True)
    except FileNotFoundError as exc:
        raise RuntimeError("latexmk not found; cannot build blinded PDF.") from exc

    # Remove auxiliary files but keep main.pdf and main.bbl.
    aux_exts = [".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".synctex.gz", ".blg"]
    for ext in aux_exts:
        target = DEST_DIR / f"main{ext}"
        if target.exists():
            target.unlink()


def populate_destination() -> None:
    if DEST_DIR.exists():
        shutil.rmtree(DEST_DIR)
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    # Flatten manuscript source
    flatten_main_tex()

    # Essential files for LaTeX compilation
    essentials = [
        MANUSCRIPT_DIR / "sn-jnl.cls",
        MANUSCRIPT_DIR / "sn-mathphys-num.bst",
        MANUSCRIPT_DIR / "references.bib",
        TABLES_DIR / "method_comparison.tex",
        FIGURES_DIR / "Fig1.pdf",
    ]
    for path in essentials:
        if path.exists():
            _copy_file(path)

    # Build blinded PDF (produces main.pdf, main.bbl in DEST_DIR)
    build_blinded_pdf()

    # Copy manuscript artefacts (excluding items already produced in DEST_DIR)
    artefacts = [
        MANUSCRIPT_DIR / "title-page.pdf",
        MANUSCRIPT_DIR / "title-page.tex",
        MANUSCRIPT_DIR / "cover-letter.pdf",
        MANUSCRIPT_DIR / "cover-letter.tex",
        MANUSCRIPT_DIR / "cover-letter.txt",
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
