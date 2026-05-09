---
week: 1
day: 1
slice: "02_src_layout_and_public_api"
title: "src layout and public API"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 02_src_layout_and_public_api — src layout and public API

## Objective

Create the package directory layout and expose the initial public API.

## Context

The package should use the `src/` layout. The public import target for users is `from skilllogboard import RunLogger`.

## Dependencies

- 01_pyproject_and_package_metadata

## Target Files

- src/skilllogboard/__init__.py
- src/skilllogboard/_version.py
- src/skilllogboard/core/__init__.py
- src/skilllogboard/core/logger.py
- src/skilllogboard/cli/__init__.py

## Implementation Steps

1. Create `src/skilllogboard/` and subpackages required for Week 1.
2. Add `__init__.py` files for all importable packages.
3. Create `_version.py` with `__version__`.
4. Expose `RunLogger` and `__version__` from `skilllogboard.__init__`.
5. Add a minimal `RunLogger` placeholder class if the full implementation does not exist yet.

## Acceptance Criteria

- `from skilllogboard import RunLogger, __version__` succeeds.
- `skilllogboard.__all__` includes `RunLogger` and `__version__`.
- No heavy optional dependency is imported from the package root.

## Verification Commands

```bash
python -c "from skilllogboard import RunLogger, __version__; print(__version__)"
```

## Non-goals

- Do not implement full RunLogger behavior here unless needed for import smoke tests.

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
**Verification command(s):** python -c "from skilllogboard import RunLogger, __version__; print(__version__)"  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
