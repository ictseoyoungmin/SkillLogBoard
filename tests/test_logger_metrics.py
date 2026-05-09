import csv
import json

import pytest

from skilllogboard import RunLogger
from tests.helpers import read_jsonl, read_yaml


def _rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_log_metric_writes_csv_and_event(tmp_path):
    logger = RunLogger(project="demo", run_name="metric", root_dir=tmp_path / "runs")

    logger.log_metric("val/acc", 0.9, step=1, split="val")

    rows = _rows(logger.run_dir / "metrics.csv")
    events = read_jsonl(logger.run_dir / "events.jsonl")
    metric_events = [event for event in events if event["type"] == "metric"]

    assert rows[-1]["name"] == "val/acc"
    assert rows[-1]["value"] == "0.9"
    assert rows[-1]["step"] == "1"
    assert json.loads(rows[-1]["metadata_json"]) == {"split": "val"}
    assert metric_events[-1]["key"] == "val/acc"
    assert metric_events[-1]["value"] == 0.9
    assert metric_events[-1]["step"] == 1
    assert metric_events[-1]["metadata"] == {"split": "val"}


def test_log_metric_rejects_non_scalar_and_bad_step(tmp_path):
    logger = RunLogger(project="demo", run_name="bad", root_dir=tmp_path / "runs")

    with pytest.raises(TypeError, match="int or float"):
        logger.log_metric("val/acc", {"value": 1})
    with pytest.raises(TypeError, match="step"):
        logger.log_metric("val/acc", 1.0, step=1.2)
    with pytest.raises(ValueError, match="finite"):
        logger.log_metric("val/acc", float("nan"))


def test_log_metrics_batch_preserves_order_and_metadata(tmp_path):
    logger = RunLogger(project="demo", run_name="batch", root_dir=tmp_path / "runs")

    logger.log_metrics({"train/loss": 1.0, "val/acc": 0.8}, step=2, epoch=2)
    logger.log_metrics({}, step=3)

    rows = _rows(logger.run_dir / "metrics.csv")
    events = [event for event in read_jsonl(logger.run_dir / "events.jsonl") if event["type"] == "metric"]

    assert [row["name"] for row in rows] == ["train/loss", "val/acc"]
    assert [event["key"] for event in events] == ["train/loss", "val/acc"]
    assert all(event["metadata"] == {"epoch": 2} for event in events)


def test_best_metric_tracking_max_mode(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="best-max",
        root_dir=tmp_path / "runs",
        main_metric={"name": "val/acc", "mode": "max"},
    )

    logger.log_metric("val/acc", 0.7, step=1)
    logger.log_metric("val/loss", 1.0, step=1)
    logger.log_metric("val/acc", 0.6, step=2)
    logger.log_metric("val/acc", 0.9, step=3)

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    assert manifest["best_metric"]["name"] == "val/acc"
    assert manifest["best_metric"]["mode"] == "max"
    assert manifest["best_metric"]["best_value"] == 0.9
    assert manifest["best_metric"]["best_step"] == 3


def test_best_metric_tracking_min_mode(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="best-min",
        root_dir=tmp_path / "runs",
        main_metric={"name": "val/loss", "mode": "min"},
    )

    logger.log_metric("val/loss", 1.0, step=1)
    logger.log_metric("val/loss", 1.2, step=2)
    logger.log_metric("val/loss", 0.5, step=3)

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    assert manifest["best_metric"]["best_value"] == 0.5
    assert manifest["best_metric"]["best_step"] == 3
