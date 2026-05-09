---
week: 5
day: 1
slice: "03_manifest_config_metric_indexer"
title: "manifest/config/metric indexer"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 03_manifest_config_metric_indexer — manifest/config/metric indexer

## Objective

Load manifest, config, metrics, and skill trace summaries for each discovered run.

## Context

A run index should be generated from saved files, not from live logger state.

## Dependencies

- 02_run_discovery_recursive_scan

## Target Files

- src/skilllogboard/compare/run_index.py
- tests/test_compare_index.py

## Implementation Steps

1. Implement `load_run_record(run_dir)`.
2. Read `manifest.yaml` safely.
3. Read `config.yaml` if present.
4. Read `metrics.csv` and compute latest values per metric.
5. Read `skill_trace.jsonl` if present and summarize warning/error counts.
6. Read artifact index count if present.
7. Return a RunRecord/dict.
8. Add tests for complete and partial run directories.

## Acceptance Criteria

- Complete run records include manifest/config/latest metrics.
- Partial run records do not crash.
- Warning/error counts from skill_trace are included when present.
- Tests verify missing optional file behavior.

## Verification Commands

```bash
pytest -q tests/test_compare_index.py
```

## Non-goals

- Do not aggregate across runs yet.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
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

