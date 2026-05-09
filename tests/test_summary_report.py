import json

from skilllogboard import RunLogger
from skilllogboard.cli.main import main
from skilllogboard.reports.markdown_report import build_summary
from tests.helpers import read_yaml


def test_summary_includes_manifest_config_metrics_and_artifacts(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("payload", encoding="utf-8")
    logger = RunLogger(
        project="demo",
        run_name="summary",
        root_dir=tmp_path / "runs",
        config={
            "model_name": "TinyNet",
            "dataset_name": "Synthetic",
            "seed": 42,
            "optimizer": "AdamW",
            "lr": 0.001,
            "batch_size": 8,
        },
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metric("val/acc", 0.8, step=1)
    logger.log_metric("val/acc", 0.9, step=2)
    logger.log_artifact("payload", artifact)

    out = build_summary(logger.run_dir)
    text = out.read_text(encoding="utf-8")

    assert "# Run Summary" in text
    assert "Project: `demo`" in text
    assert "Run: `summary`" in text
    assert "Status: `running`" in text
    assert "model_name: `TinyNet`" in text
    assert "dataset_name: `Synthetic`" in text
    assert "Best metric: `val/acc` = `0.9` at step `2`" in text
    assert "| `val/acc` | `0.9` | `2` |" in text
    assert "| `payload` | `artifact` | `artifacts/artifact.txt` | `copy` |" in text


def test_summary_handles_missing_optional_files(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    out = build_summary(run_dir)
    text = out.read_text(encoding="utf-8")

    assert "Project: `unknown`" in text
    assert "No `config.yaml` file was found or it was empty." in text
    assert "No metrics have been logged yet." in text
    assert "No artifacts, images, or tables have been logged yet." in text


def test_logger_finish_and_cli_report_write_useful_summary(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="finish-report",
        root_dir=tmp_path / "runs",
        config={"model_name": "TinyNet"},
    )
    logger.log_metric("train/loss", 1.0, step=0)
    logger.finish(build_report=True)

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    assert manifest["files"]["summary"] == "summary.md"
    text = (logger.run_dir / "summary.md").read_text(encoding="utf-8")
    assert "Run: `finish-report`" in text
    assert "| `train/loss` | `1.0` | `0` |" in text

    (logger.run_dir / "summary.md").write_text("old", encoding="utf-8")
    assert main(["report", str(logger.run_dir)]) == 0
    assert "Run: `finish-report`" in (logger.run_dir / "summary.md").read_text(encoding="utf-8")


def test_summary_lists_image_and_table_outputs(tmp_path):
    image = tmp_path / "plot.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    logger = RunLogger(project="demo", run_name="media", root_dir=tmp_path / "runs")
    logger.log_image("plot", image)
    logger.log_table("scores", [{"metric": "acc", "value": 0.9}])

    build_summary(logger.run_dir)
    text = (logger.run_dir / "summary.md").read_text(encoding="utf-8")
    index = json.loads((logger.run_dir / "artifact_index.json").read_text(encoding="utf-8"))

    assert {record["type"] for record in index["artifacts"]} == {"image", "table"}
    assert "| `plot` | `image` | `images/plot.png` | `copy` |" in text
    assert "| `scores` | `table` | `tables/scores.csv` | `copy` |" in text
