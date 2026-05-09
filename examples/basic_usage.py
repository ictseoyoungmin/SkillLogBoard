"""Minimal v0.1 smoke test for SkillLogBoard."""

from pathlib import Path
from tempfile import TemporaryDirectory

from skilllogboard import RunLogger


def main() -> None:
    logger = RunLogger(
        project="demo",
        run_name="baseline",
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
    logger.finish(build_dashboard=True, build_report=True)
    print(f"Run written to: {logger.run_dir}")


if __name__ == "__main__":
    main()
