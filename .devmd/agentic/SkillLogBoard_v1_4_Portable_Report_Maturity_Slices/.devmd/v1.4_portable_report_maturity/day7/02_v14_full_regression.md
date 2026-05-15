---
milestone: "v1.4"
phase: "Portable Report Maturity"
day: "day7"
slice: "02_v14_full_regression"
title: "v1.4 full regression"
priority: "P1"
status: "completed"
target_version: "v1.4"
---

# 02_v14_full_regression — v1.4 full regression

## Objective

Run full regression for report maturity.

## Context

v1.4 matures static dashboard/report outputs into portable, offline-friendly research evidence packages with manifests, figures, tables, and provenance metadata.

## Dependencies

- v1.3 Commercial Live UI completed or planned separately.
- Static dashboard/report outputs remain independent from the Live Board app.
- Report Artifact Layer v0.7+ concepts are available.

## Target Files

- .github/workflows/ci.yml
- tests/
- .devmd/v1.4_portable_report_maturity/**/*.md

## Implementation Steps

1. Run ruff.
2. Run full pytest.
3. Run report-specific tests.
4. Run rich demo.
5. Run build no-isolation.
6. Confirm GitHub Actions green after push.

## Acceptance Criteria

- Ruff passes.
- Full pytest passes.
- Report tests pass.
- Rich demo passes.
- Build passes.
- Latest CI is green or explicitly noted.

## Verification Commands

```bash
pip install -e ".[dev,dashboard,report,live]"
ruff check .
pytest -q
pytest -q tests/test_report_manifest.py tests/test_report_provenance.py tests/test_report_rendering.py tests/test_report_assets.py tests/test_report_figures.py tests/test_report_tables.py tests/test_cli_report.py
python examples/live_demo.py --multi-run --runs 5 --rich
python -m build --no-isolation
```

## Non-goals

- Do not require the Live Board server to view static reports.
- Do not require external CDN/network access for portable reports.
- Do not replace report artifacts with screenshots only.
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
**Completed at:** 2026-05-15  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -m ruff check .`; `.venv/bin/python -m pytest -q`; `.venv/bin/python examples/live_demo.py --multi-run --runs 5 --rich`; `.venv/bin/python -m skilllogboard.cli.main report validate runs/live_demo/report --json`; `.venv/bin/python -m skilllogboard.cli.main report bundle runs/live_demo/report --output runs/live_demo/report.zip`; `.venv/bin/python -m build --no-isolation`  
**Notes:** Implemented and verified as part of the v1.4 portable report maturity pass. Static reports remain separate from the Live Board and render without external CDN dependencies.  

<!-- AGENT_STATUS: COMPLETED -->

