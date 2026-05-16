# v1.5 Release Candidate Note

v1.5 adds performance, retention, and operational guardrails while preserving SkillLogBoard's
local-first file model.

## Release Checklist

- Rebuild a project index with `skilllog index rebuild PROJECT_DIR`.
- Preview large-project filters with `skilllog runs list PROJECT_DIR --filter "tag:nightly"`.
- Verify lazy series behavior through `/api/series` or `/api/compare`.
- Preview retention with `skilllog prune PROJECT_DIR --json`.
- Preview JSONL rotation with `skilllog rotate RUN_DIR --max-lines 100000 --json`.
- Generate agent handoff and confirm both `agent/handoff.md` and `agent/handoff.json` exist.
- Run `ruff`, focused v1.5 tests, full pytest, and package build before tagging.

## Guardrails

- Prune and rotate commands default to dry-run.
- Destructive deletion remains guarded behind an explicit external retention runner.
- Agent safety gates deny protected core and manifest paths unless a human changes policy.
- The project index is derived data and can be deleted or rebuilt at any time.
