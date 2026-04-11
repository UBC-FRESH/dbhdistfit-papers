"""Empirical shape summary and tiered distribution sweep for R2."""

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


def classify_shape(y: np.ndarray) -> str:
    if y.size < 3:
        return "right-peaked/flat"
    smooth = np.convolve(y, [0.25, 0.5, 0.25], mode="same")
    smooth[0] = 0.5 * (y[0] + y[1])
    smooth[-1] = 0.5 * (y[-1] + y[-2])
    peak_idx = int(np.argmax(smooth))
    rel = peak_idx / max(1, (y.size - 1))
    if rel <= 0.2:
        return "inverse-J-ish"
    if rel <= 0.6:
        return "unimodal-mid"
    return "right-peaked/flat"


def fit_metrics_for_group(x: np.ndarray, y: np.ndarray, distributions: list[str]) -> dict[str, object]:
    method_best = {"1sc": np.inf, "1st": np.inf, "2sc": np.inf}
    failures = {"1sc": 0, "1st": 0, "2sc": 0}
    rmse_candidates: list[float] = []
    maxabs_candidates: list[float] = []
    rows: list[dict[str, object]] = []

    for dist in distributions:
        try:
            fits = fit_family(x, y, dist)
        except Exception as exc:
            for method in failures:
                failures[method] += 1
            rows.append({"distribution": dist, "status": f"fit_failed:{type(exc).__name__}"})
            continue

        aicc_1sc = aicc(fits["1sc"])
        aicc_1st = aicc(fits["1st"], delta_k=2)
        aicc_2sc = aicc(fits["2sc"], delta_k=1)

        method_best["1sc"] = min(method_best["1sc"], aicc_1sc)
        method_best["1st"] = min(method_best["1st"], aicc_1st)
        method_best["2sc"] = min(method_best["2sc"], aicc_2sc)

        delta = np.asarray(fits["1st"].best_fit) - np.asarray(fits["2sc"].best_fit)
        rmse_candidates.append(float(np.sqrt(np.mean(delta**2))))
        maxabs_candidates.append(float(np.max(np.abs(delta))))

        rows.append(
            {
                "distribution": dist,
                "status": "ok",
                "aicc_1sc": aicc_1sc,
                "aicc_1st": aicc_1st,
                "aicc_2sc": aicc_2sc,
                "rmse_1st_vs_2sc": rmse_candidates[-1],
                "max_abs_1st_vs_2sc": maxabs_candidates[-1],
            }
        )

    winner = min(method_best, key=method_best.get)
    rmse = float(np.mean(rmse_candidates)) if rmse_candidates else np.nan
    max_abs = float(np.mean(maxabs_candidates)) if maxabs_candidates else np.nan

    return {
        "winner_method": winner,
        "best_aicc_1sc": method_best["1sc"],
        "best_aicc_1st": method_best["1st"],
        "best_aicc_2sc": method_best["2sc"],
        "rmse_1st_vs_2sc": rmse,
        "max_abs_1st_vs_2sc": max_abs,
        "failures_1sc": failures["1sc"],
        "failures_1st": failures["1st"],
        "failures_2sc": failures["2sc"],
        "detail_rows": rows,
    }


def to_latex_table(df: pd.DataFrame, path: Path) -> None:
    if df.empty:
        path.write_text("% empty table\n", encoding="utf-8")
        return
    path.write_text(df.to_latex(index=False, float_format="%.4g"), encoding="utf-8")


