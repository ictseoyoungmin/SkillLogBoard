---
week: 1
day: 5
slice: "04_git_snapshot_capture"
title: "git snapshot capture"
priority: "P1"
status: "completed"
target_version: "v0.1-dev"
---

# 04_git_snapshot_capture — git snapshot capture

## Objective

Implement a safe git snapshot helper.

## Context

`git.json` should capture commit/branch/dirty status when available, but must not fail outside a git repository.

## Dependencies

- 03_system_snapshot_capture

## Target Files

- src/skilllogboard/core/config_capture.py
- tests/test_config_capture.py

## Implementation Steps

1. Implement `capture_git(repo_dir='.')`.
2. Use subprocess calls to `git rev-parse HEAD`, `git rev-parse --abbrev-ref HEAD`, and `git diff --quiet`.
3. Return `available: false` and error text if git is unavailable or not a repository.
4. Add tests that the function returns a dictionary and does not raise in a temp directory.

## Acceptance Criteria

- `capture_git()` never raises in a non-git directory.
- Result includes `available` boolean.
- If available, commit and branch are included.

## Verification Commands

```bash
pytest -q tests/test_config_capture.py
```

## Non-goals

- Do not implement remote URL capture or diff patch capture.

## Handoff Notes

- Keep changes minimal and local to the target files.
- Prefer simple, explicit implementation over clever abstractions.
- Do not implement future-week features unless explicitly required by this slice.
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
**Completed at:** 2026-05-09 21:49  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_config_capture.py  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
