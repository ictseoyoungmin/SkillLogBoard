---
week: 6
day: 2
slice: "01_ir_drop_template_definition"
title: "IR-drop template definition"
priority: "P0"
status: "completed"
target_version: "v0.5-research-templates"
---

# 01_ir_drop_template_definition — IR-drop template definition

## Objective

Define `ir-drop` template.

## Context

IR-drop is a primary research use case, but no private data should be assumed.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/plugins/ir_drop.py
- src/skilllogboard/plugins/registry.py
- tests/test_ir_drop_template.py

## Implementation Steps

1. Create ir-drop descriptor.
2. Define metrics train/loss,val/mae,val/high_drop_f1,val/raw_mae.
3. Define default Skills.md rules.
4. Define example config fields.
5. Register template.
6. Test descriptor and default skills.

## Acceptance Criteria

- ir-drop registered.
- Default skills parse.
- High-drop metric convention present.
- No dataset dependency.

## Verification Commands

```bash
pytest -q tests/test_ir_drop_template.py tests/test_skills_parser.py
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
**Verification command(s):** .venv/bin/pytest -q tests/test_ir_drop_template.py tests/test_skills_parser.py tests/test_plugins.py tests/test_cli_templates.py  
**Notes:** Added registered `ir-drop` descriptor, default config, default skills, and high-drop metric convention.

<!-- AGENT_STATUS: COMPLETED -->
