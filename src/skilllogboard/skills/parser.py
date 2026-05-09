"""Parser for the limited Skills.md RULE-* block format."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import re

import yaml

VALID_STATUSES = {"MVP", "Planned", "Experimental"}


class SkillsParseError(ValueError):
    """Raised when a RULE block is malformed."""


@dataclass
class RuleSpec:
    rule_id: str
    rule_type: str
    severity: str = "warning"
    status: str = "MVP"
    message: str = ""
    params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "type": self.rule_type,
            "severity": self.severity,
            "status": self.status,
            "message": self.message,
            "params": self.params,
        }


def parse_skills(path: str | Path) -> list[RuleSpec]:
    return parse_skills_text(Path(path).read_text(encoding="utf-8"))


def parse_skills_text(text: str) -> list[RuleSpec]:
    rules: list[RuleSpec] = []
    current_id: str | None = None
    current_fields: dict[str, Any] = {}

    def flush() -> None:
        nonlocal current_id, current_fields
        if current_id is None:
            return
        rules.append(_build_spec(current_id, current_fields))
        current_id = None
        current_fields = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        heading = re.match(r"^##\s+(RULE-[A-Za-z0-9_-]+)\s*$", line)
        if heading:
            flush()
            current_id = heading.group(1)
            current_fields = {}
            continue
        if current_id is None:
            continue
        if line.startswith("## "):
            flush()
            continue
        if not line or line.startswith("#"):
            continue
        if not line.startswith("- "):
            continue
        key, value = _parse_bullet(line)
        current_fields[key] = value

    flush()
    return rules


def _parse_bullet(line: str) -> tuple[str, Any]:
    body = line[2:].strip()
    if ":" not in body:
        raise SkillsParseError(f"Malformed rule metadata line: {line}")
    key, raw_value = body.split(":", 1)
    key = key.strip()
    raw_value = raw_value.strip()
    if not key:
        raise SkillsParseError(f"Missing metadata key in line: {line}")
    if raw_value == "":
        return key, ""
    try:
        value = yaml.safe_load(raw_value)
    except yaml.YAMLError as exc:
        raise SkillsParseError(f"Could not parse metadata value for {key!r}: {raw_value}") from exc
    return key, value


def _build_spec(rule_id: str, fields: dict[str, Any]) -> RuleSpec:
    fields = dict(fields)
    if "type" not in fields:
        raise SkillsParseError(f"Rule {rule_id} is missing required field: type")
    rule_type = str(fields.pop("type"))
    severity = str(fields.pop("severity", "warning"))
    status = _normalize_status(str(fields.pop("status", "MVP")))
    message = str(fields.pop("message", ""))
    return RuleSpec(
        rule_id=rule_id,
        rule_type=rule_type,
        severity=severity,
        status=status,
        message=message,
        params=fields,
    )


def _normalize_status(value: str) -> str:
    normalized = value.strip()
    lower = normalized.lower()
    if lower in {"mvp", "supported", "implemented"}:
        return "MVP"
    if lower in {"planned", "planned-v0.3", "planned-v0.4", "planned-v0.5"}:
        return "Planned"
    if lower in {"experimental", "experiment"}:
        return "Experimental"
    return normalized if normalized in VALID_STATUSES else "Planned"
