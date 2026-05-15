# SkillLogBoard v1.4 Cleanup Slices

## Purpose

This cleanup pass follows the v1.4 Portable Report Maturity implementation review.

v1.4 is functionally complete, but the following items should be cleaned up before starting v1.5:

```text
1. Package version still reports 1.2.0.dev0
2. Changelog/status/docs should explicitly reflect v1.4 completion
3. GitHub Actions / CI green should be confirmed
4. Portable report validation JSON can be made more agent-friendly
5. Package/report docs should clarify offline JS/CSS behavior
6. Baseline delta fields should be documented as present but partially operational if not fully wired
7. Final v1.4 smoke evidence should be collected in one release-candidate note
```

## Scope Boundary

Allowed:

- Version and metadata cleanup
- Docs, changelog, status matrix updates
- Report validation JSON polish
- Tests for already-implemented v1.4 functionality
- CI verification and release-candidate note

Not allowed:

- v1.5 project index
- retention/pruning implementation
- JSONL rotation implementation
- agent safety gate implementation
- PyPI/TestPyPI publishing

## Recommended Execution Order

```text
.devmd/v1.4_cleanup/
  01_version_and_package_metadata_sync.md
  02_docs_changelog_status_matrix_sync.md
  03_report_validation_json_polish.md
  04_portable_report_docs_and_baseline_delta_note.md
  05_ci_and_full_regression_evidence.md
  06_v14_release_candidate_closeout.md
```

## Completion Protocol

Each slice has an Agent Completion Block. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partially implemented work.
