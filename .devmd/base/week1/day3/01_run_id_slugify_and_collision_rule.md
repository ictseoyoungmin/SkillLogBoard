---
week: 1
day: 3
slice: "01_run_id_slugify_and_collision_rule"
title: "RunId slugify and collision rule"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 01_run_id_slugify_and_collision_rule — RunId slugify and collision rule

## Objective

Implement deterministic run id generation and collision-safe run directory resolution.

## Context

Run folders must be safe across Linux, macOS, Windows, and WSL. A run id should combine timestamp and slugified run name.

## Dependencies

- day1/02_src_layout_and_public_api

## Target Files

- src/skilllogboard/core/run_id.py
- tests/test_run_id.py

## Implementation Steps

1. Implement `slugify(value: str, max_length: int = 64)`.
2. Implement `make_run_id(run_name, created_at=None)` using local timezone timestamp.
3. Implement `ensure_unique_run_dir(project_dir, run_id)` that appends numeric suffixes on collision.
4. Handle empty or unsafe run names gracefully.
5. Add tests for ASCII names, Korean names, symbols, empty names, and collisions.

## Acceptance Criteria

- Run ids contain a timestamp prefix and a filesystem-safe slug.
- Unsafe characters are replaced with `_`.
- Existing directories do not collide; a suffix is returned.
- Tests pass on pathlib paths.

## Verification Commands

```bash
pytest -q tests/test_run_id.py
```

## Non-goals

- Do not create run directories in `ensure_unique_run_dir`; only return the path.

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
**Verification command(s):** pytest -q tests/test_run_id.py  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
