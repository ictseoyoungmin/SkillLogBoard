---
week: 7
day: 5
slice: "01_full_release_candidate_test_matrix"
title: "full release candidate test matrix"
priority: "P0"
status: "completed"
target_version: "v0.6-release-hardening"
---

# 01_full_release_candidate_test_matrix — full release candidate test matrix

## Objective

Run the full release candidate verification matrix locally as far as the environment allows.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- docs/release_checklist.md
- .devmd/week7/**/*.md

## Implementation Steps

1. Run editable install with dev/dashboard extras.
2. Run CLI help.
3. Run full pytest suite.
4. Run core examples.
5. Run build no-isolation.
6. Record any isolated build limitation in completion notes.

## Acceptance Criteria

- Editable install succeeds.
- skilllog --help succeeds.
- pytest -q succeeds.
- basic/ir-drop/trajectory examples succeed.
- python -m build --no-isolation succeeds.
- Any environment limitation is documented.

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

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-10 21:20
**Completed by:** coding agent
**Verification command(s):** .venv/bin/pip install -e ".[dev,dashboard]"; .venv/bin/skilllog --help; .venv/bin/pytest -q; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation
**Notes:** Full local release candidate matrix passed. `pytest -q` passed with 131 tests. Local isolated venv creation uses `virtualenv` fallback because system `venv/ensurepip` is unavailable.

<!-- AGENT_STATUS: COMPLETED -->
