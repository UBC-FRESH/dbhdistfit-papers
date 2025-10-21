"""Generate manuscript figures comparing control and test methods."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from . import fitting
from .common import (
    compression_factor,
    ensure_dir,
    expansion_factor,
    load_binned_dataset,
    load_yaml,
)


def _prepare_series(df, baf: float = 2.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x = df["dbh_cm"].to_numpy()
    tally = df["tally"].to_numpy()
    if "expansion_factor" in df.columns:
        expansion = df["expansion_factor"].to_numpy()
    else:
        expansion = np.vectorize(expansion_factor)(x, baf=baf)
    compression = 1.0 / expansion
    stand_table = tally * expansion
    return x, tally, stand_table, compression


def render_panel(ax, x, empirical, control_series, test_series, labels, title, style):
    ax.scatter(x, empirical, color="black", s=25, alpha=0.6, label=labels["data"])
    ax.plot(x, control_series, linestyle="--", color=style["line"], label=labels["control"])
    ax.plot(x, test_series, linestyle="-", color=style["line"], label=labels["test"])
    ax.set_title(title)
    ax.set_xlabel("DBH (cm)")
    ax.legend(fontsize=8)


def main(config_path: Path) -> None:
    cfg = load_yaml(config_path)
    output_dir = ensure_dir(cfg.get("output_dir", "figures"))
    palette = cfg.get("styling", {}).get("palette", "muted")
    sns.set(style="whitegrid", palette=palette)

    data = load_binned_dataset(cfg.get("dataset"))
    meta_plots = cfg.get("meta_plots", [])
    distributions = cfg.get("distributions", ["weibull", "gamma"])
    dpi = cfg.get("styling", {}).get("dpi", 300)
    baf = cfg.get("baf", 2.0)

    for meta in meta_plots:
        species = meta["species_group"]
        cover = meta["cover_type"]
        dists = meta.get("distributions", distributions)
        subset = data[(data["species_group"] == species) & (data["cover_type"] == cover)].copy()
        if subset.empty:
            raise ValueError(f"No data for species_group={species}, cover_type={cover}")

        x, tally, stand_table, compression = _prepare_series(subset, baf=baf)

        fig, axes = plt.subplots(
            nrows=len(dists),
            ncols=2,
            figsize=(8, 3 * len(dists)),
            sharex=True,
            constrained_layout=True,
        )
        if len(dists) == 1:
            axes = np.array([axes])

        for row, dist_name in enumerate(dists):
            dispatch: Dict[str, callable] = fitting.method_dispatch(dist_name)
            control = dispatch["control"](x, tally)
            test = dispatch["test"](x, tally)

            control_hps = control.fitted
            control_stand = control_hps / compression
            test_stand = test.fitted
            test_hps = test_stand * compression

            render_panel(
                axes[row][0],
                x,
                tally,
                control_hps,
                test_hps,
                {"data": "HPS tally", "control": "Control (size-biased)", "test": "Test (weighted)"},
                f"{dist_name.title()} – HPS space",
                {"line": sns.color_palette()[0]},
            )
            render_panel(
                axes[row][1],
                x,
                stand_table,
                control_stand,
                test_stand,
                {"data": "Stand table", "control": "Control (projected)", "test": "Test"},
                f"{dist_name.title()} – Stand table space",
                {"line": sns.color_palette()[1 % len(sns.color_palette())]},
            )

        for ax in axes[:, 0]:
            ax.set_ylabel("Counts")

        filename = f"{species}_{cover}_comparison.png"
        fig_path = output_dir / filename
        fig.savefig(fig_path, dpi=dpi)
        plt.close(fig)
        print(f"[figures] saved {fig_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate manuscript figures.")
    parser.add_argument("--config", type=Path, default=Path("config/figures.yml"))
    args = parser.parse_args()
    main(args.config)
