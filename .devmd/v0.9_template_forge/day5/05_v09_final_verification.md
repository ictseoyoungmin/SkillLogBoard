---
milestone: "v0.9"
phase: "Template Forge"
day: "5"
slice: "05_v09_final_verification"
title: "v0.9 final verification"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 05_v09_final_verification — v0.9 final verification

## Objective

Complete final v0.9 verification and prepare candidate notes.

## Context

This closes the Template Forge milestone.

## Dependencies

- 04_backward_compatibility_regression

## Target Files

- CHANGELOG.md
- README.md
- .devmd/v0.9_template_forge/**/*.md

## Implementation Steps

1. Run editable install with dev/dashboard extras.
2. Run full tests.
3. Run template forge-specific tests.
4. Run examples.
5. Run build no-isolation.
6. Execute a temporary end-to-end flow: init-brief -> plan -> scaffold -> validate.
7. Confirm no LLM/cloud/heavy dependencies were added to core.
8. Update all completion blocks or document blockers.

## Acceptance Criteria

- Full test suite passes.
- Template Forge tests pass.
- Examples pass.
- Build no-isolation passes.
- Forge end-to-end scaffold/validate flow works.
- Core dependency boundary remains intact.
- Docs are synchronized.

## Verification Commands

```bash
pip install -e ".[dev,dashboard]"
pytest -q
pytest -q tests/test_template_forge_brief.py tests/test_template_forge_spec.py tests/test_template_forge_harness.py tests/test_template_forge_scaffold.py tests/test_template_forge_validator.py tests/test_cli_template_forge.py
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python -m build --no-isolation
```

## Non-goals

- Do not begin v1.0 Live Board implementation.

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
