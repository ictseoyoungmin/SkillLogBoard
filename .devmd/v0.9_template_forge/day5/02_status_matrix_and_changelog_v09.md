---
milestone: "v0.9"
phase: "Template Forge"
day: "5"
slice: "02_status_matrix_and_changelog_v09"
title: "status matrix and changelog v0.9"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 02_status_matrix_and_changelog_v09 — status matrix and changelog v0.9

## Objective

Update status matrix and changelog for v0.9 while keeping Live Board planned.

## Context

Docs must accurately mark Template Forge as implemented only after scaffold and validation work is done.

## Dependencies

- 01_docs_template_forge

## Target Files

- docs/status_matrix.md
- CHANGELOG.md
- README.md

## Implementation Steps

1. Add CHANGELOG v0.9 entry.
2. Mark Template Forge scaffold/validate implemented if tests pass.
3. Mark built-in LLM code generation as Not planned / Non-goal.
4. Mark Live Board as Planned.
5. Keep TensorBoard/W&B import, Prometheus/Grafana, cloud sync, multi-user auth as out of scope unless roadmap says otherwise.

## Acceptance Criteria

- CHANGELOG contains v0.9 entry.
- Status matrix includes Template Forge.
- Docs do not claim built-in LLM support.
- Live Board remains Planned.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
status = Path('docs/status_matrix.md').read_text(encoding='utf-8')
assert 'Template Forge' in status or 'template forge' in status.lower()
changelog = Path('CHANGELOG.md').read_text(encoding='utf-8')
assert '0.9' in changelog or 'v0.9' in changelog
print('v0.9 status/changelog checks passed')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.8/v0.7/v0.6 public APIs and run folder compatibility.
- Template Forge is a scaffold/harness/validation system. It must not embed LLM inference or call cloud APIs.
- Generated template code must be local, inspectable, dependency-light, and testable with synthetic examples.
- Core install must remain lightweight. Do not add torch, lightning, sklearn, pandas, matplotlib, LLM SDKs, or domain packages to core dependencies.
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
**Completed at:** 2026-05-13  
**Completed by:** Codex  
**Verification command(s):** ruff check; Template Forge tests; full pytest; examples; build no-isolation; forge CLI e2e smoke check  
**Notes:** v0.9 Template Forge implemented as a local scaffold/harness/validation layer. No built-in LLM, cloud API, automatic domain-code generation, or heavy core dependency was added.  

<!-- AGENT_STATUS: COMPLETED -->
