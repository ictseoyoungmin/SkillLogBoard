# Template Forge Harness

Generated templates must remain local, inspectable, and dependency-light.

## Required Files

- `src/skilllogboard/plugins/{module_name}.py`
- `examples/{module_name}_example.py`
- `tests/test_{module_name}_template.py`
- `docs/templates/{module_name}.md`
- `.skilllog/template_spec.md`
- `.skilllog/template_harness.md`

## Validation Gates

- Plugin descriptor follows `SkillLogTemplate`.
- Synthetic example runs without external data.
- Tests and docs exist.
- Default skills are parseable before implemented status.
- Core dependencies do not add torch, lightning, sklearn, pandas, matplotlib, LLM SDKs, cloud SDKs, or domain packages.

## Non-Goals

- SkillLogBoard does not call LLMs.
- SkillLogBoard does not generate final domain-specific research code automatically.
- SkillLogBoard does not contact cloud services.

Implemented status is allowed only after validation passes and the template is intentionally registered.
