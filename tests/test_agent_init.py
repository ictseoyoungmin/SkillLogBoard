from skilllogboard.agent.skills import ensure_skilllog_control_plane
from skilllogboard.reports.report_spec import parse_report_spec


def test_ensure_skilllog_control_plane_creates_expected_files(tmp_path):
    result = ensure_skilllog_control_plane(tmp_path)

    assert (tmp_path / ".skilllog" / "agent_skills.md").exists()
    assert (tmp_path / ".skilllog" / "experiment_plan.md").exists()
    assert (tmp_path / ".skilllog" / "rules.md").exists()
    assert (tmp_path / ".skilllog" / "report_spec.md").exists()
    assert (tmp_path / ".skilllog" / "README.md").exists()
    assert len(result.created) == 5
    assert parse_report_spec(tmp_path / ".skilllog" / "report_spec.md")


def test_ensure_skilllog_control_plane_does_not_overwrite_by_default(tmp_path):
    ensure_skilllog_control_plane(tmp_path)
    plan = tmp_path / ".skilllog" / "experiment_plan.md"
    plan.write_text("custom", encoding="utf-8")

    result = ensure_skilllog_control_plane(tmp_path)

    assert plan.read_text(encoding="utf-8") == "custom"
    assert str(plan) in result.skipped


def test_ensure_skilllog_control_plane_template_hint(tmp_path):
    ensure_skilllog_control_plane(tmp_path, template="ir-drop")

    text = (tmp_path / ".skilllog" / "experiment_plan.md").read_text(encoding="utf-8")
    assert "ir-drop" in text
