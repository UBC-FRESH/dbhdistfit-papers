"""Optional nemora integration with local fallback distributions."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
from scipy.stats import lognorm

from .distributions import exponential_pdf, gamma_pdf, lognormal_pdf, weibull_pdf

PdfFn = Callable[[np.ndarray, dict[str, float]], np.ndarray]
SampleFn = Callable[[np.random.Generator, int, dict[str, float]], np.ndarray]


@dataclass(frozen=True)
class AdapterDistribution:
    name: str
    pdf: PdfFn
    sampler: SampleFn


def _sample_weibull(rng: np.random.Generator, size: int, params: dict[str, float]) -> np.ndarray:
    a = float(params["a"])
    beta = float(params["beta"])
    return beta * rng.weibull(a, size=size)


def _sample_gamma(rng: np.random.Generator, size: int, params: dict[str, float]) -> np.ndarray:
    beta = float(params["beta"])
    p = float(params["p"])
    return rng.gamma(shape=p, scale=beta, size=size)


def _sample_lognormal(rng: np.random.Generator, size: int, params: dict[str, float]) -> np.ndarray:
    if "sigma2" in params:
        sigma = float(np.sqrt(max(params["sigma2"], 1e-12)))
        mu = float(params["mu"])
    else:
        sigma = float(params["sigma"])
        mu = float(params["mu"])
    return rng.lognormal(mean=mu, sigma=sigma, size=size)


def _sample_exponential(rng: np.random.Generator, size: int, params: dict[str, float]) -> np.ndarray:
    beta = float(params["beta"])
    return rng.exponential(scale=beta, size=size)


def _sample_uniform(rng: np.random.Generator, size: int, params: dict[str, float]) -> np.ndarray:
    low = float(params["low"])
    high = float(params["high"])
    return rng.uniform(low=low, high=high, size=size)


LOCAL_DISTRIBUTIONS: dict[str, AdapterDistribution] = {
    "weibull": AdapterDistribution(
        name="weibull",
        pdf=lambda x, p: weibull_pdf(x, p["a"], p["beta"], p.get("s", 1.0)),
        sampler=_sample_weibull,
    ),
    "gamma": AdapterDistribution(
        name="gamma",
        pdf=lambda x, p: gamma_pdf(x, p["beta"], p["p"], p.get("s", 1.0)),
        sampler=_sample_gamma,
    ),
    "lognormal": AdapterDistribution(
        name="lognormal",
        pdf=lambda x, p: lognormal_pdf(x, p["mu"], p.get("sigma2", p.get("sigma", 0.3) ** 2), p.get("s", 1.0)),
        sampler=_sample_lognormal,
    ),
    "exponential": AdapterDistribution(
        name="exponential",
        pdf=lambda x, p: exponential_pdf(x, p["beta"], p.get("s", 1.0)),
        sampler=_sample_exponential,
    ),
    "uniform": AdapterDistribution(
        name="uniform",
        pdf=lambda x, p: np.where((x >= p["low"]) & (x <= p["high"]), 1.0 / (p["high"] - p["low"]), 0.0),
        sampler=_sample_uniform,
    ),
}


class NemoraAdapter:
    """Expose a stable API regardless of nemora availability."""

    def __init__(self) -> None:
        self.backend = "local"
        self.nemora_version = ""
        self.nemora_commit = ""
        self._nemora_module = None
        self._registry = dict(LOCAL_DISTRIBUTIONS)
        self._load_nemora_if_available()

    def provenance(self) -> dict[str, str]:
        return {
            "backend": self.backend,
            "nemora_version": self.nemora_version,
            "nemora_commit": self.nemora_commit,
        }

    def list_distributions(self) -> list[str]:
        return sorted(self._registry.keys())

    def has_distribution(self, name: str) -> bool:
        return name in self._registry

    def sample(self, name: str, rng: np.random.Generator, size: int, params: dict[str, float]) -> np.ndarray:
        if name not in self._registry:
            raise KeyError(f"Distribution '{name}' is unavailable in adapter registry")
        return self._registry[name].sampler(rng, size, params)

    def pdf(self, name: str, x: np.ndarray, params: dict[str, float]) -> np.ndarray:
        if name not in self._registry:
            raise KeyError(f"Distribution '{name}' is unavailable in adapter registry")
        return self._registry[name].pdf(x, params)

    def _load_nemora_if_available(self) -> None:
        nemora = self._try_import_nemora()
        if nemora is None:
            return

        self.backend = "nemora"
        self._nemora_module = nemora
        self.nemora_version = getattr(nemora, "__version__", "")

        module_file = Path(nemora.__file__).resolve()
        repo_root = module_file.parents[3] if len(module_file.parents) > 3 else module_file.parent
        git_dir = repo_root / ".git"
        if git_dir.exists():
            try:
                self.nemora_commit = (
                    subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True)
                    .strip()
                )
            except Exception:
                self.nemora_commit = ""

        try:
            from nemora.distributions import get_distribution, list_distributions
        except Exception:
            return

        alias = {
            "w": "weibull",
            "ga": "gamma",
            "ln": "lognormal",
            "exp": "exponential",
        }

        for dist_name in list_distributions():
            normalized = alias.get(dist_name, dist_name)
            try:
                dist = get_distribution(dist_name)
            except Exception:
                continue
            if normalized in self._registry:
                continue

            def _pdf_factory(d):
                return lambda x, p: d.pdf(np.asarray(x, dtype=float), p)

            # Use local samplers unless nemora distribution has inverse CDF helpers.
            sampler = LOCAL_DISTRIBUTIONS.get(normalized, LOCAL_DISTRIBUTIONS["gamma"]).sampler
            self._registry[normalized] = AdapterDistribution(normalized, _pdf_factory(dist), sampler)

    def _try_import_nemora(self):
        try:
            return importlib.import_module("nemora")
        except Exception:
            pass

        env_path = os.environ.get("NEMORA_SRC_PATH")
        candidates = []
        if env_path:
            candidates.append(Path(env_path))
        candidates.extend(
            [
                Path("/home/gep/projects/nemora/src"),
                Path(__file__).resolve().parents[3] / "nemora" / "src",
            ]
        )

        for candidate in candidates:
            if candidate.exists() and str(candidate) not in sys.path:
                sys.path.insert(0, str(candidate))
                try:
                    return importlib.import_module("nemora")
                except Exception:
                    continue
        return None


def build_adapter() -> NemoraAdapter:
    return NemoraAdapter()
