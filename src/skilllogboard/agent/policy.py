"""Agent decision policy."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class AgentDecision:
    outcome: str
    reason: str
    suggested_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def decide_next_action(status: str, severity: str | None = None, retry_count: int = 0) -> AgentDecision:
    normalized_status = (status or "").lower()
    normalized_severity = (severity or "").lower()
    if normalized_status in {"passed", "pass", "ok", "completed"} and normalized_severity not in {"error", "critical"}:
        return AgentDecision("continue", "validation passed")
    if normalized_severity == "warning":
        return AgentDecision("fix-and-retry", "warning can usually be fixed locally", "Apply the suggested fix and rerun validation.")
    if retry_count >= 2 or normalized_severity in {"critical", "blocked"}:
        return AgentDecision("escalate", "retries exhausted or critical issue", "Ask for human review before mutating protected files.")
    if normalized_status in {"failed", "error"} or normalized_severity == "error":
        return AgentDecision("retry", "error may be transient or fixable", "Retry once after inspecting logs.")
    return AgentDecision("stop", "unknown state", "Collect handoff evidence before continuing.")
