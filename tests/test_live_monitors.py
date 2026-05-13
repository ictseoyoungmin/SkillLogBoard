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


def test_gpu_monitor_reports_missing_nvidia_smi(monkeypatch):
    def fake_run(*args, **kwargs):
        raise FileNotFoundError("nvidia-smi")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = sample_gpu_metrics()

    assert result["skipped"] is True
    assert "nvidia-smi unavailable" in result["warning"]


def test_gpu_monitor_warns_on_empty_output(monkeypatch):
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: SimpleNamespace(stdout=""))

    result = sample_gpu_metrics()

    assert result["skipped"] is True
    assert "no parseable GPU rows" in result["warning"]


def test_gpu_monitor_warns_on_malformed_output(monkeypatch):
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(stdout="this is not csv\n"),
    )

    result = sample_gpu_metrics()

    assert result["skipped"] is True
    assert "no parseable GPU rows" in result["warning"]
