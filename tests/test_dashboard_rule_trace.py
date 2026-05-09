from skilllogboard import RunLogger
from skilllogboard.dashboards.static_builder import build_dashboard


def test_dashboard_rule_audit_renders_warnings_and_planned(tmp_path):
    logger = RunLogger(project="demo", run_name="audit", root_dir=tmp_path / "runs")
    skills = tmp_path / "Skills.md"
    skills.write_text(
        """
## RULE-CONFIG-001
- type: required_config
- keys: [model_name]
- severity: warning
- status: MVP
- message: model_name is required.

## RULE-VIS-001
- type: dashboard_panel
- keys: [metric_curve]
- severity: info
- status: Planned
- message: dashboard panel rule is planned.
""",
        encoding="utf-8",
    )
    logger.run_skill_checks(skills_path=skills, stage="finish")

    html = build_dashboard(logger.run_dir).read_text(encoding="utf-8")

    assert "Rule Audit" in html
    assert "RULE-CONFIG-001" in html
    assert "warning" in html
    assert "RULE-VIS-001" in html
    assert "planned" in html


def test_dashboard_rule_audit_empty_state(tmp_path):
    logger = RunLogger(project="demo", run_name="no-audit", root_dir=tmp_path / "runs")

    html = build_dashboard(logger.run_dir).read_text(encoding="utf-8")

    assert "Rule Audit" in html
    assert "No skill_trace.jsonl rule results are available." in html
