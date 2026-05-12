---
week: 3-cleanup
day: cleanup
slice: "01_readme_path_version_changelog_cleanup"
title: "README path, version, and changelog cleanup"
priority: "P0"
status: "completed"
target_version: "v0.2-cleanup"
---

# 01_readme_path_version_changelog_cleanup — README path, version, and changelog cleanup

## Objective

Clean up documentation/version inconsistencies discovered after Week 3.

## Context

Week 3 implemented static dashboard functionality. README examples and version/changelog language should reflect the actual v0.2 dashboard milestone.

## Dependencies

- Week 3 completed

## Target Files

- README.md
- CHANGELOG.md
- pyproject.toml
- src/skilllogboard/_version.py
- docs/status_matrix.md

## Implementation Steps

1. Replace any README output path such as `runs/demo//` with `runs/demo/<run_id>/`.
2. Tell users to open `runs/demo/<run_id>/dashboard.html` after running the basic example.
3. Choose and apply a consistent version strategy: `0.2.0-dev`/`0.2.0a0`, or state that v0.2 is a milestone while package version remains unchanged.
4. Split CHANGELOG into clear v0.1 MVP and v0.2 dashboard candidate sections.
5. Keep Week 4+ features marked Planned.

## Acceptance Criteria

- README does not contain `runs/demo//`.
- README explains how to find `dashboard.html`.
- Version wording is consistent.
- CHANGELOG has a clear v0.2 dashboard entry.
- Status matrix does not mark rule engine/compare/plugins as implemented.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
readme=Path('README.md').read_text(encoding='utf-8')
assert 'runs/demo//' not in readme
assert 'dashboard.html' in readme
print('README cleanup OK')
PY
pytest -q
```

## Non-goals

- Do not implement Skills.md parser here.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 3.
- Do not implement Week 5+ features unless this file explicitly asks for a placeholder.
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
**Completed at:** 2026-05-09 23:49  
**Completed by:** coding agent  
**Verification command(s):** python - <<'PY' README cleanup check; pytest -q  
**Notes:** README paths, version wording, changelog grouping, and v0.2 dashboard docs were checked successfully.

<!-- AGENT_STATUS: COMPLETED -->

