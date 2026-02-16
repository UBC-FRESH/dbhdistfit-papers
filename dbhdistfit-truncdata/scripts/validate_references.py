#!/usr/bin/env python3
"""
Validate BibTeX entries against the Crossref API and generate a report.

Optional: suggest DOIs for entries that are missing them (report-only).
"""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path
from typing import Iterable

import bibtexparser  # type: ignore
import requests
from dataclasses import dataclass


def normalise_title(title: str) -> str:
    """Lowercase and strip punctuation/extra whitespace for comparisons."""
    cleaned = re.sub(r"[^0-9a-zA-Z\\s]", " ", title)
    return " ".join(cleaned.lower().split())


def normalise_name(name: str) -> str:
    """Lowercase and strip punctuation/extra whitespace for comparisons."""
    cleaned = re.sub(r"[^0-9a-zA-Z\\s]", " ", name)
    return " ".join(cleaned.lower().split())


def extract_year(fields: dict[str, str]) -> int | None:
    year_raw = fields.get("year", "")
    match = re.search(r"(19|20)\\d{2}", year_raw)
    if match:
        return int(match.group(0))
    return None


def extract_first_author_surname(fields: dict[str, str]) -> str:
    author_raw = fields.get("author", "")
    if not author_raw:
        return ""
    first_author = author_raw.split(" and ")[0].strip().strip("{}")
    if "," in first_author:
        surname = first_author.split(",", 1)[0]
    else:
        parts = first_author.split()
        surname = parts[-1] if parts else ""
    return normalise_name(surname)


@dataclass
class EntryInfo:
    key: str
    fields: dict[str, str]
    entry_type: str


@dataclass
class DoiSuggestion:
    doi: str
    title: str
    score: float
    author_match: bool
    year_match: bool
    confidence: str


def candidate_year(item: dict) -> int | None:
    for field in ("issued", "published-print", "published-online"):
        payload = item.get(field)
        if not payload:
            continue
        date_parts = payload.get("date-parts", [])
        if date_parts and date_parts[0]:
            try:
                return int(date_parts[0][0])
            except (TypeError, ValueError):
                return None
    return None


def confidence_label(score: float, author_match: bool, year_match: bool, year_known: bool) -> str:
    if score >= 0.98 and author_match and (year_match or not year_known):
        return "high"
    if score >= 0.92 and author_match:
        return "medium"
    if score >= 0.88:
        return "low"
    return "low"


def suggest_dois(entry: EntryInfo, limit: int = 3) -> list[DoiSuggestion]:
    fields = entry.fields
    title = fields.get("title", "").strip("{}")
    if not title:
        return []

    author_surname = extract_first_author_surname(fields)
    year = extract_year(fields)

    params: dict[str, str | int] = {
        "query.bibliographic": title,
        "rows": max(limit, 3),
    }
    if author_surname:
        params["query.author"] = author_surname
    if year:
        params["filter"] = f"from-pub-date:{year},until-pub-date:{year}"

    try:
        resp = requests.get("https://api.crossref.org/works", params=params, timeout=20)
    except requests.RequestException:
        return []

    if resp.status_code != 200:
        return []

    try:
        items = resp.json()["message"]["items"]
    except (ValueError, KeyError, TypeError):
        return []

    bib_title_norm = normalise_title(title)
    suggestions: list[DoiSuggestion] = []
    for item in items:
        api_title = " ".join(item.get("title", []))
        doi = item.get("DOI")
        if not api_title or not doi:
            continue
        api_title_norm = normalise_title(api_title)
        score = difflib.SequenceMatcher(None, bib_title_norm, api_title_norm).ratio()
        if score < 0.80:
            continue

        author_match = False
        if author_surname:
            for author in item.get("author", []) or []:
                family = normalise_name(author.get("family", ""))
                if family and family == author_surname:
                    author_match = True
                    break

        year_match = False
        if year:
            item_year = candidate_year(item)
            year_match = item_year == year if item_year else False

        confidence = confidence_label(score, author_match, year_match, year is not None)
        suggestions.append(
            DoiSuggestion(
                doi=doi,
                title=api_title,
                score=score,
                author_match=author_match,
                year_match=year_match,
                confidence=confidence,
            )
        )

    suggestions.sort(key=lambda s: (s.confidence != "high", s.confidence != "medium", -s.score))
    return suggestions[:limit]


