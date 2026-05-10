---
week: 6
day: 2
slice: "04_ir_drop_docs_update"
title: "IR-drop docs update"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 04_ir_drop_docs_update — IR-drop docs update

## Objective

Document IR-drop template usage.

## Context

Users must know this is a logging/reporting template.

## Dependencies

- Previous slices in order

## Target Files

- README.md
- docs/status_matrix.md
- docs/templates.md

## Implementation Steps

1. Create/update docs/templates.md.
2. Add init/example commands.
3. List metrics/config fields.
4. State no model/data included.
5. Update status matrix.

## Acceptance Criteria

- docs/templates.md contains ir-drop.
- Status matrix marks implemented after tests.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
t=Path('docs/templates.md').read_text(encoding='utf-8')
assert 'ir-drop' in t.lower()
assert 'val/high_drop_f1' in t
print('ir-drop docs OK')
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

