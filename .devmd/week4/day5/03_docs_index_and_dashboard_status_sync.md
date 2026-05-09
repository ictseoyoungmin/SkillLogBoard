---
week: 4
day: 5
slice: "03_docs_index_and_dashboard_status_sync"
title: "docs index and dashboard status sync"
priority: "P1"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 03_docs_index_and_dashboard_status_sync — docs index and dashboard status sync

## Objective

Synchronize docs/index.html and status language with actual Week 4 implementation.

## Context

Product docs must not overclaim planned features.

## Dependencies

- Previous slices in order

## Target Files

- docs/index.html
- docs/status_matrix.md
- README.md

## Implementation Steps

1. Check docs/index.html rule type wording.
2. Mark MVP Supported vs Planned clearly.
3. Keep non-implemented templates Planned.
4. Keep scikit-learn as core logger example.
5. Keep dashboard described as static-first, not realtime/webapp.

## Acceptance Criteria

- Docs index does not mark Planned rules as Supported.
- Status labels align with docs/status_matrix.md.
- No unsupported Week 5+ feature is implemented in docs.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
for f in ['docs/status_matrix.md','docs/index.html']:
    p=Path(f)
    if p.exists():
        text=p.read_text(encoding='utf-8')
        assert 'domain_breakdown' not in text or 'Planned' in text
print('docs status sync OK')
PY
```

## Non-goals

- Do not polish visual branding.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 3.
- Do not implement Week 5+ features unless this file explicitly asks for a placeholder.
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
**Completed at:** 2026-05-09 23:49  
**Completed by:** coding agent  
**Verification command(s):** python - <<'PY' docs/status_matrix.md and docs/index.html sync check  
**Notes:** Completed and verified for Week 4 v0.3 rule engine scope.

<!-- AGENT_STATUS: COMPLETED -->

