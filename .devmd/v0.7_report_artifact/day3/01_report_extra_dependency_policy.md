---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "3"
slice: "01_report_extra_dependency_policy"
title: "report extra dependency policy"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 01_report_extra_dependency_policy — report extra dependency policy

## Objective

Add optional `report` extra for figure generation without making matplotlib a core dependency.

## Context

Static PNG figure generation likely requires matplotlib. It must be optional.

## Dependencies

- day2 table builder slices completed.

## Target Files

- pyproject.toml
- README.md
- tests/test_optional_integrations.py

## Implementation Steps

1. Add optional extra `[project.optional-dependencies].report` if not present.
2. Include `matplotlib>=3.8` or the chosen plotting dependency.
3. Do not add matplotlib to core dependencies.
4. Update README install examples for report figures.
5. Add or update dependency-boundary tests.

## Acceptance Criteria

- Core dependencies do not include matplotlib.
- `report` extra exists if figure PNG support is implemented.
- README documents optional report extra.
- Optional dependency tests pass.

## Verification Commands

```bash
pytest -q tests/test_optional_integrations.py
python - <<'PY'
from pathlib import Path
import tomllib
p = tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))
core = '\n'.join(p['project'].get('dependencies', [])).lower()
assert 'matplotlib' not in core
print('report extra dependency boundary OK')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.6 public APIs and run folder compatibility.
- Existing `summary.md`, `dashboard.html`, `compare.md`, `compare.html`, and `export-table` behavior must not regress.
- Core install must remain lightweight. Do not add matplotlib, pandas, torch, lightning, sklearn, or domain packages to core dependencies.
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
**Completed at:** 2026-05-12
**Completed by:** Codex
**Verification command(s):** .venv/bin/pytest -q; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation
**Notes:** Implemented and verified as part of the v0.7 report artifact layer pass. Optional figure generation keeps a readable skipped-dependency fallback when matplotlib is unavailable.

<!-- AGENT_STATUS: COMPLETED -->

