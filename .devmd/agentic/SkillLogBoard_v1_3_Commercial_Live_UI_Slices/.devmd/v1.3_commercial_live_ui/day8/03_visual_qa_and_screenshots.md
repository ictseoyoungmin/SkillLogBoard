---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day8"
slice: "03_visual_qa_and_screenshots"
title: "visual QA and screenshot guidance"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 03_visual_qa_and_screenshots — visual QA and screenshot guidance

## Objective

Add final visual QA and screenshot guidance for commercial UI.

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

1. Add screenshot checklist for Overview, Runs, Compare, Metric Lab, Artifacts, Reports, Agent, Settings.
2. Add layout/density criteria.
3. Add local-first language checklist.
4. Add rich demo command.

## Acceptance Criteria

- Visual QA checklist covers all commercial views.
- Screenshot commands are documented.
- Local-first language checklist exists.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/ui_design_guidelines.md').read_text(encoding='utf-8').lower()
assert 'screenshot' in text and 'compare' in text and 'agent' in text
print('visual QA docs check passed')
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

