---
milestone: "v1.4-cleanup"
phase: "Portable Report Maturity Cleanup"
slice: "02_docs_changelog_status_matrix_sync"
title: "docs, changelog, and status matrix sync"
priority: "P0"
status: "completed"
---

# 02_docs_changelog_status_matrix_sync — docs, changelog, and status matrix sync

## Objective

Update public-facing documentation to accurately reflect v1.4 Portable Report Maturity.

## Context

v1.4 Portable Report Maturity is functionally complete. This cleanup pass fixes release/version consistency, documentation truthfulness, CI verification, report validation polish, and small packaging/documentation issues before moving into v1.5 Performance, Retention, and Operational Rules.

## Target Files

- README.md
- CHANGELOG.md
- docs/status_matrix.md
- docs/report_artifacts.md
- docs/live_board.md

## Implementation Steps

1. Add or update the v1.4 changelog entry.
2. Update the status matrix to mark v1.4 report maturity features as implemented where applicable.
3. Ensure README describes Static Evidence Package and Local Live Board as separate product surfaces.
4. Ensure `docs/report_artifacts.md` covers render modes, offline behavior, manifest schema, provenance, report validate/open/bundle, and bundle zip.
5. Ensure `docs/live_board.md` does not imply static reports require the Live Board server.
6. Remove or rephrase claims that sound like cloud/SaaS, W&B replacement, or automatic AI analysis.

## Acceptance Criteria

- CHANGELOG contains a v1.4 entry.
- Status matrix includes v1.4 features and accurate completion state.
- README clearly separates portable static reports from local Live Board.
- Report artifacts docs mention offline rendering and provenance.
- No unsupported cloud/account/import claims are introduced.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
changelog = Path('CHANGELOG.md').read_text(encoding='utf-8').lower()
report_docs = Path('docs/report_artifacts.md').read_text(encoding='utf-8').lower()
readme = Path('README.md').read_text(encoding='utf-8').lower()
assert '1.4' in changelog or 'v1.4' in changelog
for token in ['offline', 'provenance', 'render mode']:
    assert token in report_docs
assert 'live board' in readme and ('portable' in readme or 'static' in readme)
print('v1.4 docs sync check passed')
PY
pytest -q tests/test_report_manifest.py tests/test_report_rendering.py
```

## Non-goals

- Do not start v1.5 implementation in this cleanup pass.
- Do not implement pruning, retention, JSONL rotation, project index, or agent safety gate here.
- Do not publish to TestPyPI/PyPI.
- Do not introduce cloud sync, multi-user auth, Prometheus/Grafana, or TensorBoard/W&B import.
- Do not make static reports depend on the Live Board server.
- Do not require external CDN/network access for portable reports.

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
