---
milestone: "v1.4-cleanup"
phase: "Portable Report Maturity Cleanup"
slice: "05_ci_and_full_regression_evidence"
title: "CI and full regression evidence"
priority: "P0"
status: "completed"
---

# 05_ci_and_full_regression_evidence — CI and full regression evidence

## Objective

Collect explicit full-regression and CI evidence for the v1.4 closeout.

## Context

v1.4 Portable Report Maturity is functionally complete. This cleanup pass fixes release/version consistency, documentation truthfulness, CI verification, report validation polish, and small packaging/documentation issues before moving into v1.5 Performance, Retention, and Operational Rules.

## Target Files

- .github/workflows/ci.yml
- docs/v1_4_release_candidate_note.md
- docs/release_candidate_checklist.md

## Implementation Steps

1. Run the full local v1.4 verification suite.
2. Run report-specific tests.
3. Run the rich demo and validate/bundle the generated report.
4. Run `python -m build --no-isolation`.
5. Check GitHub Actions after pushing if repository access is available.
6. Record exact commands and outcomes in the v1.4 release candidate note.
7. If GitHub Actions cannot be checked from the local environment, write that limitation explicitly.

## Acceptance Criteria

- Full local regression commands are recorded.
- Report-specific test suite passes.
- Rich demo report validate/bundle commands pass.
- Build passes.
- GitHub Actions status is recorded or limitation is explicitly noted.

## Verification Commands

```bash
pip install -e ".[dev,dashboard,report,live]"
ruff check .
pytest -q
pytest -q tests/test_report_manifest.py tests/test_report_rendering.py tests/test_report_assets.py tests/test_report_figures.py tests/test_report_tables.py tests/test_cli_report_artifacts.py
python examples/live_demo.py --multi-run --runs 5 --rich
python -m skilllogboard.cli.main report validate runs/live_demo/report --json
python -m skilllogboard.cli.main report bundle runs/live_demo/report --output runs/live_demo/report.zip
python -m build --no-isolation
```

## Non-goals

- Do not start v1.5 implementation in this cleanup pass.
- Do not implement pruning, retention, JSONL rotation, project index, or agent safety gate here.
- Do not publish to TestPyPI/PyPI.
- Do not introduce cloud sync, multi-user auth, Prometheus/Grafana, or TensorBoard/W&B import.
- Do not make static reports depend on the Live Board server.
- Do not require external CDN/network access for portable reports.

## Additional Notes

- Previous review could not confirm GitHub Actions status from the connector. This slice must either verify it directly or document why it cannot be verified.

## Handoff Notes

- Keep changes small and reviewable.
- Prefer documentation/status/version fixes over feature expansion.
- If a verification command cannot run due to local environment limits, record the exact blocker in the Agent Completion Block.
- Keep v1.4 static report behavior separate from v1.3 Live Board frontend behavior.
- Preserve backward compatibility for existing report package paths.

---

## Agent Completion Block## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-15  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -m ruff check .`; `.venv/bin/python -m pytest -q`; `.venv/bin/python -m pytest -q tests/test_report_manifest.py tests/test_report_rendering.py tests/test_report_assets.py tests/test_report_figures.py tests/test_report_tables.py tests/test_cli_report_artifacts.py`; `.venv/bin/python examples/live_demo.py --multi-run --runs 5 --rich`; `.venv/bin/python -m skilllogboard.cli.main report validate runs/live_demo/report --json`; `.venv/bin/python -m skilllogboard.cli.main report bundle runs/live_demo/report --output runs/live_demo/report.zip`; `.venv/bin/python -m build --no-isolation`  
**Notes:** Completed v1.4 cleanup: package/CLI version now reports 1.4.0.dev0, report validation JSON includes code/severity/suggested_action, docs and RC evidence are updated, and CI now checks package/CLI version sync. GitHub Actions logs could not be inspected because gh is not installed and no open PR was returned. Local frontend npm checks are blocked by this WSL Node launcher, but GitHub Actions uses setup-node. Ignored build/demo artifacts were generated during verification; automatic deletion was blocked by the escalation usage limit.

<!-- AGENT_STATUS: COMPLETED -->
