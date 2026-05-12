---
week: 3
day: 5
slice: "02_readme_quickstart_week3_update"
title: "README quickstart Week 3 update"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 02_readme_quickstart_week3_update — README quickstart Week 3 update

## Objective

Update README so users can install, run the example, and open the generated dashboard.

## Context

Week 3 deliverable includes README quickstart. The README should match real commands and output files.

## Dependencies

- 01_dashboard_render_smoke_test

## Target Files

- README.md
- docs/status_matrix.md

## Implementation Steps

1. Update install command for dashboard extra where needed.
2. Add or refine command sequence: install, `python examples/basic_usage.py`, open dashboard.
3. List expected output files including `dashboard.html` and `summary.md`.
4. State that dashboard is static single-run v0.2.
5. Keep Skills.md, compare, and plugins marked as planned.

## Acceptance Criteria

- README Quick Start can be followed from a fresh clone.
- README mentions how to find or open `dashboard.html`.
- README does not claim multi-run compare is implemented.
- Status matrix aligns with Week 3 status.

## Verification Commands

```bash
python examples/basic_usage.py
pytest -q
```

## Non-goals

- Do not rewrite the full product docs HTML unless explicitly requested.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 2.
- Do not implement Week 4+ features unless this file explicitly asks for a placeholder.
- Prefer deterministic, file-based output over complex runtime behavior.
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
**Completed at:** 2026-05-09 22:53  
**Completed by:** coding agent  
**Verification command(s):** python examples/basic_usage.py; pytest -q  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
