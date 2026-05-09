---
week: 1
day: 1
slice: "04_import_and_install_smoke_test"
title: "import and install smoke test"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 04_import_and_install_smoke_test — import and install smoke test

## Objective

Add and verify a minimal import/install smoke test.

## Context

Day 1 is only complete if the package can be installed and imported. This slice defines the smoke test that guards the package skeleton.

## Dependencies

- 02_src_layout_and_public_api

## Target Files

- tests/test_import.py
- scripts/smoke_test.sh

## Implementation Steps

1. Create `tests/test_import.py` that imports `skilllogboard`, `__version__`, and `RunLogger`.
2. Create `scripts/smoke_test.sh` with install/import/help commands.
3. Make sure the smoke test does not require dashboard, pandas, torch, or internet access.
4. Run the smoke test locally.

## Acceptance Criteria

- `pytest -q tests/test_import.py` passes.
- `python -c "from skilllogboard import RunLogger"` passes.
- Smoke script contains only Week 1-safe commands.

## Verification Commands

```bash
pytest -q tests/test_import.py
python -c "from skilllogboard import RunLogger; print(RunLogger)"
```

## Non-goals

- Do not test dashboard rendering in Day 1.

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
**Verification command(s):** pytest -q tests/test_import.py; python -c "from skilllogboard import RunLogger; print(RunLogger)"  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
