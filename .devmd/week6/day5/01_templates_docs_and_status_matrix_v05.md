---
week: 6
day: 5
slice: "01_templates_docs_and_status_matrix_v05"
title: "templates docs and status matrix v0.5"
priority: "P0"
status: "completed"
target_version: "v0.5-research-templates"
---

# 01_templates_docs_and_status_matrix_v05 — templates docs and status matrix v0.5

## Objective

Update docs for v0.5 templates.

## Context

Docs must reflect implemented/planned templates.

## Dependencies

- Previous slices in order

## Target Files

- README.md
- docs/templates.md
- docs/status_matrix.md
- CHANGELOG.md

## Implementation Steps

1. Add README template section.
2. Show template commands.
3. Update docs/templates.md.
4. Mark planned templates Planned.
5. Update changelog v0.5.

## Acceptance Criteria

- README documents templates.
- Status matrix separates implemented/planned.
- CHANGELOG has v0.5 entry.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
readme=Path('README.md').read_text(encoding='utf-8')
assert 'skilllog templates' in readme
assert 'ir-drop' in readme and 'trajectory' in readme
print('v0.5 docs OK')
PY
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
**Completed at:** 2026-05-10 19:57  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/python -c "v0.5 docs/version assertions"; .venv/bin/pytest -q  
**Notes:** Added v0.5 README/docs/status/changelog updates and separated implemented/planned template status.

<!-- AGENT_STATUS: COMPLETED -->
