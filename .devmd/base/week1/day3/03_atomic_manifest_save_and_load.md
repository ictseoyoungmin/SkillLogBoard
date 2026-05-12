---
week: 1
day: 3
slice: "03_atomic_manifest_save_and_load"
title: "atomic manifest save and load"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 03_atomic_manifest_save_and_load — atomic manifest save and load

## Objective

Implement atomic YAML save and simple load for the manifest.

## Context

The manifest may be updated repeatedly during a run. It should not be corrupted if an update is interrupted.

## Dependencies

- 02_manifest_dataclass_schema

## Target Files

- src/skilllogboard/core/manifest.py
- tests/test_manifest.py

## Implementation Steps

1. Implement `Manifest.save(path)` using a temp file and atomic replace.
2. Implement `load_manifest(path)` returning a dictionary.
3. Ensure parent directories are created automatically.
4. Use `yaml.safe_dump` with `allow_unicode=True` and stable readable output.
5. Add tests that save and load a manifest.

## Acceptance Criteria

- `manifest.yaml` is created when `Manifest.save()` is called.
- `load_manifest()` returns expected keys and values.
- Unicode project/run names are preserved.
- No temp manifest file remains after save.

## Verification Commands

```bash
pytest -q tests/test_manifest.py
```

## Non-goals

- Do not implement manifest migrations yet.

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
**Verification command(s):** pytest -q tests/test_manifest.py  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
