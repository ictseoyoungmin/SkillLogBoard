import yaml

from skilllogboard.dashboards.static_builder import build_dashboard


def test_dashboard_builds_for_missing_metrics_and_artifacts(tmp_path):
    run_dir = tmp_path / "partial"
    run_dir.mkdir()
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump({"project": "demo", "run_name": "partial", "status": "failed"}),
        encoding="utf-8",
    )

    out = build_dashboard(run_dir)
    html = out.read_text(encoding="utf-8")

    assert out.exists()
    assert "failed" in html
    assert "Missing optional file: metrics.csv" in html
    assert "Missing optional file: artifact_index.json" in html
    assert "No metrics have been logged yet." in html
