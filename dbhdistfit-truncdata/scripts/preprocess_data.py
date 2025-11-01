"""Prepare fixed-area PSP tally data for truncated-distribution fitting."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .common import ensure_dir, project_path

RAW_SOURCE = project_path("..", "dbhdistfit-hps", "data.local", "processed", "binned_meta_plots.parquet")
OUTPUT_PARQUET = project_path("data", "processed", "truncation_binned.parquet")
OUTPUT_DIR = OUTPUT_PARQUET.parent

# Fixed-area expansion factor (per-hectare) placeholder; will be verified against
# original PSP design once legacy notes are reviewed.
PLOT_EXPANSION_FACTOR = 10000 / 400  # e.g., 0.04 ha plot -> multiply by 25


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not Path(RAW_SOURCE).exists():
        raise FileNotFoundError(
            "Shared PSP dataset not found. Ensure the HPS project data.local copy is available"
        )

    raw = pd.read_parquet(RAW_SOURCE)
    # Replace the HPS-specific expansion logic with a constant factor derived from
    # fixed-area plot size. The raw dataset already contains `tally` counts from PSP
    # tallies; multiplying by the constant expansion places counts in stems/ha.
    processed = raw.copy()
    processed["stand_table"] = processed["tally"] * PLOT_EXPANSION_FACTOR

    ensure_dir(OUTPUT_DIR)
    processed.to_parquet(OUTPUT_PARQUET, index=False)
    processed.to_csv(OUTPUT_PARQUET.with_suffix(".csv"), index=False)
    print(f"[preprocess] wrote {OUTPUT_PARQUET} and CSV twin")


if __name__ == "__main__":
    main()
