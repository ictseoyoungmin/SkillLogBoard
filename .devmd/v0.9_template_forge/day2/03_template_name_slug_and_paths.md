---
milestone: "v0.9"
phase: "Template Forge"
day: "2"
slice: "03_template_name_slug_and_paths"
title: "template name slug and paths"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 03_template_name_slug_and_paths — template name slug and paths

## Objective

Implement safe template name normalization and output path planning.

## Context

Generated files should use safe snake_case filenames while retaining user-facing hyphenated names if desired.

## Dependencies

- 02_scaffold_file_templates

## Target Files

- src/skilllogboard/template_forge/scaffold.py
- tests/test_template_forge_scaffold.py

## Implementation Steps

1. Create `scaffold.py`.
2. Implement `normalize_template_name(name)` returning display name, slug, module_name, class-like label if needed.
3. Reject unsafe path traversal characters.
4. Implement `planned_scaffold_paths(template_name, root_dir='.')`.
5. Paths should include plugin, example, test, docs, `.skilllog/template_spec.md`, and `.skilllog/template_harness.md` if appropriate.
6. Add tests for hyphenated, underscored, spaced, and unsafe names.

## Acceptance Criteria

- Template names normalize deterministically.
- Unsafe names are rejected.
- Planned paths are correct.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_scaffold.py
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.8/v0.7/v0.6 public APIs and run folder compatibility.
- Template Forge is a scaffold/harness/validation system. It must not embed LLM inference or call cloud APIs.
- Generated template code must be local, inspectable, dependency-light, and testable with synthetic examples.
- Core install must remain lightweight. Do not add torch, lightning, sklearn, pandas, matplotlib, LLM SDKs, or domain packages to core dependencies.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13  
**Completed by:** Codex  
**Verification command(s):** ruff check; Template Forge tests; full pytest; examples; build no-isolation; forge CLI e2e smoke check  
**Notes:** v0.9 Template Forge implemented as a local scaffold/harness/validation layer. No built-in LLM, cloud API, automatic domain-code generation, or heavy core dependency was added.  

<!-- AGENT_STATUS: COMPLETED -->
