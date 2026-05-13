"""Active monitoring loop helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import threading

from skilllogboard.live.monitoring import append_monitoring_record
from skilllogboard.live.monitors import (
    sample_gpu_metrics,
    sample_process_metrics,
    sample_system_metrics,
)


def sample_once(
    run_dir: str | Path,
    monitor_system: bool = False,
    monitor_gpu: bool = False,
    monitor_process: bool = False,
) -> list[dict[str, Any]]:
    records = []
    if monitor_system:
        records.append(sample_system_metrics())
    if monitor_process:
        records.append(sample_process_metrics())
    if monitor_gpu:
        records.append(sample_gpu_metrics())
    for record in records:
        append_monitoring_record(run_dir, record)
    return records


class MonitorLoop:
    def __init__(
        self,
        run_dir: str | Path,
        interval: float = 1.0,
        monitor_system: bool = False,
        monitor_gpu: bool = False,
        monitor_process: bool = False,
    ) -> None:
        self.run_dir = Path(run_dir)
        self.interval = interval
        self.monitor_system = monitor_system
        self.monitor_gpu = monitor_gpu
        self.monitor_process = monitor_process
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def sample_once(self) -> list[dict[str, Any]]:
        return sample_once(
            self.run_dir,
            monitor_system=self.monitor_system,
            monitor_gpu=self.monitor_gpu,
            monitor_process=self.monitor_process,
        )

    def start(self) -> None:
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=max(1.0, self.interval * 2))
            self._thread = None

    def _run(self) -> None:
        while not self._stop.is_set():
            self.sample_once()
            self._stop.wait(self.interval)
