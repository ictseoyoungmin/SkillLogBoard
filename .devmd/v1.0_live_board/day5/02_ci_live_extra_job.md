---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "02_ci_live_extra_job"
title: "CI live extra job"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 02_ci_live_extra_job — CI live extra job

## Objective

Add CI coverage for the optional live extra.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- .github/workflows/ci.yml
- tests/test_live_server.py
- tests/test_cli_live.py

## Implementation Steps

1. Add separate CI job or step installing `.[dev,dashboard,live]`.
2. Run live-specific tests.
3. Keep existing core matrix unchanged.
4. Avoid tests that require a real GPU or browser.
5. Document any deferral.

## Acceptance Criteria

- CI includes live-extra verification or deferral is documented.
- Core CI remains unchanged.
- Live tests pass in CI.

## Verification Commands

```bash
pip install -e ".[dev,dashboard,live]"
pytest -q tests/test_live_state.py tests/test_live_readers.py tests/test_live_server.py tests/test_cli_live.py
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

