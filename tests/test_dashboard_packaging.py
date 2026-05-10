from importlib import resources

from skilllogboard import RunLogger
from skilllogboard.dashboards.static_builder import build_dashboard
from tests.helpers import assert_contains_sections, assert_html_document


def test_dashboard_template_is_available_as_package_data():
    template = resources.files("skilllogboard.dashboards.templates").joinpath("run.html.j2")
    text = template.read_text(encoding="utf-8")

    assert_html_document(text)
    assert "SkillLogBoard Dashboard" in text
    assert_contains_sections(
        text,
        ["Run Summary", "Main Metric", "Metrics", "Config", "Artifacts", "Rule Audit", "Files"],
    )


def test_compare_template_is_available_as_package_data():
    template = resources.files("skilllogboard.dashboards.templates").joinpath("compare.html.j2")
    text = template.read_text(encoding="utf-8")

    assert_html_document(text)
    assert "SkillLogBoard Compare" in text
    assert_contains_sections(text, ["Leaderboard", "Config Diff", "Ablation Axes", "Seed Summary"])


def test_dashboard_links_are_relative(tmp_path):
    logger = RunLogger(project="demo", run_name="relative", root_dir=tmp_path / "runs")
    logger.finish(build_dashboard=True, build_report=True)

    html = (logger.run_dir / "dashboard.html").read_text(encoding="utf-8")
    assert_html_document(html)
    assert 'href="manifest.yaml"' in html
    assert "file://" not in html
    assert "http://" not in html
    assert "https://" not in html

    out = build_dashboard(logger.run_dir)
    assert out.exists()
