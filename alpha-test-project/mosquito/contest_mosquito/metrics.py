"""Contest metrics."""

from __future__ import annotations

import numpy as np

R_HIT_METERS = 0.01


def distance_errors(pred: np.ndarray, true: np.ndarray) -> np.ndarray:
    return np.linalg.norm(np.asarray(pred, dtype=float) - np.asarray(true, dtype=float), axis=-1)


def r_hit(pred: np.ndarray, true: np.ndarray, radius: float = R_HIT_METERS) -> float:
    return float(np.mean(distance_errors(pred, true) <= radius))


def metric_summary(pred: np.ndarray, true: np.ndarray, prefix: str = "val") -> dict[str, float]:
    distances = distance_errors(pred, true)
    return {
        f"{prefix}/r_hit@1cm": r_hit(pred, true),
        f"{prefix}/mean_dist": float(np.mean(distances)),
        f"{prefix}/median_dist": float(np.median(distances)),
        f"{prefix}/p90_dist": float(np.percentile(distances, 90)),
        f"{prefix}/p95_dist": float(np.percentile(distances, 95)),
    }
