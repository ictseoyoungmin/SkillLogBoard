---
milestone: "v1.4-cleanup"
phase: "Portable Report Maturity Cleanup"
slice: "04_portable_report_docs_and_baseline_delta_note"
title: "portable report docs and baseline delta note"
priority: "P1"
status: "completed"
---

# 04_portable_report_docs_and_baseline_delta_note — portable report docs and baseline delta note

## Objective

Clarify report mode behavior and document the current baseline-delta support level honestly.

## Context

v1.4 Portable Report Maturity is functionally complete. This cleanup pass fixes release/version consistency, documentation truthfulness, CI verification, report validation polish, and small packaging/documentation issues before moving into v1.5 Performance, Retention, and Operational Rules.

## Target Files

- docs/report_artifacts.md
- README.md
- src/skilllogboard/reports/report_spec.py
- tests/test_report_spec.py

## Implementation Steps

1. Document `minimal`, `portable_interactive`, and `package` modes in a small table.
2. Clarify that `report.js` enhances local table filtering but report.html remains readable without JavaScript.
3. Clarify that `package` mode uses relative local assets and no external CDN.
4. Review `ReportSpecItem` baseline/reference/delta fields.
5. Document whether baseline delta is fully wired to generated tables or only represented in spec fields.
6. If baseline delta is not fully wired, explicitly mark it as planned for v1.5 Compare/Operational Rules.
7. Add or adjust tests only if documentation reveals a mismatch in parser behavior.

## Acceptance Criteria

- Report mode behavior is documented clearly.
- Offline/static behavior is not overstated.
- Baseline delta support level is honest.
- No unsupported automatic analysis claim is made.

## Verification Commands

```bash
pytest -q tests/test_report_spec.py
python - <<'PY'
from pathlib import Path
text = Path('docs/report_artifacts.md').read_text(encoding='utf-8').lower()
for token in ['minimal', 'portable_interactive', 'package', 'baseline']:
    assert token in text
print('portable report docs/baseline note check passed')
PY
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
