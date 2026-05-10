"""IR-drop research template.

Target version: v0.5.
"""

from __future__ import annotations

from skilllogboard.plugins.base import SkillLogTemplate


IR_DROP_SKILLS = """# IR-drop Experiment Skills

## RULE-CONFIG-IR-001
- type: required_config
- keys: [template, design_name, corner, seed]
- severity: warning
- status: MVP
- message: IR-drop runs should log template, design, corner, and seed metadata.

## RULE-METRIC-IR-001
- type: required_metric
- keys: [train/loss, val/mae, val/high_drop_f1, val/raw_mae]
- severity: warning
- status: MVP
- message: IR-drop runs should log training loss and validation quality metrics.

## RULE-METRIC-IR-002
- type: metric_threshold
- metric: val/high_drop_f1
- threshold: 0.5
- mode: max
- severity: info
- status: MVP
- message: High-drop F1 should clear the smoke-test baseline.
"""


IR_DROP_DEFAULT_CONFIG = {
    "template": "ir-drop",
    "design_name": "synthetic_power_grid",
    "corner": "typical",
    "seed": 0,
    "grid_size": "8x8",
    "label": "synthetic-no-private-data",
}


IR_DROP_METRICS = (
    "train/loss",
    "val/mae",
    "val/high_drop_f1",
    "val/raw_mae",
)


def ir_drop_template() -> SkillLogTemplate:
    return SkillLogTemplate(
        name="ir-drop",
        status="Implemented",
        description="IR-drop experiment logging template with synthetic power-grid metrics.",
        default_skills=IR_DROP_SKILLS,
        default_config=dict(IR_DROP_DEFAULT_CONFIG),
        metric_names=IR_DROP_METRICS,
        docs_notes=(
            "Logging/reporting template only; no model, private dataset, or EDA tool is included.",
            "Metric convention includes val/high_drop_f1 for compare leaderboards.",
        ),
    )
