from importlib import resources

from skilllogboard import RunLogger
from skilllogboard.dashboards.static_builder import build_dashboard


def test_dashboard_template_is_available_as_package_data():
    template = resources.files("skilllogboard.dashboards.templates").joinpath("run.html.j2")
    text = template.read_text(encoding="utf-8")

    assert text.startswith("<!doctype html>")
    assert "<html" in text
    assert "<head>" in text
    assert '<meta charset="utf-8">' in text
    assert "<body>" in text
    assert "SkillLogBoard Dashboard" in text
    assert "Run Summary" in text
    assert "Metrics" in text
    assert "Rule Audit" in text


def test_dashboard_links_are_relative(tmp_path):
    logger = RunLogger(project="demo", run_name="relative", root_dir=tmp_path / "runs")
    logger.finish(build_dashboard=True, build_report=True)

    html = (logger.run_dir / "dashboard.html").read_text(encoding="utf-8")
    assert 'href="manifest.yaml"' in html
    assert "file://" not in html
    assert "http://" not in html
    assert "https://" not in html

    out = build_dashboard(logger.run_dir)
    assert out.exists()
