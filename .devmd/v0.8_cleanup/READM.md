# SkillLogBoard v0.8 Cleanup Slices

This package contains cleanup slices for the v0.8 Agent Research Layer after review.

## Cleanup Goal

v0.8 is functionally complete. Before starting v0.9 Template Forge, perform a short cleanup pass to improve:

- agent public API clarity
- agent completion rule policy
- `agent check` strictness behavior
- handoff evidence limitations
- docs and example workflows
- CI/workflow maintenance and final verification

## Included Slices

```text
.devmd/v0.8_cleanup/
  README.md
  01_agent_public_api_exports_and_import_boundary.md
  02_agent_required_commands_rule_policy.md
  03_agent_check_strictness_and_exit_policy.md
  04_handoff_evidence_and_files_changed_docs.md
  05_agent_docs_status_changelog_and_final_verification.md
```

## Completion Protocol

Each slice has an **Agent Completion Block**. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partial work.
