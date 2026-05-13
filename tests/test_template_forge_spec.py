import json

from skilllogboard.template_forge import (
    ResearchBrief,
    TemplateSpec,
    draft_template_spec_from_brief,
    load_template_spec_template,
    parse_template_spec_text,
    render_template_spec,
)


def test_template_spec_schema_is_serializable():
    spec = TemplateSpec(
        template_name="custom-task",
        metric_names=["val/score"],
        required_rules=["required_config"],
        recommended_tables=["leaderboard"],
        recommended_figures=["metric-curve-overlay"],
    )

    data = spec.to_dict()

    assert data["template_name"] == "custom-task"
    assert json.dumps(data)


def test_parse_template_spec_template_and_filled_text():
    parsed_template = parse_template_spec_text(load_template_spec_template())
    filled = parse_template_spec_text(
        """
# TemplateSpec

## Template Name
ir-drop-custom

## Category
ir-drop

## Description
Synthetic IR-drop scaffold.

## Status
Draft

## Default Config
template: ir-drop-custom
seed: 1

## Metric Names
- val/high_drop_f1
- val/mae

## Required Rules
- required_config
- required_metric

## Recommended Tables
- leaderboard

## Recommended Figures
- metric-curve-overlay

## Synthetic Example Plan
Generate a small synthetic grid.
"""
    )

    assert parsed_template.template_name == "custom-template"
    assert filled.default_config["seed"] == 1
    assert filled.metric_names == ["val/high_drop_f1", "val/mae"]


def test_draft_template_spec_from_brief_preserves_metrics_outputs_and_todos():
    brief = ResearchBrief(
        research_topic="Predict trajectories",
        task_type="trajectory",
        input_data="synthetic paths",
        target="future position",
        main_metric="val/pb_score",
        secondary_metrics=["val/ade"],
        required_outputs=["report"],
        experiment_axes=["seed"],
    )

    spec = draft_template_spec_from_brief(brief, template_name="trajectory-custom")
    text = render_template_spec(spec)

    assert spec.template_name == "trajectory-custom"
    assert spec.metric_names == ["val/pb_score", "val/ade"]
    assert spec.required_outputs == ["report"]
    assert "TODO" in text
