---
milestone: "v1.5-cleanup"
phase: "Performance, Retention, and Operational Rules Cleanup"
slice: "01_prune_execute_wording_and_safety_note"
title: "prune execute wording and safety note"
priority: "P0"
status: "pending"
---

# 01_prune_execute_wording_and_safety_note — prune execute wording and safety note

## Objective

Make `skilllog prune` CLI behavior unambiguous and prevent users from mistaking v1.5 planning for destructive deletion.

## Context

v1.5 Performance, Retention, and Operational Rules is functionally complete. This cleanup pass closes four review items before packaging, beta release, or the next roadmap milestone:

1. `skilllog prune --execute` can be misunderstood because v1.5 still produces a plan rather than deleting files.
2. Retention `keep_best` currently risks treating larger values as better even for loss/error metrics.
3. Project index artifact counting can be made lighter for large projects.
4. CI and v1.5 release-candidate evidence should be collected explicitly.

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/retention/planner.py
- docs/operational_rules.md
- docs/v1_5_release_candidate_note.md
- tests/test_cli_prune.py
- tests/test_prune_planner.py

## Implementation Steps

1. Review current `skilllog prune` CLI options and help text, especially `--execute`.
2. Decide whether to remove `--execute`, rename it, or keep it with stronger wording. Preferred safe option: keep backward compatibility but describe it as `mark plan as non-dry-run; does not delete files in v1.5`.
3. Ensure CLI output clearly states that v1.5 prune produces a plan and does not delete files.
4. If `--execute` remains, add a warning line in non-JSON output and a structured field in JSON output such as `destructive_actions_performed: false`.
5. Update `docs/operational_rules.md` to state that Safety Gate / retention planning is not a destructive file deletion runner.
6. Update `docs/v1_5_release_candidate_note.md` guardrails with the exact prune behavior.
7. Add or update tests that assert `skilllog prune --execute` does not delete run directories.
8. Add tests that assert prune help/output includes non-destructive wording.

## Acceptance Criteria

- `skilllog prune` default remains dry-run.
- `skilllog prune --execute` does not delete files in v1.5.
- CLI help/output makes non-destructive behavior explicit.
- JSON output includes enough information for agents/users to know whether destructive actions were performed.
- Operational docs and RC note contain the same safety policy.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_prune.py tests/test_prune_planner.py
python -m skilllogboard.cli.main prune --help
python -m skilllogboard.cli.main prune runs --json || true
python -m skilllogboard.cli.main prune runs --execute --json || true
```

## Non-goals

- Do not start a new v1.6 feature milestone in this cleanup pass.
- Do not implement destructive pruning/deletion as default behavior.
- Do not add a database backend for the project index.
- Do not add cloud sync, multi-user auth, Prometheus/Grafana, or TensorBoard/W&B import.
- Do not weaken local-first file-backed behavior.
- Do not publish to TestPyPI/PyPI in this cleanup pass.

## Additional Notes

- Do not implement actual deletion in this slice.
- If the project does not currently have `tests/test_cli_prune.py`, create it or place equivalent coverage in the existing CLI test file and document the path used.

## Handoff Notes

- Keep cleanup changes narrow and reviewable.
- Prefer safety, explicit wording, and policy correctness over feature expansion.
- If a verification command cannot run due to local environment limits, record the exact blocker in the Agent Completion Block.
- Preserve backward compatibility for existing v1.5 CLI and data files where possible.
- Update docs/changelog/status matrix when user-visible behavior or policy wording changes.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-16
**Completed by:** Claude (Sonnet 4.6)
**Verification command(s):**
- .venv/bin/pytest tests/test_cli_prune.py tests/test_v15_retention_agent.py -q
**Notes:**
- Added `destructive_actions_performed: false` to `plan_prune()` return value.
- Updated CLI text output to always print safety note; `--execute` text clarified as "PLAN (no files deleted)".
- Updated `--execute` help text: "Mark plan as non-dry-run; does not delete files in v1.5".
- Created tests/test_cli_prune.py with 4 tests covering dry-run default, execute non-deletion, text safety note, external runner note.
- Updated docs/operational_rules.md and docs/v1_5_release_candidate_note.md.

<!-- AGENT_STATUS: COMPLETED -->