def main(tiers_path: Path | str) -> None:
    cfg = load_yaml(tiers_path)
    data = pd.read_parquet(project_path(cfg.get("dataset", "data/processed/truncation_binned.parquet")))
    table_dir = ensure_dir(project_path(cfg.get("output_dir_tables", "tables")))
    fig_dir = ensure_dir(project_path(cfg.get("output_dir_figures", "figures")))

    adapter = build_adapter()
    provenance = adapter.provenance()

    core = list(cfg.get("core", ["weibull", "gamma"]))
    supplemental = list(cfg.get("supplemental", []))

    local_supported = {"weibull", "gamma", "lognormal", "exponential"}
    core_supported = [d for d in core if d in local_supported]

    group_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []

    for (sg, ct), group in data.groupby(["species_group", "cover_type"]):
        g = group.sort_values("dbh_cm")
        x = g["dbh_cm"].to_numpy(dtype=float)
        y = g["relative_frequency"].to_numpy(dtype=float)
        shape_class = classify_shape(y)

        metrics = fit_metrics_for_group(x, y, core_supported)
        group_rows.append(
            {
                "species_group": sg,
                "cover_type": ct,
                "shape_class": shape_class,
                "winner_method": metrics["winner_method"],
                "best_aicc_1sc": metrics["best_aicc_1sc"],
                "best_aicc_1st": metrics["best_aicc_1st"],
                "best_aicc_2sc": metrics["best_aicc_2sc"],
                "rmse_1st_vs_2sc": metrics["rmse_1st_vs_2sc"],
                "max_abs_1st_vs_2sc": metrics["max_abs_1st_vs_2sc"],
                "failures_1sc": metrics["failures_1sc"],
                "failures_1st": metrics["failures_1st"],
                "failures_2sc": metrics["failures_2sc"],
                **provenance,
            }
        )

        for row in metrics["detail_rows"]:
            detail_rows.append({"species_group": sg, "cover_type": ct, "shape_class": shape_class, **row, **provenance})

    group_df = pd.DataFrame(group_rows)
    detail_df = pd.DataFrame(detail_rows)

    shape_summary = (
        group_df.groupby(["shape_class", "winner_method"], as_index=False)
        .size()
        .rename(columns={"size": "win_count"})
    )

    shape_metrics = (
        group_df.groupby("shape_class", as_index=False)
        .agg(
            n_groups=("species_group", "count"),
            mean_rmse_1st_vs_2sc=("rmse_1st_vs_2sc", "mean"),
            mean_max_abs_1st_vs_2sc=("max_abs_1st_vs_2sc", "mean"),
            total_failures_1sc=("failures_1sc", "sum"),
            total_failures_1st=("failures_1st", "sum"),
            total_failures_2sc=("failures_2sc", "sum"),
        )
    )

    supplemental_rows = []
    available = set(adapter.list_distributions())
    for dist in supplemental:
        normalized = dist.lower()
        supplemental_rows.append(
            {
                "distribution": normalized,
                "available_in_adapter": normalized in available,
                "supported_in_pipeline": normalized in local_supported,
                **provenance,
            }
        )
    supplemental_df = pd.DataFrame(supplemental_rows)

    group_df.to_csv(table_dir / "shape_robustness_group_level.csv", index=False)
    detail_df.to_csv(table_dir / "distribution_sweep_core_detail.csv", index=False)
    shape_summary.to_csv(table_dir / "shape_robustness_summary.csv", index=False)
    shape_metrics.to_csv(table_dir / "shape_robustness_metrics.csv", index=False)
    supplemental_df.to_csv(table_dir / "distribution_sweep_supplemental_registry.csv", index=False)

    to_latex_table(shape_summary, table_dir / "shape_robustness_summary.tex")
    to_latex_table(shape_metrics, table_dir / "shape_robustness_metrics.tex")
    to_latex_table(supplemental_df, table_dir / "distribution_sweep_supplemental_registry.tex")

    if not shape_summary.empty:
        pivot = shape_summary.pivot(index="shape_class", columns="winner_method", values="win_count").fillna(0)
        ax = pivot.plot(kind="bar", figsize=(8, 4), rot=20)
        ax.set_xlabel("Shape class")
        ax.set_ylabel("Count of best-method wins")
        ax.set_title("Method wins by empirical shape class (core distributions)")
        plt.tight_layout()
        plt.savefig(fig_dir / "shape_robustness_wins.pdf")
        plt.savefig(fig_dir / "shape_robustness_wins.png", dpi=300)
        plt.close()

    print("[distribution-sweep] wrote shape + tiered sweep artefacts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run R2 empirical shape and distribution sweep")
    parser.add_argument("--tiers", type=Path, default=project_path("config", "distribution_tiers.yml"))
    args = parser.parse_args()
    main(args.tiers)
