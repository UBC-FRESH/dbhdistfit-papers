"""Canonical synthetic robustness experiments for R2."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from .common import ensure_dir, load_yaml, project_path
    from .fitting import aicc, fit_family
    from .nemora_adapter import build_adapter
except ImportError:  # pragma: no cover
    import sys
    from pathlib import Path as _Path

    sys.path.append(str(_Path(__file__).resolve().parents[1]))
    from scripts.common import ensure_dir, load_yaml, project_path
    from scripts.fitting import aicc, fit_family
    from scripts.nemora_adapter import build_adapter


def _binned_relative_frequency(samples: np.ndarray, dbh_min: float, dbh_max: float, bin_width: float) -> tuple[np.ndarray, np.ndarray]:
    edges = np.arange(dbh_min, dbh_max + bin_width, bin_width)
    hist, edges = np.histogram(samples, bins=edges)
    centers = edges[:-1] + 0.5 * bin_width
    area = float(np.sum(hist) * bin_width)
    if area <= 0:
        y = np.zeros_like(centers)
    else:
        y = hist / area
    return centers, y


def _method_winner(scores: dict[str, float]) -> str:
    return min(scores, key=scores.get)


def main(config_path: Path | str) -> None:
    cfg = load_yaml(config_path)
    seed = int(cfg.get("seed", 20260402))
    rng = np.random.default_rng(seed)
    n_replicates = int(cfg.get("n_replicates", 20))
    sample_sizes = list(cfg.get("sample_sizes", [2000]))
    dbh_min = float(cfg.get("dbh_min", 10.0))
    dbh_max = float(cfg.get("dbh_max", 60.0))
    bin_width = float(cfg.get("bin_width_cm", 2.0))

    fit_distributions = [str(x).lower() for x in cfg.get("fit_distributions", ["weibull", "gamma"])]
    supported = {"weibull", "gamma", "lognormal", "exponential"}
    fit_distributions = [d for d in fit_distributions if d in supported]

    table_dir = ensure_dir(project_path(cfg.get("output_dir_tables", "tables")))
    fig_dir = ensure_dir(project_path(cfg.get("output_dir_figures", "figures")))

    adapter = build_adapter()
    provenance = adapter.provenance()

    rows: list[dict[str, object]] = []

    for scenario in cfg.get("scenarios", []):
        scenario_name = scenario["name"]
        scenario_desc = scenario.get("description", "")
        generator = scenario.get("generator", {})
        dist_name = str(generator.get("distribution", "weibull")).lower()
        params = dict(generator.get("params", {}))

        for sample_size in sample_sizes:
            for rep in range(n_replicates):
                draws = adapter.sample(dist_name, rng, int(sample_size), params)
                draws = draws[(draws >= dbh_min) & (draws <= dbh_max)]
                if draws.size < 100:
                    continue

                x, y = _binned_relative_frequency(draws, dbh_min, dbh_max, bin_width)
                method_best = {"1sc": np.inf, "1st": np.inf, "2sc": np.inf}

                for fit_dist in fit_distributions:
                    try:
                        fits = fit_family(x, y, fit_dist)
                    except Exception as exc:
                        rows.append(
                            {
                                "scenario": scenario_name,
                                "scenario_description": scenario_desc,
                                "sample_size": int(sample_size),
                                "replicate": rep,
                                "generator_distribution": dist_name,
                                "fit_distribution": fit_dist,
                                "status": f"fit_failed:{type(exc).__name__}",
                                **provenance,
                            }
                        )
                        continue

                    aicc_1sc = aicc(fits["1sc"])
                    aicc_1st = aicc(fits["1st"], delta_k=2)
                    aicc_2sc = aicc(fits["2sc"], delta_k=1)
                    method_best["1sc"] = min(method_best["1sc"], aicc_1sc)
                    method_best["1st"] = min(method_best["1st"], aicc_1st)
                    method_best["2sc"] = min(method_best["2sc"], aicc_2sc)

                    delta = np.asarray(fits["1st"].best_fit) - np.asarray(fits["2sc"].best_fit)
                    rmse = float(np.sqrt(np.mean(delta**2)))
                    max_abs = float(np.max(np.abs(delta)))

                    rows.append(
                        {
                            "scenario": scenario_name,
                            "scenario_description": scenario_desc,
                            "sample_size": int(sample_size),
                            "replicate": rep,
                            "generator_distribution": dist_name,
                            "fit_distribution": fit_dist,
                            "status": "ok",
                            "aicc_1sc": aicc_1sc,
                            "aicc_1st": aicc_1st,
                            "aicc_2sc": aicc_2sc,
                            "rmse_1st_vs_2sc": rmse,
                            "max_abs_1st_vs_2sc": max_abs,
                            **provenance,
                        }
                    )

                rows.append(
                    {
                        "scenario": scenario_name,
                        "scenario_description": scenario_desc,
                        "sample_size": int(sample_size),
                        "replicate": rep,
                        "generator_distribution": dist_name,
                        "fit_distribution": "__winner__",
                        "status": "winner",
                        "winner_method": _method_winner(method_best),
                        "best_aicc_1sc": method_best["1sc"],
                        "best_aicc_1st": method_best["1st"],
                        "best_aicc_2sc": method_best["2sc"],
                        **provenance,
                    }
                )

    df = pd.DataFrame(rows)
    df.to_csv(table_dir / "simulation_robustness.csv", index=False)

    winners = df[(df["status"] == "winner") & (df["fit_distribution"] == "__winner__")].copy()
    win_summary = (
        winners.groupby(["scenario", "sample_size", "winner_method"], as_index=False)
        .size()
        .rename(columns={"size": "win_count"})
    )
    win_summary.to_csv(table_dir / "simulation_robustness_wins.csv", index=False)

    metrics = df[df["status"] == "ok"].groupby(["scenario", "sample_size"], as_index=False).agg(
        mean_rmse_1st_vs_2sc=("rmse_1st_vs_2sc", "mean"),
        mean_max_abs_1st_vs_2sc=("max_abs_1st_vs_2sc", "mean"),
        mean_aicc_1sc=("aicc_1sc", "mean"),
        mean_aicc_1st=("aicc_1st", "mean"),
        mean_aicc_2sc=("aicc_2sc", "mean"),
    )
    metrics.to_csv(table_dir / "simulation_robustness_metrics.csv", index=False)

    combined = win_summary.merge(metrics, on=["scenario", "sample_size"], how="left")
    combined.to_latex(table_dir / "simulation_robustness.tex", index=False, float_format="%.4g")

    if not win_summary.empty:
        fig, axes = plt.subplots(1, len(sample_sizes), figsize=(4.5 * len(sample_sizes), 4), sharey=True)
        if len(sample_sizes) == 1:
            axes = [axes]
        for ax, ss in zip(axes, sample_sizes):
            subset = win_summary[win_summary["sample_size"] == ss]
            pivot = subset.pivot(index="scenario", columns="winner_method", values="win_count").fillna(0)
            pivot.plot(kind="bar", ax=ax, rot=20)
            ax.set_title(f"Sample size = {ss}")
            ax.set_xlabel("Scenario")
            ax.set_ylabel("Winner count")
        plt.tight_layout()
        plt.savefig(fig_dir / "simulation_robustness.pdf")
        plt.savefig(fig_dir / "simulation_robustness.png", dpi=300)
        plt.close()

    print("[simulations] wrote simulation robustness artefacts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run canonical synthetic simulation robustness checks")
    parser.add_argument("--config", type=Path, default=project_path("config", "simulations.yml"))
    args = parser.parse_args()
    main(args.config)
