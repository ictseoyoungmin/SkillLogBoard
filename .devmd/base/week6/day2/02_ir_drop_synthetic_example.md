---
week: 6
day: 2
slice: "02_ir_drop_synthetic_example"
title: "IR-drop synthetic example"
priority: "P0"
status: "completed"
target_version: "v0.5-research-templates"
---

# 02_ir_drop_synthetic_example — IR-drop synthetic example

## Objective

Add lightweight IR-drop example.

## Context

Example should run without torch or external data.

## Dependencies

- Previous slices in order

## Target Files

- examples/ir_drop_example.py
- tests/test_ir_drop_template.py
- README.md

## Implementation Steps

1. Create/update example.
2. Use RunLogger with ir_drop_demo.
3. Log IR-drop metrics.
4. Log small artifact/table.
5. Run skill checks.
6. Finish dashboard/report.
7. Print run dir.

## Acceptance Criteria

- Example runs without external data.
- Run has metrics, dashboard, summary, skill_trace.

## Verification Commands

```bash
python examples/ir_drop_example.py
pytest -q tests/test_ir_drop_template.py
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 5.
- Keep optional integrations optional; core install must not require heavy ML packages.
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
**Completed at:** 2026-05-10 19:46  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/python examples/ir_drop_example.py; .venv/bin/pytest -q tests/test_ir_drop_template.py tests/test_skills_parser.py tests/test_plugins.py tests/test_cli_templates.py  
**Notes:** Added synthetic example that logs metrics, table/artifact, skill trace, summary, and dashboard without external data.

<!-- AGENT_STATUS: COMPLETED -->
