"""Fitting utilities comparing size-biased and weighted methods."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Tuple

import numpy as np
from scipy.optimize import curve_fit

from .common import expansion_factor, compression_factor
from . import distributions as dist


Pdf = Callable[..., np.ndarray]


@dataclass
class FitResult:
    params: np.ndarray
    covariance: np.ndarray
    rss: float
    fitted: np.ndarray


def _fit_curve(x: np.ndarray, y: np.ndarray, pdf: Pdf, p0: Tuple[float, ...], **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    params, cov = curve_fit(pdf, x, y, p0=p0, maxfev=200000, **kwargs)
    fitted = pdf(x, *params)
    return params, cov, fitted


def fit_control_weibull(x: np.ndarray, tally: np.ndarray, alpha: float = 2.0) -> FitResult:
    """Fit the reference (size-biased) Weibull PDF to HPS tally data."""
    pdf = lambda x, a, b, s: dist.weibull_sb_pdf(x, a, b, s, alpha=alpha)
    params, cov, fitted = _fit_curve(x, tally, pdf, p0=(2.0, 20.0, tally.max()))
    rss = float(np.sum((tally - fitted) ** 2))
    return FitResult(params=params, covariance=cov, rss=rss, fitted=fitted)


def fit_control_gamma(x: np.ndarray, tally: np.ndarray, alpha: float = 2.0) -> FitResult:
    """Fit the reference (size-biased) Gamma PDF to HPS tally data."""
    pdf = lambda x, beta, p, s: dist.gamma_sb_pdf(x, beta, p, s, alpha=alpha)
    params, cov, fitted = _fit_curve(x, tally, pdf, p0=(15.0, 3.0, tally.max()))
    rss = float(np.sum((tally - fitted) ** 2))
    return FitResult(params=params, covariance=cov, rss=rss, fitted=fitted)


def fit_test_weibull(x: np.ndarray, tally: np.ndarray, baf: float = 2.0) -> FitResult:
    """Fit the alternative weighted Weibull PDF on expanded HPS stand table data."""
    stand_table = tally * np.vectorize(expansion_factor)(x, baf=baf)
    weights = np.vectorize(compression_factor)(x, baf=baf)
    pdf = lambda x, a, b, s: dist.weibull_pdf(x, a, b, s)
    params, cov, fitted = _fit_curve(
        x,
        stand_table,
        pdf,
        p0=(2.0, 20.0, stand_table.max()),
        sigma=weights,
        absolute_sigma=False,
    )
    rss = float(np.sum((stand_table - fitted) ** 2))
    return FitResult(params=params, covariance=cov, rss=rss, fitted=fitted)


def fit_test_gamma(x: np.ndarray, tally: np.ndarray, baf: float = 2.0) -> FitResult:
    """Fit the alternative weighted Gamma PDF on expanded HPS stand table data."""
    stand_table = tally * np.vectorize(expansion_factor)(x, baf=baf)
    weights = np.vectorize(compression_factor)(x, baf=baf)
    pdf = lambda x, beta, p, s: dist.gamma_pdf(x, beta, p, s)
    params, cov, fitted = _fit_curve(
        x,
        stand_table,
        pdf,
        p0=(15.0, 3.0, stand_table.max()),
        sigma=weights,
        absolute_sigma=False,
    )
    rss = float(np.sum((stand_table - fitted) ** 2))
    return FitResult(params=params, covariance=cov, rss=rss, fitted=fitted)


def method_dispatch(distribution: str) -> Dict[str, Callable]:
    """Return fitting functions for control/test pairing by distribution name."""
    distribution = distribution.lower()
    if distribution.startswith("w"):
        return {"control": fit_control_weibull, "test": fit_test_weibull}
    if distribution.startswith("g"):
        return {"control": fit_control_gamma, "test": fit_test_gamma}
    raise ValueError(f"Unsupported distribution '{distribution}'.")
