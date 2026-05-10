"""Trajectory/JEPA research template.

Target version: v0.5.
"""

from __future__ import annotations

from skilllogboard.plugins.base import SkillLogTemplate


TRAJECTORY_SKILLS = """# Trajectory Experiment Skills

## RULE-CONFIG-TRAJ-001
- type: required_config
- keys: [template, model, dataset, seed, encoder, horizon, lr, batch_size]
- severity: warning
- status: MVP
- message: Trajectory runs should log model, dataset, horizon, and training metadata.

## RULE-METRIC-TRAJ-001
- type: required_metric
- keys: [train/loss, val/loss, val/pb_score, val/endpoint_error]
- severity: warning
- status: MVP
- message: Trajectory runs should log loss, PB score, and endpoint error.

## RULE-METRIC-TRAJ-002
- type: metric_threshold
- metric: val/pb_score
- threshold: 0.5
- mode: max
- severity: info
- status: MVP
- message: PB score should clear the smoke-test baseline.
"""


TRAJECTORY_DEFAULT_CONFIG = {
    "template": "trajectory",
    "model": "synthetic_jepa_baseline",
    "dataset": "synthetic_trajectories",
    "seed": 0,
    "encoder": "tiny-mlp",
    "horizon": 12,
    "lr": 0.001,
    "batch_size": 16,
}


TRAJECTORY_METRICS = (
    "train/loss",
    "val/loss",
    "val/pb_score",
    "val/endpoint_error",
)


def trajectory_template() -> SkillLogTemplate:
    return SkillLogTemplate(
        name="trajectory",
        status="Implemented",
        description="Trajectory experiment logging template with PB score and endpoint metrics.",
        default_skills=TRAJECTORY_SKILLS,
        default_config=dict(TRAJECTORY_DEFAULT_CONFIG),
        metric_names=TRAJECTORY_METRICS,
        docs_notes=(
            "Logging/reporting template only; model training and datasets are user-provided.",
            "Metric convention includes val/pb_score for compare leaderboards.",
        ),
    )
