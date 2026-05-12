---
week: 5
day: 1
slice: "02_run_discovery_recursive_scan"
title: "run discovery recursive scan"
priority: "P0"
status: "completed"
target_version: "v0.4-compare"
---

# 02_run_discovery_recursive_scan — run discovery recursive scan

## Objective

Implement run discovery under a project or runs root directory.

## Context

D21 requires run discovery and manifest indexing. The scanner should find directories containing `manifest.yaml`.

## Dependencies

- 01_compare_data_contract

## Target Files

- src/skilllogboard/compare/run_index.py
- tests/test_compare_index.py

## Implementation Steps

1. Implement `discover_runs(root_dir)`.
2. Recursively find directories containing `manifest.yaml`.
3. Ignore hidden/cache/build directories where appropriate.
4. Return sorted run paths for deterministic output.
5. Handle missing root directory with readable error or empty result according to CLI needs.
6. Add tests for nested project/run layout.

## Acceptance Criteria

- `discover_runs()` finds multiple run folders.
- Results are deterministic.
- Missing or empty root is handled clearly.
- Tests cover nested `runs/<project>/<run_id>` layout.

## Verification Commands

```bash
pytest -q tests/test_compare_index.py
```

## Non-goals

- Do not parse all metrics yet.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
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
**Completed at:** 2026-05-10 00:36  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_compare_index.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

