"""Template Forge validation checks."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import ast
import re

from skilllogboard.template_forge.scaffold import planned_scaffold_paths
from skilllogboard.skills.parser import SkillsParseError, parse_skills_text

OUTCOME_PASSED = "passed"
OUTCOME_WARNING = "warning"
OUTCOME_ERROR = "error"
OUTCOME_SKIPPED = "skipped"

HEAVY_CORE_DEPENDENCIES = {
    "torch",
    "lightning",
    "pytorch-lightning",
    "sklearn",
    "scikit-learn",
    "pandas",
    "matplotlib",
    "openai",
    "anthropic",
    "wandb",
    "tensorboard",
}


@dataclass
class TemplateValidationResult:
    check_id: str
    name: str
    outcome: str
    severity: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_template_files(template_name: str, root_dir: str | Path = ".") -> list[TemplateValidationResult]:
    paths = planned_scaffold_paths(template_name, root_dir=root_dir).to_dict()
    return [_file_result(key, Path(path)) for key, path in paths.items()]


def validate_template(template_name: str, root_dir: str | Path = ".") -> list[TemplateValidationResult]:
    root = Path(root_dir)
    paths = planned_scaffold_paths(template_name, root_dir=root).to_dict()
    results = validate_template_files(template_name, root_dir=root)
    results.extend(
        [
            _plugin_descriptor_check(Path(paths["plugin"])),
            _skills_parse_check(Path(paths["plugin"])),
            _synthetic_example_check(Path(paths["example"])),
            _docs_check(Path(paths["docs"])),
            _dependency_policy_check(root / "pyproject.toml"),
            _status_check(Path(paths["plugin"])),
        ]
    )
    return results


def check_core_dependency_policy(pyproject_text: str) -> TemplateValidationResult:
    deps = _core_dependencies_from_pyproject(pyproject_text)
    bad = sorted(dep for dep in deps if _dependency_name(dep) in HEAVY_CORE_DEPENDENCIES)
    if bad:
        return TemplateValidationResult(
            "dependencies",
            "Core dependency policy",
            OUTCOME_ERROR,
            "error",
            "Heavy or cloud dependencies found in core dependencies.",
            {"dependencies": bad},
        )
    return TemplateValidationResult(
        "dependencies",
        "Core dependency policy",
        OUTCOME_PASSED,
        "info",
        "Core dependency policy passed.",
        {"dependencies": deps},
    )


def _file_result(check_id: str, path: Path) -> TemplateValidationResult:
    if path.exists():
        return TemplateValidationResult(
            f"files.{check_id}",
            f"{check_id} file",
            OUTCOME_PASSED,
            "info",
            f"Found {check_id} file.",
            {"path": str(path)},
        )
    return TemplateValidationResult(
        f"files.{check_id}",
        f"{check_id} file",
        OUTCOME_ERROR,
        "error",
        f"Missing {check_id} file: {path}",
        {"path": str(path)},
    )


def _plugin_descriptor_check(path: Path) -> TemplateValidationResult:
    if not path.exists():
        return _skipped("plugin", "Plugin descriptor", "Plugin file is missing.")
    text = path.read_text(encoding="utf-8")
    required = ["SkillLogTemplate", "default_config", "metric_names", "default_skills", "docs_notes"]
    missing = [name for name in required if name not in text]
    if missing:
        return TemplateValidationResult(
            "plugin",
            "Plugin descriptor",
            OUTCOME_ERROR,
            "error",
            "Plugin descriptor fields are missing.",
            {"missing": missing},
        )
    if "TODO" in text:
        return TemplateValidationResult(
            "plugin",
            "Plugin descriptor",
            OUTCOME_WARNING,
            "warning",
            "Plugin scaffold still contains TODO markers.",
            {"path": str(path)},
        )
    parsed = _parse_plugin_literals(text)
    missing_values = []
    if not parsed.get("default_config"):
        missing_values.append("default_config")
    if not parsed.get("metric_names"):
        missing_values.append("metric_names")
    if not parsed.get("default_skills"):
        missing_values.append("default_skills")
    if missing_values:
        return TemplateValidationResult(
            "plugin",
            "Plugin descriptor",
            OUTCOME_ERROR,
            "error",
            "Plugin descriptor fields are present but empty or not statically readable.",
            {"missing": missing_values},
        )
    return TemplateValidationResult("plugin", "Plugin descriptor", OUTCOME_PASSED, "info", "Plugin descriptor found.")


def _skills_parse_check(path: Path) -> TemplateValidationResult:
    if not path.exists():
        return _skipped("skills", "Default skills", "Plugin file is missing.")
    text = path.read_text(encoding="utf-8")
    default_skills = _parse_plugin_literals(text).get("default_skills")
    if default_skills is None:
        return _skipped("skills", "Default skills", "No statically readable DEFAULT_SKILLS found.")
    if "## RULE-" not in default_skills:
        return TemplateValidationResult(
            "skills",
            "Default skills",
            OUTCOME_WARNING,
            "warning",
            "Default skills scaffold does not contain parseable rule blocks yet.",
        )
    try:
        rules = parse_skills_text(default_skills)
    except SkillsParseError as exc:
        return TemplateValidationResult(
            "skills",
            "Default skills",
            OUTCOME_ERROR,
            "error",
            "Default skills could not be parsed.",
            {"error": str(exc)},
        )
    if not rules:
        return TemplateValidationResult(
            "skills",
            "Default skills",
            OUTCOME_WARNING,
            "warning",
            "Default skills did not yield any rules.",
        )
    return TemplateValidationResult(
        "skills",
        "Default skills",
        OUTCOME_PASSED,
        "info",
        "Default skills contain rule blocks.",
        {"rules": [rule.rule_id for rule in rules]},
    )


def _synthetic_example_check(path: Path) -> TemplateValidationResult:
    if not path.exists():
        return _skipped("example", "Synthetic example", "Example file is missing.")
    text = path.read_text(encoding="utf-8")
    missing = [needle for needle in ["RunLogger", "synthetic", "log_metric"] if needle not in text]
    if missing:
        return TemplateValidationResult(
            "example",
            "Synthetic example",
            OUTCOME_ERROR,
            "error",
            "Synthetic example scaffold is missing required markers.",
            {"missing": missing},
        )
    return TemplateValidationResult(
        "example",
        "Synthetic example",
        OUTCOME_PASSED,
        "info",
        "Synthetic example scaffold looks dependency-light.",
    )


def _docs_check(path: Path) -> TemplateValidationResult:
    if not path.exists():
        return _skipped("docs", "Template docs", "Docs file is missing.")
    text = path.read_text(encoding="utf-8")
    required = ["Overview", "Metrics", "Config", "Rules", "Example Usage", "Limitations"]
    missing = [section for section in required if section not in text]
    if missing:
        return TemplateValidationResult(
            "docs",
            "Template docs",
            OUTCOME_ERROR,
            "error",
            "Template docs are missing required sections.",
            {"missing": missing},
        )
    return TemplateValidationResult("docs", "Template docs", OUTCOME_PASSED, "info", "Template docs found.")


def _dependency_policy_check(path: Path) -> TemplateValidationResult:
    if not path.exists():
        return _skipped("dependencies", "Core dependency policy", "pyproject.toml is missing.")
    return check_core_dependency_policy(path.read_text(encoding="utf-8"))


def _status_check(path: Path) -> TemplateValidationResult:
    if not path.exists():
        return _skipped("status", "Template status", "Plugin file is missing.")
    text = path.read_text(encoding="utf-8")
    if 'status="Implemented"' in text or 'status = "Implemented"' in text:
        if "TODO" not in text:
            return TemplateValidationResult(
                "status",
                "Template status",
                OUTCOME_PASSED,
                "info",
                "Template is marked Implemented and contains no TODO markers.",
            )
        return TemplateValidationResult(
            "status",
            "Template status",
            OUTCOME_WARNING,
            "warning",
            "Template is marked Implemented; ensure validation and registration are complete.",
        )
    return TemplateValidationResult(
        "status",
        "Template status",
        OUTCOME_PASSED,
        "info",
        "Template is not marked Implemented by default.",
    )


def _skipped(check_id: str, name: str, message: str) -> TemplateValidationResult:
    return TemplateValidationResult(check_id, name, OUTCOME_SKIPPED, "info", message)


def _core_dependencies_from_pyproject(text: str) -> list[str]:
    match = re.search(r"(?ms)^\[project\].*?^dependencies\s*=\s*\[(.*?)^\]", text)
    if not match:
        return []
    return re.findall(r"['\"]([^'\"]+)['\"]", match.group(1))


def _dependency_name(requirement: str) -> str:
    return re.split(r"[<>=!~;\[]", requirement.strip().lower(), maxsplit=1)[0]


def _parse_plugin_literals(text: str) -> dict[str, Any]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}
    values: dict[str, Any] = {}
    constants: dict[str, Any] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        constants[target.id] = ast.literal_eval(node.value)
                    except (ValueError, SyntaxError):
                        continue
    for key, constant_name in [
        ("default_config", "DEFAULT_CONFIG"),
        ("metric_names", "METRIC_NAMES"),
        ("default_skills", "DEFAULT_SKILLS"),
    ]:
        if constant_name in constants:
            values[key] = constants[constant_name]
    return values
