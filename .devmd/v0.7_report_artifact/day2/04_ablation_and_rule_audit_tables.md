---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "2"
slice: "04_ablation_and_rule_audit_tables"
title: "ablation and rule audit tables"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 04_ablation_and_rule_audit_tables — ablation and rule audit tables

## Objective

Implement report table adapters for ablation summary and rule audit summary.

## Context

Research reports need ablation tables and rule audit evidence, not only leaderboard rankings.

## Dependencies

- 03_seed_summary_table_adapter

## Target Files

- src/skilllogboard/reports/table_builder.py
- src/skilllogboard/compare/config_diff.py
- tests/test_report_tables.py

## Implementation Steps

1. Implement `build_ablation_summary_table(...)` using existing ablation/config diff helpers where possible.
2. Implement `build_rule_audit_table(root_dir_or_records)` reading `skill_trace.jsonl` summaries.
3. For ablation summary, include axis/key, value, count, best, mean if available.
4. For rule audit, include rule_id, outcome, severity, message, run_id if available.
5. Add tests for both table types.

## Acceptance Criteria

- Ablation summary table can be generated.
- Rule audit table can be generated.
- Both tables export to Markdown and CSV through common helpers.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_report_tables.py tests/test_config_diff.py
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

