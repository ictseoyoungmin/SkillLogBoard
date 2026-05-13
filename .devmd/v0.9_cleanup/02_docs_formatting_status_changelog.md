---
milestone: "v0.9-cleanup"
phase: "Template Forge Cleanup"
slice: "02_docs_formatting_status_changelog"
title: "docs formatting, status matrix, and changelog polish"
priority: "P0"
status: "completed"
target_version: "v0.9-cleanup"
---

# 02_docs_formatting_status_changelog — docs formatting, status matrix, and changelog polish

## Objective

Normalize formatting and status documentation after v0.9 so implemented vs planned features are easy to distinguish.

## Context

v0.9 Template Forge is functionally complete and CI is green. This cleanup phase polishes docs, CLI UX, validator depth, and CI maintenance before v1.0 Live Board.

## Target Files

- docs/template_forge.md
- docs/agent_research_layer.md
- docs/status_matrix.md
- CHANGELOG.md
- pyproject.toml

## Implementation Steps

1. Review raw Markdown formatting in template forge docs, agent docs, status matrix, and changelog.
2. Fix accidental single-line blocks, broken lists, malformed tables, or inconsistent headings.
3. Ensure Template Forge is marked Implemented for v0.9.
4. Ensure Live Board is still marked Planned for v1.0.
5. Ensure excluded integrations remain out of scope.
6. Add a small v0.9 cleanup entry to CHANGELOG if appropriate.

## Acceptance Criteria

- Docs render cleanly in GitHub Markdown.
- Status matrix accurately distinguishes Implemented/Planned/Out of scope.
- CHANGELOG contains v0.9 cleanup information if changed.
- No planned feature is incorrectly marked implemented.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
status = Path('docs/status_matrix.md').read_text(encoding='utf-8').lower()
assert 'template forge' in status or 'forge' in status
assert 'live' in status
print('status docs check passed')
PY
```

## Non-goals

- Do not begin v1.0 Live Board implementation.
- Do not add built-in LLM inference, cloud calls, or automatic code generation.
- Do not implement new domain templates directly.
- Do not change public RunLogger APIs.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this cleanup focused.
- Preserve v0.9 behavior and all existing tests.
- If an item is deferred, update docs and record the reason below.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -c "from pathlib import Path; status=Path('docs/status_matrix.md').read_text(encoding='utf-8').lower(); assert 'template forge' in status or 'forge' in status; assert 'live' in status; print('status docs check passed')"`; `.venv/bin/python -m ruff check .`  
**Notes:** Template Forge remains implemented, Live Board remains planned, and cloud/multi-user/import integrations are explicitly out of scope.

<!-- AGENT_STATUS: COMPLETED -->
