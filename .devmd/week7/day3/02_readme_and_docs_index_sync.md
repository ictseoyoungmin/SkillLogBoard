---
week: 7
day: 3
slice: "02_readme_and_docs_index_sync"
title: "README and docs index sync"
priority: "P0"
status: "pending"
target_version: "v0.6-release-hardening"
---

# 02_readme_and_docs_index_sync — README and docs index sync

## Objective

Clean README and docs/index.html for v0.6 candidate readability and consistency.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- README.md
- docs/index.html
- docs/status_matrix.md

## Implementation Steps

1. Ensure README sections are coherent and current.
2. Ensure docs/index.html does not contradict status matrix.
3. Keep planned features labeled Planned.
4. Remove stale broken paths or outdated v0.1/v0.2-only wording.

## Acceptance Criteria

- README contains install and quickstart commands.
- README references rule engine, compare, and templates accurately.
- docs/index.html does not contradict status matrix.
- No stale runs/demo// paths remain.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
readme=Path('README.md').read_text(encoding='utf-8')
assert 'pip install' in readme and 'skilllog --help' in readme
assert 'runs/demo//' not in readme
print('README/docs sync checks passed')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 6.
- Do not implement Week 8+ publishing unless explicitly instructed.
- Keep optional integrations optional. Core install must not require torch, lightning, sklearn, pandas, or domain-specific packages.
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

