"""TemplateSpec.md contract, parser, and deterministic draft generation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from importlib import resources
from pathlib import Path
from typing import Any
import re

import yaml

from skilllogboard.template_forge.research_brief import ResearchBrief

TEMPLATE_STATUSES = {"Draft", "Scaffolded", "Implemented", "Planned"}


@dataclass
class TemplateSpec:
    template_name: str
    category: str = "custom"
    description: str = ""
    default_config: dict[str, Any] = field(default_factory=dict)
    metric_names: list[str] = field(default_factory=list)
    required_rules: list[str] = field(default_factory=list)
    recommended_tables: list[str] = field(default_factory=list)
    recommended_figures: list[str] = field(default_factory=list)
    synthetic_example_plan: str = "TODO: describe dependency-light synthetic data generation."
    dependency_policy: list[str] = field(default_factory=list)
    required_outputs: list[str] = field(default_factory=list)
    experiment_axes: list[str] = field(default_factory=list)
    status: str = "Draft"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_template_spec_template() -> str:
    return resources.files("skilllogboard.template_forge.harness").joinpath(
        "template_spec_template.md"
    ).read_text(encoding="utf-8")


def parse_template_spec(path: str | Path) -> TemplateSpec:
    return parse_template_spec_text(Path(path).read_text(encoding="utf-8"))


def parse_template_spec_text(text: str) -> TemplateSpec:
    sections = _markdown_sections(text)
    name = _first_text(sections, "template_name") or "custom-template"
    status = _first_text(sections, "status") or "Draft"
    if status not in TEMPLATE_STATUSES:
        status = "Draft"
    return TemplateSpec(
        template_name=name,
        category=_first_text(sections, "category") or "custom",
        description=_first_text(sections, "description"),
        default_config=_parse_mapping(sections.get("default_config", "")),
        metric_names=_list_text(sections, "metric_names", "metrics"),
        required_rules=_list_text(sections, "required_rules", "rules"),
        recommended_tables=_list_text(sections, "recommended_tables", "tables"),
        recommended_figures=_list_text(sections, "recommended_figures", "figures"),
        synthetic_example_plan=_first_text(sections, "synthetic_example_plan")
        or "TODO: describe dependency-light synthetic data generation.",
        dependency_policy=_list_text(sections, "dependency_policy"),
        required_outputs=_list_text(sections, "required_outputs"),
        experiment_axes=_list_text(sections, "experiment_axes", "axes"),
        status=status,
    )


def draft_template_spec_from_brief(
    brief: ResearchBrief,
    template_name: str | None = None,
) -> TemplateSpec:
    name = template_name or _slugify(brief.task_type or brief.research_topic or "custom-template")
    metrics = [metric for metric in [brief.main_metric, *brief.secondary_metrics] if metric]
    rules = ["required_config", "required_metric"]
    if brief.main_metric:
        rules.append("metric_threshold")
    return TemplateSpec(
        template_name=name,
        category=brief.task_type or "custom",
        description=brief.research_topic or "TODO: describe the research template.",
        default_config={
            "template": name,
            "seed": 0,
            "data": brief.input_data or "TODO: describe synthetic input data",
            "target": brief.target or "TODO: describe target",
        },
        metric_names=metrics or ["TODO: metric/name"],
        required_rules=rules,
        recommended_tables=["leaderboard", "config-diff", "rule-audit"],
        recommended_figures=["metric-curve-overlay"],
        synthetic_example_plan=(
            "TODO: create a deterministic synthetic example that requires no external data."
        ),
        dependency_policy=[
            "Core template must run with SkillLogBoard core dependencies only.",
            "Optional domain dependencies must stay outside core dependencies.",
        ],
        required_outputs=list(brief.required_outputs),
        experiment_axes=list(brief.experiment_axes),
        status="Draft",
    )


def render_template_spec(spec: TemplateSpec) -> str:
    default_config = yaml.safe_dump(spec.default_config, sort_keys=True).strip()
    sections = [
        "# TemplateSpec",
        "",
        "## Template Name",
        spec.template_name,
        "",
        "## Category",
        spec.category,
        "",
        "## Description",
        spec.description,
        "",
        "## Status",
        spec.status,
        "",
        "## Default Config",
        default_config or "{}",
        "",
        "## Metric Names",
        *_render_list(spec.metric_names),
        "",
        "## Required Rules",
        *_render_list(spec.required_rules),
        "",
        "## Recommended Tables",
        *_render_list(spec.recommended_tables),
        "",
        "## Recommended Figures",
        *_render_list(spec.recommended_figures),
        "",
        "## Synthetic Example Plan",
        spec.synthetic_example_plan,
        "",
        "## Dependency Policy",
        *_render_list(spec.dependency_policy),
        "",
        "## Required Outputs",
        *_render_list(spec.required_outputs),
        "",
        "## Experiment Axes",
        *_render_list(spec.experiment_axes),
        "",
    ]
    return "\n".join(sections)


def _render_list(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- TODO"]


def _markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            current = re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", match.group(1).lower())).strip("_")
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def _first_text(sections: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = _clean_scalar(sections.get(key, ""))
        if value:
            return value
    return ""


def _list_text(sections: dict[str, str], *keys: str) -> list[str]:
    for key in keys:
        items = _parse_list(sections.get(key, ""))
        if items:
            return items
    return []


def _parse_list(value: str) -> list[str]:
    items: list[str] = []
    for line in value.splitlines():
        stripped = line.strip()
        if not stripped or stripped.lower().startswith("todo"):
            continue
        if stripped.startswith(("-", "*")):
            stripped = stripped[1:].strip()
        if stripped:
            items.append(stripped)
    return items


def _parse_mapping(value: str) -> dict[str, Any]:
    if not value.strip():
        return {}
    try:
        loaded = yaml.safe_load(value)
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _clean_scalar(value: str) -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if not stripped or stripped.lower().startswith("todo"):
            continue
        if stripped.startswith(("-", "*")):
            stripped = stripped[1:].strip()
        return stripped
    return ""


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "custom-template"
