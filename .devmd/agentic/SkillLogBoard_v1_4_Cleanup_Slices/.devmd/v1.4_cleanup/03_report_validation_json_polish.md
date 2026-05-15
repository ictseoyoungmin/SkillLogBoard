---
milestone: "v1.4-cleanup"
phase: "Portable Report Maturity Cleanup"
slice: "03_report_validation_json_polish"
title: "report validation JSON polish"
priority: "P1"
status: "completed"
---

# 03_report_validation_json_polish — report validation JSON polish

## Objective

Make `skilllog report validate --json` more agent-friendly without starting the full v1.5 feedback schema work.

## Context

v1.4 Portable Report Maturity is functionally complete. This cleanup pass fixes release/version consistency, documentation truthfulness, CI verification, report validation polish, and small packaging/documentation issues before moving into v1.5 Performance, Retention, and Operational Rules.

## Target Files

- src/skilllogboard/reports/validate.py
- src/skilllogboard/cli/main.py
- tests/test_cli_report_artifacts.py
- tests/test_report_manifest.py
- docs/report_artifacts.md

## Implementation Steps

1. Review current `ReportValidationResult` JSON fields.
2. Add optional stable fields if low-risk: `code`, `severity`, and `suggested_action`.
3. Keep existing fields such as `outcome`, `name`, `message`, and `path` backward-compatible.
4. Map common report validation failures to readable codes, for example `MISSING_MANIFEST`, `MANIFEST_SCHEMA_ERROR`, `MISSING_OUTPUT`, `OFFLINE_HTML_EXTERNAL_REFERENCE`, `OUTPUT_SKIPPED`.
5. Update tests to verify JSON output remains valid and includes the new fields.
6. Document that this is a lightweight v1.4 polish step; full agent feedback integration remains v1.5 work.

## Acceptance Criteria

- `report validate --json` remains backward-compatible.
- JSON output includes stable enough fields for agent parsing.
- Validation errors include a suggested action where feasible.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_report_artifacts.py tests/test_report_manifest.py tests/test_report_rendering.py
python examples/live_demo.py --multi-run --runs 5 --rich
python -m skilllogboard.cli.main report validate runs/live_demo/report --json
```

## Non-goals

- Do not start v1.5 implementation in this cleanup pass.
- Do not implement pruning, retention, JSONL rotation, project index, or agent safety gate here.
- Do not publish to TestPyPI/PyPI.
- Do not introduce cloud sync, multi-user auth, Prometheus/Grafana, or TensorBoard/W&B import.
- Do not make static reports depend on the Live Board server.
- Do not require external CDN/network access for portable reports.

## Additional Notes

- Do not overbuild the full v1.5 `agent/feedback.py` schema here. This slice is a small compatibility polish only.

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
