---
week: 6
day: 3
slice: "04_trajectory_docs_update"
title: "trajectory docs update"
priority: "P0"
status: "completed"
target_version: "v0.5-research-templates"
---

# 04_trajectory_docs_update — trajectory docs update

## Objective

Document trajectory template usage.

## Context

Users should understand this is a logging/reporting template.

## Dependencies

- Previous slices in order

## Target Files

- README.md
- docs/status_matrix.md
- docs/templates.md

## Implementation Steps

1. Add trajectory section to docs/templates.md.
2. List metrics/config fields.
3. Add example command.
4. Update status matrix.
5. State model training is user-provided.

## Acceptance Criteria

- docs/templates.md contains trajectory.
- Status matrix updated.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
t=Path('docs/templates.md').read_text(encoding='utf-8')
assert 'trajectory' in t.lower()
assert 'val/pb_score' in t
print('trajectory docs OK')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 5.
- Keep optional integrations optional; core install must not require heavy ML packages.
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
**Completed at:** 2026-05-10 19:49  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/python -c "trajectory docs assertions"; .venv/bin/pytest -q tests/test_trajectory_template.py tests/test_ir_drop_template.py tests/test_skills_parser.py tests/test_plugins.py tests/test_cli_templates.py  
**Notes:** Added trajectory docs section, metrics/config fields, example command, and user-provided training scope note.

<!-- AGENT_STATUS: COMPLETED -->
