---
week: 4-cleanup
day: cleanup
slice: "01_update_readme_for_v03_rule_engine"
title: "update README for v0.3 rule engine"
priority: "P0"
status: "pending"
target_version: "v0.3-cleanup"
---

# 01_update_readme_for_v03_rule_engine — update README for v0.3 rule engine

## Objective

Update README so it reflects the completed v0.3 Skills.md rule engine and fixes stale v0.2-only wording.

## Context

Week 4 added Skills.md parsing, MVP rule execution, skill_trace.jsonl, RunLogger.run_skill_checks(), and dashboard Rule Audit. README still appears to emphasize v0.2 static dashboard and may contain stale run path text.

## Dependencies

- Week 4 completed

## Target Files

- README.md
- docs/status_matrix.md

## Implementation Steps

1. Replace stale output path examples such as `runs/demo//` with `runs/demo/<run_id>/`.
2. Add a `v0.3 Skills.md Rule Engine` or equivalent section.
3. List MVP supported rules: required_config, required_metric, metric_threshold, best_last_gap, artifact_required.
4. Add a minimal usage example for `logger.run_skill_checks(skills_path='Skills.md')` or CLI/API workflow if implemented.
5. Mention generated `skill_trace.jsonl` and dashboard Rule Audit section.
6. Keep `dashboard_panel`, `domain_breakdown`, multi-run compare, and plugins marked Planned unless implemented.
7. Ensure Quick Start still works for basic_usage and dashboard.

## Acceptance Criteria

- README contains v0.3 rule engine section.
- README mentions `skill_trace.jsonl`.
- README mentions the 5 MVP supported rules.
- README does not contain `runs/demo//`.
- README does not claim Week 5 compare or Week 6 plugins are implemented.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text=Path('README.md').read_text(encoding='utf-8')
assert 'runs/demo//' not in text
assert 'skill_trace.jsonl' in text
for s in ['required_config','required_metric','metric_threshold','best_last_gap','artifact_required']:
    assert s in text
print('README v0.3 checks passed')
PY
pytest -q
```

## Non-goals

- Do not rewrite the full README from scratch unless necessary.

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

