"""Minimal smoke test for Week 1 skeleton."""

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
        )

    logger.log_note("Minimal smoke test run.")
    logger.finish(build_dashboard=True, build_report=True)
    print(f"Run written to: {logger.run_dir}")


if __name__ == "__main__":
    main()
