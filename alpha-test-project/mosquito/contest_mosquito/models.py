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
    fold_rows: list[dict[str, float | int]]
    model_label: str


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
