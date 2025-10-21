"""Generate manuscript tables summarising method comparisons."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from . import fitting
from .common import (
    compression_factor,
    ensure_dir,
    expansion_factor,
    load_binned_dataset,
    load_yaml,
)


def chisquare(observed: np.ndarray, expected: np.ndarray) -> float:
    mask = expected > 0
    return float(np.sum(((observed[mask] - expected[mask]) ** 2) / expected[mask]))


def main(config_path: Path) -> None:
    cfg = load_yaml(config_path)
    output_dir = ensure_dir(cfg.get("output_dir", "tables"))
    data = load_binned_dataset(cfg.get("dataset"))
    baf = cfg.get("baf", 2.0)
    meta_plots = cfg.get("meta_plots")
    if not meta_plots:
        unique = data[["species_group", "cover_type"]].drop_duplicates()
        unique["distributions"] = [["weibull", "gamma"]] * len(unique)
        meta_plots = unique.to_dict("records")

    records: List[Dict[str, float]] = []

    for meta in meta_plots:
        species = meta["species_group"]
        cover = meta["cover_type"]
        dists = meta.get("distributions", ["weibull", "gamma"])
        subset = data[(data["species_group"] == species) & (data["cover_type"] == cover)].copy()
        if subset.empty:
            continue

        x = subset["dbh_cm"].to_numpy()
        tally = subset["tally"].to_numpy()
        expansion = (
            subset["expansion_factor"].to_numpy()
            if "expansion_factor" in subset.columns
            else np.vectorize(expansion_factor)(x, baf=baf)
        )
        compression = 1.0 / expansion
        stand_table = tally * expansion
        sample_size = int(subset["tally"].sum())

        for dist_name in dists:
            dispatch: Dict[str, callable] = fitting.method_dispatch(dist_name)
            control = dispatch["control"](x, tally)
            test = dispatch["test"](x, tally)
            control_stand = control.fitted / compression
            test_stand = test.fitted

            rss_diff = float(np.sum((control_stand - test_stand) ** 2))

            record = {
                "species_group": species,
                "cover_type": cover,
                "distribution": dist_name,
                "sample_size": sample_size,
                "rss_control_hps": control.rss,
                "rss_test_stand": test.rss,
                "rss_diff_stand": rss_diff,
                "chisq_control": chisquare(tally, control.fitted),
                "chisq_test": chisquare(stand_table, test.fitted),
            }
            records.append(record)

    df = pd.DataFrame.from_records(records)
    if df.empty:
        raise ValueError("No records generated – ensure the processed dataset is populated.")

    csv_path = output_dir / "method_comparison.csv"
    df.to_csv(csv_path, index=False)
    print(f"[tables] wrote {csv_path}")

    latex_path = output_dir / "method_comparison.tex"
    df.to_latex(latex_path, index=False, float_format="%.3e")
    print(f"[tables] wrote {latex_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate manuscript tables.")
    parser.add_argument("--config", type=Path, default=Path("config/tables.yml"))
    args = parser.parse_args()
    main(args.config)
