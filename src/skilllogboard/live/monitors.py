"""Optional system, process, and GPU monitors."""

from __future__ import annotations

from typing import Any
import os
import subprocess


def sample_system_metrics() -> dict[str, Any]:
    psutil = _import_psutil()
    if psutil is None:
        return _skipped("system", "psutil is not installed; install skilllogboard[live].")
    try:
        return {
            "source": "system",
            "type": "system",
            "metrics": {
                "cpu_percent": psutil.cpu_percent(interval=None),
                "ram_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage(os.getcwd()).percent,
            },
        }
    except Exception as exc:
        return _skipped("system", f"system metrics unavailable: {exc}")


def sample_process_metrics(pid: int | None = None) -> dict[str, Any]:
    psutil = _import_psutil()
    if psutil is None:
        return _skipped("process", "psutil is not installed; install skilllogboard[live].")
    try:
        process = psutil.Process(pid or os.getpid())
        return {
            "source": "process",
            "type": "process",
            "metrics": {
                "pid": process.pid,
                "rss_mb": round(process.memory_info().rss / (1024 * 1024), 3),
                "cpu_percent": process.cpu_percent(interval=None),
            },
        }
    except Exception as exc:
        return _skipped("process", f"process metrics unavailable: {exc}")


def sample_gpu_metrics() -> dict[str, Any]:
    command = [
        "nvidia-smi",
        "--query-gpu=index,utilization.gpu,memory.used,memory.total,temperature.gpu",
        "--format=csv,noheader,nounits",
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=2)
    except Exception as exc:
        return _skipped("gpu", f"nvidia-smi unavailable: {exc}")
    gpus = []
    for line in result.stdout.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 5:
            continue
        gpus.append(
            {
                "index": _as_int(parts[0]),
                "utilization_percent": _as_float(parts[1]),
                "memory_used_mb": _as_float(parts[2]),
                "memory_total_mb": _as_float(parts[3]),
                "temperature_c": _as_float(parts[4]),
            }
        )
    if not gpus:
        return _skipped("gpu", "nvidia-smi returned no parseable GPU rows.")
    return {"source": "gpu", "type": "gpu", "metrics": {"gpus": gpus}}


def _import_psutil():
    try:
        import psutil  # type: ignore
    except ImportError:
        return None
    return psutil


def _skipped(source: str, reason: str) -> dict[str, Any]:
    return {"source": source, "type": source, "metrics": {}, "skipped": True, "warning": reason}


def _as_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: str) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
