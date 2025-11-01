"""Probability distribution helpers for truncated-diameter modelling."""

from __future__ import annotations

import numpy as np
from scipy.integrate import quad
from scipy.special import gamma as gamma_fn

DBH_MIN = 10.0
DBH_MAX = 60.0


def _to_numpy(x: np.ndarray | float) -> np.ndarray:
    return np.asarray(x, dtype=float)


def weibull_pdf(x: np.ndarray | float, a: float, beta: float, s: float = 1.0) -> np.ndarray:
    x = _to_numpy(x)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        y = s * (a * np.power(x, a - 1.0) * np.exp(-np.power(x / beta, a))) / np.power(beta, a)
    return np.nan_to_num(y)


def gamma_pdf(x: np.ndarray | float, beta: float, p: float, s: float = 1.0) -> np.ndarray:
    x = _to_numpy(x)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        y = s * (np.power(x, p - 1.0) * np.exp(-x / beta)) / (np.power(beta, p) * gamma_fn(p))
    return np.nan_to_num(y)


def truncated_weibull_pdf(x: np.ndarray | float, a: float, beta: float,
                          xmin: float = DBH_MIN, xmax: float = DBH_MAX) -> np.ndarray:
    norm = quad(lambda t: weibull_pdf(t, a, beta, 1.0), xmin, xmax, limit=200)[0]
    if norm == 0:
        return np.zeros_like(_to_numpy(x))
    base = weibull_pdf(x, a, beta, 1.0)
    x = _to_numpy(x)
    mask = (x >= xmin) & (x <= xmax)
    out = np.zeros_like(x)
    out[mask] = base[mask] / norm
    return out


def truncated_gamma_pdf(x: np.ndarray | float, beta: float, p: float,
                        xmin: float = DBH_MIN, xmax: float = DBH_MAX) -> np.ndarray:
    norm = quad(lambda t: gamma_pdf(t, beta, p, 1.0), xmin, xmax, limit=200)[0]
    if norm == 0:
        return np.zeros_like(_to_numpy(x))
    base = gamma_pdf(x, beta, p, 1.0)
    x = _to_numpy(x)
    mask = (x >= xmin) & (x <= xmax)
    out = np.zeros_like(x)
    out[mask] = base[mask] / norm
    return out
