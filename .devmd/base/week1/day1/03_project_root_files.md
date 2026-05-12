---
week: 1
day: 1
slice: "03_project_root_files"
title: "project root files"
priority: "P1"
status: "completed"
target_version: "v0.1-dev"
---

# 03_project_root_files — project root files

## Objective

Add repository-level documentation and hygiene files needed for development.

## Context

The repository should be usable by a human developer and an AI coding agent without additional context.

## Dependencies

- 01_pyproject_and_package_metadata

## Target Files

- README.md
- CHANGELOG.md
- LICENSE
- .gitignore
- docs/roadmap.md

## Implementation Steps

1. Create a concise README with install, CLI, and minimal usage placeholders.
2. Create a CHANGELOG with `0.1.0-dev` entry.
3. Add a permissive license placeholder such as MIT.
4. Add `.gitignore` entries for Python build artifacts, caches, virtualenvs, and generated `runs/`.
5. Add `docs/roadmap.md` with version milestones.

## Acceptance Criteria

- README includes `pip install -e` instructions.
- README includes a minimal `RunLogger` usage example.
- Generated local artifacts such as `runs/` are ignored by git.

## Verification Commands

```bash
test -f README.md
test -f .gitignore
```

## Non-goals

- Do not write full product documentation here; keep it lightweight.

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
**Verification command(s):** test -f README.md; test -f .gitignore  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
