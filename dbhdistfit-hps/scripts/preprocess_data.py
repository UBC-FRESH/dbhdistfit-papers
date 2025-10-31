"""Generate binned meta-plot datasets from the interim PSP inventory pickle."""

from __future__ import annotations

import argparse
import copyreg
import math
import os
from pathlib import Path
from typing import Iterable, Tuple

import numpy as np
import pandas as pd

try:  # Optional dependency
    from datalad import api as datalad_api
except ImportError:  # pragma: no cover - datalad not installed
    datalad_api = None

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "data"
INTERIM_PATH = DATA_ROOT / "interim" / "tiges_final_full.p"
OUTPUT_DIR = DATA_ROOT / "processed"


def _allow_blockmanager_pickle() -> None:
    """Monkey patch copyreg._reconstructor to allow legacy pandas pickles."""

    original = copyreg._reconstructor

    def custom_reconstructor(cls, base, state):  # type: ignore[override]
        if base is object and hasattr(cls, "__new__"):
            obj = cls.__new__(cls)
            if state is not None and hasattr(obj, "__setstate__"):
                obj.__setstate__(state)
            return obj
        return original(cls, base, state)

    copyreg._reconstructor = custom_reconstructor


def ensure_local(path: Path) -> None:
    """Fetch the target path via DataLad if configured and missing."""
    if path.exists() or datalad_api is None:
        return
    try:
        datalad_api.get(str(path))
    except Exception:
        pass


def load_interim_dataframe(path: Path) -> pd.DataFrame:
    """Load the interim PSP dataset from a legacy pickle."""
    ensure_local(path)
    if not path.exists():
        raise FileNotFoundError(f"Interim dataset not found at {path}")

    _allow_blockmanager_pickle()
    with path.open("rb") as handle:
        df = pd.read_pickle(handle)  # type: ignore[arg-type]
    return df.reset_index(drop=True)


def compile_bin_data(
    data: pd.DataFrame,
    bins: Iterable[int] | None = None,
    xmin_mm: int = 90,
    xmax_mm: int = 610,
    width_mm: int = 20,
    expansion_factor_faps: float = 25.0,
    pid_colname: str = "id_pep",
    dbh_colname: str = "dhpmm",
    normed: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """Replicate the binning logic from the original notebook."""
    if bins is None:
        bins = np.arange(xmin_mm, xmax_mm + width_mm, width_mm)

    df = data.reset_index().set_index(pid_colname)
    bin_vals, bin_edges = np.histogram(df[dbh_colname], bins=bins, range=(xmin_mm, xmax_mm))
    bin_vals = bin_vals * expansion_factor_faps  # convert to stems / ha
    bin_centers = (bin_edges[:-1] + (width_mm * 0.5)) * 0.1  # convert mm to cm

    if normed and bin_vals.sum() > 0:
        scale = float(0.1 * width_mm * bin_vals.sum())
        bin_vals = bin_vals * pow(scale, -1)

    return bin_centers, bin_vals


def expansion_factor(dbh_cm: np.ndarray, baf: float = 2.0) -> np.ndarray:
    """Return HPS expansion factor for DBH values (cm)."""
    return baf / (math.pi * (dbh_cm * 0.01 * 0.5) ** 2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate binned PSP meta-plot dataset.")
    parser.add_argument(
        "--input",
        type=Path,
        default=INTERIM_PATH,
        help="Path to interim tiges_final_full.p pickle.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory to write processed datasets.",
    )
    args = parser.parse_args()

    df = load_interim_dataframe(args.input)
    if not {"groupe3", "type_couv", "dhpmm", "id_pep"}.issubset(df.columns):
        raise ValueError("Unexpected dataframe schema in interim dataset.")

    grouped = df.set_index(["groupe3", "type_couv"])
    records = []

    for (species_group, cover_type), subset in grouped.groupby(level=[0, 1]):
        subset = subset.reset_index(level=[0, 1], drop=True)
        xdata, ydata = compile_bin_data(subset)
        for dbh_cm, tally in zip(xdata, ydata):
            if tally <= 0:
                continue
            records.append(
                {
                    "species_group": species_group,
                    "cover_type": cover_type,
                    "dbh_cm": round(float(dbh_cm), 6),
                    "tally": float(tally),
                    "expansion_factor": float(expansion_factor(np.array([dbh_cm]))[0]),
                }
            )

    output_df = pd.DataFrame.from_records(records)
    if output_df.empty:
        raise RuntimeError("Preprocessing produced no records – check input data.")

    counts = output_df.groupby(["species_group", "cover_type"]).size()
    valid_keys = counts[counts >= 3].index
    output_df = (
        output_df.set_index(["species_group", "cover_type"])
        .loc[valid_keys]
        .reset_index()
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = args.output_dir / "binned_meta_plots.parquet"
    csv_path = args.output_dir / "binned_meta_plots.csv"
    for target in (parquet_path, csv_path):
        if target.exists():
            if datalad_api is not None:
                try:
                    datalad_api.unlock(str(target))
                except Exception:
                    pass
            try:
                target.unlink()
            except FileNotFoundError:
                pass
    output_df.to_parquet(parquet_path, index=False)
    output_df.to_csv(csv_path, index=False)

    print(f"[preprocess] wrote {len(output_df)} records to {parquet_path}")


if __name__ == "__main__":
    os.environ.setdefault("PANDAS_ALLOW_BLOCKMANAGER_PICKLE", "1")
    main()
