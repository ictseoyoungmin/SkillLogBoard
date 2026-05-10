---
week: 6
day: 1
slice: "04_template_status_docs_sync"
title: "template status docs sync"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 04_template_status_docs_sync — template status docs sync

## Objective

Document implemented/planned template status.

## Context

Docs sync must be explicit.

## Dependencies

- Previous slices in order

## Target Files

- docs/status_matrix.md
- README.md
- docs/index.html

## Implementation Steps

1. Add template status table.
2. Mark non-implemented templates Planned.
3. State optional integrations remain optional.
4. Do not claim heavy dependencies required.

## Acceptance Criteria

- Template statuses explicit.
- Planned templates not described as implemented.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
t=Path('docs/status_matrix.md').read_text(encoding='utf-8')
assert 'ir-drop' in t or 'IR-drop' in t
assert 'trajectory' in t.lower()
print('template docs OK')
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

