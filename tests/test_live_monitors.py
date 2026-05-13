from types import SimpleNamespace
import subprocess

from skilllogboard.live.monitors import sample_gpu_metrics, sample_process_metrics, sample_system_metrics


def test_system_and_process_monitors_do_not_crash_without_psutil(monkeypatch):
    monkeypatch.setattr("skilllogboard.live.monitors._import_psutil", lambda: None)

    assert sample_system_metrics()["skipped"] is True
    assert sample_process_metrics()["skipped"] is True


def test_gpu_monitor_parses_nvidia_smi_output(monkeypatch):
    def fake_run(*args, **kwargs):
        return SimpleNamespace(stdout="0, 55, 1024, 8192, 61\n")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = sample_gpu_metrics()

    assert result["metrics"]["gpus"][0]["index"] == 0
    assert result["metrics"]["gpus"][0]["utilization_percent"] == 55.0
