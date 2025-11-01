"""Create diagnostic figures comparing truncated-fit methods."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
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


def main(config_path: Path | str = DEFAULT_CFG) -> None:
    cfg = load_yaml(config_path)
    data_path = project_path(cfg["dataset"])
    data = pd.read_parquet(data_path)
    out_dir = ensure_dir(project_path(cfg.get("output_dir", "figures")))

    palette = cfg.get("styling", {}).get("palette", "deep")
    dpi = cfg.get("styling", {}).get("dpi", 300)
    sns.set(style="whitegrid", palette=palette)

    for meta in cfg.get("meta_plots", []):
        species = meta["species_group"]
        cover = meta["cover_type"]
        subset = data[(data["species_group"] == species) & (data["cover_type"] == cover)].sort_values("dbh_cm")
        if subset.empty:
            print(f"[figures] no data for {species}-{cover}")
            continue

        distributions = meta.get("distributions", ["weibull", "gamma"])
        ncols = len(distributions)
        fig, axes = plt.subplots(1, ncols, figsize=(3.5 * ncols, 3.2), sharey=True)
        if ncols == 1:
            axes = [axes]

        x = subset["dbh_cm"].to_numpy()
        y = subset["relative_frequency"].to_numpy()

        for ax, dist in zip(axes, distributions):
            fits = fit_family(x, y, dist)
            ax.plot(x, y, marker="o", linestyle="", color="black", label="Empirical")
            ax.plot(x, fits["1sc"].best_fit, linestyle="-", color="C0", label="Complete (1sc)")
            ax.plot(x, fits["1st"].best_fit, linestyle="--", color="C1", label="Truncated (1st)")
            ax.plot(x, fits["2sc"].best_fit, linestyle=":", color="C2", label="Two-stage (2sc)")
            ax.set_xlabel("DBH (cm)")
            ax.set_title(f"{dist.title()}")
            ax.grid(True, alpha=0.3)
        axes[0].set_ylabel("Relative frequency")
        axes[-1].legend(fontsize=8, loc="upper right")
        fig.suptitle(meta.get("title") or f"{species}-{cover}")
        fig.tight_layout()
        filename = out_dir / f"{meta['name']}.pdf"
        fig.savefig(filename, dpi=dpi)
        fig.savefig(filename.with_suffix(".png"), dpi=dpi)
        plt.close(fig)
        print(f"[figures] wrote {filename} and PNG twin")


if __name__ == "__main__":
    main()
