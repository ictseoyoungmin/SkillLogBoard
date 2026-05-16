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
- `skilllog prune --execute` marks the plan as non-dry-run but does NOT delete or archive files in v1.5. Destructive deletion requires an explicit external retention runner.
- JSON prune output always includes `destructive_actions_performed: false` so agents and pipelines can verify no files were removed.
- Agent safety gates deny protected core and manifest paths unless a human changes policy.
- The project index is derived data and can be deleted or rebuilt at any time.
- Retention `keep_best` respects `best_metric_mode` (max or min). Loss/error metrics should set `best_metric_mode: min` to avoid protecting the worst run.
- Project index artifact counts use a lightweight counter; full artifact metadata is never loaded during index rebuilds.

## v1.5 Cleanup Verification (2026-05-16)

- ruff check src tests: All checks passed.
- pytest -q: 282 passed.
- 80-run rich demo: 80 run directories created under runs/live_demo.
- Package build --no-isolation: skilllogboard-1.5.0.dev0 tar.gz and wheel produced.
