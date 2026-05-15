---
milestone: "v1.4-cleanup"
phase: "Portable Report Maturity Cleanup"
slice: "06_v14_release_candidate_closeout"
title: "v1.4 release candidate closeout"
priority: "P0"
status: "completed"
---

# 06_v14_release_candidate_closeout — v1.4 release candidate closeout

## Objective

Create the final v1.4 closeout note and prepare the handoff into v1.5.

## Context

v1.4 Portable Report Maturity is functionally complete. This cleanup pass fixes release/version consistency, documentation truthfulness, CI verification, report validation polish, and small packaging/documentation issues before moving into v1.5 Performance, Retention, and Operational Rules.

## Target Files

- docs/v1_4_release_candidate_note.md
- docs/release_candidate_checklist.md
- docs/status_matrix.md
- .devmd/v1.4_cleanup/*.md

## Implementation Steps

1. Summarize v1.4 completed features: render modes, manifest v2, provenance, offline CSS/JS, chart specs, SVG fallback, report validate/open/bundle.
2. List exact verification commands run and results.
3. List known limitations or deferred items for v1.5, especially agent feedback schema, retention/pruning, baseline delta expansion, and operational rules.
4. Confirm that no publishing was performed.
5. Confirm that static reports remain separate from the Live Board.
6. Update this cleanup folder's statuses after all cleanup slices are done.

## Acceptance Criteria

- v1.4 release candidate note exists and is specific.
- Deferred v1.5 items are listed clearly.
- No TestPyPI/PyPI publishing was performed.
- v1.4 cleanup is ready for review.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
note = Path('docs/v1_4_release_candidate_note.md')
assert note.exists()
text = note.read_text(encoding='utf-8').lower()
for token in ['v1.4', 'portable', 'report', 'verification', 'v1.5']:
    assert token in text
print('v1.4 RC closeout check passed')
PY
pytest -q
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
