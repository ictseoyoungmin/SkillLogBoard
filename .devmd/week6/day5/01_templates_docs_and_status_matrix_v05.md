---
week: 6
day: 5
slice: "01_templates_docs_and_status_matrix_v05"
title: "templates docs and status matrix v0.5"
priority: "P0"
status: "pending"
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

