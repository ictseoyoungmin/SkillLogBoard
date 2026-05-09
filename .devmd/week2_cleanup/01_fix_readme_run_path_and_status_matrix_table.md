---
week: 2-cleanup
day: cleanup
slice: "01_fix_readme_run_path_and_status_matrix_table"
title: "fix README run path and status matrix table"
priority: "P0"
status: "completed"
target_version: "v0.1-cleanup"
---

# 01_fix_readme_run_path_and_status_matrix_table — fix README run path and status matrix table

## Objective

Clean up Week 2 documentation issues before Week 3 work starts.

## Context

Week 2 review found that README may show the generated run path as `runs/demo//` and `docs/status_matrix.md` may not render as a valid Markdown table. These are documentation correctness issues, not feature work.

## Dependencies

- Week 2 completed

## Target Files

- README.md
- docs/status_matrix.md

## Implementation Steps

1. Open README and replace any ambiguous or broken run path such as `runs/demo//` with `runs/demo/<run_id>/`.
2. Ensure README Quick Start uses the current working RunLogger API.
3. Open `docs/status_matrix.md` and convert the feature status section into a valid GitHub Markdown table.
4. Ensure v0.1 implemented items are clearly marked as implemented.
5. Ensure Week 3+ items are marked as Planned or Placeholder rather than fully Supported.
6. Keep wording concise and implementation-aligned.

## Acceptance Criteria

- README does not contain `runs/demo//`.
- README output path examples use `runs/<project>/<run_id>/` format.
- `docs/status_matrix.md` contains a valid Markdown table delimiter row such as `|---|---|---|---|`.
- Static Dashboard is not overclaimed as fully implemented before Week 3.
- Skills.md, multi-run compare, and plugins remain Planned.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
readme = Path('README.md').read_text(encoding='utf-8')
assert 'runs/demo//' not in readme
status = Path('docs/status_matrix.md').read_text(encoding='utf-8')
assert '|---' in status
print('docs cleanup checks passed')
PY
```

## Non-goals

- Do not implement dashboard or CLI features in this cleanup slice.

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
**Verification command(s):** python - <<'PY' docs cleanup check  
**Notes:** Completed cleanup checks.  

<!-- AGENT_STATUS: COMPLETED -->
