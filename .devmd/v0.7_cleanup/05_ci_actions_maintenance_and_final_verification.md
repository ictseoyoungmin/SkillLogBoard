---
milestone: "v0.7-cleanup"
phase: "Report Artifact Layer Cleanup"
slice: "05_ci_actions_maintenance_and_final_verification"
title: "CI actions maintenance and final verification"
priority: "P1"
status: "pending"
target_version: "v0.7-cleanup"
---

# 05_ci_actions_maintenance_and_final_verification — CI actions maintenance and final verification

## Objective

Resolve minor CI maintenance warnings where practical and run final v0.7 cleanup verification.

## Context

v0.7 Report Artifact Layer is functionally complete and CI is green. This cleanup phase resolves API, documentation, optional figure testing, and CI polish issues before starting v0.8 Agent Research Layer.

## Dependencies

- v0.7 Report Artifact Layer completed.
- Latest main CI is green.

## Target Files

- .github/workflows/ci.yml
- CHANGELOG.md
- .devmd/v0.7_cleanup/**/*.md

## Implementation Steps

1. Inspect GitHub Actions workflow for maintenance warnings such as Node runtime deprecation.
2. If newer stable action versions are available and safe, update `actions/checkout` and `actions/setup-python` versions.
3. Do not make risky workflow changes solely for warning cleanup.
4. Run full local verification.
5. Run report-extra verification if the optional report extra exists.
6. Confirm latest GitHub Actions run is green after push.
7. Update this slice completion block with local and CI verification results.

## Acceptance Criteria

- Full test suite passes.
- Build no-isolation passes.
- Examples pass.
- Report-extra tests pass or are explicitly deferred with reason.
- CI workflow remains valid.
- Latest GitHub Actions run is green after cleanup push.

## Verification Commands

```bash
pip install -e ".[dev,dashboard]"
skilllog --help
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python -m build --no-isolation
pip install -e ".[dev,dashboard,report]"
pytest -q tests/test_report_figures.py tests/test_cli_report_artifacts.py
```

## Non-goals

- Do not begin v0.8 Agent Research Layer implementation.
- Do not implement Template Forge or Live Board.
- Do not change public RunLogger APIs.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this cleanup focused.
- Preserve v0.7 behavior and all existing tests.
- If an item is deferred, update docs and record the reason below.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-12
**Completed by:** Codex
**Verification command(s):** .venv/bin/ruff check .; .venv/bin/pytest -q; .venv/bin/pytest -q tests/test_report_figures.py tests/test_cli_report_artifacts.py; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation
**Notes:** Completed v0.7 cleanup: public report API exports, ReportSpec FIG execution/skipped-warning behavior, optional report-extra tests and CI job, docs placeholder polish, and final local verification.

<!-- AGENT_STATUS: COMPLETED -->

