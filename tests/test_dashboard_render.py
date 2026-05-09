from skilllogboard import RunLogger
from skilllogboard.cli.main import main
from skilllogboard.dashboards.static_builder import build_dashboard
from tests.helpers import read_yaml


def test_build_dashboard_renders_core_sections(tmp_path):
    logger = RunLogger(project="demo", run_name="render", root_dir=tmp_path / "runs")
    logger.log_metric("val/acc", 0.9, step=1)
    logger.finish(build_report=True)

    out = build_dashboard(logger.run_dir)
    html = out.read_text(encoding="utf-8")

    assert out.exists()
    assert "Run Summary" in html
    assert "SkillLogBoard Dashboard" in html
    assert "Main Metric" in html
    assert "Metrics" in html
    assert "Config" in html
    assert "Artifacts" in html
    assert "Files" in html
    assert 'href="manifest.yaml"' in html


def test_logger_finish_and_cli_dashboard_update_manifest_and_html(tmp_path):
    logger = RunLogger(project="demo", run_name="api-dashboard", root_dir=tmp_path / "runs")
    logger.finish(build_dashboard=True)

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    assert manifest["files"]["dashboard"] == "dashboard.html"
    assert (logger.run_dir / "dashboard.html").stat().st_size > 0

    (logger.run_dir / "dashboard.html").write_text("old", encoding="utf-8")
    assert main(["dashboard", str(logger.run_dir)]) == 0
    assert "SkillLogBoard Dashboard" in (logger.run_dir / "dashboard.html").read_text(encoding="utf-8")
