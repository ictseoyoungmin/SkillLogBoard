---
week: 5
day: 5
slice: "04_docs_status_for_v04_compare"
title: "docs and status for v0.4 compare"
priority: "P1"
status: "completed"
target_version: "v0.4-compare"
---

# 04_docs_status_for_v04_compare — docs and status for v0.4 compare

## Objective

Update README, status matrix, and changelog for Week 5 compare features.

## Context

Docs/Implementation sync requires compare features to move from Planned to Implemented only after they work.

## Dependencies

- 03_cli_compare_and_export_table

## Target Files

- README.md
- CHANGELOG.md
- docs/status_matrix.md

## Implementation Steps

1. Add README section for multi-run compare.
2. Show commands for `skilllog compare` and `skilllog export-table`.
3. Update docs/status_matrix.md to mark Multi-run Compare as Implemented MVP/v0.4.
4. Keep research plugins as Planned.
5. Add CHANGELOG v0.4 candidate entry.

## Acceptance Criteria

- README contains compare usage.
- Status matrix marks compare implemented and plugins planned.
- CHANGELOG contains v0.4 compare entry.
- Docs do not overclaim Week 6 plugins.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
readme=Path('README.md').read_text(encoding='utf-8')
assert 'skilllog compare' in readme
status=Path('docs/status_matrix.md').read_text(encoding='utf-8')
assert 'Compare' in status
print('v0.4 docs checks passed')
PY
```

## Non-goals

- Do not document plugins as implemented.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
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
**Completed at:** 2026-05-10 00:36  
**Completed by:** coding agent  
**Verification command(s):** python - <<'PY' v0.4 docs checks  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

