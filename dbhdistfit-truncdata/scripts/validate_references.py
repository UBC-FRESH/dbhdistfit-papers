#!/usr/bin/env python3
"""
Validate the manuscript bibliography against the Crossref API.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import bibtexparser  # type: ignore
import requests


CROSSREF_WORKS_URL = "https://api.crossref.org/works"

CROSSREF_WORKS_URL = "https://api.crossref.org/works"


def _normalise_title(title: str) -> str:
    cleaned = re.sub(r"[^0-9a-zA-Z\\s]", " ", title)
    return " ".join(cleaned.lower().split())


@dataclass
class Entry:
    key: str
    fields: dict[str, str]


def _iter_entries(bib_path: Path) -> Iterable[Entry]:
    text = bib_path.read_text(encoding="utf-8")

    entries: list[dict[str, str]] = []
    if hasattr(bibtexparser, "parse_string"):
        try:
            library = bibtexparser.parse_string(text)
            entries = getattr(library, "entries", [])
        except AttributeError:
            entries = []

    if not entries and hasattr(bibtexparser, "loads"):
        database = bibtexparser.loads(text)
        entries = getattr(database, "entries", [])

    for entry in entries:
        if hasattr(entry, "fields"):
            field_map = {field.key.lower(): field.value.strip() for field in entry.fields}
            key = entry.key
        else:
            field_map = {
                k.lower(): (v.strip() if isinstance(v, str) else v)
                for k, v in entry.items()
                if k.lower() not in {"id", "entrytype"}
            }
            key = entry.get("ID", "")
        yield Entry(key=key, fields=field_map)


def _lookup_by_title(title: str, author: str | None = None) -> tuple[int | None, dict | None]:
    params = {"query.bibliographic": title, "rows": 1}
    if author:
        params["query.author"] = author
    try:
        resp = requests.get(CROSSREF_WORKS_URL, params=params, timeout=20)
    except requests.RequestException:
        return None, None
    if resp.status_code != 200:
        return resp.status_code, None
    try:
        items = resp.json().get("message", {}).get("items", [])
    except ValueError:
        return resp.status_code, None
    if not items:
        return resp.status_code, None
    return resp.status_code, items[0]


def _validate_entry(entry: Entry) -> list[str]:
    lines = [f"Entry: {entry.key}"]
    doi = entry.fields.get("doi")
    if not doi:
        lines.append("  DOI: (missing)")
        title = entry.fields.get("title", "").strip("{}")
        if not title:
            lines.append("  Crossref status: n/a (no title)")
            return lines
        author = entry.fields.get("author")
        lead_author = author.split(" and ")[0] if author else None
        status, candidate = _lookup_by_title(title, lead_author)
        if status is None:
            lines.append("  Crossref status: error (network)")
        elif candidate is None:
            lines.append(f"  Crossref search status: {status if status is not None else 'n/a'} (no match)")
        else:
            lines.append(f"  Crossref search status: {status}")
            candidate_title = " ".join(candidate.get("title", []))
            candidate_doi = candidate.get("DOI")
            if candidate_doi:
                lines.append(f"  Suggested DOI: {candidate_doi}")
            if candidate_title:
                match = _normalise_title(candidate_title) == _normalise_title(title)
                lines.append(f"  Title match: {'yes' if match else 'no'}")
                if not match:
                    lines.append(f"    Bib title: {title}")
                    lines.append(f"    API title: {candidate_title}")
        return lines

    doi_clean = doi.replace("https://doi.org/", "").strip()
    url = f"{CROSSREF_WORKS_URL}/{doi_clean}"
    lines.append(f"  DOI: {doi}")

    try:
        resp = requests.get(url, timeout=20)
    except requests.RequestException as exc:
        lines.append(f"  Crossref status: error ({exc})")
        return lines

    lines.append(f"  Crossref status: {resp.status_code}")
    if resp.status_code != 200:
        return lines

    try:
        message = resp.json()["message"]
    except (ValueError, KeyError):
        lines.append("  Title match: unavailable (invalid JSON)")
        return lines

    api_title = " ".join(message.get("title", []))
    bib_title = entry.fields.get("title", "").strip("{}")
    if api_title and bib_title:
        match = _normalise_title(api_title) == _normalise_title(bib_title)
        lines.append(f"  Title match: {'yes' if match else 'no'}")
        if not match:
            lines.append(f"    Bib title: {bib_title}")
            lines.append(f"    API title: {api_title}")
    else:
        lines.append("  Title match: unavailable")

    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate BibTeX references against Crossref.")
    parser.add_argument(
        "--bib",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "manuscript" / "references.bib",
        help="Path to the BibTeX file (default: manuscript/references.bib).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "reference-validation-report.txt",
        help="Path to write the validation report (default: project root).",
    )
    args = parser.parse_args()

    bib_path = args.bib.resolve()
    if not bib_path.exists():
        raise FileNotFoundError(f"BibTeX file not found: {bib_path}")

    report_lines = ["Reference validation report (Crossref)", ""]
    for entry in _iter_entries(bib_path):
        report_lines.extend(_validate_entry(entry))
        report_lines.append("")

    output_path = args.output.resolve()
    output_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote report to {output_path}")


if __name__ == "__main__":
    main()
