---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day3"
slice: "04_overview_manual_visual_qa"
title: "Overview/Runs visual QA checklist"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 04_overview_manual_visual_qa — Overview/Runs visual QA checklist

## Objective

Add visual QA notes for Overview and Runs.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- docs/ui_design_guidelines.md
- docs/release_candidate_checklist.md

## Implementation Steps

1. Add checks for overview hierarchy, run table density, nav clarity, local-first language.
2. Add screenshot guidance for Overview and Runs.
3. Keep checklist practical.

## Acceptance Criteria

- Visual QA docs updated.
- Overview/Runs screenshot criteria exist.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/ui_design_guidelines.md').read_text(encoding='utf-8').lower()
assert 'overview' in text and 'runs' in text
print('overview/runs visual QA docs check passed')
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

