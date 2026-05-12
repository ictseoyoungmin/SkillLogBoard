---
week: 1
day: 5
slice: "05_week1_integration_smoke_test"
title: "Week 1 integration smoke test"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 05_week1_integration_smoke_test — Week 1 integration smoke test

## Objective

Verify that the Week 1 skeleton can create a minimal run evidence package.

## Context

This slice connects package install, RunLogger placeholder, writers, manifest, config, events, metrics, report, and dashboard placeholders.

## Dependencies

- day5/01_metrics_csv_writer_schema
- day5/02_config_yaml_capture
- day5/03_system_snapshot_capture
- day5/04_git_snapshot_capture

## Target Files

- src/skilllogboard/core/logger.py
- examples/basic_usage.py
- tests/test_basic_usage.py
- README.md

## Implementation Steps

1. Ensure `RunLogger` creates `runs/<project>/<run_id>/`.
2. Ensure constructor saves `manifest.yaml`, `config.yaml`, `system.json`, `git.json`, and `events.jsonl`.
3. Ensure `log_metrics()` writes both metrics CSV rows and metric events.
4. Ensure `finish(build_dashboard=True, build_report=True)` writes `summary.md` and `dashboard.html`.
5. Create `examples/basic_usage.py` as a runnable smoke example.
6. Add `tests/test_basic_usage.py` using `tmp_path`.
7. Update README with the smoke test command.

## Acceptance Criteria

- `python examples/basic_usage.py` runs successfully.
- The run folder contains `manifest.yaml`, `config.yaml`, `metrics.csv`, `events.jsonl`, `summary.md`, and `dashboard.html`.
- `pytest -q` passes for Week 1 tests.
- `skilllog inspect <run_dir>` can print the generated manifest.

## Verification Commands

```bash
python examples/basic_usage.py
pytest -q
skilllog --help
```

## Non-goals

- Do not implement final dashboard UI.
- Do not implement Skills.md rule execution.
- Do not implement multi-run compare.

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
**Verification command(s):** python examples/basic_usage.py; pytest -q; skilllog --help  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
