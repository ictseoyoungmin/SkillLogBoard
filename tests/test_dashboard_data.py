from skilllogboard import RunLogger
from skilllogboard.dashboards.components import load_run_context


def test_load_run_context_complete_run(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("payload", encoding="utf-8")
    logger = RunLogger(
        project="demo",
        run_name="dashboard-data",
        root_dir=tmp_path / "runs",
        config={"model_name": "TinyNet"},
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metric("val/acc", 0.9, step=1)
    logger.log_artifact("artifact", artifact)
    logger.finish(build_report=True)

    context = load_run_context(logger.run_dir)

    assert context["manifest"]["run_name"] == "dashboard-data"
    assert context["config"]["model_name"] == "TinyNet"
    assert context["metric_series"]["val/acc"][0]["value"] == 0.9
    assert context["events_summary"]["by_type"]["metric"] == 1
    assert context["artifacts"][0]["name"] == "artifact"
    assert {"label": "manifest.yaml", "href": "manifest.yaml"} in context["file_links"]


def test_load_run_context_partial_run_has_defaults(tmp_path):
    run_dir = tmp_path / "partial"
    run_dir.mkdir()

    context = load_run_context(run_dir)

    assert context["manifest"] == {}
    assert context["config"] == {}
    assert context["metrics"] == []
    assert context["metric_series"] == {}
    assert context["events_summary"]["count"] == 0
    assert context["artifacts"] == []
    assert context["warnings"]
