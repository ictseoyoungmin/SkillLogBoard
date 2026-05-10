---
week: 6-cleanup
day: cleanup
slice: "02_verify_readme_and_templates_rendering"
title: "verify README and templates rendering"
priority: "P0"
status: "pending"
target_version: "v0.5-cleanup"
---

# 02_verify_readme_and_templates_rendering — verify README and templates rendering

## Objective

Verify README and docs/templates.md render cleanly and accurately distinguish implemented and planned templates.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- 01_update_status_matrix_sklearn_example

## Target Files

- README.md
- docs/templates.md
- docs/status_matrix.md

## Implementation Steps

1. Check README includes `skilllog templates`, `skilllog init --template ir-drop`, and trajectory template usage.
2. Check docs/templates.md has valid Markdown table separators.
3. Ensure `ir-drop` and `trajectory` are marked implemented.
4. Ensure classification, segmentation, and finance-dashboard are marked Planned.
5. Fix table formatting if GitHub rendering is likely to break.

## Acceptance Criteria

- README documents template commands.
- docs/templates.md has valid Markdown table delimiter row.
- Implemented and Planned template statuses are distinct.
- No planned template is presented as implemented.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
readme=Path('README.md').read_text(encoding='utf-8')
assert 'skilllog templates' in readme and 'ir-drop' in readme and 'trajectory' in readme
templates=Path('docs/templates.md').read_text(encoding='utf-8')
assert '|---' in templates and 'Planned' in templates
print('README/templates rendering checks passed')
PY
```

## Non-goals

- Do not implement planned templates.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 6.
- Do not implement Week 8+ publishing unless explicitly instructed.
- Keep optional integrations optional. Core install must not require torch, lightning, sklearn, pandas, or domain-specific packages.
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

