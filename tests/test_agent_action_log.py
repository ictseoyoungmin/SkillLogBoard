import json

from skilllogboard.agent.action_log import AgentAction, append_agent_action, read_agent_actions


def test_agent_action_schema_minimal_and_full():
    minimal = AgentAction(actor="codex", action="run tests", status="completed")
    full = AgentAction(
        actor="codex",
        action="build report",
        status="completed",
        target="report",
        command="skilllog report build",
        outputs=["report/report.md"],
        duration_sec=1.5,
        metadata={"metric": "val/acc"},
    )

    assert minimal.to_dict()["actor"] == "codex"
    assert full.to_dict()["outputs"] == ["report/report.md"]
    json.dumps(full.to_dict())


def test_append_and_read_agent_actions_preserves_order(tmp_path):
    append_agent_action(tmp_path, {"actor": "a", "action": "first", "status": "completed"})
    append_agent_action(tmp_path, {"actor": "a", "action": "second", "status": "completed"})

    records = read_agent_actions(tmp_path)

    assert (tmp_path / "agent" / "actions.jsonl").exists()
    assert [record["action"] for record in records] == ["first", "second"]


def test_read_agent_actions_missing_returns_empty(tmp_path):
    assert read_agent_actions(tmp_path) == []
