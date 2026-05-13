# SkillLogBoard v1.0 Local-first Live Board Slices

This package contains the v1.0 Local-first Live Board development plan and agent-executable slices.

## v1.0 Goal

Implement a local-first live experiment control board:

- `skilllog watch`
- local watch server
- browser-based live board
- passive run-folder polling
- optional active monitoring
- `monitoring.jsonl`
- live state aggregation
- run status, metric curves, event timeline, rule audit, artifact feed, log tail
- project-level watch overview

## Explicit Non-goals

- no TensorBoard import
- no W&B import
- no Prometheus/Grafana integration
- no cloud sync
- no multi-user auth
- no remote collaboration
- no database backend
- no model registry
- no deployment server

## Included Files

```text
SkillLogBoard_v1.0_Live_Board_DevPlan.md

.devmd/v1.0_live_board/
  README.md
  day1/
  day2/
  day3/
  day4/
  day5/
```

## Completion Protocol

Each slice has an Agent Completion Block. After finishing a slice:

1. Tick completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partial work.
