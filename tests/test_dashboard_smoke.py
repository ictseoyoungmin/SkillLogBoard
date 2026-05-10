from skilllogboard import RunLogger
from tests.helpers import assert_contains_sections, assert_html_document


def test_dashboard_smoke_contains_core_sections(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("payload", encoding="utf-8")
    image = tmp_path / "plot.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    logger = RunLogger(
        project="demo",
        run_name="dashboard-smoke",
        root_dir=tmp_path / "runs",
        config={"model_name": "TinyNet"},
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metrics({"train/loss": 1.0, "val/acc": 0.8}, step=0)
    logger.log_artifact("artifact", artifact)
    logger.log_image("plot", image)
    logger.log_table("scores", [{"metric": "val/acc", "value": 0.8}])
    logger.finish(build_dashboard=True, build_report=True)

    html = (logger.run_dir / "dashboard.html").read_text(encoding="utf-8")
    assert (logger.run_dir / "dashboard.html").stat().st_size > 0
    assert_html_document(html)
    assert_contains_sections(
        html,
        ["Run Summary", "Main Metric", "Metrics", "Config", "Artifacts", "Rule Audit", "Files"],
    )
