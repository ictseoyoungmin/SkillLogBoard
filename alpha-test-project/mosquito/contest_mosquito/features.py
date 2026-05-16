"""Feature builders for residual trajectory models."""

from __future__ import annotations

import numpy as np

from contest_mosquito.physics import predict_physics


def make_features(x: np.ndarray, base_method: str = "cv_last1") -> np.ndarray:
    last = x[:, -1, :]
    centered = (x - last[:, None, :]).reshape(x.shape[0], -1)
    diffs = np.diff(x, axis=1)
    acc = np.diff(diffs, axis=1)
    speed = np.linalg.norm(diffs, axis=2)
    accel_norm = np.linalg.norm(acc, axis=2)
    base = predict_physics(x, base_method)
    candidates = [
        predict_physics(x, "cv_last1"),
        predict_physics(x, "cv_last2"),
        predict_physics(x, "cv_last3"),
        predict_physics(x, "ema_velocity", alpha=0.65),
        predict_physics(x, "constant_acceleration"),
        predict_physics(x, "quadratic"),
    ]
    candidate_stack = np.stack(candidates, axis=1)
    candidate_offsets = (candidate_stack - base[:, None, :]).reshape(x.shape[0], -1)
    return np.concatenate(
        [
            x.reshape(x.shape[0], -1),
            centered,
            diffs.reshape(x.shape[0], -1),
            acc.reshape(x.shape[0], -1),
            speed,
            accel_norm,
            last,
            base,
            base - last,
            candidate_offsets,
            np.mean(diffs, axis=1),
            np.std(diffs, axis=1),
            np.max(np.abs(diffs), axis=1),
        ],
        axis=1,
    ).astype(np.float32)
