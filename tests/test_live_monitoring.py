from skilllogboard.live.monitor_loop import sample_once
from skilllogboard.live.monitoring import (
    MonitoringRecord,
    append_monitoring_record,
    read_monitoring_records,
)


def test_monitoring_jsonl_append_read_roundtrip(tmp_path):
    append_monitoring_record(
        tmp_path,
        MonitoringRecord(source="system", type="system", metrics={"cpu_percent": 1.0}),
    )

    records = read_monitoring_records(tmp_path)

    assert records[0]["source"] == "system"
    assert records[0]["metrics"]["cpu_percent"] == 1.0


def test_read_monitoring_missing_file_returns_empty(tmp_path):
    assert read_monitoring_records(tmp_path) == []


def test_sample_once_can_write_skipped_records_when_optional_monitor_missing(tmp_path, monkeypatch):
    monkeypatch.setattr("skilllogboard.live.monitor_loop.sample_system_metrics", lambda: {
        "source": "system",
        "type": "system",
        "metrics": {"cpu_percent": 1},
    })

    records = sample_once(tmp_path, monitor_system=True)

    assert records[0]["metrics"]["cpu_percent"] == 1
    assert read_monitoring_records(tmp_path)[0]["source"] == "system"
