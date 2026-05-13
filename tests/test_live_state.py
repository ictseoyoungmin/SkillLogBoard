import json

import yaml

from skilllogboard.live.state import build_live_run_state


def test_build_live_run_state_aggregates_local_files(tmp_path):
    (tmp_path / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": "r1", "status": "running"}),
        encoding="utf-8",
    )
    (tmp_path / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\n"
        "t0,0,val/acc,0.5,val,{}\n"
        "t1,1,val/acc,0.7,val,{}\n",
        encoding="utf-8",
    )
    (tmp_path / "events.jsonl").write_text(
        json.dumps({"type": "note", "message": "started"}) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "skill_trace.jsonl").write_text(
        json.dumps({"rule_id": "RULE-1", "outcome": "passed"}) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "monitoring.jsonl").write_text(
        json.dumps({"source": "system", "type": "system", "metrics": {"cpu_percent": 1}})
        + "\n",
        encoding="utf-8",
    )
    log_file = tmp_path / "train.log"
    log_file.write_text("one\ntwo\n", encoding="utf-8")

    state = build_live_run_state(tmp_path, limits={"logs": 1}, log_file=log_file).to_dict()

    assert state["mode"] == "run"
    assert state["status"] == "running"
    assert state["metrics"]["val/acc"]["value"] == 0.7
    assert state["events"][0]["type"] == "note"
    assert state["rules"][0]["rule_id"] == "RULE-1"
    assert state["monitoring"][0]["source"] == "system"
    assert state["logs"] == ["two"]


def test_build_live_run_state_warns_for_missing_files(tmp_path):
    state = build_live_run_state(tmp_path)

    assert state.status == "unknown"
    assert "missing manifest.yaml" in state.warnings
    assert "missing metrics.csv" in state.warnings
