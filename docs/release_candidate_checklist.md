# Release Candidate Checklist

## v1.1.1 Live Board Compare Candidate

- [ ] Confirm package version is `1.1.1.dev0`.
- [ ] Confirm README, Live Board docs, changelog, and status matrix mention v1.1.1 compare mode.
- [ ] Run lint and focused Live Board tests:

```bash
python -m ruff check .
python -m pytest tests/test_live_project.py tests/test_live_server.py tests/test_live_state.py tests/test_live_ui_snapshot.py
```

- [ ] Run the full regression suite:

```bash
python -m pytest
```

- [ ] Run package verification:

```bash
python -m build --no-isolation
```

- [ ] Smoke the multi-run demo:

```bash
python examples/live_demo.py --multi-run
skilllog watch runs/live_demo --project --no-open
```

## Manual UI QA

- [ ] Single-run mode loads metric catalog, chart transforms, context tray, detail drawer, artifact preview, and metric lab.
- [ ] Project mode loads compare candidates, shared metrics, and status counts.
- [ ] Compare mode shows a bounded overlay, run picker drawer, best/latest/baseline role badges, legend visibility toggles, raw/normalized values, and step/relative alignment.
- [ ] Bottom tray starts collapsed and can be expanded.
- [ ] Side panel compact mode works without hiding primary chart controls.
- [ ] Artifact preview drawer displays metadata only and does not inline large report/table/figure files.
- [ ] Narrow viewport preserves readable controls without overlapping text.

## Non-Goals

- No TensorBoard or W&B import.
- No Prometheus or Grafana integration.
- No cloud sync.
- No multi-user auth.
- No database backend.
- No frontend build system such as React, Vue, or Svelte.
- No TestPyPI, PyPI, GitHub Release, or publishing action in this candidate pass.
