---
milestone: "v0.9"
phase: "Template Forge"
day: "5"
slice: "05_v09_final_verification"
title: "v0.9 final verification"
priority: "P0"
status: "pending"
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

- [ ] Implementation completed
- [ ] Acceptance criteria verified
- [ ] Tests or smoke checks executed
- [ ] No unrelated files changed
- [ ] Notes added below if anything was skipped or deferred

**Status:** PENDING  
**Completed at:**  
**Completed by:**  
**Verification command(s):**  
**Notes:**  

<!-- AGENT_STATUS: PENDING -->

