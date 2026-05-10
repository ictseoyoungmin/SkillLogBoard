"""Dependency-free research template descriptors."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SkillLogTemplate:
    name: str
    status: str
    description: str
    default_skills: str = ""
    default_config: dict[str, Any] = field(default_factory=dict)
    metric_names: tuple[str, ...] = ()
    docs_notes: tuple[str, ...] = ()

    @property
    def is_implemented(self) -> bool:
        return self.status.lower() == "implemented"


SkillLogPlugin = SkillLogTemplate
