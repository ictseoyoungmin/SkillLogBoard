---
week: 7
day: 2
slice: "01_ci_matrix_review_and_update"
title: "CI matrix review and update"
priority: "P0"
status: "completed"
target_version: "v0.6-release-hardening"
---

# 01_ci_matrix_review_and_update — CI matrix review and update

## Objective

Review and update GitHub Actions CI for release-hardening coverage.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- .github/workflows/ci.yml

## Implementation Steps

1. Ensure Python matrix includes supported Python versions.
2. Ensure CI installs with dev/dashboard extras.
3. Ensure CI runs ruff, pytest, and python -m build.
4. Keep workflow concise and deterministic.

## Acceptance Criteria

- CI has Python matrix.
- CI runs lint, tests, and build.
- Workflow YAML is valid by inspection.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text=Path('.github/workflows/ci.yml').read_text(encoding='utf-8')
for s in ['pytest','ruff','python -m build']:
    assert s in text
print('CI workflow content check passed')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 6.
- Do not implement Week 8+ publishing unless explicitly instructed.
- Keep optional integrations optional. Core install must not require torch, lightning, sklearn, pandas, or domain-specific packages.
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
**Completed at:** 2026-05-10 21:10
**Completed by:** coding agent
**Verification command(s):** .venv/bin/python -c "CI workflow content check"
**Notes:** CI now installs `.[dev,dashboard]`, runs `ruff check .`, `pytest -q`, and `python -m build` across Python 3.9-3.11.

<!-- AGENT_STATUS: COMPLETED -->
