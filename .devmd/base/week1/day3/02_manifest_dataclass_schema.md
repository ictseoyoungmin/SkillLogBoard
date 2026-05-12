---
week: 1
day: 3
slice: "02_manifest_dataclass_schema"
title: "Manifest dataclass schema"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 02_manifest_dataclass_schema — Manifest dataclass schema

## Objective

Implement the manifest schema used by every run folder.

## Context

`manifest.yaml` is the top-level index for a run evidence package. It must contain enough metadata to inspect a run without opening all files.

## Dependencies

- 01_run_id_slugify_and_collision_rule

## Target Files

- src/skilllogboard/core/manifest.py
- tests/test_manifest.py

## Implementation Steps

1. Create a `Manifest` dataclass.
2. Include fields: project, run_name, run_id, run_dir, created_at, updated_at, status, framework, task_type, model_name, dataset_name, seed, main_metric, best_metric, files, tags, error_summary.
3. Add `to_dict()` and `touch()` helpers.
4. Keep fields serializable with standard YAML.
5. Add tests for default values and required fields.

## Acceptance Criteria

- A `Manifest` object can be instantiated with required fields.
- Default `status` is `running`.
- `files` defaults to an empty dict.
- `created_at` is ISO-like text.

## Verification Commands

```bash
pytest -q tests/test_manifest.py
```

## Non-goals

- Do not implement best metric computation yet.

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
