"""Common utilities for the dbhdistfit-hps reproducible pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: str | Path) -> Dict[str, Any]:
    """Load a YAML configuration file."""
    with Path(path).open("r", encoding="utf8") as handle:
        return yaml.safe_load(handle)


def ensure_dir(path: str | Path) -> Path:
    """Ensure that a directory exists and return its Path."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def load_binned_dataset(path: str | Path | None = None) -> pd.DataFrame:
    """Load the pre-binned meta-plot dataset required for figure/table generation.

    Expects columns:
        species_group, cover_type, dbh_cm, tally, expansion_factor

    The dataset can be stored as Parquet or CSV. Raises FileNotFoundError if
    neither exists to prompt the user to run preprocessing first.
    """
    candidates = []
    if path:
        candidates.append(Path(path))
    else:
        candidates.extend(
            [
                PROJECT_ROOT / "data" / "processed" / "binned_meta_plots.parquet",
                PROJECT_ROOT / "data" / "processed" / "binned_meta_plots.csv",
            ]
        )

    for candidate in candidates:
        if not candidate.exists():
            continue
        if candidate.suffix == ".parquet":
            try:
                return pd.read_parquet(candidate)
            except ImportError:
                continue
        if candidate.suffix in {".csv", ".tsv"}:
            return pd.read_csv(candidate)

    raise FileNotFoundError(
        "No processed dataset found. Expected Parquet or CSV at "
        "`data/processed/binned_meta_plots` – run preprocessing to create it."
    )


def expansion_factor(dbh_cm: float, baf: float = 2.0) -> float:
    """Return stand table expansion factor for the given DBH and BAF."""
    return baf / (3.141592653589793 * (dbh_cm * 0.01 * 0.5) ** 2)


def compression_factor(dbh_cm: float, baf: float = 2.0) -> float:
    """Return reciprocal of the HPS expansion factor."""
    return 1.0 / expansion_factor(dbh_cm, baf=baf)
