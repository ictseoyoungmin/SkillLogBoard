import json

from skilllogboard.template_forge import (
    ResearchBrief,
    load_research_brief_template,
    parse_research_brief_text,
)


def test_research_brief_schema_is_serializable():
    brief = ResearchBrief(
        research_topic="Trajectory prediction",
        task_type="trajectory",
        input_data="synthetic coordinates",
        target="next point",
        main_metric="val/pb_score",
        secondary_metrics=["val/ade"],
        experiment_axes=["seed", "history_length"],
        required_outputs=["synthetic example"],
        constraints=["no external data"],
    )

    data = brief.to_dict()

    assert data["main_metric"] == "val/pb_score"
    assert json.dumps(data)


def test_parse_research_brief_template_and_filled_text():
    template = load_research_brief_template()
    parsed_template = parse_research_brief_text(template)
    filled = parse_research_brief_text(
        """
# ResearchBrief

## Research Topic
IR-drop hotspot detection.

## Task Type
ir-drop

## Input Data
Synthetic power grid tensors.

## Target
Hotspot mask.

## Main Metric
val/high_drop_f1

## Secondary Metrics
- val/mae
- val/raw_mae

## Experiment Axes
- seed
- corner

## Required Outputs
- report
- dashboard
"""
    )

    assert parsed_template.constraints
    assert filled.task_type == "ir-drop"
    assert filled.secondary_metrics == ["val/mae", "val/raw_mae"]
    assert "corner" in filled.experiment_axes
