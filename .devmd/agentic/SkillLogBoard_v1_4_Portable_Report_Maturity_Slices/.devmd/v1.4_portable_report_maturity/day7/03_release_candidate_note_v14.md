---
milestone: "v1.4"
phase: "Portable Report Maturity"
day: "day7"
slice: "03_release_candidate_note_v14"
title: "release candidate note v1.4"
priority: "P1"
status: "completed"
target_version: "v1.4"
---

# 03_release_candidate_note_v14 — release candidate note v1.4

## Objective

Prepare v1.4 release candidate note.

## Context

v1.4 matures static dashboard/report outputs into portable, offline-friendly research evidence packages with manifests, figures, tables, and provenance metadata.

## Dependencies

- v1.3 Commercial Live UI completed or planned separately.
- Static dashboard/report outputs remain independent from the Live Board app.
- Report Artifact Layer v0.7+ concepts are available.

## Target Files

- docs/v1_4_release_candidate_note.md
- docs/release_candidate_checklist.md

## Implementation Steps

1. Summarize report maturity features.
2. List offline/portable verification commands.
3. List known non-goals.
4. List manual report QA steps.
5. Do not publish.

## Acceptance Criteria

- v1.4 RC note exists.
- Manual QA steps are listed.
- Publishing is not performed.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/v1_4_release_candidate_note.md').read_text(encoding='utf-8').lower()
assert 'portable' in text and 'report' in text
print('v1.4 RC note check passed')
PY
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

