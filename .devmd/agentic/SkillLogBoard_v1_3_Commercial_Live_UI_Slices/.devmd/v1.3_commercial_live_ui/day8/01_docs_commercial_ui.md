---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day8"
slice: "01_docs_commercial_ui"
title: "docs commercial UI update"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 01_docs_commercial_ui — docs commercial UI update

## Objective

Document v1.3 Commercial Live UI.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- README.md
- docs/live_board.md
- docs/ui_design_guidelines.md
- docs/status_matrix.md

## Implementation Steps

1. Update README screenshots/description placeholders.
2. Document frontend source vs packaged runtime.
3. Document all views.
4. Document local-first/no-cloud constraints.
5. Update status matrix.

## Acceptance Criteria

- Docs explain v1.3 UI.
- Docs explain users do not need Node at runtime.
- Status matrix updated.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/live_board.md').read_text(encoding='utf-8').lower()
assert 'react' in text or 'compiled' in text
assert 'local' in text
print('v1.3 docs check passed')
PY
```

## Non-goals

- Do not require Node.js at runtime for end users.
- Do not add GraphQL/Apollo/Redux unless separately approved.
- Do not include node_modules in the Python package.
- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not perform TestPyPI/PyPI publishing in this slice.
- Do not weaken local-first, inspectable-file behavior.

## Handoff Notes

- Keep the slice focused and reviewable.
- Prefer additive state/API fields over breaking existing contracts.
- Keep static dashboard/report portability separate from Live Board app behavior.
- If an item is deferred, document the reason in the Agent Completion Block.
- Update related docs/status/changelog when user-visible behavior changes.

---

## Agent Completion Block

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

