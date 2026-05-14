# Release Checklist

SkillLogBoard v0.6 release hardening focuses on verification, packaging, and documentation.

## v1.1.1 Live Board Candidate Notes

- [ ] Confirm the candidate version is `1.1.1.dev0`.
- [ ] Run focused Live Board checks:

```bash
python -m pytest tests/test_live_project.py tests/test_live_server.py tests/test_live_ui_snapshot.py
```

- [ ] Run the multi-run compare fixture:

```bash
python examples/live_demo.py --multi-run
skilllog watch runs/live_demo --project --no-open
```

- [ ] Confirm `/api/compare` stays local-first and bounded: no TensorBoard/W&B import,
  Prometheus/Grafana integration, cloud sync, auth, database, or frontend build system.
- [ ] Confirm manual visual QA covers desktop/mobile project compare, run picker, overlay legend,
  raw/normalized mode, collapsed tray, compact panel, and artifact preview drawer.

## Environment

- [ ] Confirm the release candidate version:

```bash
python -c "import skilllogboard; print(skilllogboard.__version__)"
```

- [ ] Confirm the CLI is available:

```bash
skilllog --help
```

## Install

- [ ] Verify editable install with release-hardening extras:

```bash
python -m pip install -e ".[dev,dashboard]"
```

- [ ] Verify a fresh virtual environment:

```bash
bash scripts/verify_fresh_venv.sh
```

## Tests

- [ ] Run the full test suite:

```bash
pytest -q
```

- [ ] Run the local smoke script:

```bash
bash scripts/smoke_test.sh
```

## Examples

- [ ] Run lightweight examples:

```bash
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python examples/sklearn_example.py
```

## Build

- [ ] Verify local no-isolation package build:

```bash
python -m build --no-isolation
```

- [ ] Verify generated wheel install:

```bash
bash scripts/verify_wheel_install.sh
```

- [ ] Verify isolated package build in CI or Docker before publishing:

```bash
python -m build
```

Optional Docker check:

```bash
docker build -f Dockerfile.test .
```

Build policy:

- `python -m build --no-isolation` is the local packaging smoke check.
- An isolated `python -m build` should pass in CI or Docker before a release is published.
- If a local Python installation cannot create build environments because `venv` or `ensurepip`
  is unavailable, record it as an environment limitation and verify isolated build elsewhere.

## Docs

- [ ] Confirm README install, quickstart, compare, and template sections are current.
- [ ] Confirm `docs/templates.md` separates implemented and planned templates.
- [ ] Confirm `docs/status_matrix.md` does not mark planned templates as implemented.

## CI

- [ ] Confirm GitHub Actions runs lint, tests, and build across supported Python versions.
- [ ] Confirm optional integrations are not required for core tests.

## Artifacts

- [ ] Confirm `dist/` contains a wheel and sdist for the current candidate.
- [ ] Confirm dashboard templates and `default_skills.md` are included in package data.
- [ ] Clean local generated artifacts when preparing a source handoff:

```bash
rm -rf build/ dist/ *.egg-info src/*.egg-info .pytest_cache/ .ruff_cache/
```

## Release Decision

- [ ] Record the release readiness decision before publishing.
- [ ] Do not publish to PyPI or create a GitHub release until the decision record is complete.

## Template Status

- Implemented: `ir-drop`, `trajectory`.
- Planned: `classification`, `segmentation`, `finance-dashboard`.

## Optional Integrations

Core install must remain lightweight. PyTorch, Lightning, pandas/table support, and
framework-specific examples stay behind optional extras or user-provided environments.
