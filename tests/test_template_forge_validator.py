from skilllogboard.template_forge import TemplateSpec, scaffold_template_from_spec
from skilllogboard.template_forge.validator import (
    TemplateValidationResult,
    check_core_dependency_policy,
    validate_template,
    validate_template_files,
)


def _spec():
    return TemplateSpec(
        template_name="custom-task",
        description="Custom task scaffold.",
        default_config={"template": "custom-task", "seed": 0},
        metric_names=["val/score"],
        required_rules=["required_config", "required_metric"],
        recommended_tables=["leaderboard"],
        recommended_figures=["metric-curve-overlay"],
    )


def test_template_validation_result_is_serializable():
    result = TemplateValidationResult("x", "X", "passed", "info", "ok")

    assert result.to_dict()["outcome"] == "passed"


def test_validate_template_files_reports_missing_and_present_files(tmp_path):
    missing = validate_template_files("custom-task", root_dir=tmp_path)
    scaffold_template_from_spec(_spec(), root_dir=tmp_path)
    present = validate_template_files("custom-task", root_dir=tmp_path)

    assert any(result.outcome == "error" for result in missing)
    assert all(result.outcome == "passed" for result in present)


def test_validate_template_warns_for_draft_todos_but_no_file_errors(tmp_path):
    scaffold_template_from_spec(_spec(), root_dir=tmp_path)
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies = ["pyyaml>=6.0"]\n',
        encoding="utf-8",
    )

    results = validate_template("custom-task", root_dir=tmp_path)

    assert not any(result.check_id.startswith("files.") and result.outcome == "error" for result in results)
    assert any(result.outcome == "warning" for result in results)
    assert any(result.check_id == "dependencies" and result.outcome == "passed" for result in results)


def test_core_dependency_policy_detects_heavy_core_dependency():
    result = check_core_dependency_policy(
        """
[project]
dependencies = [
  "pyyaml>=6.0",
  "torch",
]
"""
    )

    assert result.outcome == "error"
    assert "torch" in result.details["dependencies"]
