"""Classical model training routines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from contest_mosquito.features import make_features
from contest_mosquito.metrics import metric_summary
from contest_mosquito.physics import predict_physics


@dataclass
class ExperimentResult:
    oof_pred: np.ndarray
    test_pred: np.ndarray
    metrics: dict[str, float]
    fold_rows: list[dict[str, Any]]
    model_label: str


def evaluate_bucketed_finite_difference(
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    cv_splits: int,
    seed: int,
    n_speed_bins: int = 3,
    n_curvature_bins: int = 1,
    coefficient_count: int = 3,
    maxiter: int = 35,
) -> ExperimentResult:
    from scipy.optimize import differential_evolution

    train_diffs = np.diff(train_x, axis=1)[:, ::-1, :]
    test_diffs = np.diff(test_x, axis=1)[:, ::-1, :]
    train_last = train_x[:, -1, :]
    test_last = test_x[:, -1, :]
    train_speed, train_curvature = _motion_bucket_features(train_diffs)
    test_speed, test_curvature = _motion_bucket_features(test_diffs)
    kf = KFold(n_splits=cv_splits, shuffle=True, random_state=seed)
    oof_pred = np.zeros_like(train_y, dtype=np.float32)
    fold_rows: list[dict[str, float | int]] = []

    def predict(last: np.ndarray, diffs: np.ndarray, coefficients: np.ndarray) -> np.ndarray:
        count = min(len(coefficients), diffs.shape[1])
        return last + np.einsum("k,nkc->nc", coefficients[:count], diffs[:, :count, :])

    def fit_coefficients(indices: np.ndarray, fold_seed: int) -> np.ndarray:
        def objective(coefficients: np.ndarray) -> float:
            pred = predict(train_last[indices], train_diffs[indices], coefficients)
            return -metric_summary(pred, train_y[indices], prefix="val")["val/r_hit@1cm"]

        result = differential_evolution(
            objective,
            [(-2.0, 4.0)] * coefficient_count,
            seed=fold_seed,
            maxiter=maxiter,
            popsize=10,
            polish=False,
            tol=1e-4,
            workers=1,
        )
        return np.asarray(result.x, dtype=np.float32)

    final_coefficients: dict[tuple[int, int], np.ndarray] = {}
    for fold, (fit_idx, val_idx) in enumerate(kf.split(train_x)):
        speed_edges = _quantile_edges(train_speed[fit_idx], n_speed_bins)
        curvature_edges = _quantile_edges(train_curvature[fit_idx], n_curvature_bins)
        fit_speed_bins = np.digitize(train_speed[fit_idx], speed_edges)
        fit_curvature_bins = np.digitize(train_curvature[fit_idx], curvature_edges)
        val_speed_bins = np.digitize(train_speed[val_idx], speed_edges)
        val_curvature_bins = np.digitize(train_curvature[val_idx], curvature_edges)
        fallback = fit_coefficients(fit_idx, seed + fold * 1000)
        for speed_bin in range(n_speed_bins):
            for curvature_bin in range(n_curvature_bins):
                local_fit = fit_idx[
                    (fit_speed_bins == speed_bin) & (fit_curvature_bins == curvature_bin)
                ]
                local_val_mask = (val_speed_bins == speed_bin) & (
                    val_curvature_bins == curvature_bin
                )
                if not np.any(local_val_mask):
                    continue
                coefficients = (
                    fit_coefficients(local_fit, seed + fold * 1000 + speed_bin * 100 + curvature_bin)
                    if len(local_fit) >= 100
                    else fallback
                )
                val_local = val_idx[local_val_mask]
                oof_pred[val_local] = predict(
                    train_last[val_local],
                    train_diffs[val_local],
                    coefficients,
                ).astype(np.float32)
        fold_rows.append({"fold": fold, **metric_summary(oof_pred[val_idx], train_y[val_idx], prefix="val")})

    full_speed_edges = _quantile_edges(train_speed, n_speed_bins)
    full_curvature_edges = _quantile_edges(train_curvature, n_curvature_bins)
    full_speed_bins = np.digitize(train_speed, full_speed_edges)
    full_curvature_bins = np.digitize(train_curvature, full_curvature_edges)
    fallback = fit_coefficients(np.arange(len(train_x)), seed + 9000)
    for speed_bin in range(n_speed_bins):
        for curvature_bin in range(n_curvature_bins):
            local = np.flatnonzero(
                (full_speed_bins == speed_bin) & (full_curvature_bins == curvature_bin)
            )
            final_coefficients[(speed_bin, curvature_bin)] = (
                fit_coefficients(local, seed + 10_000 + speed_bin * 100 + curvature_bin)
                if len(local) >= 100
                else fallback
            )
    test_speed_bins = np.digitize(test_speed, full_speed_edges)
    test_curvature_bins = np.digitize(test_curvature, full_curvature_edges)
    test_pred = np.zeros((len(test_x), 3), dtype=np.float32)
    for speed_bin in range(n_speed_bins):
        for curvature_bin in range(n_curvature_bins):
            mask = (test_speed_bins == speed_bin) & (test_curvature_bins == curvature_bin)
            if not np.any(mask):
                continue
            test_pred[mask] = predict(
                test_last[mask],
                test_diffs[mask],
                final_coefficients[(speed_bin, curvature_bin)],
            ).astype(np.float32)

    metrics = metric_summary(oof_pred, train_y, prefix="val")
    metrics["val/fold_min_r_hit"] = float(min(row["val/r_hit@1cm"] for row in fold_rows))
    return ExperimentResult(
        oof_pred=oof_pred,
        test_pred=test_pred,
        metrics=metrics,
        fold_rows=fold_rows,
        model_label="physics:bucketed_finite_diff",
    )


def evaluate_physics(
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    method: str,
    params: dict[str, Any] | None = None,
) -> ExperimentResult:
    params = params or {}
    oof_pred = predict_physics(train_x, method, **params)
    test_pred = predict_physics(test_x, method, **params)
    metrics = metric_summary(oof_pred, train_y, prefix="val")
    return ExperimentResult(
        oof_pred=oof_pred,
        test_pred=test_pred,
        metrics=metrics,
        fold_rows=[{"fold": -1, **metrics}],
        model_label=f"physics:{method}",
    )


def evaluate_residual_model(
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    base_method: str,
    cv_splits: int,
    seed: int,
    model_kind: str = "lightgbm",
    model_params: dict[str, Any] | None = None,
) -> ExperimentResult:
    model_params = model_params or {}
    features = make_features(train_x, base_method=base_method)
    test_features = make_features(test_x, base_method=base_method)
    base_train = predict_physics(train_x, base_method)
    base_test = predict_physics(test_x, base_method)
    residual = train_y - base_train
    oof_pred = np.zeros_like(train_y, dtype=np.float32)
    fold_rows: list[dict[str, float | int]] = []
    splitter = KFold(n_splits=cv_splits, shuffle=True, random_state=seed)
    estimator = _make_estimator(model_kind, model_params, seed)

    for fold, (train_idx, val_idx) in enumerate(splitter.split(features)):
        model = clone(estimator)
        model.fit(features[train_idx], residual[train_idx])
        fold_pred = base_train[val_idx] + model.predict(features[val_idx])
        oof_pred[val_idx] = fold_pred.astype(np.float32)
        row = {"fold": fold, **metric_summary(fold_pred, train_y[val_idx], prefix="val")}
        fold_rows.append(row)

    full_model = clone(estimator)
    full_model.fit(features, residual)
    test_pred = base_test + full_model.predict(test_features)
    metrics = metric_summary(oof_pred, train_y, prefix="val")
    metrics["val/fold_min_r_hit"] = float(min(row["val/r_hit@1cm"] for row in fold_rows))
    return ExperimentResult(
        oof_pred=oof_pred,
        test_pred=test_pred.astype(np.float32),
        metrics=metrics,
        fold_rows=fold_rows,
        model_label=f"residual:{model_kind}:{base_method}",
    )


def _make_estimator(model_kind: str, params: dict[str, Any], seed: int):
    model_kind = model_kind.lower()
    if model_kind == "lightgbm":
        try:
            from lightgbm import LGBMRegressor

            defaults: dict[str, Any] = {
                "n_estimators": 900,
                "learning_rate": 0.025,
                "num_leaves": 31,
                "subsample": 0.9,
                "colsample_bytree": 0.9,
                "reg_alpha": 0.0,
                "reg_lambda": 0.2,
                "objective": "regression",
                "random_state": seed,
                "n_jobs": -1,
                "verbosity": -1,
            }
            defaults.update(params)
            return MultiOutputRegressor(LGBMRegressor(**defaults))
        except Exception:
            model_kind = "hist_gradient_boosting"
    if model_kind == "extra_trees":
        defaults = {"n_estimators": 500, "random_state": seed, "n_jobs": -1, "min_samples_leaf": 2}
        defaults.update(params)
        return ExtraTreesRegressor(**defaults)
    if model_kind == "knn":
        defaults = {"n_neighbors": 80, "weights": "distance", "p": 2, "n_jobs": -1}
        defaults.update(params)
        return make_pipeline(StandardScaler(), KNeighborsRegressor(**defaults))
    if model_kind == "ridge":
        defaults = {"alpha": 0.0001}
        defaults.update(params)
        return make_pipeline(StandardScaler(), Ridge(**defaults))
    defaults = {
        "max_iter": 500,
        "learning_rate": 0.035,
        "max_leaf_nodes": 31,
        "l2_regularization": 0.05,
        "random_state": seed,
    }
    defaults.update(params)
    return MultiOutputRegressor(HistGradientBoostingRegressor(**defaults))


def _motion_bucket_features(diffs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    speed = np.linalg.norm(diffs[:, 0, :], axis=1)
    curvature = np.linalg.norm(diffs[:, 0, :] - diffs[:, 1, :], axis=1) / (speed + 1e-6)
    return speed, curvature


def _quantile_edges(values: np.ndarray, bins: int) -> np.ndarray:
    if bins <= 1:
        return np.asarray([])
    edges = np.quantile(values, np.linspace(0.0, 1.0, bins + 1)[1:-1])
    return np.unique(edges)
