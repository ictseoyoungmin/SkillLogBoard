---
week: 4-cleanup
day: cleanup
slice: "04_fix_docs_skills_table_rendering"
title: "fix docs/skills table rendering"
priority: "P0"
status: "completed"
target_version: "v0.3-cleanup"
---

# 04_fix_docs_skills_table_rendering — fix docs/skills table rendering

## Objective

Make docs/skills.md render cleanly as Markdown and clearly separate MVP Supported and Planned rule types.

## Context

docs/skills.md content is mostly correct, but table formatting may be fragile. This cleanup should make it easy to read on GitHub.

## Dependencies

- Week 4 completed

## Target Files

- docs/skills.md

## Implementation Steps

1. Rewrite the rule status section as a valid Markdown table.
2. Include columns: Rule Type, Status, Required Fields, Purpose.
3. List all MVP rules with status `MVP Supported`.
4. List `dashboard_panel` and `domain_breakdown` as `Planned`.
5. Add one valid Skills.md example block.
6. Document missing required fields should result in readable rule results, not crashes.
7. Ensure no unsupported rule is described as executable.

## Acceptance Criteria

- docs/skills.md has a valid Markdown table delimiter row.
- All five MVP rules appear.
- `dashboard_panel` and `domain_breakdown` are marked Planned.
- At least one example RULE block is present.
- Docs do not claim planned rules are executed.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text=Path('docs/skills.md').read_text(encoding='utf-8')
assert '|---' in text
for s in ['required_config','required_metric','metric_threshold','best_last_gap','artifact_required']:
    assert s in text
assert 'Planned' in text
print('docs/skills rendering checks passed')
PY
```

## Non-goals

- Do not design a new DSL.

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
**Verification command(s):** python - <<'PY' docs/skills rendering checks  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

