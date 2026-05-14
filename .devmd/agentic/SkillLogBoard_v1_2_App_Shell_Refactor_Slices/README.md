# SkillLogBoard v1.2 App Shell Refactor Slices

## Purpose

v1.2 converts the Live Board from a single composite dashboard into a real local app shell:

```text
Overview
Runs
Compare
Metric Lab
Artifacts
Reports
Agent
Local Settings
```

This milestone should make project mode understandable, avoid feature clutter, and prevent performance problems as the number of runs grows.

## Core Product Decision

Static outputs and Live Board have different purposes:

```text
Static dashboard/report:
  portable evidence document
  Jinja2 + inline/local assets
  no app shell requirement

Live Board:
  local app shell
  view-level navigation
  lazy state loading
  local FastAPI backend
```

## Included Structure

```text
SkillLogBoard_v1.2_App_Shell_Refactor_DevPlan.md

.devmd/v1.2_app_shell_refactor/
  README.md
  day1/
  day2/
  day3/
  day4/
  day5/
  day6/
  day7/
```

## Completion Protocol

Each slice has an Agent Completion Block. After finishing a slice:

1. Tick completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partial work.

## Final Verification

```bash
pip install -e ".[dev,dashboard,live]"
ruff check .
pytest -q
python examples/live_demo.py --multi-run --runs 5 --rich
skilllog --help
skilllog watch --help
python -m build --no-isolation
```
