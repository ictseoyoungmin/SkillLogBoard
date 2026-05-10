---
week: 7
day: 5
slice: "03_week7_final_verification_and_v06_candidate"
title: "Week 7 final verification and v0.6 candidate"
priority: "P0"
status: "pending"
target_version: "v0.6-release-hardening"
---

# 03_week7_final_verification_and_v06_candidate — Week 7 final verification and v0.6 candidate

## Objective

Finalize Week 7 release hardening and mark v0.6 candidate status.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- CHANGELOG.md
- README.md
- docs/release_checklist.md
- .devmd/week7/**/*.md

## Implementation Steps

1. Run final verification command set.
2. Fix only blocking failures.
3. Ensure release notes, release checklist, and release decision docs exist.
4. Update CHANGELOG with v0.6 release-hardening candidate notes.
5. Confirm all Week 7 completion blocks are completed or blockers are documented.
6. Record final limitations and next step recommendation.

## Acceptance Criteria

- Full test suite passes.
- Examples pass.
- Build no-isolation passes.
- Release docs exist.
- CHANGELOG has v0.6 candidate entry.
- Week 7 completion blocks are updated.

## Verification Commands

```bash
pip install -e ".[dev,dashboard]"
skilllog --help
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python -m build --no-isolation
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

