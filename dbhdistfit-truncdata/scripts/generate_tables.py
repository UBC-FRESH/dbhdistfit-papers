"""Generate parameter comparison tables for the truncated-diameter manuscript."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from .common import ensure_dir, load_yaml, project_path
    from .fitting import aicc, fit_all_meta_plots, select_best_model
except ImportError:  # pragma: no cover
    import sys

    from pathlib import Path as _Path

    sys.path.append(str(_Path(__file__).resolve().parents[1]))
    from scripts.common import ensure_dir, load_yaml, project_path
    from scripts.fitting import aicc, fit_all_meta_plots, select_best_model

CONFIG_DEFAULT = project_path("config", "tables.yml")
OUTPUT_CSV = project_path("tables", "method_comparison.csv")
OUTPUT_JSON = project_path("tables", "method_comparison.json")
OUTPUT_TEX = project_path("tables", "method_comparison.tex")


def format_params(result, exclude_scaling: bool = True) -> str:
    entries = []
    for name, param in result.params.items():
        if exclude_scaling and name == "s":
            continue
        if not param.vary:
            continue
        stderr = param.stderr if param.stderr is not None else 0.0
        entries.append(f"{name} = {param.value:.2f}±{stderr:.2f}")
    return ", ".join(entries)


def fit_distance_metrics(result_a, result_b) -> dict[str, float]:
    delta = result_a.best_fit - result_b.best_fit
    rmse = float((delta ** 2).mean() ** 0.5)
    max_abs = float(abs(delta).max())
    mean_abs = float(abs(delta).mean())
    return {"rmse": rmse, "max_abs": max_abs, "mean_abs": mean_abs}


def main(config_path: Path | str = CONFIG_DEFAULT) -> None:
    cfg = load_yaml(config_path)
    dataset = project_path(cfg["dataset"])
    if not dataset.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset}")

    data = pd.read_parquet(dataset)
    species_groups = sorted(data["species_group"].unique())
    cover_types = sorted(data["cover_type"].unique())

    fits = fit_all_meta_plots(data, species_groups, cover_types)

    rows = []
    summary = {}
    for key, dist_results in fits.items():
        sg, ct = key
        try:
            dist_name, stage1, stage2 = select_best_model(dist_results)
        except ValueError:
            continue
        aicc_1sc = aicc(dist_results[dist_name]["1sc"])
        aicc_1st = aicc(dist_results[dist_name]["1st"], delta_k=2)
        aicc_2sc_stage1 = aicc(stage1)
        aicc_2sc_stage2 = aicc(stage2, delta_k=1)
        distances = fit_distance_metrics(dist_results[dist_name]["1st"], stage2)

        row = {
            "species_group": sg,
            "cover_type": ct,
            "distribution": dist_name,
            "stage1_params": format_params(stage1),
            "stage2_params": format_params(stage2),
            "aicc_1sc": aicc_1sc,
            "aicc_1st": aicc_1st,
            "aicc_2sc_stage1": aicc_2sc_stage1,
            "aicc_2sc_stage2": aicc_2sc_stage2,
            "rmse_1st_vs_2sc": distances["rmse"],
            "max_abs_1st_vs_2sc": distances["max_abs"],
        }
        rows.append(row)
        summary.setdefault(sg, {})[ct] = {
            "distribution": dist_name,
            "stage1": {name: float(param.value) for name, param in stage1.params.items() if name != "s"},
            "stage2": {name: float(param.value) for name, param in stage2.params.items() if name != "s"},
            "aicc_1sc": float(aicc_1sc),
            "aicc_1st": float(aicc_1st),
            "aicc_2sc_stage1": float(aicc_2sc_stage1),
            "aicc_2sc_stage2": float(aicc_2sc_stage2),
            "rmse_1st_vs_2sc": float(distances["rmse"]),
            "max_abs_1st_vs_2sc": float(distances["max_abs"]),
            "mean_abs_1st_vs_2sc": float(distances["mean_abs"]),
        }

    output_dir = ensure_dir(OUTPUT_CSV.parent)
    df = pd.DataFrame(rows)
    df.sort_values(["species_group", "cover_type"], inplace=True)
    df.to_csv(OUTPUT_CSV, index=False)
    latex_df = df.rename(
        columns={
            "species_group": "Species Group",
            "cover_type": "Cover Type",
            "distribution": "Distribution",
            "stage1_params": "Stage 1 Parameters",
            "stage2_params": "Stage 2 Parameters",
            "aicc_1sc": "AICc (1sc)",
            "aicc_1st": "AICc (1st)",
            "aicc_2sc_stage1": "AICc (2sc S1)",
            "aicc_2sc_stage2": "AICc (2sc S2)",
            "rmse_1st_vs_2sc": "RMSE(1st-2sc)",
            "max_abs_1st_vs_2sc": "Max|1st-2sc|",
        }
    )
    float_fmt = {
        "AICc (Stage 2)": "{:.1f}".format,
    }

    latex_table = latex_df.to_latex(
        index=False,
        escape=False,
        longtable=False,
        formatters=float_fmt,
    )
    OUTPUT_TEX.write_text(latex_table)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2))

    print(f"[tables] wrote {OUTPUT_CSV}, {OUTPUT_TEX}, and {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
