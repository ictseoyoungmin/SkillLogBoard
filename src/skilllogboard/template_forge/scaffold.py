"""Template Forge scaffold generation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from importlib import resources
from pathlib import Path
import re

from skilllogboard.template_forge.template_spec import TemplateSpec, render_template_spec


@dataclass(frozen=True)
class TemplateName:
    display_name: str
    slug: str
    module_name: str
    class_name: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ScaffoldPaths:
    plugin: str
    example: str
    test: str
    docs: str
    template_spec: str
    template_harness: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class ScaffoldResult:
    template_name: str
    root_dir: str
    created: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def normalize_template_name(name: str) -> TemplateName:
    raw = name.strip()
    if not raw:
        raise ValueError("template name must be non-empty")
    if "/" in raw or "\\" in raw or ".." in raw:
        raise ValueError(f"unsafe template name: {name}")
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    if not slug:
        raise ValueError(f"unsafe template name: {name}")
    module_name = slug.replace("-", "_")
    class_name = "".join(part.capitalize() for part in module_name.split("_")) + "Template"
    return TemplateName(display_name=raw, slug=slug, module_name=module_name, class_name=class_name)


def planned_scaffold_paths(template_name: str, root_dir: str | Path = ".") -> ScaffoldPaths:
    normalized = normalize_template_name(template_name)
    root = Path(root_dir)
    module = normalized.module_name
    return ScaffoldPaths(
        plugin=str(root / "src" / "skilllogboard" / "plugins" / f"{module}.py"),
        example=str(root / "examples" / f"{module}_example.py"),
        test=str(root / "tests" / f"test_{module}_template.py"),
        docs=str(root / "docs" / "templates" / f"{module}.md"),
        template_spec=str(root / ".skilllog" / "template_spec.md"),
        template_harness=str(root / ".skilllog" / "template_harness.md"),
    )


def scaffold_template_from_spec(
    spec: TemplateSpec,
    root_dir: str | Path = ".",
    force: bool = False,
) -> ScaffoldResult:
    normalized = normalize_template_name(spec.template_name)
    paths = planned_scaffold_paths(spec.template_name, root_dir=root_dir)
    root = Path(root_dir)
    result = ScaffoldResult(spec.template_name, str(root))
    values = _format_values(spec, normalized)
    writes = {
        paths.plugin: _load_harness("plugin_template.py.txt").format(**values),
        paths.example: _load_harness("example_template.py.txt").format(**values),
        paths.test: _load_harness("test_template.py.txt").format(**values),
        paths.docs: _load_harness("docs_template.md").format(**values),
        paths.template_spec: render_template_spec(spec),
        paths.template_harness: _load_harness("template_harness.md"),
    }
    for path_text, content in writes.items():
        path = Path(path_text)
        if path.exists() and not force:
            result.skipped.append(str(path))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        result.created.append(str(path))
    return result


def _load_harness(name: str) -> str:
    return resources.files("skilllogboard.template_forge.harness").joinpath(name).read_text(
        encoding="utf-8"
    )


def _format_values(spec: TemplateSpec, normalized: TemplateName) -> dict[str, str]:
    metric_names = spec.metric_names or ["metric/value"]
    metric_tuple = ", ".join(repr(metric) for metric in metric_names)
    if len(metric_names) == 1:
        metric_tuple += ","
    return {
        "template_name": spec.template_name,
        "slug": normalized.slug,
        "module_name": normalized.module_name,
        "class_name": normalized.class_name,
        "description": spec.description or "TODO: describe this template.",
        "metric_names_tuple": metric_tuple,
        "first_metric": metric_names[0],
        "default_config_repr": repr(spec.default_config or {"template": normalized.slug, "seed": 0}),
        "rules_list": "\n".join(f"- {rule}" for rule in spec.required_rules) or "- TODO",
        "tables_list": "\n".join(f"- {table}" for table in spec.recommended_tables) or "- TODO",
        "figures_list": "\n".join(f"- {figure}" for figure in spec.recommended_figures) or "- TODO",
    }
