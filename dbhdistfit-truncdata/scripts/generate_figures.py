"""Create diagnostic figures comparing truncated-fit methods."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .common import ensure_dir, load_yaml


def main(config_path: Path | str = Path("config/figures.yml")) -> None:
    cfg = load_yaml(config_path)
    data = pd.read_parquet(cfg["dataset"])
    out_dir = ensure_dir(cfg.get("output_dir", "figures"))

    palette = cfg.get("styling", {}).get("palette", "deep")
    sns.set(style="whitegrid", palette=palette)

    for meta in cfg.get("meta_plots", []):
        subset = data[
            (data["species_group"] == meta["species_group"]) &
            (data["cover_type"] == meta["cover_type"])
        ]
        if subset.empty:
            print(f"[figures] no data for {meta}")
            continue

        plt.figure(figsize=(8, 4))
        sns.lineplot(
            data=subset,
            x="dbh_cm",
            y="stand_table",
            hue="method",
            style="distribution",
        )
        plt.title(f"{meta['species_group']} – {meta['cover_type']}")
        plt.xlabel("DBH (cm)")
        plt.ylabel("Stems per hectare")
        filename = out_dir / f"{meta['name']}.png"
        plt.savefig(filename, dpi=cfg.get("styling", {}).get("dpi", 300))
        plt.close()
        print(f"[figures] wrote {filename}")


if __name__ == "__main__":
    main()
