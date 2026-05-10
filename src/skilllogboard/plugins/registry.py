"""Research template registry."""

from __future__ import annotations

from collections import OrderedDict

from skilllogboard.plugins.base import SkillLogTemplate
from skilllogboard.plugins.ir_drop import ir_drop_template
from skilllogboard.plugins.trajectory import trajectory_template


class TemplateRegistry:
    def __init__(self) -> None:
        self._templates: OrderedDict[str, SkillLogTemplate] = OrderedDict()

    def register(self, template: SkillLogTemplate) -> SkillLogTemplate:
        if not template.name:
            raise ValueError("template name must be non-empty")
        self._templates[template.name] = template
        return template

    def get(self, name: str) -> SkillLogTemplate:
        return self._templates[name]

    def list(self) -> list[SkillLogTemplate]:
        return list(self._templates.values())


def _build_default_registry() -> TemplateRegistry:
    registry = TemplateRegistry()
    registry.register(ir_drop_template())
    registry.register(trajectory_template())
    for name, description in [
        ("classification", "Classification template placeholder."),
        ("segmentation", "Segmentation template placeholder."),
        ("finance-dashboard", "Finance dashboard template placeholder."),
    ]:
        registry.register(
            SkillLogTemplate(
                name=name,
                status="Planned",
                description=description,
                docs_notes=("Planned template; no files are generated yet.",),
            )
        )
    return registry


DEFAULT_REGISTRY = _build_default_registry()


def register(plugin: SkillLogTemplate) -> SkillLogTemplate:
    return DEFAULT_REGISTRY.register(plugin)


def get_plugin(name: str) -> SkillLogTemplate:
    return get_template(name)


def get_template(name: str) -> SkillLogTemplate:
    return DEFAULT_REGISTRY.get(name)


def list_templates() -> list[SkillLogTemplate]:
    return DEFAULT_REGISTRY.list()
