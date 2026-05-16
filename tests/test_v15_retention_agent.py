import json

import yaml

from skilllogboard.agent.feedback import feedback_list
from skilllogboard.agent.handoff import build_agent_handoff, read_agent_handoff_json
from skilllogboard.agent.policy import decide_next_action
from skilllogboard.agent.safety import AgentSafetyGate
from skilllogboard.cli.main import main
from skilllogboard.retention.jsonl import rotate_jsonl
from skilllogboard.retention.planner import plan_prune
from skilllogboard.retention.policy import RetentionPolicy


def _run(root, name, baseline=False):
    run_dir = root / name
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": name, "status": "completed", "baseline": baseline}),
        encoding="utf-8",
    )
    (run_dir / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\n,1,score,1.0,val,{}\n",
        encoding="utf-8",
    )
    return run_dir


def test_prune_planner_is_dry_run_and_protects_baseline(tmp_path):
    _run(tmp_path, "baseline", baseline=True)
    _run(tmp_path, "old")

    plan = plan_prune(tmp_path, RetentionPolicy(keep_latest=0, keep_best=0, dry_run=True))

    assert plan["dry_run"] is True
    by_id = {action["run_id"]: action for action in plan["actions"]}
    assert by_id["baseline"]["action"] == "keep"
    assert by_id["old"]["action"] == "archive"


def test_jsonl_rotation_cli_defaults_to_dry_run(tmp_path, capsys):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "events.jsonl").write_text('{"type":"a"}\n{"type":"b"}\n', encoding="utf-8")

    assert main(["rotate", str(run_dir), "--max-lines", "1", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["dry_run"] is True
    assert payload["should_rotate"] is True

    plan = rotate_jsonl(run_dir / "events.jsonl", max_lines=1, dry_run=False)
    assert plan.should_rotate is True
    assert (run_dir / "events.jsonl.1.jsonl").exists()
    assert (run_dir / "events.jsonl.summary.json").exists()


def test_agent_safety_policy_feedback_and_json_handoff(tmp_path):
    gate = AgentSafetyGate()
    assert not gate.evaluate_path("pyproject.toml").allowed
    assert gate.evaluate_path("docs/operational_rules.md").allowed
    assert decide_next_action("failed", "error", retry_count=2).outcome == "escalate"
    assert feedback_list([{"outcome": "error", "code": "X", "message": "broken"}])[0]["errors"] == ["broken"]

    run_dir = _run(tmp_path, "agent-run")
    out = build_agent_handoff(run_dir, actor="codex", task="v1.5", next_steps="Run pytest.")
    payload = read_agent_handoff_json(out.with_name("handoff.json"))
    assert payload["summary"]["task"] == "v1.5"
    assert "Run pytest." in payload["next_actions"]
