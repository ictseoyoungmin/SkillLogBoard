import json

from skilllogboard.agent.action_log import append_agent_action
from skilllogboard.agent.handoff import build_agent_handoff
from skilllogboard.skills.agent_rules import (
    agent_actions_required,
    agent_handoff_required,
    agent_no_error_rules,
    agent_required_commands,
)
from skilllogboard.skills.parser import RuleSpec
from skilllogboard.skills.rules import execute_rule


def test_agent_rule_helpers_handle_missing_and_present_files(tmp_path):
    assert agent_handoff_required(tmp_path).outcome == "error"
    assert agent_actions_required(tmp_path).outcome == "error"

    append_agent_action(tmp_path, {"actor": "codex", "action": "x", "status": "completed"})
    build_agent_handoff(tmp_path)
    (tmp_path / "skill_trace.jsonl").write_text(
        json.dumps({"rule_id": "RULE-1", "outcome": "passed", "severity": "warning"}) + "\n",
        encoding="utf-8",
    )

    assert agent_handoff_required(tmp_path).outcome == "passed"
    assert agent_actions_required(tmp_path).outcome == "passed"
    assert agent_no_error_rules(tmp_path).outcome == "passed"


def test_agent_rules_integrate_with_builtin_executor(tmp_path):
    append_agent_action(tmp_path, {"actor": "codex", "action": "x", "status": "completed"})
    build_agent_handoff(tmp_path)

    result = execute_rule(
        RuleSpec("RULE-AGENT", "agent_handoff_required", severity="error"),
        {"run_dir": str(tmp_path)},
    )

    assert result.outcome == "passed"


def test_agent_required_commands_checks_completed_command_substrings(tmp_path):
    append_agent_action(
        tmp_path,
        {
            "actor": "codex",
            "action": "run tests",
            "status": "completed",
            "command": "pytest -q tests/test_agent_rules.py",
        },
    )
    append_agent_action(
        tmp_path,
        {
            "actor": "codex",
            "action": "run lint",
            "status": "failed",
            "command": "ruff check .",
        },
    )

    passed = agent_required_commands(tmp_path, ["pytest -q"])
    missing = agent_required_commands(tmp_path, ["ruff check ."], severity="warning")
    builtin = execute_rule(
        RuleSpec("RULE-CMD", "agent_required_commands", params={"keys": ["pytest -q"]}),
        {"run_dir": str(tmp_path)},
    )

    assert passed.outcome == "passed"
    assert missing.outcome == "warning"
    assert missing.details["missing"] == ["ruff check ."]
    assert builtin.outcome == "passed"
