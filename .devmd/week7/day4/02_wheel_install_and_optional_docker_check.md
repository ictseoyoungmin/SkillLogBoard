---
week: 7
day: 4
slice: "02_wheel_install_and_optional_docker_check"
title: "wheel install and optional Docker check"
priority: "P0"
status: "completed"
target_version: "v0.6-release-hardening"
---

# 02_wheel_install_and_optional_docker_check — wheel install and optional Docker check

## Objective

Verify wheel install path and optionally add Docker-based clean build check.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- scripts/verify_wheel_install.sh
- Dockerfile.test
- docs/release_checklist.md

## Implementation Steps

1. Create or document wheel install verification.
2. Build wheel with python -m build --no-isolation if needed.
3. Install generated wheel into temporary environment if possible.
4. Optionally add Dockerfile.test for isolated build/test check.
5. Document Docker as optional.

## Acceptance Criteria

- Wheel install verification script or docs exist.
- Docker verification is optional.
- No secrets or sudo are required.

## Verification Commands

```bash
test -f scripts/verify_wheel_install.sh || grep -i wheel docs/release_checklist.md
test -f Dockerfile.test || grep -i Docker docs/release_checklist.md
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
**Completed at:** 2026-05-10 21:15
**Completed by:** coding agent
**Verification command(s):** bash -n scripts/verify_wheel_install.sh; bash scripts/verify_wheel_install.sh dist/skilllogboard-0.6.0.dev0-py3-none-any.whl; test -f Dockerfile.test
**Notes:** Added wheel install verification script and optional Dockerfile.test. Local `python -m venv` lacks ensurepip, so scripts fall back to `virtualenv`; wheel install verification passed.

<!-- AGENT_STATUS: COMPLETED -->
