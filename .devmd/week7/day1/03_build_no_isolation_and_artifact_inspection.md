---
week: 7
day: 1
slice: "03_build_no_isolation_and_artifact_inspection"
title: "build no-isolation and artifact inspection"
priority: "P0"
status: "pending"
target_version: "v0.6-release-hardening"
---

# 03_build_no_isolation_and_artifact_inspection — build no-isolation and artifact inspection

## Objective

Build wheel/sdist with --no-isolation and inspect artifacts.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- dist/
- CHANGELOG.md
- docs/release_checklist.md

## Implementation Steps

1. Run python -m build --no-isolation.
2. Confirm both .whl and .tar.gz exist in dist/.
3. Document isolated build limitation if local system lacks venv/ensurepip.
4. Ensure CI/Docker later verifies isolated build.

## Acceptance Criteria

- No-isolation build succeeds.
- dist contains wheel and sdist.
- Build limitation policy is documented if needed.

## Verification Commands

```bash
python -m build --no-isolation
python - <<'PY'
from pathlib import Path
files=list(Path('dist').glob('*'))
assert any(p.suffix=='.whl' for p in files)
assert any(str(p).endswith('.tar.gz') for p in files)
print([p.name for p in files])
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

