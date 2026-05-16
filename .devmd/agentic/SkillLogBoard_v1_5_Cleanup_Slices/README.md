# SkillLogBoard v1.5 Cleanup Slices

## Purpose

This cleanup pass follows the v1.5 implementation review. v1.5 is functionally complete, but four release-hygiene items should be addressed before treating it as a clean release candidate.

## Scope

```text
.devmd/v1.5_cleanup/
  01_prune_execute_wording_and_safety_note.md
  02_retention_best_metric_mode_policy.md
  03_project_index_artifact_count_lightweighting.md
  04_ci_and_v15_release_candidate_closeout.md
```

## Cleanup Goals

```text
1. Make prune CLI wording unambiguous and safe.
2. Make retention best-run protection aware of metric mode.
3. Avoid expensive artifact enumeration during project index rebuilds.
4. Record CI/full-regression evidence in the v1.5 release candidate note.
```

## Completion Protocol

Each slice has an Agent Completion Block. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partially implemented work.

## Recommended Final Verification

```bash
pip install -e ".[dev,dashboard,report,live]"
ruff check .
pytest -q
pytest -q tests/test_live_project.py tests/test_live_server.py
pytest -q tests/test_retention_policy.py tests/test_prune_planner.py tests/test_cli_prune.py
pytest -q tests/test_project_index.py tests/test_metric_summary_cache.py
python examples/live_demo.py --multi-run --runs 80 --rich
python -m build --no-isolation
```
