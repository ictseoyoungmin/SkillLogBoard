import json

from skilllogboard import RunLogger
from skilllogboard.agent.action_log import append_agent_action
from skilllogboard.agent.checks import AgentCheckResult, check_agent_completion
from skilllogboard.agent.handoff import build_agent_handoff


def _make_run(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="agent-check",
        root_dir=tmp_path / "runs",
        config={"model_name": "Tiny", "dataset_name": "Demo", "seed": 1},
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metric("val/acc", 0.8, step=1)
    logger.finish()
    return logger.run_dir


def test_agent_check_result_serializes():
    result = AgentCheckResult("x", "Check", "passed", "info", "ok")
    assert result.to_dict()["outcome"] == "passed"


def test_agent_completion_checks_missing_agent_files_are_errors(tmp_path):
    run_dir = _make_run(tmp_path)

    results = check_agent_completion(run_dir)

    errors = {result.check_id for result in results if result.outcome == "error"}
    assert "actions" in errors
    assert "handoff" in errors


def test_agent_completion_checks_pass_after_handoff_and_actions(tmp_path):
    run_dir = _make_run(tmp_path)
    (run_dir / "skill_trace.jsonl").write_text(
        json.dumps({"rule_id": "RULE-1", "outcome": "passed", "severity": "warning"}) + "\n",
        encoding="utf-8",
    )
    append_agent_action(run_dir, {"actor": "codex", "action": "done", "status": "completed"})
    build_agent_handoff(run_dir)

    results = check_agent_completion(run_dir)

    assert not [result for result in results if result.outcome == "error"]


def test_agent_completion_checks_detect_error_rules_and_required_report(tmp_path):
    run_dir = _make_run(tmp_path)
    (run_dir / "skill_trace.jsonl").write_text(
        json.dumps({"rule_id": "RULE-ERR", "outcome": "error", "severity": "error"}) + "\n",
        encoding="utf-8",
    )
    append_agent_action(run_dir, {"actor": "codex", "action": "done", "status": "completed"})
    build_agent_handoff(run_dir)

    results = check_agent_completion(run_dir, require_report=True)

    errors = {result.check_id for result in results if result.outcome == "error"}
    assert "no-error-rules" in errors
    assert "report-manifest" in errors
