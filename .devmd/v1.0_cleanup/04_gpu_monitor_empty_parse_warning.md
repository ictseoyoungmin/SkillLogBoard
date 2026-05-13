---
milestone: "v1.0-cleanup"
phase: "Local-first Live Board Cleanup"
slice: "04_gpu_monitor_empty_parse_warning"
title: "GPU monitor empty-parse warning"
priority: "P0"
status: "completed"
target_version: "v1.0-cleanup"
---

# 04_gpu_monitor_empty_parse_warning — GPU monitor empty-parse warning

## Objective

Make GPU monitor behavior explicit when `nvidia-smi` succeeds but no parseable GPU rows are found.

## Context

v1.0 Local-first Live Board is functionally complete and CI is green. This cleanup phase resolves practical usability, server behavior, performance, and test-coverage issues before release-candidate packaging.

## Dependencies

- v1.0 Local-first Live Board implementation completed.
- Latest main CI is green.
- v0.7 Report Artifact Layer, v0.8 Agent Research Layer, and v0.9 Template Forge remain compatible.

## Target Files

- src/skilllogboard/live/monitors.py
- tests/test_live_monitors.py
- docs/live_board.md

## Implementation Steps

1. Inspect `sample_gpu_metrics()` behavior when subprocess succeeds with empty or malformed stdout.
2. If stdout is empty or no GPU rows are parsed, return a warning or skipped marker rather than a silent empty `gpus` list.
3. Keep normal successful parsing behavior unchanged.
4. Keep missing `nvidia-smi` behavior as a readable skipped warning.
5. Add tests for empty stdout and malformed stdout.
6. Update docs to explain GPU monitor skip/warning semantics.

## Acceptance Criteria

- Successful parse still returns GPU metrics.
- Missing `nvidia-smi` still returns skipped/warning.
- Empty or malformed output returns a visible warning/skipped state.
- Tests cover normal, missing, empty, and malformed cases.

## Verification Commands

```bash
pytest -q tests/test_live_monitors.py
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not replace static dashboard/report/compare artifacts.
- Do not add heavy dependencies to core.
- Do not perform PyPI/TestPyPI release work in this cleanup slice.

## Required Notes

- Do not add NVML or GPU library dependencies.
- Do not require an actual GPU in tests.

## Handoff Notes

- Keep this cleanup focused and small.
- Preserve local-first, file-based, inspectable behavior.
- Missing optional live dependencies must produce readable messages or skipped tests.
- If an item is deferred, update docs/status and record the reason in the Agent Completion Block.
- Do not expand this cleanup into a v1.1 UI redesign.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13
**Completed by:** Codex
**Verification command(s):** .venv/bin/python -m ruff check .; .venv/bin/python -m pytest -q; .venv/bin/python -m build --no-isolation; .venv/bin/skilllog --help; .venv/bin/skilllog watch --help; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python examples/live_demo.py; .venv/bin/pip install -e .[dev,dashboard,live]; .venv/bin/python -m pytest -q tests/test_live_state.py tests/test_live_readers.py tests/test_live_project.py tests/test_live_server.py tests/test_live_monitoring.py tests/test_live_monitors.py tests/test_cli_live.py tests/test_live_packaging.py tests/test_live_ui_snapshot.py; .venv/bin/pip install -e .[dev,dashboard,report]; .venv/bin/python -m pytest -q tests/test_report_figures.py tests/test_cli_report_artifacts.py
**Notes:** Local verification completed. GitHub Actions was not checked after push because no push was performed in this session.

<!-- AGENT_STATUS: COMPLETED -->

