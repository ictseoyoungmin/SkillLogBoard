"""Minimal v0.1 smoke test for SkillLogBoard."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from tempfile import TemporaryDirectory

from skilllogboard import RunLogger


def main(root_dir: str | Path = "runs") -> Path:
    logger = RunLogger(
        project="demo",
        run_name="baseline",
        root_dir=root_dir,
        config={
            "model_name": "TinyNet",
            "dataset_name": "Synthetic",
            "seed": 42,
            "optimizer": "AdamW",
            "lr": 1e-3,
            "batch_size": 8,
        },
        main_metric={"name": "val/acc", "mode": "max"},
    )

    for epoch in range(3):
        logger.log_metrics(
            {
                "train/loss": 1.0 / (epoch + 1),
                "val/acc": 0.75 + 0.05 * epoch,
            },
            step=epoch,
            phase="demo",
        )

    with TemporaryDirectory() as tmp:
        artifact_source = Path(tmp) / "example_artifact.txt"
        artifact_source.write_text(
            "small generated artifact for the basic usage example\n",
            encoding="utf-8",
        )
        logger.log_artifact("example_artifact", artifact_source)

    logger.log_note("Minimal smoke test run.")
    skills_path = logger.run_dir / "Skills.default.md"

    skills_path.write_text(
        resources.files("skilllogboard.skills")
        .joinpath("default_skills.md")
        .read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    logger.run_skill_checks(skills_path)
    logger.finish(build_dashboard=True, build_report=True)
    print(f"Run written to: {logger.run_dir}")
    return logger.run_dir


if __name__ == "__main__":
    main()
