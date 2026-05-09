import json

import yaml

from skilllogboard import RunLogger


def test_basic_run(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="baseline",
        config={"model_name": "TinyNet", "dataset_name": "Synthetic", "seed": 42},
        root_dir=tmp_path / "runs",
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metrics({"train/loss": 1.0, "val/acc": 0.8}, step=0)
    logger.finish(build_dashboard=True, build_report=True)

    assert (logger.run_dir / "manifest.yaml").exists()
    assert (logger.run_dir / "config.yaml").exists()
    assert (logger.run_dir / "system.json").exists()
    assert (logger.run_dir / "git.json").exists()
    assert (logger.run_dir / "metrics.csv").exists()
    assert (logger.run_dir / "events.jsonl").exists()
    assert (logger.run_dir / "summary.md").exists()
    assert (logger.run_dir / "dashboard.html").exists()

    manifest = yaml.safe_load((logger.run_dir / "manifest.yaml").read_text(encoding="utf-8"))
    assert manifest["status"] == "completed"
    assert manifest["files"]["metrics"] == "metrics.csv"
    assert manifest["files"]["events"] == "events.jsonl"
    assert manifest["files"]["summary"] == "summary.md"
    assert manifest["files"]["dashboard"] == "dashboard.html"

    config = yaml.safe_load((logger.run_dir / "config.yaml").read_text(encoding="utf-8"))
    assert config["model_name"] == "TinyNet"

    events = [
        json.loads(line)
        for line in (logger.run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert any(event["type"] == "metric" and event["key"] == "val/acc" for event in events)
    assert events[-1]["key"] == "finish"
