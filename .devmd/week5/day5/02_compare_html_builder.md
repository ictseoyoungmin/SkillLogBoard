---
week: 5
day: 5
slice: "02_compare_html_builder"
title: "compare HTML builder"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 02_compare_html_builder — compare HTML builder

## Objective

Generate a static compare.html report.

## Context

Week 5 deliverable includes compare.html. Keep it static and file-system openable.

## Dependencies

- 01_compare_report_builder

## Target Files

- src/skilllogboard/dashboards/compare_builder.py
- src/skilllogboard/dashboards/templates/compare.html.j2
- tests/test_compare_report.py

## Implementation Steps

1. Create `compare.html.j2` or inline fallback template.
2. Render sections: Leaderboard, Config Diff, Ablation Axes, Seed Summary.
3. Use minimal standalone HTML structure.
4. Link to individual run dashboard.html files where available.
5. Add tests that compare.html exists and contains section headings.

## Acceptance Criteria

- compare.html is generated.
- compare.html is standalone static HTML.
- Section headings are present.
- Run dashboard links are relative where possible.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_compare_report.py
```

## Non-goals

- Do not implement interactive charts.

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

