---
week: 3
day: 4
slice: "02_cli_init_docs_status_templates"
title: "CLI init docs status templates"
priority: "P1"
status: "completed"
target_version: "v0.2-dashboard"
---

# 02_cli_init_docs_status_templates — CLI init docs status templates

## Objective

Ensure `skilllog init` creates docs/status scaffolding that does not overclaim unsupported features.

## Context

Docs/Implementation sync requires planned features to be marked clearly. `skilllog init` can help bootstrap a safe workspace.

## Dependencies

- 01_cli_dashboard_report_inspect_refinement

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/skills/default_skills.md
- docs/status_matrix.md
- tests/test_cli.py

## Implementation Steps

1. Review what `skilllog init` creates.
2. Ensure default Skills.md marks only safe MVP placeholders and does not claim rule engine execution before Week 4.
3. Optionally create or suggest `docs/status_matrix.md` only if the command already manages docs scaffolding.
4. Add tests ensuring init does not overwrite existing files.

## Acceptance Criteria

- `skilllog init` remains idempotent.
- Generated Skills.md does not overclaim Week 4 rule execution.
- Existing Skills.md is not overwritten.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli.py
```

## Non-goals

- Do not implement Skills.md parser.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 2.
- Do not implement Week 4+ features unless this file explicitly asks for a placeholder.
- Prefer deterministic, file-based output over complex runtime behavior.
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
**Completed at:** 2026-05-09 22:53  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_cli.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
