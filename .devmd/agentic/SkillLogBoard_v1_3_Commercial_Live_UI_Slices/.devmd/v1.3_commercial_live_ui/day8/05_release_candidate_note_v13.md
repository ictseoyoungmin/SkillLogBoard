---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day8"
slice: "05_release_candidate_note_v13"
title: "release candidate note v1.3"
priority: "P1"
status: "pending"
target_version: "v1.3"
---

# 05_release_candidate_note_v13 — release candidate note v1.3

## Objective

Prepare release candidate note for the commercial Live UI.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- docs/release_candidate_checklist.md
- docs/v1_3_release_candidate_note.md

## Implementation Steps

1. Summarize completed UI features.
2. List manual QA steps.
3. List known non-goals.
4. List packaging/build verification commands.
5. Do not publish to TestPyPI/PyPI.

## Acceptance Criteria

- v1.3 RC note exists.
- Manual QA steps are listed.
- Publishing is not performed.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/v1_3_release_candidate_note.md').read_text(encoding='utf-8').lower()
assert 'release candidate' in text and 'live ui' in text
print('v1.3 RC note check passed')
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

