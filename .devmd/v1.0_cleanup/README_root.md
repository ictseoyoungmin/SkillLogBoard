# SkillLogBoard v1.0 Cleanup Slices

This package contains cleanup slices for the v1.0 Local-first Live Board after code review.

## Cleanup Goal

v1.0 Live Board is functionally complete. Before release-candidate packaging or TestPyPI work, perform a focused cleanup pass for:

- UI/API polling interval consistency
- project watch discovery performance
- actual HTTP smoke coverage for the Live Board server
- GPU monitor empty-parse warning behavior
- docs/status/changelog synchronization and final verification

## Included Slices

```text
.devmd/v1.0_cleanup/
  README.md
  01_live_poll_interval_and_health_config.md
  02_project_watch_discovery_performance.md
  03_live_server_http_smoke_test.md
  04_gpu_monitor_empty_parse_warning.md
  05_live_docs_status_and_final_verification.md
```

## Completion Protocol

Each slice has an **Agent Completion Block**. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partial work.

If a slice is blocked by environment limitations, use:

```text
**Status:** COMPLETED_WITH_ENV_LIMITATION
<!-- AGENT_STATUS: COMPLETED_WITH_ENV_LIMITATION -->
```

and explain the limitation in `Notes`.

## Final Verification

```bash
pip install -e ".[dev,dashboard,live]"
skilllog --help
skilllog watch --help
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python examples/live_demo.py
python -m build --no-isolation
```

If the `report` extra exists:

```bash
pip install -e ".[dev,dashboard,report]"
pytest -q tests/test_report_figures.py tests/test_cli_report_artifacts.py
```
