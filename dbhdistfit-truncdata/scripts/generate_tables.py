"""Generate comparison tables for truncated distribution fits."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .common import ensure_dir, load_yaml


def main(config_path: Path | str = Path("config/tables.yml")) -> None:
    cfg = load_yaml(config_path)
    data = pd.read_parquet(cfg["dataset"])
    out_dir = ensure_dir(cfg.get("output_dir", "tables"))

    # Placeholder aggregation --- to be replaced with actual comparative metrics.
    summary = (
        data.groupby(["species_group", "cover_type", "distribution", "method"])
        ["rss", "chi_square"]
        .sum()
        .reset_index()
    )

    csv_path = out_dir / "method_comparison.csv"
    summary.to_csv(csv_path, index=False)
    print(f"[tables] wrote {csv_path}")


if __name__ == "__main__":
    main()
