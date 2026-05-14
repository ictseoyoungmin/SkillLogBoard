"""Create a small run folder that can be watched with `skilllog watch`."""

from __future__ import annotations

import argparse
from pathlib import Path
import time

from skilllogboard import RunLogger


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Live Board demo run folders.")
    parser.add_argument("--multi-run", action="store_true", help="create several comparable runs")
    parser.add_argument("--runs", type=int, default=3, help="number of runs for --multi-run")
    args = parser.parse_args()
    if args.multi_run:
        run_dirs = [_write_demo_run(index, root_dir=Path("runs/live_demo")) for index in range(args.runs)]
        print(f"Project directory: {Path('runs/live_demo')}")
        print("Run directories:")
        for run_dir in run_dirs:
            print(f"- {run_dir}")
        print("Watch command: skilllog watch runs/live_demo --project --no-open")
        return
    logger = _create_logger("baseline", seed=7, root_dir=Path("runs/live_demo"))
    _write_steps(logger, offset=0.0)
    logger.finish(build_dashboard=True, build_report=True)
    print(f"Run directory: {logger.run_dir}")
    print(f"Watch command: skilllog watch {logger.run_dir} --no-open")


def _write_demo_run(index: int, root_dir: Path) -> Path:
    run_name = "baseline" if index == 0 else f"candidate-{index}"
    logger = _create_logger(run_name, seed=7 + index, root_dir=root_dir)
    _write_steps(logger, offset=index * 0.025)
    logger.finish(build_dashboard=True, build_report=True)
    return logger.run_dir


def _create_logger(run_name: str, seed: int, root_dir: Path) -> RunLogger:
    return RunLogger(
        project="live-demo",
        run_name=run_name,
        config={"model_name": "TinyLiveNet", "dataset_name": "synthetic", "seed": seed},
        main_metric={"name": "val/acc", "mode": "max"},
        root_dir=root_dir,
    )


def _write_steps(logger: RunLogger, offset: float) -> None:
    for step in range(5):
        logger.log_metrics(
            {
                "train/loss": round(1.0 / (step + 1 + offset), 4),
                "val/acc": round(0.55 + step * 0.07 + offset, 4),
            },
            step=step,
        )
        logger.log_note(f"live demo step {step}")
        time.sleep(0.05)


if __name__ == "__main__":
    main()