def iter_entries(bib_path: Path) -> Iterable[EntryInfo]:
    """Yield normalized bib entries from the provided .bib file."""
    text = bib_path.read_text(encoding="utf-8")

    library = None
    entries = []

    if hasattr(bibtexparser, "parse_string"):
        try:
            library = bibtexparser.parse_string(text)
            entries = getattr(library, "entries", [])
        except AttributeError:
            library = None

    if not entries and hasattr(bibtexparser, "loads"):
        database = bibtexparser.loads(text)
        entries = getattr(database, "entries", [])

    for entry in entries:
        if hasattr(entry, "fields"):
            field_map = {
                field.key.lower(): field.value.strip()
                for field in entry.fields
            }
            key = entry.key
            entry_type = getattr(entry, "entry_type", "") or getattr(entry, "type", "")
        elif isinstance(entry, dict):
            key = entry.get("ID", "")
            field_map = {
                k.lower(): (v.strip() if isinstance(v, str) else v)
                for k, v in entry.items()
                if k.lower() not in {"id", "entrytype"}
            }
            entry_type = entry.get("ENTRYTYPE", "")
        else:
            continue

        yield EntryInfo(key=key, fields=field_map, entry_type=str(entry_type).lower())


def validate_entry(entry: EntryInfo, suggest_missing: bool = False, suggest_limit: int = 3) -> list[str]:
    """Validate a single entry and return report lines."""
    fields = entry.fields
    lines = [f"Entry: {entry.key}"]
    if entry.entry_type:
        lines.append(f"  Type: {entry.entry_type}")
    isbn = fields.get("isbn")
    if isbn:
        lines.append(f"  ISBN: {isbn}")

    doi = fields.get("doi")
    if not doi:
        lines.append("  DOI: (missing)")
        lines.append("  Crossref status: n/a")
        if suggest_missing:
            suggestions = suggest_dois(entry, limit=suggest_limit)
            if suggestions:
                lines.append("  DOI suggestions (Crossref search):")
                for suggestion in suggestions:
                    author_flag = "yes" if suggestion.author_match else "no"
                    year_flag = "yes" if suggestion.year_match else "no"
                    lines.append(
                        "    - "
                        f"{suggestion.doi} "
                        f"(confidence={suggestion.confidence}, "
                        f"title_score={suggestion.score:.2f}, "
                        f"author_match={author_flag}, "
                        f"year_match={year_flag})"
                    )
                    lines.append(f"      Title: {suggestion.title}")
            else:
                lines.append("  DOI suggestions: none found")
        return lines

    doi_clean = doi.replace("https://doi.org/", "").strip()
    url = f"https://api.crossref.org/works/{doi_clean}"
    lines.append(f"  DOI: {doi}")

    try:
        resp = requests.get(url, timeout=20)
    except requests.RequestException as exc:  # network or HTTP error
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
    bib_title = fields.get("title", "").strip("{}")
    if api_title and bib_title:
        match = normalise_title(api_title) == normalise_title(bib_title)
        lines.append(f"  Title match: {'yes' if match else 'no'}")
        if not match:
            lines.append(f"    Bib title: {bib_title}")
            lines.append(f"    API title: {api_title}")
    else:
        lines.append("  Title match: unavailable")

    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate BibTeX references against Crossref."
    )
    parser.add_argument(
        "--bib",
        default=Path(__file__).resolve().parent.parent / "references.bib",
        type=Path,
        help="Path to the BibTeX file (default: repository references.bib).",
    )
    parser.add_argument(
        "--output",
        default=Path(__file__).resolve().parent.parent
        / "reference-validation-report.txt",
        type=Path,
        help="Path to write the validation report (default: reference-validation-report.txt in repository root).",
    )
    parser.add_argument(
        "--suggest-doi",
        action="store_true",
        help="Suggest DOIs for entries that are missing them (report-only; no .bib changes).",
    )
    parser.add_argument(
        "--suggest-limit",
        type=int,
        default=3,
        help="Maximum DOI suggestions to list per missing entry (default: 3).",
    )
    args = parser.parse_args()

    bib_path = args.bib.resolve()
    if not bib_path.exists():
        raise FileNotFoundError(f"BibTeX file not found: {bib_path}")

    output_lines = ["Reference validation report (Crossref)", ""]
    for entry in iter_entries(bib_path):
        output_lines.extend(
            validate_entry(entry, suggest_missing=args.suggest_doi, suggest_limit=args.suggest_limit)
        )
        output_lines.append("")  # blank line between entries

    output_path = args.output.resolve()
    output_path.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"Wrote report to {output_path}")


if __name__ == "__main__":
    main()
