# SkillLogBoard Week 1 Development Slices

This directory contains small, agent-executable development slices for Week 1.

## Dev

For development, use the .venv created with "virtualenv --always-copy.venv". If necessary for verification, you can delete it and recreate it.

## Week 1 Goal

Build the foundational package skeleton and file-based run evidence schema:

- installable Python package
- `src/skilllogboard` layout
- CLI entry point and basic commands
- RunId generation
- Manifest schema and atomic save/load
- Event schema and JSONL writer
- Metrics CSV writer
- Config/system/git snapshot helpers
- Week 1 integration smoke test

## Completion Protocol

Each slice file contains an **Agent Completion Block** at the bottom.

After finishing a slice, the agent must:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for any skipped, deferred, or partially implemented item.

## Recommended Execution Order

Follow day and slice order:

```text
week1 : day1 -> day2 -> day3 -> day4 -> day5
```

Do not start a later slice if its dependency slice failed.
