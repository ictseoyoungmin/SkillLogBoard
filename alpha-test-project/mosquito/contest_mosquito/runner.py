"""CLI runner for mosquito contest experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import json
import time

import numpy as np
import pandas as pd
import yaml

from skilllogboard import RunLogger

from contest_mosquito.backlog import append_feedback, write_experiment_backlog
from contest_mosquito.data import load_contest_data, write_submission
from contest_mosquito.ensemble import run_optional_ensemble
from contest_mosquito.jepa import evaluate_jepa_torch
from contest_mosquito.models import evaluate_physics, evaluate_residual_model


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--make-submission", action="store_true")
    parser.add_argument("--refresh-cache", action="store_true")
    parser.add_argument("--limit-train", type=int)
    parser.add_argument("--limit-test", type=int)
    args = parser.parse_args(argv)
    config = _load_config(args.config)
    return run_experiment(config, args)


def run_experiment(config: dict[str, Any], args: argparse.Namespace) -> int:
    start = time.perf_counter()
    paths = config.get("paths", {})
    config_dir = Path(config.get("__config_dir__", "."))
    data_root = _resolve_path(paths.get("data_root", "data"), config_dir)
    results_root = _resolve_path(paths.get("results_root", "results"), config_dir)
    cache_dir = results_root / "cache"
    backlog_dir = results_root / "backlog"
    submission_dir = results_root / "submissions"
    skilllog_root = results_root / "skilllog"
    experiment = config.get("experiment", {})
    model_cfg = config.get("model", {})
    cv_cfg = config.get("cv", {})
    submission_cfg = config.get("submission", {})
    name = str(experiment.get("name", "mosquito_experiment"))
    seed = int(experiment.get("seed", 20260517))
    threshold = float(submission_cfg.get("threshold", 0.7))
    data = load_contest_data(
        data_root,
        cache_dir=cache_dir,
        limit_train=args.limit_train,
        limit_test=args.limit_test,
        refresh_cache=args.refresh_cache,
    )
    config_for_log = {**config, "runtime_args": vars(args)}
    logger = RunLogger(
        project="mosquito-contest",
        run_name=name,
        root_dir=skilllog_root,
        config=config_for_log,
        main_metric={"name": "val/r_hit@1cm", "mode": "max"},
        tags=list(experiment.get("tags", [])),
        framework="numpy/sklearn/torch",
        task_type="trajectory-regression",
    )
    try:
        model_type = str(model_cfg.get("type", "physics")).lower()
        if model_type == "physics":
            result = evaluate_physics(
                data.train_x,
                data.train_y,
                data.test_x,
                method=str(model_cfg.get("method", "cv_last1")),
                params=dict(model_cfg.get("params", {})),
            )
        elif model_type in {"residual_lgbm", "residual"}:
            result = evaluate_residual_model(
                data.train_x,
                data.train_y,
                data.test_x,
                base_method=str(model_cfg.get("base_method", "cv_last1")),
                cv_splits=int(cv_cfg.get("n_splits", 5)),
                seed=seed,
                model_kind=str(model_cfg.get("model_kind", "lightgbm")),
                model_params=dict(model_cfg.get("params", {})),
            )
        elif model_type == "jepa_torch":
            result = evaluate_jepa_torch(
                data.train_x,
                data.train_y,
                data.test_x,
                base_method=str(model_cfg.get("base_method", "cv_last1")),
                cv_splits=int(cv_cfg.get("n_splits", 5)),
                seed=seed,
                params=dict(model_cfg.get("params", {})),
            )
        elif model_type == "ensemble":
            payload = run_optional_ensemble(
                candidate_paths=list(model_cfg.get("candidate_paths", [])),
                true_y=data.train_y,
                min_single_score=float(model_cfg.get("min_single_score", 0.68)),
                min_submission_score=threshold,
                min_gain=float(model_cfg.get("min_gain", 0.003)),
                seed=seed,
                trials=int(model_cfg.get("trials", 4000)),
            )
            if payload.get("status") != "ready":
                logger.log_note(f"ensemble skipped: {payload.get('reason')}")
                metrics = {
                    "val/r_hit@1cm": float(payload.get("ensemble_score", payload.get("best_single_score", 0.0))),
                    "runtime/sec": time.perf_counter() - start,
                }
                _log_metrics(logger, metrics)
                _write_json(logger.run_dir / "ensemble_skip.json", payload)
                logger.log_artifact("ensemble_skip", logger.run_dir / "ensemble_skip.json", copy=False)
                _finish(logger, backlog_dir, name, metrics, result_label="ensemble:skipped")
                return 0
            result = _ensemble_result(payload)
        else:
            raise ValueError(f"unsupported model.type: {model_type}")

        metrics = dict(result.metrics)
        metrics["runtime/sec"] = time.perf_counter() - start
        _log_metrics(logger, metrics)
        _write_outputs(logger.run_dir, result, data.train_ids, data.test_ids)
        logger.log_artifact("oof_and_test_predictions", logger.run_dir / "predictions.npz", copy=False)
        logger.log_table("fold_metrics", pd.DataFrame(result.fold_rows))
        _maybe_write_submission(
            logger=logger,
            submission_dir=submission_dir,
            experiment_name=name,
            test_ids=data.test_ids,
            test_pred=result.test_pred,
            score=metrics["val/r_hit@1cm"],
            threshold=threshold,
            force=args.make_submission,
        )
        _finish(logger, backlog_dir, name, metrics, result.model_label)
        return 0
    except Exception as exc:
        logger.fail(exc)
        raise


def _maybe_write_submission(
    logger: RunLogger,
    submission_dir: Path,
    experiment_name: str,
    test_ids: np.ndarray,
    test_pred: np.ndarray,
    score: float,
    threshold: float,
    force: bool,
) -> None:
    if score < threshold:
        logger.log_note(f"submission gated: score {score:.6f} < {threshold:.6f}")
        return
    if force:
        logger.log_note("--make-submission supplied; threshold gate still controls file creation")
    filename = f"{experiment_name}_{logger.run_id}_valid{score:.4f}_submission.csv"
    path = write_submission(submission_dir / filename, test_ids, test_pred)
    logger.log_artifact("submission", path, copy=True)


def _finish(
    logger: RunLogger,
    backlog_dir: Path,
    experiment_name: str,
    metrics: dict[str, float],
    result_label: str,
) -> None:
    backlog = write_experiment_backlog(
        backlog_dir,
        run_id=logger.run_id,
        experiment_name=experiment_name,
        metrics=metrics,
        notes={
            "가설": f"- `{result_label}` can improve +80ms position prediction under R-Hit@1cm.",
            "설계": "- 5-fold random validation, train-only fitting, test used only for final inference.",
            "artifact 인사이트": "- Inspect `predictions.npz`, fold metric tables, and distance quantiles before next run.",
            "다음 실험": "- Tune residual capacity, then enable ensemble only after a strong single model appears.",
        },
    )
    append_feedback(backlog_dir / "skilllog_alpha_feedback.md", logger.run_id, metrics)
    logger.log_artifact("experiment_backlog", backlog, copy=True)
    logger.finish(build_dashboard=True, build_report=True)


def _write_outputs(run_dir: Path, result, train_ids: np.ndarray, test_ids: np.ndarray) -> None:
    np.savez_compressed(
        run_dir / "predictions.npz",
        train_ids=train_ids,
        test_ids=test_ids,
        oof_pred=result.oof_pred,
        test_pred=result.test_pred,
    )
    _write_json(run_dir / "metrics_summary.json", result.metrics)


def _log_metrics(logger: RunLogger, metrics: dict[str, float]) -> None:
    for key, value in sorted(metrics.items()):
        if isinstance(value, (int, float, np.floating)):
            logger.log_metric(key, float(value), step=0)


def _ensemble_result(payload: dict[str, Any]):
    from contest_mosquito.models import ExperimentResult

    metrics = {"val/r_hit@1cm": float(payload["ensemble_score"]), "val/ensemble_gain": float(payload["gain"])}
    return ExperimentResult(
        oof_pred=np.asarray(payload["oof_pred"], dtype=np.float32),
        test_pred=np.asarray(payload["test_pred"], dtype=np.float32),
        metrics=metrics,
        fold_rows=[{"fold": -1, **metrics}],
        model_label="ensemble:weighted",
    )


def _load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path).resolve()
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    config["__config_dir__"] = str(config_path.parent)
    return config


def _resolve_path(raw: str | Path, config_dir: Path) -> Path:
    path = Path(raw)
    if path.is_absolute() or path.exists():
        return path
    project_root = config_dir.parent
    return project_root / path


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
