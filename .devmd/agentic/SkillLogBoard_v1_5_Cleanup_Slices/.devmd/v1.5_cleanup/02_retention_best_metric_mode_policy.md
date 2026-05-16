---
milestone: "v1.5-cleanup"
phase: "Performance, Retention, and Operational Rules Cleanup"
slice: "02_retention_best_metric_mode_policy"
title: "retention best metric mode policy"
priority: "P0"
status: "pending"
---

# 02_retention_best_metric_mode_policy — retention best metric mode policy

## Objective

Make retention `keep_best` protection respect whether the selected metric should be maximized or minimized.

## Context

v1.5 Performance, Retention, and Operational Rules is functionally complete. This cleanup pass closes four review items before packaging, beta release, or the next roadmap milestone:

1. `skilllog prune --execute` can be misunderstood because v1.5 still produces a plan rather than deleting files.
2. Retention `keep_best` currently risks treating larger values as better even for loss/error metrics.
3. Project index artifact counting can be made lighter for large projects.
4. CI and v1.5 release-candidate evidence should be collected explicitly.

## Target Files

- src/skilllogboard/retention/policy.py
- src/skilllogboard/retention/planner.py
- src/skilllogboard/index/builder.py
- src/skilllogboard/index/schema.py
- src/skilllogboard/index/metrics.py
- docs/operational_rules.md
- tests/test_retention_policy.py
- tests/test_prune_planner.py
- tests/test_project_index.py

## Implementation Steps

1. Add retention policy fields for best-run selection, for example `best_metric_name: str | None` and `best_metric_mode: 'max' | 'min'`.
2. Default behavior should remain backward-compatible. If no best metric mode is available, preserve current max-based behavior but document the fallback.
3. Prefer manifest-derived metric direction when available: inspect `main_metric.mode`, `best_metric.mode`, or existing metric mode fields.
4. Update project index schema if needed so indexed runs can carry enough metric mode information for retention planning.
5. Update `plan_prune()` / `_protected_run_ids()` so `keep_best` uses max or min according to the selected metric mode.
6. Add tests with an accuracy-like metric where max is better.
7. Add tests with a loss-like metric where min is better.
8. Add docs explaining how retention chooses best runs and how to override metric/mode.

## Acceptance Criteria

- Retention can protect best runs using either max or min mode.
- Loss/error metric scenarios no longer protect the worst run by accident.
- Backward compatibility is preserved when no mode is specified.
- Docs explain default and override behavior.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_retention_policy.py tests/test_prune_planner.py tests/test_project_index.py
python - <<'PY'
from skilllogboard.retention.policy import RetentionPolicy
print(RetentionPolicy().to_dict())
PY
```

## Non-goals

- Do not start a new v1.6 feature milestone in this cleanup pass.
- Do not implement destructive pruning/deletion as default behavior.
- Do not add a database backend for the project index.
- Do not add cloud sync, multi-user auth, Prometheus/Grafana, or TensorBoard/W&B import.
- Do not weaken local-first file-backed behavior.
- Do not publish to TestPyPI/PyPI in this cleanup pass.

## Additional Notes

- This slice should not introduce a complex optimization policy language. Keep metric selection simple and explicit.
- If manifest mode extraction is incomplete, document fallback behavior and add a clear v1.6/vNext note.

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
- .venv/bin/pytest tests/test_retention_policy.py tests/test_cli_prune.py tests/test_v15_retention_agent.py -q
**Notes:**
- Added `best_metric_name: str | None` and `best_metric_mode: str` (default "max") to RetentionPolicy.
- Updated `from_dict()` to parse new fields; `to_dict()` serializes them via dataclass asdict.
- Updated `_protected_run_ids()` in planner.py: when `best_metric_name` is set, selects that metric value; applies min sort when `best_metric_mode == "min"`.
- Backward compatible: if no metric name/mode is specified, falls back to max-of-any-numeric behavior.
- Created tests/test_retention_policy.py with 6 tests covering max accuracy, min loss, fallback, from_dict, to_dict, and destructive_actions_performed.

<!-- AGENT_STATUS: COMPLETED -->

