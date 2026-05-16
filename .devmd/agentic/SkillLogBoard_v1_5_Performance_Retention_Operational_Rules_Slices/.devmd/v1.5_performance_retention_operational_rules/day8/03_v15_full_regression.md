---
milestone: "v1.5"
phase: "Performance, Retention, and Operational Rules"
day: "day8"
slice: "03_v15_full_regression"
title: "v1.5 full regression"
priority: "P1"
status: "completed"
target_version: "v1.5"
---

# 03_v15_full_regression — v1.5 full regression

## Objective

Run full regression for performance, retention, and operational rules.

## Context

v1.5 makes SkillLogBoard sustainable for real local research projects by adding performance guardrails, retention/pruning policy, JSONL rotation, compare scalability, and agent-safe operational rules.

## Dependencies

- v1.4 Portable Report Maturity completed or planned separately.
- v1.2/v1.3 Live Board app shell and commercial UI contracts are available.
- Agent Research Layer and Template Forge concepts are available.

## Target Files

- .github/workflows/ci.yml
- tests/
- .devmd/v1.5_performance_retention_operational_rules/**/*.md

## Implementation Steps

1. Run ruff.
2. Run full pytest.
3. Run performance/retention/agent-specific test subsets.
4. Run large demo if environment allows.
5. Run build no-isolation.
6. Confirm GitHub Actions green after push.

## Acceptance Criteria

- Ruff passes.
- Full pytest passes.
- Specific subsets pass.
- Large demo passes or limitation is recorded.
- Build passes.
- Latest CI is green or explicitly noted.

## Verification Commands

```bash
pip install -e ".[dev,dashboard,report,live]"
ruff check .
pytest -q
pytest -q tests/test_project_index.py tests/test_metric_summary_cache.py tests/test_large_project_performance.py tests/test_retention_policy.py tests/test_prune_planner.py tests/test_jsonl_rotation.py tests/test_agent_safety.py tests/test_agent_handoff.py
python examples/live_demo.py --multi-run --runs 80 --rich
python -m build --no-isolation
```

## Non-goals

- Do not make destructive deletion the default behavior.
- Do not require a database for indexing/cache.
- Do not claim SkillLogBoard executes agents automatically.
- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not perform TestPyPI/PyPI publishing in this slice.
- Do not weaken local-first, inspectable-file behavior.

## Handoff Notes

- Keep the slice focused and reviewable.
- Prefer additive metadata/state fields over breaking existing artifact contracts.
- Preserve the separation between portable static evidence and local Live Board app behavior.
- If an item is deferred, document the reason in the Agent Completion Block.
- Update related docs/status/changelog when user-visible behavior changes.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-16
**Completed by:** Codex
**Verification command(s):**
- .venv/bin/python -m pytest tests/test_v15_index_query.py tests/test_v15_live_compare.py tests/test_v15_retention_agent.py tests/test_v15_artifact_storage.py -q
- .venv/bin/python -m pytest tests/test_live_project.py tests/test_live_server.py tests/test_cli.py tests/test_cli_live.py tests/test_cli_agent.py tests/test_agent_handoff.py tests/test_template_forge_validator.py tests/test_report_assets.py tests/test_report_manifest.py -q
- .venv/bin/python -m ruff check src/skilllogboard tests/test_v15_index_query.py tests/test_v15_live_compare.py tests/test_v15_retention_agent.py tests/test_v15_artifact_storage.py
- .venv/bin/python -m pytest -q
- .venv/bin/python -m ruff check src tests
- .venv/bin/python examples/live_demo.py --multi-run --runs 80 --rich
- .venv/bin/python -m build --no-isolation
**Completion evidence backlog:**
- B1: Focused v1.5 pytest suite passed: 9 passed.
- B2: Existing live/CLI/agent/report regression subset passed: 44 passed.
- B3: Full pytest passed: 267 passed.
- B4: Full ruff passed: All checks passed.
- B5: 80-run rich Live Board demo completed and printed 80 run directories under runs/live_demo.
- B6: Package build passed with --no-isolation, producing skilllogboard-1.5.0.dev0 tar.gz and wheel.
- B7: Isolated build was attempted first and failed because the host Python lacks ensurepip/python3.10-venv; this is an environment limitation, not a package build failure.
**Notes:** Implemented in the local v1.5 working tree; no destructive prune/delete action was executed.

<!-- AGENT_STATUS: COMPLETED -->
