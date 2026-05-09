from skilllogboard import RunLogger
from skilllogboard.dashboards.static_builder import build_dashboard


def test_dashboard_displays_config_table_and_nested_values(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="config-dashboard",
        root_dir=tmp_path / "runs",
        config={"model_name": "TinyNet", "nested": {"width": 32}, "layers": [1, 2]},
    )

    html = build_dashboard(logger.run_dir).read_text(encoding="utf-8")

    assert "Config" in html
    assert "model_name" in html
    assert "TinyNet" in html
    assert "nested.width" in html
    assert "[1, 2]" in html


def test_dashboard_displays_artifact_image_table_links_and_file_links(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("payload", encoding="utf-8")
    image = tmp_path / "plot.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    logger = RunLogger(project="demo", run_name="links", root_dir=tmp_path / "runs")
    logger.log_artifact("artifact", artifact)
    logger.log_image("plot", image)
    logger.log_table("scores", [{"metric": "acc", "value": 0.9}])
    logger.finish(build_report=True, build_dashboard=True)

    html = (logger.run_dir / "dashboard.html").read_text(encoding="utf-8")

    assert "Artifacts" in html
    assert 'href="artifacts/artifact.txt"' in html
    assert 'href="images/plot.png"' in html
    assert 'href="tables/scores.csv"' in html
    assert 'href="manifest.yaml"' in html
    assert 'href="config.yaml"' in html
    assert 'href="metrics.csv"' in html
    assert 'href="events.jsonl"' in html
    assert 'href="summary.md"' in html
    assert 'href="artifact_index.json"' in html


def test_dashboard_config_and_artifact_empty_states(tmp_path):
    run_dir = tmp_path / "partial"
    run_dir.mkdir()

    html = build_dashboard(run_dir).read_text(encoding="utf-8")

    assert "No config values are available." in html
    assert "No artifacts, images, or tables have been logged yet." in html
