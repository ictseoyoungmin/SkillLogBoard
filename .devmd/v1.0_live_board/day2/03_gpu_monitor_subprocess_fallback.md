---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "03_gpu_monitor_subprocess_fallback"
title: "GPU monitor subprocess fallback"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 03_gpu_monitor_subprocess_fallback — GPU monitor subprocess fallback

## Objective

Implement optional GPU monitor using `nvidia-smi` subprocess with graceful skip.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/live/monitors.py
- tests/test_live_monitors.py

## Implementation Steps

1. Implement `sample_gpu_metrics()` using `nvidia-smi` if available.
2. Avoid hard NVML dependency in core.
3. Parse index, utilization, memory used/total, temperature if possible.
4. Return skipped warning when NVIDIA tooling is unavailable.
5. Add tests with mocked subprocess output.

## Acceptance Criteria

- GPU monitor works with mocked nvidia-smi output.
- No GPU environment is required for tests.
- Missing nvidia-smi is a skip/warning.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_monitors.py
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add database backend.
- Do not replace static dashboard/report/compare.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this slice focused and small.
- Preserve all existing v0.6-v0.9 behavior.
- Missing optional live dependencies must produce readable messages or skipped tests.
- The Live Board should watch local files; it should not become a SaaS/observability platform.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13
**Completed by:** Codex
**Verification command(s):** .venv/bin/python -m ruff check .; .venv/bin/python -m pytest -q; .venv/bin/python -m build --no-isolation; .venv/bin/python examples/live_demo.py
**Notes:** Isolated python -m build could not create an ensurepip venv in this environment, so package verification was rerun successfully with --no-isolation.

<!-- AGENT_STATUS: COMPLETED -->

