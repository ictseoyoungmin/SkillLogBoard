"""Create a small run folder that can be watched with `skilllog watch`."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
import math
from pathlib import Path
import time

from skilllogboard import RunLogger


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Live Board demo run folders.")
    parser.add_argument("--multi-run", action="store_true", help="create several comparable runs")
    parser.add_argument("--runs", type=int, default=3, help="number of runs for --multi-run")
    parser.add_argument("--rich", action="store_true", help="create richer showcase evidence")
    args = parser.parse_args()
    if args.multi_run:
        project_root = Path("runs/live_demo")
        count = max(args.runs, 5) if args.rich else args.runs
        run_dirs = [
            _write_demo_run(index, root_dir=project_root, rich=args.rich)
            for index in range(count)
        ]
        if args.rich:
            _write_portable_report_package(project_root, project_root / "report")
        print(f"Project directory: {Path('runs/live_demo')}")
        print("Run directories:")
        for run_dir in run_dirs:
            print(f"- {run_dir}")
        print("Watch command: skilllog watch runs/live_demo --project --no-open")
        print("Latest-only command: skilllog watch runs/live_demo --project --latest --no-open")
        return
    logger = _create_logger("baseline", seed=7, root_dir=Path("runs/live_demo"))
    if args.rich:
        _write_rich_steps(logger, profile=_profile_for_index(0))
        _write_showcase_evidence(logger, profile=_profile_for_index(0))
        logger.finish()
        _write_portable_report_package(logger.run_dir, logger.run_dir / "report")
    else:
        _write_steps(logger, offset=0.0)
        logger.finish(build_dashboard=True, build_report=True)
    print(f"Run directory: {logger.run_dir}")
    print(f"Watch command: skilllog watch {logger.run_dir} --no-open")
    print(f"Project watch command: skilllog watch {Path('runs/live_demo')} --project --no-open")


def _write_demo_run(index: int, root_dir: Path, rich: bool = False) -> Path:
    profile = _profile_for_index(index)
    run_name = profile["name"] if rich else ("baseline" if index == 0 else f"candidate-{index}")
    logger = _create_logger(run_name, seed=7 + index, root_dir=root_dir)
    if rich:
        _write_rich_steps(logger, profile=profile)
        _write_showcase_evidence(logger, profile=profile)
    else:
        _write_steps(logger, offset=index * 0.025)
    if profile.get("status") == "failed":
        logger.fail("synthetic validation divergence")
    elif profile.get("status") == "running":
        logger.manifest.save(logger.run_dir / "manifest.yaml")
    else:
        logger.finish()
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


def _profile_for_index(index: int) -> dict[str, float | str]:
    profiles: list[dict[str, float | str]] = [
        {"name": "baseline", "status": "completed", "quality": 0.78, "loss": 1.0, "speed": 1.0},
        {"name": "best", "status": "completed", "quality": 0.91, "loss": 0.86, "speed": 1.12},
        {"name": "overfit", "status": "completed", "quality": 0.84, "loss": 0.72, "speed": 0.96},
        {"name": "failed", "status": "failed", "quality": 0.58, "loss": 1.25, "speed": 0.82},
        {"name": "current", "status": "running", "quality": 0.87, "loss": 0.92, "speed": 1.04},
    ]
    if index < len(profiles):
        return profiles[index]
    return {
        "name": f"candidate-{index}",
        "status": "completed",
        "quality": 0.74 + index * 0.015,
        "loss": 1.0 - index * 0.025,
        "speed": 0.9 + index * 0.035,
    }


def _write_rich_steps(logger: RunLogger, profile: dict[str, float | str]) -> None:
    quality = float(profile["quality"])
    loss_scale = float(profile["loss"])
    speed = float(profile["speed"])
    name = str(profile["name"])
    metric_rows = []
    event_rows = []
    best_value = None
    best_step = None
    for step in range(24):
        progress = step / 23
        wave = math.sin(step / 3) * 0.006
        train_loss = loss_scale * (1.18 - 0.78 * progress) + wave
        val_loss = loss_scale * (1.08 - 0.58 * progress) + wave * 0.6
        val_acc = 0.48 + (quality - 0.48) * (1 - math.exp(-3.2 * progress)) + wave
        val_f1 = max(0.0, val_acc - 0.025 + math.cos(step / 4) * 0.004)
        if name == "overfit" and step > 13:
            val_loss += (step - 13) * 0.018
            val_acc -= (step - 13) * 0.004
        if name == "failed" and step > 9:
            val_loss += (step - 9) * 0.05
            val_acc -= (step - 9) * 0.014
        metrics = {
            "train/loss": round(max(train_loss, 0.02), 5),
            "val/loss": round(max(val_loss, 0.02), 5),
            "val/acc": round(max(min(val_acc, 0.99), 0.0), 5),
            "val/f1": round(max(min(val_f1, 0.99), 0.0), 5),
            "lr": round(0.001 * (0.5 + 0.5 * (1 + math.cos(progress * math.pi))), 7),
            "grad_norm": round(1.4 - progress * 0.75 + abs(wave) * 12, 5),
            "throughput": round(420 * speed + step * 2.5, 3),
            "step_time": round(max(0.05, 0.24 / speed - step * 0.002), 5),
            "gpu/memory": round(4.2 + speed * 1.4 + math.sin(step / 5) * 0.16, 4),
        }
        timestamp = datetime.now().astimezone().isoformat()
        for metric_name, value in metrics.items():
            metric_rows.append(
                {
                    "timestamp": timestamp,
                    "step": step,
                    "name": metric_name,
                    "value": value,
                    "group": metric_name.split("/", 1)[0] if "/" in metric_name else "",
                    "metadata_json": json.dumps({"phase": "rich-demo"}),
                }
            )
            event_rows.append(
                {
                    "type": "metric",
                    "key": metric_name,
                    "value": value,
                    "step": step,
                    "metadata": {"phase": "rich-demo"},
                    "timestamp": timestamp,
                }
            )
        if best_value is None or metrics["val/acc"] > best_value:
            best_value = metrics["val/acc"]
            best_step = step
        if step in {0, 8, 16, 23}:
            event_rows.append(
                {
                    "type": "milestone",
                    "key": f"phase-{step}",
                    "value": f"{name} reached step {step}",
                    "step": step,
                    "severity": "info",
                    "timestamp": datetime.now().astimezone().isoformat(),
                }
            )
        if name in {"overfit", "failed"} and step in {14, 18}:
            event_rows.append(
                {
                    "type": "warning",
                    "key": "validation-watch",
                    "value": f"{name} validation trend needs review",
                    "step": step,
                    "severity": "warning",
                    "timestamp": datetime.now().astimezone().isoformat(),
                }
            )
    with (logger.run_dir / "metrics.csv").open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["timestamp", "step", "name", "value", "group", "metadata_json"],
        )
        writer.writerows(metric_rows)
    with (logger.run_dir / "events.jsonl").open("a", encoding="utf-8") as f:
        f.writelines(json.dumps(row) + "\n" for row in event_rows)
    logger.manifest.best_metric = {
        "name": "val/acc",
        "mode": "max",
        "best_value": best_value,
        "best_step": best_step,
        "timestamp": datetime.now().astimezone().isoformat(),
    }


def _write_showcase_evidence(logger: RunLogger, profile: dict[str, float | str]) -> None:
    _write_lightweight_outputs(logger, profile)
    logger.log_table(
        "validation_snapshot",
        [
            {"split": "train", "loss": 0.42, "samples": 2400},
            {"split": "validation", "loss": 0.51, "samples": 600},
        ],
        source="rich-demo",
    )
    checkpoint = logger.run_dir / "_checkpoint.txt"
    checkpoint.write_text(f"checkpoint for {profile['name']}\n", encoding="utf-8")
    logger.log_artifact("checkpoint", checkpoint)
    (logger.run_dir / "report" / "figures").mkdir(parents=True, exist_ok=True)
    (logger.run_dir / "report" / "figures" / "learning_curve.svg").write_text(
        "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 120 40\">"
        "<polyline points=\"0,35 30,22 60,14 90,10 120,8\" fill=\"none\" stroke=\"#2dd4bf\"/>"
        "</svg>\n",
        encoding="utf-8",
    )
    (logger.run_dir / "report" / "tables").mkdir(parents=True, exist_ok=True)
    (logger.run_dir / "report" / "tables" / "leaderboard.csv").write_text(
        "run,metric,value\n"
        f"{profile['name']},val/acc,{profile['quality']}\n",
        encoding="utf-8",
    )
    _write_rule_trace(logger.run_dir, str(profile["name"]))
    _write_agent_workspace(logger.run_dir, str(profile["name"]))


def _write_lightweight_outputs(logger: RunLogger, profile: dict[str, float | str]) -> None:
    logger.run_dir.joinpath("summary.md").write_text(
        f"# Rich Demo Summary\n\nRun `{profile['name']}` uses deterministic local showcase data.\n",
        encoding="utf-8",
    )
    logger.run_dir.joinpath("dashboard.html").write_text(
        "<!doctype html><title>Rich Demo Dashboard</title><h1>Rich Demo Dashboard</h1>\n",
        encoding="utf-8",
    )
    logger.manifest.files["summary"] = "summary.md"
    logger.manifest.files["dashboard"] = "dashboard.html"


def _write_rule_trace(run_dir: Path, run_name: str) -> None:
    rows = [
        {"rule_id": "METRIC-COVERAGE", "outcome": "passed", "step": 4, "severity": "info"},
        {"rule_id": "REPORT-ARTIFACTS", "outcome": "passed", "step": 12, "severity": "info"},
        {
            "rule_id": "VALIDATION-TREND",
            "outcome": "warning" if run_name in {"overfit", "failed"} else "passed",
            "step": 18,
            "severity": "warning" if run_name in {"overfit", "failed"} else "info",
        },
    ]
    (run_dir / "skill_trace.jsonl").write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_agent_workspace(run_dir: Path, run_name: str) -> None:
    agent_dir = run_dir / "agent"
    agent_dir.mkdir(exist_ok=True)
    actions = [
        {
            "action": "inspect",
            "status": "completed",
            "target": "metric coverage",
            "files_changed": ["metrics.csv", "summary.md"],
        },
        {
            "action": "verify",
            "status": "completed" if run_name != "failed" else "needs-review",
            "target": "showcase evidence",
            "files_changed": ["report/tables/leaderboard.csv", "report/figures/learning_curve.svg"],
        },
    ]
    (agent_dir / "actions.jsonl").write_text(
        "".join(json.dumps(action) + "\n" for action in actions),
        encoding="utf-8",
    )
    (agent_dir / "handoff.md").write_text(f"# Handoff\n\nRun `{run_name}` is ready for local review.\n", encoding="utf-8")
    (agent_dir / "decisions.md").write_text("# Decisions\n\n- Keep demo evidence local and deterministic.\n", encoding="utf-8")


def _write_portable_report_package(root_dir: Path, output_dir: Path) -> None:
    from skilllogboard.reports.report_builder import build_report_package

    build_report_package(
        root_dir,
        metric="val/acc",
        mode="max",
        output_dir=output_dir,
        group_by=["model_name"],
        render_mode="package",
    )


if __name__ == "__main__":
    main()
