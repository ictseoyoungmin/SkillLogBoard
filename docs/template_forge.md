# Template Forge

Template Forge is the v0.9 local scaffold and validation layer for creating new
SkillLogBoard-compatible research templates.

It does not call LLMs, does not contact cloud APIs, and does not generate final domain-specific
research code automatically. It writes local harness files that a human or external coding agent can
fill and validate.

## Workflow

```bash
skilllog forge init-brief --output ResearchBrief.md
skilllog forge plan --brief ResearchBrief.md --name custom-task --output TemplateSpec.md
skilllog forge scaffold --spec TemplateSpec.md --root-dir .
skilllog forge validate custom-task --root-dir .
```

## ResearchBrief

`ResearchBrief.md` is the user-authored starting point. It describes:

- research topic
- task type
- input data
- target
- main metric
- secondary metrics
- experiment axes
- required outputs
- constraints

## TemplateSpec

`TemplateSpec.md` is the reviewable intermediate artifact before files are scaffolded. It includes:

- template name and category
- default config
- metric names
- required rules
- recommended tables and figures
- synthetic example plan
- dependency policy
- status

The `plan` command maps a brief into a deterministic draft spec with TODO markers where the system
should not invent domain-specific details.

## Scaffolded Files

`skilllog forge scaffold` creates:

- `src/skilllogboard/plugins/{module_name}.py`
- `examples/{module_name}_example.py`
- `tests/test_{module_name}_template.py`
- `docs/templates/{module_name}.md`
- `.skilllog/template_spec.md`
- `.skilllog/template_harness.md`

Existing files are skipped unless `--force` is passed.

## Validation

`skilllog forge validate TEMPLATE_NAME` checks file presence, plugin descriptor shape, synthetic
example markers, docs sections, default skills markers, template status, and core dependency policy.
It returns non-zero on error-level validation failures and supports `--json`.

Draft scaffolds may produce warnings while TODO markers remain. A template should be marked
Implemented only after TODOs are resolved, tests pass, docs are complete, and validation is clean.
