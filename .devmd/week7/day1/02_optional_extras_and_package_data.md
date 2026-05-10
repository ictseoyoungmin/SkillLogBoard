---
week: 7
day: 1
slice: "02_optional_extras_and_package_data"
title: "optional extras and package data"
priority: "P0"
status: "pending"
target_version: "v0.6-release-hardening"
---

# 02_optional_extras_and_package_data — optional extras and package data

## Objective

Validate optional extras and ensure runtime package data is included in builds.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- pyproject.toml
- MANIFEST.in
- tests/test_optional_integrations.py
- tests/test_dashboard_packaging.py

## Implementation Steps

1. Review project dependencies and optional extras.
2. Ensure core dependencies do not include torch, lightning, sklearn, pandas, or domain packages.
3. Ensure dashboard templates and default_skills.md are included as package data.
4. Strengthen package data tests if needed.

## Acceptance Criteria

- Core dependencies remain lightweight.
- Optional integrations remain optional.
- Dashboard templates are packaged.
- default_skills.md is packaged.
- Relevant tests pass.

## Verification Commands

```bash
pytest -q tests/test_optional_integrations.py tests/test_dashboard_packaging.py
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

