"""Agent-specific rule helpers using existing RuleResult shape."""

from __future__ import annotations

from pathlib import Path
import json

from skilllogboard.skills.parser import RuleSpec
from skilllogboard.skills.rules import OUTCOME_PASSED, RuleResult

COMMAND_SUCCESS_STATUSES = {"completed", "passed", "success", "ok"}


def agent_handoff_required(run_dir: str | Path, severity: str = "error") -> RuleResult:
    spec = RuleSpec("AGENT-HANDOFF-REQUIRED", "agent_handoff_required", severity=severity)
    path = Path(run_dir) / "agent" / "handoff.md"
    if path.exists():
        return _passed(spec, "Agent handoff found.", {"path": str(path)})
    return _failure(spec, f"Missing agent handoff: {path}", {"path": str(path)})


def agent_actions_required(run_dir: str | Path, severity: str = "error") -> RuleResult:
    spec = RuleSpec("AGENT-ACTIONS-REQUIRED", "agent_actions_required", severity=severity)
    path = Path(run_dir) / "agent" / "actions.jsonl"
    if path.exists() and path.read_text(encoding="utf-8").strip():
        return _passed(spec, "Agent actions found.", {"path": str(path)})
    return _failure(spec, f"Missing agent actions: {path}", {"path": str(path)})


def agent_no_error_rules(run_dir: str | Path, severity: str = "error") -> RuleResult:
    spec = RuleSpec("AGENT-NO-ERROR-RULES", "agent_no_error_rules", severity=severity)
    path = Path(run_dir) / "skill_trace.jsonl"
    if not path.exists():
        return _failure(spec, f"Missing skill trace: {path}", {"path": str(path)})
    errors = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("outcome") == "error" or record.get("severity") == "error":
            errors.append(record.get("rule_id", "unknown"))
    if errors:
        return _failure(spec, "Error-level rule results found.", {"rules": errors})
    return _passed(spec, "No error-level rule results found.", {})


def agent_required_commands(
    run_dir: str | Path,
    commands: list[str] | tuple[str, ...] | str,
    severity: str = "error",
) -> RuleResult:
    spec = RuleSpec("AGENT-REQUIRED-COMMANDS", "agent_required_commands", severity=severity)
    required = _as_list(commands)
    if not required:
        return _failure(spec, "Missing required commands.", {"missing": ["commands"]})
    path = Path(run_dir) / "agent" / "actions.jsonl"
    if not path.exists():
        return _failure(spec, f"Missing agent actions: {path}", {"path": str(path), "missing": required})

    matched: dict[str, str] = {}
    for action in _read_action_records(path):
        command = str(action.get("command", ""))
        status = str(action.get("status", "")).lower()
        if not command or status not in COMMAND_SUCCESS_STATUSES:
            continue
        for required_command in required:
            if required_command in command and required_command not in matched:
                matched[required_command] = command

    missing = [command for command in required if command not in matched]
    if missing:
        return _failure(spec, f"Missing required agent commands: {', '.join(missing)}", {"missing": missing})
    return _passed(spec, "Required agent commands were logged.", {"commands": required, "matched": matched})


def _passed(spec: RuleSpec, message: str, details: dict) -> RuleResult:
    return RuleResult(spec.rule_id, spec.rule_type, spec.severity, spec.status, OUTCOME_PASSED, message, details)


def _failure(spec: RuleSpec, message: str, details: dict) -> RuleResult:
    outcome = "error" if spec.severity == "error" else "warning"
    return RuleResult(spec.rule_id, spec.rule_type, spec.severity, spec.status, outcome, message, details)


def _as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return [str(value)]


def _read_action_records(path: Path) -> list[dict]:
    records: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    return records
