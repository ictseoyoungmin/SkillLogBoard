"""Create a small run folder that can be watched with `skilllog watch`."""

from __future__ import annotations

from pathlib import Path
import time

from skilllogboard import RunLogger


def main() -> None:
    logger = RunLogger(
        project="live-demo",
        run_name="baseline",
        config={"model_name": "TinyLiveNet", "dataset_name": "synthetic", "seed": 7},
        main_metric={"name": "val/acc", "mode": "max"},
        root_dir=Path("runs/live_demo"),
    )
    for step in range(5):
        logger.log_metrics(
            {
                "train/loss": round(1.0 / (step + 1), 4),
                "val/acc": round(0.55 + step * 0.07, 4),
            },
            step=step,
        )
        logger.log_note(f"live demo step {step}")
        time.sleep(0.05)
    logger.finish(build_dashboard=True, build_report=True)
    print(f"Run directory: {logger.run_dir}")
    print(f"Watch command: skilllog watch {logger.run_dir} --no-open")


if __name__ == "__main__":
    main()
