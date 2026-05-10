---
week: 7
day: 3
slice: "01_release_checklist_document"
title: "release checklist document"
priority: "P0"
status: "completed"
target_version: "v0.6-release-hardening"
---

# 01_release_checklist_document — release checklist document

## Objective

Create a release checklist for v0.6 candidate validation.

## Context

This slice belongs to the post-Week 6 cleanup / Week 7 release-hardening phase. Keep implementation focused, deterministic, and compatible with the existing public API.

## Dependencies

- Previous slices in numeric order.

## Target Files

- docs/release_checklist.md

## Implementation Steps

1. Include sections: environment, install, tests, examples, build, docs, CI, artifacts, release decision.
2. Include exact commands.
3. Use checkbox format for manual review.
4. Include known environment limitations.

## Acceptance Criteria

- Release checklist exists.
- Checklist includes install/test/example/build/docs/CI checks.
- Checklist includes exact commands.
- Checklist mentions no-isolation build limitation policy.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text=Path('docs/release_checklist.md').read_text(encoding='utf-8')
for s in ['pytest -q','python -m build','skilllog --help']:
    assert s in text
print('release checklist checks passed')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 6.
- Do not implement Week 8+ publishing unless explicitly instructed.
- Keep optional integrations optional. Core install must not require torch, lightning, sklearn, pandas, or domain-specific packages.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-10 21:12
**Completed by:** coding agent
**Verification command(s):** .venv/bin/python -c "release checklist checks"; .venv/bin/pytest -q tests/test_examples.py
**Notes:** Expanded release checklist with environment, install, tests, examples, build, docs, CI, artifacts, and release decision sections.

<!-- AGENT_STATUS: COMPLETED -->
