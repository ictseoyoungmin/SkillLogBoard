"""Project-level .skilllog control plane helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path


CONTROL_FILES = {
    "agent_skills.md": "agent_skills.md",
    "experiment_plan.md": "experiment_plan.md",
    "rules.md": "rules.md",
    "report_spec.md": "report_spec.md",
    "README.md": "skilllog_readme.md",
}


@dataclass
class ControlPlaneResult:
    root_dir: str
    skilllog_dir: str
    created: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "root_dir": self.root_dir,
            "skilllog_dir": self.skilllog_dir,
            "created": self.created,
            "skipped": self.skipped,
        }


def ensure_skilllog_control_plane(
    root_dir: str | Path = ".",
    template: str | None = None,
    force: bool = False,
) -> ControlPlaneResult:
    root = Path(root_dir)
    skilllog_dir = root / ".skilllog"
    skilllog_dir.mkdir(parents=True, exist_ok=True)
    result = ControlPlaneResult(str(root), str(skilllog_dir))
    for output_name, template_name in CONTROL_FILES.items():
        target = skilllog_dir / output_name
        if target.exists() and not force:
            result.skipped.append(str(target))
            continue
        text = _template_text(template_name)
        if output_name == "experiment_plan.md" and template:
            text = _apply_template_hint(text, template)
        target.write_text(text, encoding="utf-8")
        result.created.append(str(target))
    return result


def load_agent_template(name: str) -> str:
    return _template_text(name)


def _template_text(name: str) -> str:
    return resources.files("skilllogboard.agent.templates").joinpath(name).read_text(encoding="utf-8")


def _apply_template_hint(text: str, template: str) -> str:
    try:
        from skilllogboard.plugins.registry import get_template

        descriptor = get_template(template)
    except Exception:
        return text.replace("{template_hint}", f"- Template: `{template}`")
    metrics = ", ".join(descriptor.metric_names) if descriptor.metric_names else "TBD"
    return text.replace(
        "{template_hint}",
        f"- Template: `{descriptor.name}`\n- Template status: `{descriptor.status}`\n"
        f"- Suggested metrics: `{metrics}`",
    )
