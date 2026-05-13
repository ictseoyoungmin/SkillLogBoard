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
    assert state["metric_catalog"][0]["name"] == "val/acc"
    assert state["selected_metrics"] == ["val/acc"]
    assert state["pinned_metrics"] == ["val/acc"]
    assert state["context_markers"][0]["source"] == "event"
    assert state["agent_workspace"]["actions_count"] == 0


def test_build_live_run_state_warns_for_missing_files(tmp_path):
    state = build_live_run_state(tmp_path)

    assert state.status == "unknown"
    assert "missing manifest.yaml" in state.warnings
    assert "missing metrics.csv" in state.warnings


def test_live_run_state_reads_report_and_agent_workspace(tmp_path):
    (tmp_path / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": "r1", "status": "completed"}),
        encoding="utf-8",
    )
    (tmp_path / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\nt,1,score,3.0,eval,{}\n",
        encoding="utf-8",
    )
    (tmp_path / "summary.md").write_text("# Summary\n", encoding="utf-8")
    agent_dir = tmp_path / "agent"
    agent_dir.mkdir()
    (agent_dir / "actions.jsonl").write_text(
        json.dumps({"action": "verify", "status": "completed"}) + "\n",
        encoding="utf-8",
    )
    (agent_dir / "handoff.md").write_text("# Handoff\n", encoding="utf-8")

    state = build_live_run_state(tmp_path).to_dict()

    assert state["report_artifacts"][0]["name"] == "summary.md"
    assert state["agent_workspace"]["actions_count"] == 1
    assert state["agent_workspace"]["handoff"] is True
