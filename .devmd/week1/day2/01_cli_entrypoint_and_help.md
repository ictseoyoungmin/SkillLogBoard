---
week: 1
day: 2
slice: "01_cli_entrypoint_and_help"
title: "CLI entrypoint and help"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 01_cli_entrypoint_and_help — CLI entrypoint and help

## Objective

Implement the `skilllog` CLI entry point and help output.

## Context

The development plan requires `skilllog --help` to pass in Week 1. Use `argparse` unless there is a strong reason to add a dependency.

## Dependencies

- day1/01_pyproject_and_package_metadata
- day1/02_src_layout_and_public_api

## Target Files

- src/skilllogboard/cli/main.py
- pyproject.toml
- tests/test_cli.py

## Implementation Steps

1. Implement `main(argv=None)` in `skilllogboard.cli.main`.
2. Create an `ArgumentParser` with program name `skilllog`.
3. Add `--version` support using `skilllogboard.__version__`.
4. Add subparser placeholders for `init`, `inspect`, `dashboard`, `report`, `compare`, and `export-table`.
5. Return integer exit codes from command handlers.
6. Add tests for `--help` and `--version` using subprocess or direct parser invocation.

## Acceptance Criteria

- `skilllog --help` exits with code 0.
- `skilllog --version` exits with code 0.
- The help output lists the expected subcommands.
- No optional dashboard dependencies are required for `--help`.

## Verification Commands

```bash
skilllog --help
skilllog --version
pytest -q tests/test_cli.py
```

## Non-goals

- Do not implement actual compare/export-table behavior in this slice.

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
**Verification command(s):** skilllog --help; skilllog --version; pytest -q tests/test_cli.py  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
