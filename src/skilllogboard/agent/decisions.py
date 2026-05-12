"""Markdown decision log helpers for run-level agent notes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def append_agent_decision(
    run_dir: str | Path,
    actor: str,
    topic: str,
    decision: str,
    reason: str,
    alternatives: list[str] | None = None,
    impact: str | None = None,
) -> Path:
    path = Path(run_dir) / "agent" / "decisions.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("# Agent Decisions\n\n", encoding="utf-8")
    lines = [
        f"## {topic}",
        "",
        f"- Timestamp: `{datetime.now().astimezone().isoformat()}`",
        f"- Actor: `{actor}`",
        f"- Decision: {decision}",
        f"- Reason: {reason}",
    ]
    if alternatives:
        lines.append(f"- Alternatives: {', '.join(alternatives)}")
    if impact:
        lines.append(f"- Impact: {impact}")
    lines.append("")
    with path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path
