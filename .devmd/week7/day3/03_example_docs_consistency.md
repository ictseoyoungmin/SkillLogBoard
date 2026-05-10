---
week: 7
day: 3
slice: "03_example_docs_consistency"
title: "example docs consistency"
priority: "P0"
status: "completed"
target_version: "v0.6-release-hardening"
---

# 03_example_docs_consistency — example docs consistency

## Objective

Ensure examples documented in README/docs exist and run or skip cleanly.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- examples/
- README.md
- docs/templates.md
- tests/test_examples.py

## Implementation Steps

1. Collect example filenames referenced in README and docs.
2. Ensure referenced files exist.
3. Ensure lightweight examples are smoke-tested.
4. Mark optional examples clearly if any require optional dependencies.

## Acceptance Criteria

- Documented examples exist.
- Lightweight examples are smoke-tested.
- Optional examples are clearly marked optional.

## Verification Commands

```bash
pytest -q tests/test_examples.py
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
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
**Completed at:** 2026-05-10 21:12
**Completed by:** coding agent
**Verification command(s):** .venv/bin/pytest -q tests/test_examples.py; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py
**Notes:** Added documented-example existence coverage and verified lightweight examples run successfully.

<!-- AGENT_STATUS: COMPLETED -->
