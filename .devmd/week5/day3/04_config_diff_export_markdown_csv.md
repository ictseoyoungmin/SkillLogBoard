---
week: 5
day: 3
slice: "04_config_diff_export_markdown_csv"
title: "config diff export Markdown and CSV"
priority: "P1"
status: "pending"
target_version: "v0.4-compare"
---

# 04_config_diff_export_markdown_csv — config diff export Markdown and CSV

## Objective

Export config diff and ablation axes to Markdown/CSV-friendly formats.

## Context

Week 5 outputs should be usable in reports or papers.

## Dependencies

- 03_ablation_axis_extraction

## Target Files

- src/skilllogboard/compare/config_diff.py
- tests/test_config_diff.py

## Implementation Steps

1. Implement CSV export for config diff rows or ensure rows are compatible with shared CSV writer.
2. Implement Markdown table output for config diff.
3. Implement Markdown summary for ablation axes.
4. Add tests for valid Markdown delimiter row and CSV output.

## Acceptance Criteria

- Config diff Markdown table renders correctly.
- CSV output has stable columns.
- Ablation axes summary is readable.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_config_diff.py
```

## Non-goals

- Do not implement full compare report yet.

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

