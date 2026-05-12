---
week: 5-cleanup
day: cleanup
slice: "02_fix_docs_skills_markdown_table"
title: "fix docs/skills Markdown table"
priority: "P0"
status: "completed"
target_version: "v0.4-cleanup"
---

# 02_fix_docs_skills_markdown_table — fix docs/skills Markdown table

## Objective

Fix MVP/Planned rule table rendering.

## Context

docs/skills.md table may be broken around rule rows.

## Dependencies

- Week 5 completed

## Target Files

- docs/skills.md

## Implementation Steps

1. Rewrite rule table with valid Markdown.
2. Use columns Rule Type, Status, Required Fields, Purpose.
3. Include all five MVP rules.
4. Include dashboard_panel and domain_breakdown as Planned.
5. Keep an example RULE block.

## Acceptance Criteria

- Table has delimiter row.
- All MVP rules are present.
- Planned rules remain Planned.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
t=Path('docs/skills.md').read_text(encoding='utf-8')
assert '|---' in t
for s in ['required_config','required_metric','metric_threshold','best_last_gap','artifact_required']: assert s in t
assert 'Planned' in t
print('docs skills OK')
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
**Completed at:** 2026-05-10 19:40  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/python -c "docs/skills table assertions"; .venv/bin/pytest -q  
**Notes:** Existing `docs/skills.md` table already satisfied the required Markdown structure and rule coverage.

<!-- AGENT_STATUS: COMPLETED -->
