---
milestone: "v1.4-cleanup"
phase: "Portable Report Maturity Cleanup"
slice: "01_version_and_package_metadata_sync"
title: "version and package metadata sync"
priority: "P0"
status: "completed"
---

# 01_version_and_package_metadata_sync — version and package metadata sync

## Objective

Synchronize package metadata with the completed v1.4 milestone.

## Context

v1.4 Portable Report Maturity is functionally complete. This cleanup pass fixes release/version consistency, documentation truthfulness, CI verification, report validation polish, and small packaging/documentation issues before moving into v1.5 Performance, Retention, and Operational Rules.

## Target Files

- pyproject.toml
- src/skilllogboard/_version.py
- README.md
- CHANGELOG.md
- docs/status_matrix.md

## Implementation Steps

1. Check the current package version in `pyproject.toml` and `src/skilllogboard/_version.py` if present.
2. Update the version from the stale v1.2 value to an appropriate v1.4 development value, such as `1.4.0.dev0`, unless the project uses another versioning convention.
3. Search for stale `1.2.0.dev0`, `v1.2`, or `v1.3` claims that now describe v1.4 behavior incorrectly.
4. Keep v1.2/v1.3 historical changelog entries intact; only fix current package/version metadata and misleading current-state wording.
5. Run package metadata and CLI version checks.

## Acceptance Criteria

- `pyproject.toml` no longer reports `1.2.0.dev0` as the current version.
- `skilllog --version` or equivalent version path reports the same version as package metadata if supported.
- No current-state README/status claim contradicts v1.4 completion.
- Historical changelog entries remain intact.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('pyproject.toml').read_text(encoding='utf-8')
assert 'version = "1.4.0.dev0"' in text or 'version = "1.4.0' in text
assert 'version = "1.2.0.dev0"' not in text
print('version metadata check passed')
PY
python -m skilllogboard.cli.main --version || skilllog --version || true
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

- The exact version string may be `1.4.0.dev0`, `1.4.0a0`, or project-specific, but it must not remain `1.2.0.dev0` after v1.4 completion.

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
