"""Create diagnostic figures comparing truncated-fit methods."""

from __future__ import annotations

import string
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

try:
    from .common import ensure_dir, load_yaml, project_path
    from .fitting import fit_family
except ImportError:  # pragma: no cover
    import sys

    from pathlib import Path as _Path

    sys.path.append(str(_Path(__file__).resolve().parents[1]))
    from scripts.common import ensure_dir, load_yaml, project_path
    from scripts.fitting import fit_family

DEFAULT_CFG = project_path("config", "figures.yml")


def _as_2d(array: np.ndarray) -> np.ndarray:
    """Ensure axes array is 2D for consistent indexing."""
    if array.ndim == 1:
        return array[None, :]
    return array


def main(config_path: Path | str = DEFAULT_CFG) -> None:
    cfg = load_yaml(config_path)
    data_path = project_path(cfg["dataset"])
    data = pd.read_parquet(data_path)
    out_dir = ensure_dir(project_path(cfg.get("output_dir", "figures")))

    styling = cfg.get("styling", {})
    palette = styling.get("palette", "deep")
    dpi = styling.get("dpi", 300)
    row_height = styling.get("row_height", 2.8)
    col_width = styling.get("col_width", 3.2)
    panel_labels = styling.get("panel_labels") or list(string.ascii_lowercase)
    title_size = styling.get("title_size", 9)
    axis_label_size = styling.get("axis_label_size", 8)
    tick_label_size = styling.get("tick_label_size", 7)
    legend_fontsize = styling.get("legend_fontsize", 7)
    panel_offset = tuple(styling.get("panel_offset", (-0.18, 1.02)))
    sns.set(style="whitegrid", palette=palette)

    meta_configs = cfg.get("meta_plots", [])
    if not meta_configs:
        print("[figures] no meta-plot entries specified")
        return

    max_cols = max(len(meta.get("distributions", ["weibull", "gamma"])) for meta in meta_configs)
    combined_fig, combined_axes = plt.subplots(
        nrows=len(meta_configs),
        ncols=max_cols,
        figsize=(col_width * max_cols, row_height * len(meta_configs)),
        sharex=True,
        sharey=True,
    )
    combined_axes = np.array(combined_axes)
    combined_axes = _as_2d(combined_axes)

    label_iter = iter(panel_labels)

    for row_idx, meta in enumerate(meta_configs):
        species = meta["species_group"]
        cover = meta["cover_type"]
        subset = data[(data["species_group"] == species) & (data["cover_type"] == cover)].sort_values("dbh_cm")
        if subset.empty:
            print(f"[figures] no data for {species}-{cover}")
            continue

        distributions = meta.get("distributions", ["weibull", "gamma"])
        x = subset["dbh_cm"].to_numpy()
        y = subset["relative_frequency"].to_numpy()

        fig, axes = plt.subplots(
            1,
            len(distributions),
            figsize=(col_width * len(distributions), row_height),
            sharex=True,
            sharey=True,
        )
        if len(distributions) == 1:
            axes = np.array([axes])

        for col_idx, dist in enumerate(distributions):
            panel_label = next(label_iter, "?")
            fits = fit_family(x, y, dist)

            for ax, annotate in (
                (axes[col_idx], False),
                (combined_axes[row_idx, col_idx], True),
            ):
                ax.plot(
                    x,
                    y,
                    marker="o",
                    markersize=4,
                    markerfacecolor="none",
                    markeredgecolor="black",
                    markeredgewidth=0.8,
                    linestyle="",
                    color="black",
                    label="Empirical",
                )
                ax.plot(x, fits["1sc"].best_fit, linestyle="-", color="C0", label="Complete (1sc)")
                ax.plot(x, fits["1st"].best_fit, linestyle="--", color="C1", label="Truncated (1st)")
                ax.plot(x, fits["2sc"].best_fit, linestyle=":", color="C2", label="Two-stage (2sc)")
                ax.set_xlabel("DBH (cm)", fontsize=axis_label_size)
                ax.set_title(dist.title(), fontsize=title_size)
                ax.grid(True, alpha=0.3)
                ax.tick_params(labelsize=tick_label_size)
                if annotate:
                    ax.annotate(
                        f"({panel_label})",
                        xy=panel_offset,
                        xycoords="axes fraction",
                        va="bottom",
                        ha="left",
                        fontweight="bold",
                        fontsize=axis_label_size,
                    )

        axes[0].set_ylabel("Relative frequency", fontsize=axis_label_size)
        axes[-1].legend(fontsize=legend_fontsize, loc="upper right")
        fig.suptitle(meta.get("title") or f"{species}-{cover}", fontsize=title_size)
        fig.tight_layout()
        filename = out_dir / f"{meta['name']}.pdf"
        fig.savefig(filename, dpi=dpi)
        fig.savefig(filename.with_suffix(".png"), dpi=dpi)
        plt.close(fig)
        print(f"[figures] wrote {filename} and PNG twin")

        # Blank any unused combined axes in this row.
        for extra_idx in range(len(distributions), max_cols):
            combined_axes[row_idx, extra_idx].axis("off")

        combined_axes[row_idx, 0].set_ylabel("Relative frequency", fontsize=axis_label_size)
        combined_axes[row_idx, len(distributions) - 1].legend(fontsize=legend_fontsize, loc="upper right")

    combined_name = cfg.get("combined_name", "diameter_distribution_comparison")
    combined_path = out_dir / f"{combined_name}.pdf"
    # Reduce duplicate tick/axis labels while keeping smaller fonts.
    for ax in combined_axes[:-1, :].flatten():
        if not ax.has_data():
            continue
        ax.set_xlabel("")
        ax.tick_params(labelbottom=False)
    for ax in combined_axes[:, 1:].flatten():
        if not ax.has_data():
            continue
        ax.set_ylabel("")
        ax.tick_params(labelleft=False)
    for ax in combined_axes.flatten():
        if not ax.has_data():
            continue
        ax.tick_params(labelsize=tick_label_size)
    for ax in combined_axes[-1, :].flatten():
        if not ax.has_data():
            continue
        ax.set_xlabel("DBH (cm)", fontsize=axis_label_size)
    for ax in combined_axes[:, 0].flatten():
        if not ax.has_data():
            continue
        ax.set_ylabel("Relative frequency", fontsize=axis_label_size)

    combined_fig.tight_layout(h_pad=1.2, w_pad=0.6)
    combined_fig.savefig(combined_path, dpi=dpi)
    combined_fig.savefig(combined_path.with_suffix(".png"), dpi=dpi)
    plt.close(combined_fig)
    print(f"[figures] wrote combined figure {combined_path} and PNG twin")


if __name__ == "__main__":
    main()
