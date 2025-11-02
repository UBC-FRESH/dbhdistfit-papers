"""Prepare fixed-area PSP tally data for truncated-distribution fitting."""

from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from pandas.compat import pickle_compat

try:
    from .common import ensure_dir, project_path
except ImportError:  # pragma: no cover - allow execution as a script
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.common import ensure_dir, project_path

LEGACY_PICKLE_ENV = "DBHDISTFIT_TRUNCDATA_PICKLE"
LEGACY_PICKLE_PATH = project_path("..", "pspdistfit", "dat", "misc", "tiges_final_full.p")
OUTPUT_PARQUET = project_path("data", "processed", "truncation_binned.parquet")
OUTPUT_DIR = OUTPUT_PARQUET.parent

# Fixed-area permanent sample plot size: 0.04 ha (400 m²)
PLOT_AREA_HA = 0.04
PLOT_EXPANSION_FACTOR = 1.0 / PLOT_AREA_HA  # 25 stems/plot -> stems per hectare
DBH_MIN = 10.0
DBH_MAX = 60.0
BIN_WIDTH_CM = 2.0
BIN_WIDTH_MM = int(BIN_WIDTH_CM * 10)
BIN_EDGES_MM = np.arange(int(DBH_MIN * 10) - BIN_WIDTH_MM // 2, int(DBH_MAX * 10) + BIN_WIDTH_MM, BIN_WIDTH_MM)


def _patch_legacy_blockmanager() -> None:
    """Allow pandas to load legacy BlockManager pickles under 2.x."""
    if getattr(pickle_compat, "_legacy_blockmanager_patch", False):
        return

    original = pickle_compat.load_reduce

    def _load_reduce(self):  # type: ignore[override]
        stack = self.stack
        args = stack.pop()
        func = stack[-1]
        try:
            stack[-1] = func(*args)
            return
        except TypeError:
            if args and isinstance(args[0], type) and args[0].__name__ in {"BlockManager", "SingleBlockManager"}:
                cls = args[0]
                stack[-1] = cls.__new__(cls)
                return
        return original(self)

    pickle_compat.load_reduce = _load_reduce
    pickle_compat.Unpickler.dispatch[pickle.REDUCE[0]] = _load_reduce
    pickle_compat._legacy_blockmanager_patch = True


def _resolve_legacy_path() -> Path:
    """Return the path to the legacy PSP pickle, honouring overrides."""
    candidate = os.environ.get(LEGACY_PICKLE_ENV)
    return Path(candidate) if candidate else Path(LEGACY_PICKLE_PATH)


def load_legacy_dataframe(path: Path) -> pd.DataFrame:
    """Load the archived PSP tally dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Legacy PSP pickle not found at {path}. "
            "Set DBHDISTFIT_TRUNCDATA_PICKLE to override the location."
        )
    _patch_legacy_blockmanager()
    with path.open("rb") as handle:
        df = pickle_compat.load(handle, encoding="latin1")
    return df.reset_index(drop=True)


def compile_bin_data(subset: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Aggregate DBH counts into fixed-width classes."""
    counts, edges = np.histogram(subset["dhpmm"], bins=BIN_EDGES_MM)
    tallies = counts.astype(float) * PLOT_EXPANSION_FACTOR
    centers = (edges[:-1] + (BIN_WIDTH_MM * 0.5)) * 0.1  # convert mm to cm
    return centers, tallies


def bin_legacy_psp(data: pd.DataFrame) -> pd.DataFrame:
    """Bin the legacy PSP tallies by species group and cover type."""
    required = {"groupe3", "type_couv", "dhpmm", "id_pep"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Legacy dataframe missing columns: {', '.join(sorted(missing))}")

    subset = data[list(required)].dropna()
    subset = subset.rename(columns={"groupe3": "species_group", "type_couv": "cover_type"})
    lower_mm = int(DBH_MIN * 10) - BIN_WIDTH_MM // 2
    upper_mm = int(DBH_MAX * 10) + BIN_WIDTH_MM // 2
    subset = subset[(subset["dhpmm"] >= lower_mm) & (subset["dhpmm"] <= upper_mm)]

    records = []
    for (species_group, cover_type), group in subset.groupby(["species_group", "cover_type"]):
        centers, tallies = compile_bin_data(group)
        for dbh_cm, tally in zip(centers, tallies):
            if tally <= 0 or not (DBH_MIN <= dbh_cm <= DBH_MAX):
                continue
            records.append(
                {
                    "species_group": species_group,
                    "cover_type": cover_type,
                    "dbh_cm": float(dbh_cm),
                    "tally": float(tally),
                }
            )

    output = pd.DataFrame.from_records(records)
    if output.empty:
        raise RuntimeError("Binning PSP tallies produced no data.")

    counts = output.groupby(["species_group", "cover_type"]).size()
    valid = counts[counts >= 3].index
    output = (
        output.set_index(["species_group", "cover_type"])
        .loc[valid]
        .reset_index()
        .sort_values(["species_group", "cover_type", "dbh_cm"])
        .reset_index(drop=True)
    )
    return output


def compute_relative_frequency(group: pd.DataFrame) -> pd.DataFrame:
    """Add relative-frequency column so areas integrate to 1."""
    group = group.sort_values("dbh_cm").copy()
    bin_edges = np.sort(group["dbh_cm"].unique())
    if len(bin_edges) > 1:
        bin_width = np.diff(bin_edges).min()
    else:
        bin_width = BIN_WIDTH_CM
    total = (group["stand_table"] * bin_width).sum()
    if total > 0:
        group["relative_frequency"] = group["stand_table"] / total
    else:
        group["relative_frequency"] = 0.0
    group["bin_width_cm"] = bin_width
    return group


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    legacy_path = _resolve_legacy_path()
    legacy_df = load_legacy_dataframe(legacy_path)
    raw = bin_legacy_psp(legacy_df)

    processed = raw.copy()
    processed["stand_table"] = processed["tally"] * PLOT_EXPANSION_FACTOR
    totals = processed.groupby(["species_group", "cover_type"])["stand_table"].transform("sum")
    processed["relative_frequency"] = processed["stand_table"] / (totals * BIN_WIDTH_CM)
    processed["bin_width_cm"] = BIN_WIDTH_CM

    ensure_dir(OUTPUT_DIR)
    processed.to_parquet(OUTPUT_PARQUET, index=False)
    processed.to_csv(OUTPUT_PARQUET.with_suffix(".csv"), index=False)
    print(f"[preprocess] wrote {OUTPUT_PARQUET} (and CSV twin)")


if __name__ == "__main__":
    main()
