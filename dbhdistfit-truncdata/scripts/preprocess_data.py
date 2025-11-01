"""Prepare fixed-area PSP tally data for truncated-distribution fitting."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

try:
    from .common import ensure_dir, project_path
except ImportError:  # pragma: no cover - allow execution as a script
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.common import ensure_dir, project_path

RAW_SOURCE = project_path("..", "dbhdistfit-hps", "data.local", "processed", "binned_meta_plots.parquet")
OUTPUT_PARQUET = project_path("data", "processed", "truncation_binned.parquet")
OUTPUT_DIR = OUTPUT_PARQUET.parent

# Fixed-area permanent sample plot size: 0.04 ha (400 m²)
PLOT_AREA_HA = 0.04
PLOT_EXPANSION_FACTOR = 1.0 / PLOT_AREA_HA  # 25 stems/plot -> stems per hectare
DBH_MIN = 10.0
DBH_MAX = 60.0


def compute_relative_frequency(group: pd.DataFrame) -> pd.DataFrame:
    """Add relative-frequency column so areas integrate to 1."""
    group = group.sort_values("dbh_cm").copy()
    bin_edges = np.sort(group["dbh_cm"].unique())
    if len(bin_edges) > 1:
        bin_width = np.diff(bin_edges).min()
    else:
        bin_width = 2.0
    total = (group["stand_table"] * bin_width).sum()
    if total > 0:
        group["relative_frequency"] = group["stand_table"] / (total)
    else:
        group["relative_frequency"] = 0.0
    group["bin_width_cm"] = bin_width
    return group


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = Path(RAW_SOURCE)
    if not raw_path.exists():
        raise FileNotFoundError(
            f"Shared PSP dataset not found at {RAW_SOURCE}. "
            "Ensure the HPS project data.local copy is available."
        )

    raw = pd.read_parquet(raw_path)
    # Restrict to doubly-truncated DBH range used in the legacy analysis.
    raw = raw[(raw["dbh_cm"] >= DBH_MIN) & (raw["dbh_cm"] <= DBH_MAX)]

    processed = raw.copy()
    processed["stand_table"] = processed["tally"] * PLOT_EXPANSION_FACTOR
    processed["bin_width_cm"] = 2.0
    totals = processed.groupby(["species_group", "cover_type"])["stand_table"].transform("sum")
    processed["relative_frequency"] = processed["stand_table"] / (totals * processed["bin_width_cm"])

    ensure_dir(OUTPUT_DIR)
    processed.to_parquet(OUTPUT_PARQUET, index=False)
    processed.to_csv(OUTPUT_PARQUET.with_suffix(".csv"), index=False)
    print(f"[preprocess] wrote {OUTPUT_PARQUET} and CSV twin")


if __name__ == "__main__":
    main()
