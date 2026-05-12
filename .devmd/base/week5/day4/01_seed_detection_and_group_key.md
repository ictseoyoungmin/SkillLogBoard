---
week: 5
day: 4
slice: "01_seed_detection_and_group_key"
title: "seed detection and group key"
priority: "P0"
status: "completed"
target_version: "v0.4-compare"
---

# 01_seed_detection_and_group_key — seed detection and group key

## Objective

Detect seed values and build group keys for seed aggregation.

## Context

D24 requires seed grouping mean/std and best/median calculations. First define grouping behavior.

## Dependencies

- day3 config diff slices

## Target Files

- src/skilllogboard/compare/seed_group.py
- tests/test_seed_group.py

## Implementation Steps

1. Implement helper to extract seed from config or manifest.
2. Implement `make_group_key(record, exclude_keys=['seed'])` using flattened config.
3. Allow optional `group_by` config keys.
4. Ensure runs that differ only by seed group together.
5. Add tests for seed in config, seed in manifest, and missing seed.

## Acceptance Criteria

- Seed extraction works from config/manifest.
- Runs differing only by seed can share group key.
- Explicit group_by works.
- Missing seed handled as None/unknown.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_seed_group.py
```

## Non-goals

- Do not aggregate metrics yet.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
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
**Completed at:** 2026-05-10 00:36  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_seed_group.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

