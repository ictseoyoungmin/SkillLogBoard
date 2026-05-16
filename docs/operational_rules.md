# SkillLogBoard Operational Rules

v1.5 keeps large local projects usable by treating expensive data as opt-in evidence, not default
state.

## Performance

- Project overview state is summary-first: manifests, metric summaries, artifact counts, warnings,
  tags, groups, and baseline roles are loaded before any full metric series.
- `.skilllogboard/index.json` is derived and rebuildable with `skilllog index rebuild PROJECT_DIR`.
  It stores run IDs, paths, status, timestamps, key metrics, tags, group, baseline role, artifact
  counts, warning counts, and metric summary cache records.
- Full per-step series are loaded only through `/api/series` or `/api/compare` for explicit run and
  metric selections. Requests are clamped by `max_runs` and `max_points`.
- Downsampling is deterministic, preserves first and last points, and reports metadata describing
  the original and returned point counts.

## Query And Compare

- Runs can be filtered with `status:`, `tag:`, `group:`, `baseline:`, `metric:name>=value`, and
  `updated>=timestamp` expressions.
- `skilllog runs list PROJECT_DIR --filter "tag:nightly status:completed"` previews matching runs.
- Compare candidates accept the same filters and expose baseline roles plus last-value deltas from
  the selected baseline run when available.

## Retention

- Pruning is dry-run by default. `skilllog prune PROJECT_DIR` emits a plan with keep/archive/delete
  candidates and reasons.
- Baseline, latest, best, and excluded-tag runs are protected by default.
- Archive-before-delete is the default policy. The archive helper writes an `archive_manifest.json`
  into the zip before any external delete workflow is allowed.
- Checkpoint retention policy fields are explicit: keep best checkpoint, keep latest checkpoint,
  optional maximum checkpoint count, and baseline checkpoint protection.

## JSONL Rotation

- JSONL rotation can be planned by line count or byte count with `skilllog rotate RUN_DIR`.
- Rotation is dry-run unless `--execute` is provided.
- Executed rotations write a summary snapshot and deterministic rotated filename, with optional
  gzip compression.

## Artifact Storage

- Artifact storage supports `copy`, `symlink`, and `hardlink` modes.
- Unsupported symlink or hardlink attempts fall back to copy and record both requested and effective
  storage modes.

## Agent Guardrails

- Agent safety gates use explicit allowed and denied path/command policies.
- Core mutation, package metadata, and run manifests are protected by default.
- Agent handoff writes both `agent/handoff.md` for humans and `agent/handoff.json` for tools with
  summary, completed tasks, next actions, blockers, verification commands, and changed files.
- Template Forge and report validation can emit structured feedback records with status, errors,
  warnings, code, path, message, and suggested action.
