---
week: 1
day: 1
slice: "01_pyproject_and_package_metadata"
title: "pyproject and package metadata"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 01_pyproject_and_package_metadata — pyproject and package metadata

## Objective

Create a valid Python packaging configuration for an installable `skilllogboard` package.

## Context

Week 1 starts by making the repository installable with `pip install -e .`. This slice should establish the project metadata, build backend, optional extras, CLI script entry point, and test/tool configuration.

## Dependencies

- None

## Target Files

- pyproject.toml
- MANIFEST.in

## Implementation Steps

1. Create or update `pyproject.toml` using setuptools build backend.
2. Set project name to `skilllogboard` and version to `0.1.0` or `0.1.0-dev`.
3. Declare Python requirement `>=3.9`.
4. Add minimal runtime dependency `pyyaml>=6.0`.
5. Add optional extras for `dev`, `dashboard`, `table`, and `torch`.
6. Register console script: `skilllog = skilllogboard.cli.main:main`.
7. Configure package discovery under `src`.
8. Add package data entries for default skills and dashboard templates.
9. Add basic Ruff and pytest configuration.

## Acceptance Criteria

- `pip install -e .` succeeds in a fresh virtual environment.
- `python -m pip show skilllogboard` shows package metadata.
- The `skilllog` entry point is declared in project metadata.

## Verification Commands

```bash
pip install -e .
python -m pip show skilllogboard
```

## Non-goals

- Do not implement package publishing or PyPI upload in this slice.

## Handoff Notes

- Keep changes minimal and local to the target files.
- Prefer simple, explicit implementation over clever abstractions.
- Do not implement future-week features unless explicitly required by this slice.
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
**Completed at:** 2026-05-09 21:49  
**Completed by:** coding agent  
**Verification command(s):** pip install -e .; python -m pip show skilllogboard  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
