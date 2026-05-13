"""Template Forge scaffold and validation helpers."""

from skilllogboard.template_forge.research_brief import (
    ResearchBrief,
    load_research_brief_template,
    parse_research_brief,
    parse_research_brief_text,
)
from skilllogboard.template_forge.scaffold import (
    ScaffoldResult,
    normalize_template_name,
    planned_scaffold_paths,
    scaffold_template_from_spec,
)
from skilllogboard.template_forge.template_spec import (
    TemplateSpec,
    draft_template_spec_from_brief,
    load_template_spec_template,
    parse_template_spec,
    parse_template_spec_text,
    render_template_spec,
)
from skilllogboard.template_forge.validator import (
    TemplateValidationResult,
    validate_template,
    validate_template_files,
)

__all__ = [
    "ResearchBrief",
    "ScaffoldResult",
    "TemplateSpec",
    "TemplateValidationResult",
    "draft_template_spec_from_brief",
    "load_research_brief_template",
    "load_template_spec_template",
    "normalize_template_name",
    "parse_research_brief",
    "parse_research_brief_text",
    "parse_template_spec",
    "parse_template_spec_text",
    "planned_scaffold_paths",
    "render_template_spec",
    "scaffold_template_from_spec",
    "validate_template",
    "validate_template_files",
]
