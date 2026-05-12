---
week: 5
day: 4
slice: "03_seed_summary_markdown_csv"
title: "seed summary Markdown and CSV"
priority: "P1"
status: "completed"
target_version: "v0.4-compare"
---

# 03_seed_summary_markdown_csv — seed summary Markdown and CSV

## Objective

Export seed group summaries for reports.

## Context

Seed summary is useful for paper-style ablation tables.

## Dependencies

- 02_seed_metric_aggregation

## Target Files

- src/skilllogboard/compare/seed_group.py
- tests/test_seed_group.py

## Implementation Steps

1. Implement stable row schema for seed summary.
2. Implement Markdown table output.
3. Implement CSV output or CSV-friendly rows.
4. Include group key, count, mean, std, median, best, best_run_id.
5. Add tests for Markdown and CSV output.

## Acceptance Criteria

- Seed summary rows are deterministic.
- Markdown table has delimiter row.
- CSV output includes expected columns.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_seed_group.py
```

## Non-goals

- Do not generate plots.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
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
**Completed at:** 2026-05-10 00:36  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_seed_group.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

