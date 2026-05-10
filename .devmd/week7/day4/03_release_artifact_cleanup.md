---
week: 7
day: 4
slice: "03_release_artifact_cleanup"
title: "release artifact cleanup"
priority: "P0"
status: "pending"
target_version: "v0.6-release-hardening"
---

# 03_release_artifact_cleanup — release artifact cleanup

## Objective

Ensure generated release artifacts and local run outputs are ignored or documented.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- .gitignore
- docs/release_checklist.md

## Implementation Steps

1. Review .gitignore for dist, build, egg-info, runs, caches, and venvs.
2. Document cleanup commands if useful.
3. Do not delete user data automatically.

## Acceptance Criteria

- .gitignore covers common generated artifacts.
- Release checklist mentions cleaning build artifacts.
- No source files are removed.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text=Path('.gitignore').read_text(encoding='utf-8')
for s in ['dist/','build/','runs/','.venv/']:
    assert s in text
print('gitignore release artifact checks passed')
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

