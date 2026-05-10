# v0.6 Release Readiness Decision

## Decision

Status: GO for v0.6 release-candidate handoff.

The candidate is ready for an internal tag or TestPyPI preparation after CI confirms the isolated
`python -m build` path. No PyPI publication or GitHub release has been performed.

## Verification Summary

Passed locally:

- Editable install with `.[dev,dashboard]`
- `skilllog --help`
- `skilllog --version` reporting `0.6.0.dev0`
- Full test suite: `131 passed`
- Lightweight examples:
  - `python examples/basic_usage.py`
  - `python examples/ir_drop_example.py`
  - `python examples/trajectory_example.py`
- Local package build: `python -m build --no-isolation`
- Wheel install verification with `scripts/verify_wheel_install.sh`

## Blockers

- None for local v0.6 release-candidate handoff.

## Deferred Checks

- Isolated `python -m build` should be confirmed in CI or Docker before publishing.
- Optional Docker verification is documented in `Dockerfile.test`; it was not required for local
  completion.

## Known Limitations

- Planned templates `classification`, `segmentation`, and `finance-dashboard` remain planned.
- Planned rule metadata `dashboard_panel` and `domain_breakdown` remains non-executing metadata.
- No online dashboard, database backend, W&B/TensorBoard import, or real-time server is included.
- Optional integrations remain user-provided and are not core dependencies.

## Next Step

Run CI, confirm isolated build, then decide whether to create a release tag or TestPyPI upload in a
separate explicit release task.
