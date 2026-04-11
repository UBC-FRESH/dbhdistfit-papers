"""Fitting utilities for truncated diameter distributions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd
from lmfit import Model

from .distributions import (
    DBH_MAX,
    DBH_MIN,
    exponential_pdf,
    gamma_pdf,
    lognormal_pdf,
    truncated_exponential_pdf,
    truncated_gamma_pdf,
    truncated_lognormal_pdf,
    truncated_weibull_pdf,
    weibull_pdf,
)

FitMap = Dict[str, "Model"]


@dataclass
class FitResults:
    species_group: str
    cover_type: str
    distribution: str
    stage1: Model
    stage2: Model


METHODS = ("1sc", "1st", "2sc")
DISTRIBUTIONS = ("weibull", "gamma")
EXPANDED_DISTRIBUTIONS = ("weibull", "gamma", "lognormal", "exponential")


def _safe_weighted_mean(x: np.ndarray, y: np.ndarray) -> float:
    total = float(np.sum(y))
    if total <= 0:
        return float(np.mean(x))
    return float(np.sum(x * y) / total)


def _safe_weighted_var(x: np.ndarray, y: np.ndarray, mean: float) -> float:
    total = float(np.sum(y))
    if total <= 0:
        return float(np.var(x))
    return float(np.sum(y * (x - mean) ** 2) / total)


def _initial_params(dist: str, x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
    mean = max(_safe_weighted_mean(x, y), 1e-3)
    var = max(_safe_weighted_var(x, y, mean), 1e-3)

    if dist == "weibull":
        a0 = 2.0 if var == 0 else max(0.5, min(5.0, (mean**2 / var) ** 0.5))
        beta0 = max(mean, 1.0)
        return {"a": a0, "beta": beta0}
    if dist == "gamma":
        beta0 = max(var / mean, 0.5) if mean > 0 else 1.0
        p0 = max(mean / beta0, 0.5)
        return {"beta": beta0, "p": p0}
    if dist == "lognormal":
        sigma2 = float(np.log(1.0 + var / (mean**2)))
        mu = float(np.log(mean) - 0.5 * sigma2)
        return {"mu": mu, "sigma2": max(sigma2, 0.05)}
    if dist == "exponential":
        return {"beta": max(mean, 1.0)}
    raise ValueError(f"Unsupported distribution {dist}")


def _build_model(dist: str, method: str):
    if dist == "weibull":
        if method == "1sc":
            def func(x, a, beta):
                return weibull_pdf(x, a, beta, 1.0)
            return Model(func)
        if method == "1st":
            def func(x, a, beta):
                return truncated_weibull_pdf(x, a, beta, DBH_MIN, DBH_MAX)
            return Model(func)
        if method == "2sc":
            def func(x, a, beta, s):
                return weibull_pdf(x, a, beta, s)
            return Model(func)

    if dist == "gamma":
        if method == "1sc":
            def func(x, beta, p):
                return gamma_pdf(x, beta, p, 1.0)
            return Model(func)
        if method == "1st":
            def func(x, beta, p):
                return truncated_gamma_pdf(x, beta, p, DBH_MIN, DBH_MAX)
            return Model(func)
        if method == "2sc":
            def func(x, beta, p, s):
                return gamma_pdf(x, beta, p, s)
            return Model(func)

    if dist == "lognormal":
        if method == "1sc":
            def func(x, mu, sigma2):
                return lognormal_pdf(x, mu, sigma2, 1.0)
            return Model(func)
        if method == "1st":
            def func(x, mu, sigma2):
                return truncated_lognormal_pdf(x, mu, sigma2, DBH_MIN, DBH_MAX)
            return Model(func)
        if method == "2sc":
            def func(x, mu, sigma2, s):
                return lognormal_pdf(x, mu, sigma2, s)
            return Model(func)

    if dist == "exponential":
        if method == "1sc":
            def func(x, beta):
                return exponential_pdf(x, beta, 1.0)
            return Model(func)
        if method == "1st":
            def func(x, beta):
                return truncated_exponential_pdf(x, beta, DBH_MIN, DBH_MAX)
            return Model(func)
        if method == "2sc":
            def func(x, beta, s):
                return exponential_pdf(x, beta, s)
            return Model(func)

    raise ValueError(f"Unsupported combination: {dist} / {method}")


def fit_family(x: np.ndarray, y: np.ndarray, dist: str) -> Dict[str, Model]:
    results = {}
    init = _initial_params(dist, x, y)

    model_1sc = _build_model(dist, "1sc")
    params_1sc = model_1sc.make_params()
    for name, value in init.items():
        params_1sc[name].set(value=value)
        if name in {"a", "beta", "p", "sigma2"}:
            params_1sc[name].min = 1e-6
    res_1sc = model_1sc.fit(y, params_1sc, x=x, nan_policy="omit")
    results["1sc"] = res_1sc

    model_1st = _build_model(dist, "1st")
    params_1st = model_1st.make_params()
    for name, value in init.items():
        params_1st[name].set(value=value)
        if name in {"a", "beta", "p", "sigma2"}:
            params_1st[name].min = 1e-6
    res_1st = model_1st.fit(y, params_1st, x=x, nan_policy="omit")
    results["1st"] = res_1st

    model_2sc = _build_model(dist, "2sc")
    params_2sc = model_2sc.make_params()
    for name, value in init.items():
        params_2sc[name].set(value=value)
        if name in {"a", "beta", "p", "sigma2"}:
            params_2sc[name].min = 1e-6
    params_2sc["s"].set(value=1.0, min=1e-6)
    stage1 = model_2sc.fit(y, params_2sc, x=x, nan_policy="omit")
    params_stage2 = stage1.params.copy()
    params_stage2["s"].vary = False
    stage2 = model_2sc.fit(y, params_stage2, x=x, nan_policy="omit")
    results["2sc"] = stage2
    results["2sc_stage1"] = stage1
    return results


def aicc(result: Model, delta_k: int = 0) -> float:
    n = result.ndata
    k = result.nvarys + 1 + delta_k
    if n <= k + 1:
        return np.inf
    aic = result.aic
    return aic + (2 * k * (k + 1)) / (n - k - 1)


def prepare_meta(data: pd.DataFrame, species_group: str, cover_type: str) -> Tuple[np.ndarray, np.ndarray]:
    subset = data[(data["species_group"] == species_group) & (data["cover_type"] == cover_type)]
    subset = subset.sort_values("dbh_cm")
    return subset["dbh_cm"].to_numpy(), subset["relative_frequency"].to_numpy()


def fit_all_meta_plots(
    data: pd.DataFrame,
    species_groups: Iterable[str],
    cover_types: Iterable[str],
    distributions: Iterable[str] = DISTRIBUTIONS,
) -> Dict[Tuple[str, str], Dict[str, Dict[str, Model]]]:
    results: Dict[Tuple[str, str], Dict[str, Dict[str, Model]]] = {}
    for sg in species_groups:
        for ct in cover_types:
            x, y = prepare_meta(data, sg, ct)
            if len(x) == 0:
                continue
            results[(sg, ct)] = {}
            for dist in distributions:
                try:
                    results[(sg, ct)][dist] = fit_family(x, y, dist)
                except Exception as exc:  # pragma: no cover - diagnostics only
                    print(f"[fit] failed for {sg}-{ct}-{dist}: {exc}")
    return results


def select_best_model(fits: Dict[str, Dict[str, Model]]) -> Tuple[str, Model, Model]:
    best_dist = None
    best_stage2 = None
    best_aicc = np.inf
    for dist, result_dict in fits.items():
        stage2 = result_dict.get("2sc")
        if stage2 is None:
            continue
        score = aicc(stage2, delta_k=1)
        if score < best_aicc:
            best_aicc = score
            best_dist = dist
            best_stage2 = stage2
    if best_dist is None or best_stage2 is None:
        raise ValueError("No successful fits available")
    stage1 = fits[best_dist]["2sc_stage1"]
    return best_dist, stage1, best_stage2
