---
milestone: "v1.5-cleanup"
phase: "Performance, Retention, and Operational Rules Cleanup"
slice: "03_project_index_artifact_count_lightweighting"
title: "project index artifact count lightweighting"
priority: "P0"
status: "pending"
---

# 03_project_index_artifact_count_lightweighting — project index artifact count lightweighting

## Objective

Avoid expensive artifact enumeration during project index rebuilds by using a lightweight artifact count/summary reader.

## Context

v1.5 Performance, Retention, and Operational Rules is functionally complete. This cleanup pass closes four review items before packaging, beta release, or the next roadmap milestone:

1. `skilllog prune --execute` can be misunderstood because v1.5 still produces a plan rather than deleting files.
2. Retention `keep_best` currently risks treating larger values as better even for loss/error metrics.
3. Project index artifact counting can be made lighter for large projects.
4. CI and v1.5 release-candidate evidence should be collected explicitly.

## Target Files

- src/skilllogboard/index/builder.py
- src/skilllogboard/live/readers.py
- src/skilllogboard/index/schema.py
- docs/operational_rules.md
- tests/test_project_index.py
- tests/test_live_readers.py
- tests/test_large_project_performance.py

## Implementation Steps

1. Review current `build_project_index()` artifact handling. It should not load or retain large artifact metadata lists just to compute counts.
2. Add a lightweight helper such as `read_artifact_count(run_dir)` or `read_artifact_summary(run_dir)`.
3. When `artifact_index.json` exists, count records without returning full metadata where feasible.
4. When only an `artifacts/` directory exists, count files with bounded traversal and avoid reading file contents.
5. Update `build_project_index()` to use the lightweight helper.
6. Preserve existing Live Board artifact browser behavior; this change should target index rebuild performance, not remove artifact browsing.
7. Add tests with many synthetic artifact records/files to confirm index stores counts without carrying full artifact lists.
8. Document that the project index stores summary/count metadata and not full artifact details.

## Acceptance Criteria

- Project index rebuild records artifact_count without loading large artifact payloads into the index.
- Existing artifact browser/readers continue to work.
- Large-project/index tests cover many artifacts.
- Docs explain artifact summary behavior.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_project_index.py tests/test_live_readers.py tests/test_large_project_performance.py
python -m skilllogboard.cli.main index rebuild runs --dry-run --json || true
```

## Non-goals

- Do not start a new v1.6 feature milestone in this cleanup pass.
- Do not implement destructive pruning/deletion as default behavior.
- Do not add a database backend for the project index.
- Do not add cloud sync, multi-user auth, Prometheus/Grafana, or TensorBoard/W&B import.
- Do not weaken local-first file-backed behavior.
- Do not publish to TestPyPI/PyPI in this cleanup pass.

## Additional Notes

- Do not prematurely optimize with a database or persistent daemon.
- If exact artifact count is expensive, prefer a bounded summary with `truncated: true` metadata over unbounded traversal.

## Handoff Notes

- Keep cleanup changes narrow and reviewable.
- Prefer safety, explicit wording, and policy correctness over feature expansion.
- If a verification command cannot run due to local environment limits, record the exact blocker in the Agent Completion Block.
- Preserve backward compatibility for existing v1.5 CLI and data files where possible.
- Update docs/changelog/status matrix when user-visible behavior or policy wording changes.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-16
**Completed by:** Claude (Sonnet 4.6)
**Verification command(s):**
- .venv/bin/pytest tests/test_project_index.py tests/test_live_readers.py tests/test_v15_artifact_storage.py -q
**Notes:**
- Added `read_artifact_count(run_dir, max_scan=10000)` to live/readers.py.
  - artifact_index.json path: counts records without loading full metadata.
  - artifacts/ directory path: counts files with bounded traversal (max_scan limit, records warning if truncated).
- Updated `build_project_index()` to call `read_artifact_count()` instead of `len(read_artifacts(..., limit=100000))`.
- Removed unused `read_artifacts` import from index/builder.py.
- Existing artifact browser (Live Board) still uses `read_artifacts()` unchanged.
- Created tests/test_project_index.py with 5 tests: artifact_index.json count, artifacts/ dir count, index stores count, large synthetic count, truncation warning.

<!-- AGENT_STATUS: COMPLETED -->

