import json

from skilllogboard.live.readers import (
    read_artifacts,
    read_events,
    read_manifest,
    read_metrics,
    read_rule_trace,
    tail_log_file,
)


def test_live_readers_handle_missing_files(tmp_path):
    manifest, warnings = read_manifest(tmp_path)
    metrics, latest, metric_warnings = read_metrics(tmp_path)

    assert manifest == {}
    assert warnings
    assert metrics == []
    assert latest == {}
    assert metric_warnings


def test_live_readers_parse_run_files(tmp_path):
    (tmp_path / "manifest.yaml").write_text("run_id: r1\nstatus: running\n", encoding="utf-8")
    (tmp_path / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\n"
        "t,1,val/acc,0.8,val,{}\n",
        encoding="utf-8",
    )
    (tmp_path / "events.jsonl").write_text(json.dumps({"type": "note", "key": "x"}) + "\n", encoding="utf-8")
    (tmp_path / "skill_trace.jsonl").write_text(
        json.dumps({"rule_id": "RULE-1", "outcome": "passed"}) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "artifact_index.json").write_text(
        json.dumps({"artifacts": [{"name": "model", "path": "artifacts/model.txt"}]}),
        encoding="utf-8",
    )

    manifest, _ = read_manifest(tmp_path)
    rows, latest, _ = read_metrics(tmp_path)
    events, _ = read_events(tmp_path)
    rules, _ = read_rule_trace(tmp_path)
    artifacts, _ = read_artifacts(tmp_path)

    assert manifest["status"] == "running"
    assert rows[0]["value"] == 0.8
    assert latest["val/acc"]["step"] == 1
    assert events[0]["type"] == "note"
    assert rules[0]["rule_id"] == "RULE-1"
    assert artifacts[0]["name"] == "model"


def test_tail_log_file_is_limited(tmp_path):
    log = tmp_path / "train.log"
    log.write_text("\n".join(f"line {idx}" for idx in range(20)), encoding="utf-8")

    lines, warnings = tail_log_file(log, limit=3)

    assert warnings == []
    assert lines == ["line 17", "line 18", "line 19"]
