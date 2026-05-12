---
week: 3
day: 5
slice: "03_static_asset_policy_and_packaging_check"
title: "static asset policy and packaging check"
priority: "P0"
status: "completed_with_env_limitation"
target_version: "v0.2-dashboard"
---

# 03_static_asset_policy_and_packaging_check — static asset policy and packaging check

## Objective

Ensure dashboard templates/assets are packaged and static dashboard does not depend on local dev-only paths.

## Context

A common failure is dashboard templates working in the repo but missing after installation. This slice checks package data and relative link behavior.

## Dependencies

- day1/02_jinja2_template_loader_and_fallback

## Target Files

- pyproject.toml
- MANIFEST.in
- src/skilllogboard/dashboards/templates/run.html.j2
- tests/test_dashboard_packaging.py

## Implementation Steps

1. Verify dashboard templates are included as package data.
2. Use package resources or another install-safe loading mechanism.
3. Ensure generated dashboard uses relative links only.
4. Add a packaging-oriented test where practical.
5. Run build or install smoke command if appropriate.

## Acceptance Criteria

- Dashboard template is available after editable install.
- Generated dashboard links are relative.
- `python -m build` still succeeds.
- Packaging test passes.

## Verification Commands

```bash
pytest -q tests/test_dashboard_packaging.py
python -m build
```

## Non-goals

- Do not introduce external CDN dependency as a hard requirement.

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

**Status:** COMPLETED_WITH_ENV_LIMITATION  
**Completed at:** 2026-05-09 23:49  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_dashboard_packaging.py; python -m build --no-isolation  
**Notes:** `python -m build` without `--no-isolation` failed because the local system Python lacks `python3.10-venv`/`ensurepip`. `python -m build --no-isolation` completed successfully, so this is tracked as an environment limitation rather than an implementation failure. Isolated build should be rechecked in GitHub Actions, Docker, or an environment with `python3.10-venv` available.

<!-- AGENT_STATUS: COMPLETED_WITH_ENV_LIMITATION -->
