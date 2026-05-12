---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "5"
slice: "02_report_check_cli"
title: "report check CLI"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 02_report_check_cli — report check CLI

## Objective

Add CLI support for checking generated report artifacts against rules.

## Context

Users and agents should be able to verify that report outputs are complete.

## Dependencies

- 01_report_artifact_rules

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/skills/report_rules.py
- tests/test_cli_report_artifacts.py

## Implementation Steps

1. Add `skilllog report check ROOT_OR_REPORT_DIR` or equivalent.
2. Support `--rules .skilllog/rules.md` if feasible.
3. Run report artifact rules and print pass/warn/error summary.
4. Optionally append report rule results to `skill_trace.jsonl` when checking a single run.
5. Add CLI tests.

## Acceptance Criteria

- `skilllog report check` appears in help.
- Command detects missing required table.
- Command detects missing required figure.
- Command returns readable output.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_report_artifacts.py tests/test_report_rules.py
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.6 public APIs and run folder compatibility.
- Existing `summary.md`, `dashboard.html`, `compare.md`, `compare.html`, and `export-table` behavior must not regress.
- Core install must remain lightweight. Do not add matplotlib, pandas, torch, lightning, sklearn, or domain packages to core dependencies.
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
**Completed at:** 2026-05-12
**Completed by:** Codex
**Verification command(s):** .venv/bin/pytest -q; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation
**Notes:** Implemented and verified as part of the v0.7 report artifact layer pass. Optional figure generation keeps a readable skipped-dependency fallback when matplotlib is unavailable.

<!-- AGENT_STATUS: COMPLETED -->

