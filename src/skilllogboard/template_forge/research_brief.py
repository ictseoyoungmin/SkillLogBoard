"""ResearchBrief.md contract and parser."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from importlib import resources
from pathlib import Path
import re


@dataclass
class ResearchBrief:
    research_topic: str = ""
    task_type: str = ""
    input_data: str = ""
    target: str = ""
    main_metric: str = ""
    secondary_metrics: list[str] = field(default_factory=list)
    experiment_axes: list[str] = field(default_factory=list)
    required_outputs: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def load_research_brief_template() -> str:
    return resources.files("skilllogboard.template_forge.harness").joinpath(
        "research_brief_template.md"
    ).read_text(encoding="utf-8")


def parse_research_brief(path: str | Path) -> ResearchBrief:
    return parse_research_brief_text(Path(path).read_text(encoding="utf-8"))


def parse_research_brief_text(text: str) -> ResearchBrief:
    sections = _markdown_sections(text)
    return ResearchBrief(
        research_topic=_first_text(sections, "research_topic"),
        task_type=_first_text(sections, "task_type"),
        input_data=_first_text(sections, "input_data", "data"),
        target=_first_text(sections, "target"),
        main_metric=_first_text(sections, "main_metric"),
        secondary_metrics=_list_text(sections, "secondary_metrics"),
        experiment_axes=_list_text(sections, "experiment_axes", "axes"),
        required_outputs=_list_text(sections, "required_outputs", "outputs"),
        constraints=_list_text(sections, "constraints"),
    )


def markdown_sections(text: str) -> dict[str, str]:
    return _markdown_sections(text)


def _markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            current = _section_key(match.group(1))
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def _section_key(title: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", title.lower())).strip("_")


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


def _clean_scalar(value: str) -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if not stripped or stripped.lower().startswith("todo"):
            continue
        if stripped.startswith(("-", "*")):
            stripped = stripped[1:].strip()
        return stripped
    return ""
