"""Agent handoff evidence collection and Markdown generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import csv
import json

import yaml

from skilllogboard.agent.action_log import read_agent_actions
from skilllogboard.reports.report_manifest import read_report_manifest


@dataclass
class HandoffEvidence:
    run_dir: str
    manifest: dict[str, Any] = field(default_factory=dict)
    metric_summary: dict[str, Any] = field(default_factory=dict)
    actions: list[dict[str, Any]] = field(default_factory=list)
    rule_summary: dict[str, int] = field(default_factory=dict)
    report_manifest: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_dir": self.run_dir,
            "manifest": self.manifest,
            "metric_summary": self.metric_summary,
            "actions": self.actions,
            "rule_summary": self.rule_summary,
            "report_manifest": self.report_manifest,
            "warnings": self.warnings,
        }


def collect_handoff_evidence(run_dir: str | Path) -> HandoffEvidence:
    run_path = Path(run_dir)
    warnings: list[str] = []
    manifest = _load_yaml(run_path / "manifest.yaml", warnings)
    metric_summary = _read_metric_summary(run_path / "metrics.csv", warnings)
    actions = read_agent_actions(run_path)
    if not actions:
        warnings.append("agent/actions.jsonl not found or empty")
    rule_summary = _read_rule_summary(run_path / "skill_trace.jsonl", warnings)
    report_manifest = {}
    report_manifest_path = run_path / "report" / "report_manifest.yaml"
    if report_manifest_path.exists():
        report_manifest = read_report_manifest(report_manifest_path)
    else:
        warnings.append("report/report_manifest.yaml not found")
    return HandoffEvidence(
        run_dir=str(run_path),
        manifest=manifest,
        metric_summary=metric_summary,
        actions=actions,
        rule_summary=rule_summary,
        report_manifest=report_manifest,
        warnings=warnings,
    )


def build_agent_handoff(
    run_dir: str | Path,
    actor: str | None = None,
    task: str | None = None,
    next_steps: str | None = None,
    output_path: str | Path | None = None,
) -> Path:
    evidence = collect_handoff_evidence(run_dir)
    out = Path(output_path) if output_path else Path(run_dir) / "agent" / "handoff.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(_render_handoff(evidence, actor=actor, task=task, next_steps=next_steps), encoding="utf-8")
    return out


def _render_handoff(
    evidence: HandoffEvidence,
    actor: str | None,
    task: str | None,
    next_steps: str | None,
) -> str:
    manifest = evidence.manifest
    lines = [
        "# Agent Handoff",
        "",
        "## Task",
        "",
        f"- Actor: `{actor or 'unknown'}`",
        f"- Task: {task or 'Unknown; edit this section with the task intent.'}",
        "",
        "## Summary",
        "",
        f"- Run ID: `{manifest.get('run_id', Path(evidence.run_dir).name)}`",
        f"- Status: `{manifest.get('status', 'unknown')}`",
        f"- Main metric: `{(manifest.get('main_metric') or {}).get('name', 'unknown')}`",
        "",
        "## Source Evidence",
        "",
        "- `manifest.yaml`" if manifest else "- `manifest.yaml` missing",
        "- `metrics.csv`" if evidence.metric_summary else "- `metrics.csv` missing or empty",
        "- `skill_trace.jsonl`" if evidence.rule_summary else "- `skill_trace.jsonl` missing or empty",
        "- `report/report_manifest.yaml`" if evidence.report_manifest else "- `report/report_manifest.yaml` missing",
        "",
        "## Commands Run",
        "",
    ]
    command_actions = [action for action in evidence.actions if action.get("command")]
    if command_actions:
        for action in command_actions:
            lines.append(f"- `{action.get('command')}` ({action.get('status')})")
    else:
        lines.append("- No command actions were logged.")
    lines.extend(["", "## Outputs", ""])
    outputs = [output for action in evidence.actions for output in action.get("outputs", [])]
    if outputs:
        lines.extend(f"- `{output}`" for output in outputs)
    else:
        lines.append("- No outputs were logged.")
    lines.extend(["", "## Rule Status", ""])
    if evidence.rule_summary:
        for key in sorted(evidence.rule_summary):
            lines.append(f"- {key}: `{evidence.rule_summary[key]}`")
    else:
        lines.append("- Unknown; no rule trace was found.")
    lines.extend(["", "## Known Issues", ""])
    if evidence.warnings:
        lines.extend(f"- {warning}" for warning in evidence.warnings)
    else:
        lines.append("- None recorded.")
    lines.extend(["", "## Next Recommended Task", "", next_steps or "- Review evidence and choose the next experiment step.", ""])
    return "\n".join(lines)


def _load_yaml(path: Path, warnings: list[str]) -> dict[str, Any]:
    if not path.exists():
        warnings.append(f"{path.name} not found")
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def _read_metric_summary(path: Path, warnings: list[str]) -> dict[str, Any]:
    if not path.exists():
        warnings.append("metrics.csv not found")
        return {}
    latest: dict[str, Any] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("name"):
                latest[row["name"]] = {"value": row.get("value"), "step": row.get("step")}
    return latest


def _read_rule_summary(path: Path, warnings: list[str]) -> dict[str, int]:
    if not path.exists():
        warnings.append("skill_trace.jsonl not found")
        return {}
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            warnings.append("skill_trace.jsonl contains invalid JSON")
            continue
        outcome = str(record.get("outcome", "unknown"))
        counts[outcome] = counts.get(outcome, 0) + 1
    return counts
