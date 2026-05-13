from pathlib import Path

import pytest

from skilllogboard.template_forge import (
    TemplateSpec,
    normalize_template_name,
    parse_template_spec,
    planned_scaffold_paths,
    scaffold_template_from_spec,
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


def test_normalize_template_name_and_reject_unsafe_names():
    normalized = normalize_template_name("Custom Task")

    assert normalized.slug == "custom-task"
    assert normalized.module_name == "custom_task"
    assert normalized.class_name == "CustomTaskTemplate"

    with pytest.raises(ValueError):
        normalize_template_name("../bad")


def test_planned_scaffold_paths_are_deterministic(tmp_path):
    paths = planned_scaffold_paths("custom-task", root_dir=tmp_path)

    assert paths.plugin.endswith("src/skilllogboard/plugins/custom_task.py")
    assert paths.example.endswith("examples/custom_task_example.py")
    assert paths.test.endswith("tests/test_custom_task_template.py")
    assert paths.docs.endswith("docs/templates/custom_task.md")
    assert paths.template_spec.endswith(".skilllog/template_spec.md")


def test_scaffold_template_from_spec_creates_todo_files_and_preserves_existing(tmp_path):
    result = scaffold_template_from_spec(_spec(), root_dir=tmp_path)
    second = scaffold_template_from_spec(_spec(), root_dir=tmp_path)
    paths = planned_scaffold_paths("custom-task", root_dir=tmp_path)

    assert len(result.created) == 6
    assert len(second.skipped) == 6
    assert "TODO" in Path(paths.plugin).read_text(encoding="utf-8")
    assert "RunLogger" in Path(paths.example).read_text(encoding="utf-8")
    assert "Overview" in Path(paths.docs).read_text(encoding="utf-8")
    assert parse_template_spec(paths.template_spec).template_name == "custom-task"
