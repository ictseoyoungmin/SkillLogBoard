"""Agent completion checks."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json


OUTCOME_PASSED = "passed"
OUTCOME_WARNING = "warning"
OUTCOME_ERROR = "error"
OUTCOME_SKIPPED = "skipped"


@dataclass
class AgentCheckResult:
    check_id: str
    name: str
    outcome: str
    severity: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def check_agent_completion(run_dir: str | Path, require_report: bool = False) -> list[AgentCheckResult]:
    run = Path(run_dir)
    results = [
        _file_check("manifest", "Manifest", run / "manifest.yaml", required=True),
        _file_check("config", "Config", run / "config.yaml", required=True),
        _file_check("metrics", "Metrics", run / "metrics.csv", required=True),
        _file_check("skill-trace", "Rule trace", run / "skill_trace.jsonl", required=False),
        _file_check("actions", "Agent actions", run / "agent" / "actions.jsonl", required=True),
        _file_check("handoff", "Agent handoff", run / "agent" / "handoff.md", required=True),
    ]
    results.append(_rule_trace_check(run / "skill_trace.jsonl"))
    if require_report:
        results.append(
            _file_check(
                "report-manifest",
                "Report manifest",
                run / "report" / "report_manifest.yaml",
                required=True,
            )
        )
    return results


def _file_check(check_id: str, name: str, path: Path, required: bool) -> AgentCheckResult:
    if path.exists():
        return AgentCheckResult(check_id, name, OUTCOME_PASSED, "info", f"{name} found.", {"path": str(path)})
    outcome = OUTCOME_ERROR if required else OUTCOME_WARNING
    severity = "error" if required else "warning"
    return AgentCheckResult(check_id, name, outcome, severity, f"{name} missing: {path}", {"path": str(path)})


def _rule_trace_check(path: Path) -> AgentCheckResult:
    if not path.exists():
        return AgentCheckResult(
            "no-error-rules",
            "No error-level rules",
            OUTCOME_WARNING,
            "warning",
            "Rule trace missing; cannot confirm rule status.",
        )
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
        return AgentCheckResult(
            "no-error-rules",
            "No error-level rules",
            OUTCOME_ERROR,
            "error",
            "Error-level rule results found.",
            {"rules": errors},
        )
    return AgentCheckResult(
        "no-error-rules",
        "No error-level rules",
        OUTCOME_PASSED,
        "info",
        "No error-level rule results found.",
    )
