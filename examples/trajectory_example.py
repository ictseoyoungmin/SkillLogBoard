"""Synthetic trajectory logging example.

This example logs generated toy metrics only. It does not train a model or load
external trajectory data.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from skilllogboard import RunLogger
from skilllogboard.plugins.trajectory import trajectory_template


def main(root_dir: str | Path = "runs") -> Path:
    template = trajectory_template()
    logger = RunLogger(
        project="trajectory_demo",
        run_name="synthetic-trajectory",
        root_dir=root_dir,
        config={**template.default_config, "seed": 11},
        main_metric={"name": "val/pb_score", "mode": "max"},
        tags=["trajectory", "synthetic"],
    )

    for step, pb_score in enumerate([0.52, 0.64, 0.71]):
        logger.log_metrics(
            {
                "train/loss": 1.1 / (step + 1),
                "val/loss": 0.82 - 0.08 * step,
                "val/pb_score": pb_score,
                "val/endpoint_error": 2.4 - 0.3 * step,
            },
            step=step,
            template="trajectory",
        )

    logger.log_table(
        "trajectory_samples",
        [
            {"sample": "scene_a", "horizon": 12, "endpoint_error": 1.9},
            {"sample": "scene_b", "horizon": 12, "endpoint_error": 2.1},
        ],
    )
    with TemporaryDirectory() as tmp:
        artifact = Path(tmp) / "synthetic_paths.txt"
        artifact.write_text("two synthetic trajectory path placeholders\n", encoding="utf-8")
        logger.log_artifact("synthetic_paths", artifact)

    skills_path = logger.run_dir / "Skills.trajectory.md"
    skills_path.write_text(template.default_skills, encoding="utf-8")
    logger.run_skill_checks(skills_path)
    logger.finish(build_dashboard=True, build_report=True)
    print(f"Trajectory run written to: {logger.run_dir}")
    return logger.run_dir


if __name__ == "__main__":
    main()
