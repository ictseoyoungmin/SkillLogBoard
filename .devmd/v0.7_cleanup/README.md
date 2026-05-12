# SkillLogBoard v0.7 Cleanup Slices

This package contains cleanup slices for the v0.7 Report Artifact Layer after GitHub review.

## Cleanup Goal

v0.7 is functionally complete. Before starting v0.8 Agent Research Layer, perform a small cleanup pass for API polish, ReportSpec behavior alignment, optional figure test coverage, README/doc rendering, and CI maintenance.

## Included Slices

```text
.devmd/v0.7_cleanup/
  README.md
  01_reports_public_api_exports.md
  02_report_spec_figure_execution_or_docs.md
  03_optional_report_extra_figure_tests_and_ci.md
  04_readme_placeholder_and_docs_polish.md
  05_ci_actions_maintenance_and_final_verification.md
```

## Completion Protocol

Each slice has an Agent Completion Block. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partial work.

## Final Verification

```bash
pip install -e ".[dev,dashboard]"
skilllog --help
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python -m build --no-isolation
```

If the `report` extra exists:

```bash
pip install -e ".[dev,dashboard,report]"
pytest -q tests/test_report_figures.py tests/test_cli_report_artifacts.py
```
