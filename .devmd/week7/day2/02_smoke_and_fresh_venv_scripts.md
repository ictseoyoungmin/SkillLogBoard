---
week: 7
day: 2
slice: "02_smoke_and_fresh_venv_scripts"
title: "smoke and fresh venv scripts"
priority: "P0"
status: "completed"
target_version: "v0.6-release-hardening"
---

# 02_smoke_and_fresh_venv_scripts — smoke and fresh venv scripts

## Objective

Consolidate local smoke and fresh virtualenv verification scripts.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- scripts/smoke_test.sh
- scripts/verify_fresh_venv.sh
- README.md

## Implementation Steps

1. Ensure smoke_test.sh runs quick checks.
2. Create verify_fresh_venv.sh or document equivalent manual virtualenv steps.
3. Avoid sudo requirements.
4. Reference scripts from README or release checklist.

## Acceptance Criteria

- Smoke script exists and is syntax-valid.
- Fresh venv verification script or manual instructions exist.
- No sudo requirement is introduced.

## Verification Commands

```bash
bash -n scripts/smoke_test.sh
test -f scripts/verify_fresh_venv.sh && bash -n scripts/verify_fresh_venv.sh || true
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

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-10 21:10
**Completed by:** coding agent
**Verification command(s):** bash -n scripts/smoke_test.sh; bash -n scripts/verify_fresh_venv.sh
**Notes:** Expanded smoke test script, added fresh venv verification script, and ignored `.fresh-venv/`.

<!-- AGENT_STATUS: COMPLETED -->
