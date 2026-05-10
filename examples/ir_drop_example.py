"""Synthetic IR-drop logging example.

This example uses generated toy values only. It does not require external data,
EDA tools, torch, or pandas.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from skilllogboard import RunLogger
from skilllogboard.plugins.ir_drop import ir_drop_template


def main(root_dir: str | Path = "runs") -> Path:
    template = ir_drop_template()
    logger = RunLogger(
        project="ir_drop_demo",
        run_name="synthetic-ir-drop",
        root_dir=root_dir,
        config={**template.default_config, "seed": 7},
        main_metric={"name": "val/high_drop_f1", "mode": "max"},
        tags=["ir-drop", "synthetic"],
    )

    for step, high_drop_f1 in enumerate([0.58, 0.67, 0.74]):
        logger.log_metrics(
            {
                "train/loss": 0.9 / (step + 1),
                "val/mae": 3.4 - 0.35 * step,
                "val/high_drop_f1": high_drop_f1,
                "val/raw_mae": 4.1 - 0.25 * step,
            },
            step=step,
            template="ir-drop",
        )

    logger.log_table(
        "hotspot_summary",
        [
            {"region": "core_top", "max_drop_mv": 82.0, "is_high_drop": True},
            {"region": "core_mid", "max_drop_mv": 49.5, "is_high_drop": False},
        ],
    )
    with TemporaryDirectory() as tmp:
        artifact = Path(tmp) / "synthetic_grid.txt"
        artifact.write_text("8x8 synthetic voltage-drop grid placeholder\n", encoding="utf-8")
        logger.log_artifact("synthetic_grid", artifact)

    skills_path = logger.run_dir / "Skills.ir-drop.md"
    skills_path.write_text(template.default_skills, encoding="utf-8")
    logger.run_skill_checks(skills_path)
    logger.finish(build_dashboard=True, build_report=True)
    print(f"IR-drop run written to: {logger.run_dir}")
    return logger.run_dir


if __name__ == "__main__":
    main()
