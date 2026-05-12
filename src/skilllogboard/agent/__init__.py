"""Local-first agent research workflow helpers."""

from skilllogboard.agent.action_log import AgentAction, append_agent_action, read_agent_actions
from skilllogboard.agent.checks import (
    OUTCOME_ERROR,
    OUTCOME_PASSED,
    OUTCOME_SKIPPED,
    OUTCOME_WARNING,
    AgentCheckResult,
    check_agent_completion,
)
from skilllogboard.agent.decisions import append_agent_decision
from skilllogboard.agent.handoff import HandoffEvidence, build_agent_handoff, collect_handoff_evidence
from skilllogboard.agent.skills import ControlPlaneResult, ensure_skilllog_control_plane, load_agent_template

__all__ = [
    "AgentAction",
    "AgentCheckResult",
    "ControlPlaneResult",
    "HandoffEvidence",
    "OUTCOME_ERROR",
    "OUTCOME_PASSED",
    "OUTCOME_SKIPPED",
    "OUTCOME_WARNING",
    "append_agent_action",
    "append_agent_decision",
    "build_agent_handoff",
    "check_agent_completion",
    "collect_handoff_evidence",
    "ensure_skilllog_control_plane",
    "load_agent_template",
    "read_agent_actions",
]
