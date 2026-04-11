#!/usr/bin/env python3
"""Create a flat Editorial Manager submission package for the truncated-data manuscript."""

from __future__ import annotations

import re
import shutil
import subprocess
import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
_MANUSCRIPT_DIR_ENV = os.environ.get("MANUSCRIPT_DIR", "manuscript")
MANUSCRIPT_DIR = (PROJECT_ROOT / _MANUSCRIPT_DIR_ENV).resolve()
FIGURES_DIR = PROJECT_ROOT / "figures"
TABLES_DIR = PROJECT_ROOT / "tables"


def _submission_label() -> str:
    """Derive a stable submission label from the manuscript directory name."""
    match = re.match(r"manuscript-(r\d+)$", MANUSCRIPT_DIR.name)
    if match:
        return f"em-submission-{match.group(1)}"
    return "em-submission"


SUBMISSION_LABEL = _submission_label()
DEST_DIR = PROJECT_ROOT / SUBMISSION_LABEL
ARCHIVE_PATH = PROJECT_ROOT / f"{SUBMISSION_LABEL}.zip"


def _copy_file(src: Path, dest_name: str | None = None) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Required submission file missing: {src}")
    dest = DEST_DIR / (dest_name or src.name)
    shutil.copy2(src, dest)


def flatten_main_tex() -> None:
    """Inline section files, neutralise identifying metadata, and rewrite asset paths."""
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
    flattened = flattened.replace(
        "https://github.com/UBC-FRESH/dbhdistfit-papers",
        "[repository URL omitted for review]",
    )
    flattened = flattened.replace(
        r"\url{[repository URL omitted for review]}",
        "[repository URL omitted for review]",
    )

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


def cleanup_aux_files() -> None:
    aux_exts = [".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".synctex.gz", ".blg"]
    for ext in aux_exts:
        target = DEST_DIR / f"main{ext}"
        if target.exists():
            target.unlink()


def inline_bibliography() -> None:
    """Inline BibTeX output so EM compilation does not depend on preserving .bbl files."""
    main_tex_path = DEST_DIR / "main.tex"
    bbl_path = DEST_DIR / "main.bbl"
    if not bbl_path.exists():
        raise FileNotFoundError(f"Expected BibTeX output missing: {bbl_path}")

    tex = main_tex_path.read_text(encoding="utf-8")
    bbl = bbl_path.read_text(encoding="utf-8").strip() + "\n"

    style_and_bib = re.compile(
        r"\\bibliographystyle\{[^}]+\}\s*\\bibliography\{[^}]+\}",
        flags=re.DOTALL,
    )
    if style_and_bib.search(tex):
        tex = style_and_bib.sub(lambda _m: bbl, tex, count=1)
    else:
        tex = re.sub(r"\\bibliography\{[^}]+\}", lambda _m: bbl, tex, count=1)

    main_tex_path.write_text(tex, encoding="utf-8")
    bbl_path.unlink()


def build_blinded_pdf() -> None:
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", "-f", "main.tex"]
    subprocess.run(cmd, cwd=DEST_DIR, check=True)
    subprocess.run(["latexmk", "-c", "main.tex"], cwd=DEST_DIR, check=True)
    cleanup_aux_files()


def populate_destination() -> None:
    if DEST_DIR.exists():
        shutil.rmtree(DEST_DIR)
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    flatten_main_tex()

    essentials = [
        MANUSCRIPT_DIR / "references.bib",
        TABLES_DIR / "method_comparison.tex",
        FIGURES_DIR / "diameter_comparison.pdf",
    ]
    for path in essentials:
        if path.exists():
            _copy_file(path)
    for bst_path in MANUSCRIPT_DIR.glob("*.bst"):
        _copy_file(bst_path)

    build_blinded_pdf()
    inline_bibliography()
    build_blinded_pdf()


def make_archive() -> None:
    if ARCHIVE_PATH.exists():
        ARCHIVE_PATH.unlink()
    cleanup_aux_files()
    # Keep the upload archive truly minimal: only files required for EM compile.
    required_members = [
        "main.tex",
        "method_comparison.tex",
        "diameter_comparison.pdf",
    ]
    with zipfile.ZipFile(ARCHIVE_PATH, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in required_members:
            src = DEST_DIR / name
            if not src.exists():
                raise FileNotFoundError(f"Required archive member missing: {src}")
            zf.write(src, arcname=name)


def main() -> None:
    populate_destination()
    make_archive()
    print(f"[em-submission] Created flat archive at {ARCHIVE_PATH}")


if __name__ == "__main__":
    main()
