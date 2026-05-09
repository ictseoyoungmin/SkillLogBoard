"""RunLogger MVP placeholder.

This file intentionally contains a small working implementation so Week 1 can
verify package installation and basic run folder creation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from skilllogboard.core.artifact_store import ArtifactStore
from skilllogboard.core.config_capture import capture_git, capture_system, save_config, save_json
from skilllogboard.core.events import Event
from skilllogboard.core.manifest import Manifest
from skilllogboard.core.run_id import ensure_unique_run_dir, make_run_id
from skilllogboard.writers.csv_writer import MetricsCsvWriter
from skilllogboard.writers.jsonl_writer import JsonlWriter


class RunLogger:
    def __init__(
        self,
        project: str,
        run_name: str,
        config: dict[str, Any] | None = None,
        root_dir: str | Path = "runs",
        main_metric: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        **metadata: Any,
    ) -> None:
        self.project = project
        self.run_name = run_name
        self.config = config or {}
        self.root_dir = Path(root_dir)
        self.project_dir = self.root_dir / project

        base_run_id = make_run_id(run_name)
        self.run_dir = ensure_unique_run_dir(self.project_dir, base_run_id)
        self.run_id = self.run_dir.name
        self.run_dir.mkdir(parents=True, exist_ok=False)

        self.manifest = Manifest(
            project=project,
            run_name=run_name,
            run_id=self.run_id,
            run_dir=str(self.run_dir),
            main_metric=main_metric,
            tags=tags or [],
            model_name=self.config.get("model_name"),
            dataset_name=self.config.get("dataset_name"),
            seed=self.config.get("seed"),
            framework=metadata.get("framework"),
            task_type=metadata.get("task_type"),
        )
        self.manifest.files.update(
            {
                "manifest": "manifest.yaml",
                "config": "config.yaml",
                "metrics": "metrics.csv",
                "events": "events.jsonl",
                "system": "system.json",
                "git": "git.json",
            }
        )

        save_config(self.config, self.run_dir / "config.yaml")
        save_json(capture_system(), self.run_dir / "system.json")
        save_json(capture_git(), self.run_dir / "git.json")

        self.events = JsonlWriter(self.run_dir / "events.jsonl")
        self.metrics = MetricsCsvWriter(self.run_dir / "metrics.csv")
        self.artifacts = ArtifactStore(self.run_dir)
        self._finished = False

        self.events.write(Event(type="lifecycle", key="start", value="running"))
        self.manifest.save(self.run_dir / "manifest.yaml")

    def log_metric(self, name: str, value: float, step: int | None = None, **metadata: Any) -> None:
        self.metrics.write_metric(name=name, value=value, step=step, metadata=metadata)
        self.events.write(Event(type="metric", key=name, value=value, step=step, metadata=metadata))

    def log_metrics(self, metrics: dict[str, float], step: int | None = None, **metadata: Any) -> None:
        for name, value in metrics.items():
            self.log_metric(name, value, step=step, **metadata)

    def log_config(self, config: dict[str, Any]) -> None:
        self.config.update(config)
        save_config(self.config, self.run_dir / "config.yaml")
        self.events.write(Event(type="config", key="config", value="updated"))

    def log_artifact(self, name: str, path: str | Path, copy: bool = True) -> str:
        rel_path = self.artifacts.log_artifact(name=name, path=path, copy=copy)
        self.events.write(Event(type="artifact", key=name, path=rel_path, metadata={"copy": copy}))
        return rel_path

    def log_note(self, text: str) -> None:
        self.events.write(Event(type="note", key="note", value=text))

    def build_dashboard(self) -> None:
        from skilllogboard.dashboards.static_builder import build_dashboard

        build_dashboard(self.run_dir)
        self.manifest.files["dashboard"] = "dashboard.html"

    def build_report(self) -> None:
        from skilllogboard.reports.markdown_report import build_summary

        build_summary(self.run_dir)
        self.manifest.files["summary"] = "summary.md"

    def finish(self, build_dashboard: bool = False, build_report: bool = False) -> None:
        if build_report:
            self.build_report()
        if build_dashboard:
            self.build_dashboard()
        self.events.write(Event(type="lifecycle", key="finish", value="completed"))
        self.manifest.status = "completed"
        self.manifest.save(self.run_dir / "manifest.yaml")
        self._finished = True

    def fail(self, error: BaseException | str) -> None:
        self.manifest.status = "failed"
        self.manifest.error_summary = str(error)
        self.events.write(Event(type="lifecycle", key="fail", value=str(error)))
        self.manifest.save(self.run_dir / "manifest.yaml")
        self._finished = True

    def __enter__(self) -> "RunLogger":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc is not None:
            self.fail(exc)
            return False
        if not self._finished:
            self.finish(build_dashboard=True, build_report=True)
        return False
