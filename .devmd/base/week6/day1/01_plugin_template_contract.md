---
week: 6
day: 1
slice: "01_plugin_template_contract"
title: "plugin and template contract"
priority: "P0"
status: "completed"
target_version: "v0.5-research-templates"
---

# 01_plugin_template_contract — plugin and template contract

## Objective

Define lightweight plugin/template contract.

## Context

Week 6 introduces research templates without heavy dependencies.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/plugins/base.py
- src/skilllogboard/plugins/registry.py
- tests/test_plugins.py
- docs/status_matrix.md

## Implementation Steps

1. Define SkillLogPlugin/template descriptor.
2. Fields: name,status,description,default_skills,default_config,metric_names,docs notes.
3. Keep objects dependency-free.
4. Implement registry register/get/list.
5. Test registry.

## Acceptance Criteria

- Registry lists templates.
- Template descriptors are dependency-free.
- Core import remains lightweight.

## Verification Commands

```bash
pytest -q tests/test_plugins.py
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
**Completed at:** 2026-05-10 19:44  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/pytest -q tests/test_plugins.py tests/test_cli_templates.py  
**Notes:** Added dependency-free `SkillLogTemplate` descriptors and registry coverage.

<!-- AGENT_STATUS: COMPLETED -->
