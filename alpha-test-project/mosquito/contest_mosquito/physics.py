"""Deterministic trajectory extrapolation baselines."""

from __future__ import annotations

import numpy as np

DT_SECONDS = 0.04
HORIZON_SECONDS = 0.08
TIMES_SECONDS = np.asarray([-0.4, -0.36, -0.32, -0.28, -0.24, -0.2, -0.16, -0.12, -0.08, -0.04, 0.0])


def predict_physics(x: np.ndarray, method: str = "cv_last1", **params: float) -> np.ndarray:
    method = method.lower()
    if method == "last":
        return x[:, -1, :].copy()
    if method.startswith("cv_last"):
        window = int(method.replace("cv_last", "") or 1)
        return constant_velocity(x, window=window)
    if method == "ema_velocity":
        return ema_velocity(x, alpha=float(params.get("alpha", 0.65)))
    if method == "constant_acceleration":
        return constant_acceleration(x)
    if method == "quadratic":
        return polynomial(x, degree=2)
    if method == "blended_cv":
        return blended_cv(x, weight=float(params.get("weight", 0.75)))
    if method == "finite_diff":
        return finite_difference(x, coefficients=params.get("coefficients", (2.49, -0.43, -0.03, -0.05, 0.02)))
    if method.startswith("ca_last_beta"):
        beta = float(params.get("beta", _parse_trailing_float(method, default=0.25)))
        horizon_steps = float(params.get("horizon_steps", HORIZON_SECONDS / DT_SECONDS))
        return constant_acceleration_beta(x, beta=beta, horizon_steps=horizon_steps)
    raise ValueError(f"unknown physics method: {method}")


def constant_velocity(x: np.ndarray, window: int = 1) -> np.ndarray:
    window = max(1, min(int(window), x.shape[1] - 1))
    velocity = (x[:, -1, :] - x[:, -1 - window, :]) / (window * DT_SECONDS)
    return x[:, -1, :] + velocity * HORIZON_SECONDS


def ema_velocity(x: np.ndarray, alpha: float = 0.65) -> np.ndarray:
    diffs = np.diff(x, axis=1) / DT_SECONDS
    weights = np.asarray([(1.0 - alpha) ** i for i in range(diffs.shape[1] - 1, -1, -1)])
    weights = weights / weights.sum()
    velocity = np.einsum("t,ntc->nc", weights, diffs)
    return x[:, -1, :] + velocity * HORIZON_SECONDS


def constant_acceleration(x: np.ndarray) -> np.ndarray:
    velocity_now = (x[:, -1, :] - x[:, -2, :]) / DT_SECONDS
    velocity_prev = (x[:, -2, :] - x[:, -3, :]) / DT_SECONDS
    acceleration = (velocity_now - velocity_prev) / DT_SECONDS
    return x[:, -1, :] + velocity_now * HORIZON_SECONDS + 0.5 * acceleration * HORIZON_SECONDS**2


def polynomial(x: np.ndarray, degree: int = 2) -> np.ndarray:
    degree = max(1, min(int(degree), 3))
    design = np.vstack([TIMES_SECONDS**power for power in range(degree, -1, -1)]).T
    target = np.asarray([0.08**power for power in range(degree, -1, -1)])
    coeff = np.linalg.pinv(design)
    weights = target @ coeff
    return np.einsum("t,ntc->nc", weights, x)


def blended_cv(x: np.ndarray, weight: float = 0.75) -> np.ndarray:
    return weight * constant_velocity(x, window=1) + (1.0 - weight) * ema_velocity(x, alpha=0.55)


def finite_difference(x: np.ndarray, coefficients: tuple[float, ...] | list[float]) -> np.ndarray:
    coeff = np.asarray(coefficients, dtype=float)
    diffs = np.diff(x, axis=1)[:, ::-1, :]
    usable = min(len(coeff), diffs.shape[1])
    return x[:, -1, :] + np.einsum("k,nkc->nc", coeff[:usable], diffs[:, :usable, :])


def constant_acceleration_beta(x: np.ndarray, beta: float = 0.25, horizon_steps: float = 2.0) -> np.ndarray:
    diffs = np.diff(x, axis=1)
    velocity = diffs[:, -1, :]
    acceleration = diffs[:, -1, :] - diffs[:, -2, :]
    return x[:, -1, :] + horizon_steps * velocity + 0.5 * horizon_steps**2 * beta * acceleration


def physics_anchor_bank(x: np.ndarray, horizon_steps: float = 2.0) -> tuple[np.ndarray, list[str]]:
    p0 = x[:, -1, :]
    velocity = np.diff(x, axis=1)
    v_last = velocity[:, -1, :]
    names: list[str] = []
    anchors: list[np.ndarray] = []

    def add(name: str, pred: np.ndarray) -> None:
        names.append(name)
        anchors.append(pred.astype(np.float32))

    add("last", p0)
    for alpha in [0.65, 0.75, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.20, 1.30, 1.45]:
        add(f"cv_alpha_{alpha:.2f}", p0 + horizon_steps * alpha * v_last)

    for window in [2, 3, 4, 5, 7, 10]:
        v_mean = velocity[:, -window:, :].mean(axis=1)
        for alpha in [0.85, 1.00, 1.15]:
            add(f"cv_mean{window}_alpha_{alpha:.2f}", p0 + horizon_steps * alpha * v_mean)

    a_last = velocity[:, -1, :] - velocity[:, -2, :]
    a_prev = velocity[:, -2, :] - velocity[:, -3, :]
    a_smooth = 0.70 * a_last + 0.30 * a_prev
    a_mean3 = (velocity[:, -1, :] - velocity[:, -4, :]) / 3.0
    for source_name, acceleration in {
        "last": a_last,
        "smooth2": a_smooth,
        "mean3": a_mean3,
    }.items():
        for beta in [-0.20, 0.00, 0.10, 0.20, 0.25, 0.35, 0.50, 0.75]:
            add(
                f"ca_{source_name}_beta_{beta:.2f}",
                p0 + horizon_steps * v_last + 0.5 * horizon_steps**2 * beta * acceleration,
            )
        for clip in [0.005, 0.010, 0.020, 0.040]:
            norm = np.linalg.norm(acceleration, axis=-1, keepdims=True).clip(min=1e-6)
            clipped = acceleration * np.minimum(clip / norm, 1.0)
            add(
                f"ca_{source_name}_clip_{clip:.3f}",
                p0 + horizon_steps * v_last + 0.5 * horizon_steps**2 * clipped,
            )

    return np.stack(anchors, axis=1).astype(np.float32), names


def _parse_trailing_float(text: str, default: float) -> float:
    try:
        return float(text.rsplit("_", maxsplit=1)[-1])
    except ValueError:
        return default
