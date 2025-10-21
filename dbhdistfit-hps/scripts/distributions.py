"""Probability distribution helpers for diameter modelling."""

from __future__ import annotations

import numpy as np
from scipy.special import gamma as gamma_fn


def generalized_gamma_pdf(x: np.ndarray | float, a: float, b: float, p: float, s: float = 1.0) -> np.ndarray:
    """Generalized gamma PDF with optional scale parameter `s`."""
    x = np.asarray(x, dtype=float)
    y = s * (a * np.power(x, a * p - 1.0) * np.exp(-np.power(x / b, a))) / (np.power(b, a * p) * gamma_fn(p))
    return np.nan_to_num(y)


def generalized_gamma_sb_pdf(
    x: np.ndarray | float, a: float, b: float, p: float, s: float, alpha: float
) -> np.ndarray:
    """Size-biased generalized gamma PDF of order `alpha`."""
    return generalized_gamma_pdf(x, a, b, p + alpha / a, s)


def weibull_pdf(x: np.ndarray | float, a: float, b: float, s: float) -> np.ndarray:
    """Weibull PDF via generalized gamma representation."""
    return generalized_gamma_pdf(x, a, b, 1.0, s)


def weibull_sb_pdf(x: np.ndarray | float, a: float, b: float, s: float, alpha: float = 2.0) -> np.ndarray:
    """Size-biased Weibull PDF with order `alpha`."""
    return generalized_gamma_sb_pdf(x, a, b, 1.0, s, alpha)


def gamma_pdf(x: np.ndarray | float, beta: float, p: float, s: float) -> np.ndarray:
    """Gamma PDF via generalized gamma representation."""
    return generalized_gamma_pdf(x, 1.0, beta, p, s)


def gamma_sb_pdf(x: np.ndarray | float, beta: float, p: float, s: float, alpha: float = 2.0) -> np.ndarray:
    """Size-biased Gamma PDF."""
    return generalized_gamma_sb_pdf(x, 1.0, beta, p, s, alpha)
