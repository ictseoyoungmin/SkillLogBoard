---
week: 5-cleanup
day: cleanup
slice: "01_fix_readme_run_id_paths"
title: "fix README run_id paths"
priority: "P0"
status: "pending"
target_version: "v0.4-cleanup"
---

# 01_fix_readme_run_id_paths — fix README run_id paths

## Objective

Remove stale `runs/demo//` path examples.

## Context

Week 5 review found broken README paths.

## Dependencies

- Week 5 completed

## Target Files

- README.md

## Implementation Steps

1. Search README for `runs/demo//`.
2. Replace with `runs/demo/<run_id>/`.
3. Replace dashboard examples with `runs/demo/<run_id>/dashboard.html`.
4. Clarify `<run_id>` is generated.
5. Keep compare docs intact.

## Acceptance Criteria

- README does not contain `runs/demo//`.
- README contains `runs/demo/<run_id>/dashboard.html`.
- README still documents `skilllog compare`.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
t=Path('README.md').read_text(encoding='utf-8')
assert 'runs/demo//' not in t
assert 'runs/demo/<run_id>/' in t
assert 'dashboard.html' in t
assert 'skilllog compare' in t
print('README paths OK')
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

