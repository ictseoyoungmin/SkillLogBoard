# SkillLogBoard Week 7 Development Slices

Week 7 turns the v0.5 feature-complete package into a release-hardened v0.6 candidate. The goal is not to add new product features, but to make installation, testing, packaging, CI, documentation, and release preparation reliable.

## Week 7 Goal

Implement v0.6 release hardening:

- packaging metadata review
- optional extras validation
- package data and template inclusion checks
- CI matrix hardening
- build and wheel/sdist verification
- fresh virtual environment install tests
- documentation consistency checks
- smoke test script consolidation
- release notes and release checklist
- final release candidate verification

## Scope Boundary

Allowed:

- `pyproject.toml` cleanup
- package version normalization
- package data / MANIFEST.in cleanup
- CI workflow updates
- test reliability improvements
- docs/checklist updates
- release note drafts
- smoke scripts
- build verification scripts
- optional Docker verification file or documentation

Not allowed:

- new dashboard features
- new Skills.md rule types
- multi-run compare feature changes beyond bug fixes
- new research templates
- W&B/TensorBoard integration
- database backend
- real-time server or Streamlit dashboard
- actual PyPI upload or GitHub release creation unless explicitly instructed

## Completion Protocol

Each slice has an **Agent Completion Block**. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for any skipped, deferred, or partially implemented item.

## Recommended Execution Order

```text
.devmd/week6_cleanup/
.devmd/week7/day1/
.devmd/week7/day2/
.devmd/week7/day3/
.devmd/week7/day4/
.devmd/week7/day5/
```

Within each day, process files in numeric order.

## Required Final Verification

```bash
pip install -e ".[dev,dashboard]"
skilllog --help
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python -m build --no-isolation
```

If isolated `python -m build` cannot run because the local system Python lacks `venv/ensurepip`, record it as an environment limitation and verify isolated build in GitHub Actions, Docker, or another environment where Python venv is available.
