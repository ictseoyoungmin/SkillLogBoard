"""RunLogger v0.1 MVP implementation."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import math

from skilllogboard.core.artifact_store import ArtifactStore
from skilllogboard.core.config_capture import capture_git, capture_system, save_config, save_json
from skilllogboard.core.events import Event
from skilllogboard.core.manifest import Manifest
from skilllogboard.core.run import STATUS_COMPLETED, STATUS_FAILED, STATUS_RUNNING, TERMINAL_STATUSES
from skilllogboard.core.run_id import ensure_unique_run_dir, make_run_id
from skilllogboard.writers.csv_writer import MetricsCsvWriter
from skilllogboard.writers.image_writer import validate_image_path
from skilllogboard.writers.jsonl_writer import JsonlWriter
from skilllogboard.writers.table_writer import save_table


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
                "artifact_index": "artifact_index.json",
            }
        )

        save_config(self.config, self.run_dir / "config.yaml")
        save_json(capture_system(), self.run_dir / "system.json")
        save_json(capture_git(), self.run_dir / "git.json")

        self.events = JsonlWriter(self.run_dir / "events.jsonl")
        self.metrics = MetricsCsvWriter(self.run_dir / "metrics.csv")
        self.artifacts = ArtifactStore(self.run_dir)
        self._finished = False

        self.events.write(Event(type="lifecycle", key="start", value=STATUS_RUNNING))
        self.manifest.save(self.run_dir / "manifest.yaml")

    def log_metric(self, name: str, value: float, step: int | None = None, **metadata: Any) -> None:
        numeric_value = self._validate_metric(name=name, value=value, step=step)
        self.metrics.write_metric(name=name, value=numeric_value, step=step, metadata=metadata)
        self.events.write(
            Event(type="metric", key=name, value=numeric_value, step=step, metadata=metadata)
        )
        self._maybe_update_best_metric(name=name, value=numeric_value, step=step)

    def log_metrics(self, metrics: dict[str, float], step: int | None = None, **metadata: Any) -> None:
        for name, value in metrics.items():
            self.log_metric(name, value, step=step, **metadata)

    def log_config(self, config: dict[str, Any]) -> None:
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")
        self.config.update(config)
        save_config(self.config, self.run_dir / "config.yaml")
        self.manifest.model_name = self.config.get("model_name")
        self.manifest.dataset_name = self.config.get("dataset_name")
        self.manifest.seed = self.config.get("seed")
        self.manifest.save(self.run_dir / "manifest.yaml")
        self.events.write(
            Event(
                type="config",
                key="config",
                value="updated",
                metadata={"keys": list(config.keys()), "merge": "shallow"},
            )
        )

    def log_artifact(self, name: str, path: str | Path, copy: bool = True) -> str:
        record = self.artifacts.log_artifact(name=name, path=path, copy=copy)
        self.events.write(
            Event(
                type="artifact",
                key=name,
                path=record.get("path") or record.get("source"),
                metadata={key: value for key, value in record.items() if key not in {"name", "type"}},
            )
        )
        return str(record.get("path") or record.get("source"))

    def log_image(self, name: str, image: str | Path, step: int | None = None, **metadata: Any) -> str:
        image_path = validate_image_path(image)
        record = self.artifacts.record_file(
            name=name,
            path=image_path,
            copy=True,
            kind="image",
            subdir="images",
        )
        self.events.write(
            Event(
                type="image",
                key=name,
                step=step,
                path=record.get("path"),
                metadata={**metadata, "source": record["source"], "size": record["size"]},
            )
        )
        return str(record["path"])

    def log_table(self, name: str, table: Any, **metadata: Any) -> str:
        table_path = save_table(name, table, self.run_dir / "tables")
        rel_path = table_path.relative_to(self.run_dir).as_posix()
        record = self.artifacts.add_record(
            {
                "name": name,
                "type": "table",
                "source": None,
                "path": rel_path,
                "copy": True,
                "size": table_path.stat().st_size,
                "timestamp": datetime.now().astimezone().isoformat(),
                "metadata": metadata,
            }
        )
        self.events.write(Event(type="table", key=name, path=rel_path, metadata=metadata))
        return str(record["path"])

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
        if self.manifest.status in TERMINAL_STATUSES:
            self._finished = True
            return
        if build_report:
            self.build_report()
        if build_dashboard:
            self.build_dashboard()
        self._set_status(STATUS_COMPLETED, event_key="finish")

    def fail(self, error: BaseException | str) -> None:
        if self.manifest.status in TERMINAL_STATUSES:
            self._finished = True
            return
        self._set_status(STATUS_FAILED, error_summary=str(error), event_key="fail")

    def close(self) -> None:
        self.finish()

    def __enter__(self) -> "RunLogger":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc is not None:
            self.fail(exc)
            return False
        if not self._finished:
            self.finish(build_dashboard=True, build_report=True)
        return False

    def _set_status(
        self,
        status: str,
        error_summary: str | None = None,
        event_key: str | None = None,
    ) -> None:
        self.manifest.status = status
        if error_summary is not None:
            self.manifest.error_summary = error_summary
        if event_key is not None:
            self.events.write(
                Event(
                    type="lifecycle",
                    key=event_key,
                    value=status if error_summary is None else error_summary,
                )
            )
        self.manifest.save(self.run_dir / "manifest.yaml")
        self._finished = status in TERMINAL_STATUSES

    def _validate_metric(self, name: str, value: float, step: int | None = None) -> float:
        if not isinstance(name, str) or not name:
            raise ValueError("metric name must be a non-empty string")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("metric value must be an int or float")
        numeric_value = float(value)
        if not math.isfinite(numeric_value):
            raise ValueError("metric value must be finite")
        if step is not None and (isinstance(step, bool) or not isinstance(step, int)):
            raise TypeError("metric step must be None or an int")
        return numeric_value

    def _maybe_update_best_metric(self, name: str, value: float, step: int | None) -> None:
        main_metric = self.manifest.main_metric or {}
        if main_metric.get("name") != name:
            return
        mode = main_metric.get("mode", "max")
        if mode not in {"max", "min"}:
            raise ValueError("main_metric mode must be 'max' or 'min'")
        current = self.manifest.best_metric
        current_value = None if current is None else current.get("best_value")
        improved = current_value is None
        if current_value is not None and mode == "max":
            improved = value > float(current_value)
        if current_value is not None and mode == "min":
            improved = value < float(current_value)
        if not improved:
            return
        self.manifest.best_metric = {
            "name": name,
            "mode": mode,
            "best_value": value,
            "best_step": step,
            "timestamp": datetime.now().astimezone().isoformat(),
        }
        self.manifest.save(self.run_dir / "manifest.yaml")
