"""Core RunLogger example with sklearn-like metrics.

This file intentionally does not import scikit-learn. It shows how a user can
log accuracy/F1-style metrics produced by any training stack.
"""

from __future__ import annotations

from pathlib import Path

from skilllogboard import RunLogger


def main(root_dir: str | Path = "runs") -> Path:
    logger = RunLogger(
        project="sklearn_demo",
        run_name="synthetic-classifier",
        root_dir=root_dir,
        config={
            "model_name": "logistic_regression_like",
            "dataset_name": "synthetic_tabular",
            "seed": 5,
            "source": "core-logger-example",
        },
        main_metric={"name": "val/f1", "mode": "max"},
        tags=["sklearn-style", "synthetic"],
    )

    for step, f1 in enumerate([0.72, 0.78, 0.81]):
        logger.log_metrics(
            {
                "train/loss": 0.7 / (step + 1),
                "val/accuracy": 0.76 + 0.04 * step,
                "val/f1": f1,
            },
            step=step,
            example="sklearn-core-logger",
        )

    logger.log_table(
        "classification_report",
        [
            {"label": "negative", "precision": 0.82, "recall": 0.79, "f1": 0.80},
            {"label": "positive", "precision": 0.80, "recall": 0.83, "f1": 0.81},
        ],
    )
    logger.finish(build_dashboard=True, build_report=True)
    print(f"sklearn-style run written to: {logger.run_dir}")
    return logger.run_dir


if __name__ == "__main__":
    main()
