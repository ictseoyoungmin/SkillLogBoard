from skilllogboard.skills.report_rules import (
    check_report_artifacts,
    report_manifest_required,
    required_figure,
    required_table,
)


def test_report_artifact_rules_detect_present_and_missing_outputs(tmp_path):
    report = tmp_path / "report"
    (report / "tables").mkdir(parents=True)
    (report / "figures").mkdir()
    (report / "tables" / "leaderboard.md").write_text("| a |\n", encoding="utf-8")
    (report / "report_manifest.yaml").write_text("report_id: demo\noutputs: []\n", encoding="utf-8")

    assert report_manifest_required(report).outcome == "passed"
    assert required_table(report, "leaderboard").outcome == "passed"
    assert required_figure(report, "curve").outcome == "warning"


def test_check_report_artifacts_returns_error_for_missing_table(tmp_path):
    results = check_report_artifacts(tmp_path, required_tables=["leaderboard"])

    assert any(result.outcome == "error" for result in results)
