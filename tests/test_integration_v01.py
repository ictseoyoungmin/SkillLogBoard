import csv

from skilllogboard import RunLogger
from tests.helpers import read_jsonl, read_yaml


def test_v01_single_run_evidence_package(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("payload", encoding="utf-8")
    image = tmp_path / "plot.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    logger = RunLogger(
        project="demo",
        run_name="v01",
        root_dir=tmp_path / "runs",
        config={"model_name": "TinyNet", "dataset_name": "Synthetic", "seed": 1},
        main_metric={"name": "val/acc", "mode": "max"},
    )

    logger.log_config({"seed": 42, "optimizer": "AdamW"})
    logger.log_metrics({"train/loss": 1.0, "val/acc": 0.8}, step=0)
    logger.log_metrics({"train/loss": 0.5, "val/acc": 0.9}, step=1)
    logger.log_note("v0.1 integration")
    logger.log_artifact("artifact", artifact)
    logger.log_image("plot", image)
    logger.log_table("scores", [{"metric": "val/acc", "value": 0.9}])
    logger.finish(build_dashboard=True, build_report=True)

    for name in [
        "manifest.yaml",
        "config.yaml",
        "system.json",
        "git.json",
        "metrics.csv",
        "events.jsonl",
        "artifact_index.json",
        "summary.md",
        "dashboard.html",
    ]:
        assert (logger.run_dir / name).exists()

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    assert manifest["status"] == "completed"
    assert manifest["best_metric"]["best_value"] == 0.9

    with (logger.run_dir / "metrics.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [row["name"] for row in rows] == ["train/loss", "val/acc", "train/loss", "val/acc"]

    events = read_jsonl(logger.run_dir / "events.jsonl")
    assert {"metric", "note", "artifact", "image", "table", "lifecycle"}.issubset(
        {event["type"] for event in events}
    )

    summary = (logger.run_dir / "summary.md").read_text(encoding="utf-8")
    assert "Run: `v01`" in summary
    assert "Best metric: `val/acc` = `0.9`" in summary
    assert "`artifacts/artifact.txt`" in summary
