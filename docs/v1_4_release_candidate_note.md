# SkillLogBoard v1.4 Release Candidate Note

v1.4 focuses on portable report maturity. Static reports remain offline evidence documents that can
be shared, reviewed, archived, and inspected without running the Live Board.

## Highlights

- Report render modes: `minimal`, `portable_interactive`, and `package`.
- Manifest schema version `2.0` with package and per-output provenance.
- Offline CSS/JS policy with no CDN dependency.
- Chart spec JSON exports for reproducible figure metadata.
- SVG fallback figures for minimal mode when optional plotting dependencies are unavailable.
- CLI helpers for `skilllog report validate`, `skilllog report open`, and
  `skilllog report bundle`.

## Verification

Local release checks run on 2026-05-15:

```bash
.venv/bin/python -m ruff check .                         # passed
.venv/bin/python -m pytest -q                            # 258 passed
.venv/bin/python -m pytest -q tests/test_report_manifest.py tests/test_report_rendering.py tests/test_report_assets.py tests/test_report_figures.py tests/test_report_tables.py tests/test_cli_report_artifacts.py  # 18 passed
.venv/bin/python examples/live_demo.py --multi-run --runs 5 --rich  # passed
.venv/bin/python -m skilllogboard.cli.main report validate runs/live_demo/report --json  # passed, ok=true
.venv/bin/python -m skilllogboard.cli.main report bundle runs/live_demo/report --output runs/live_demo/report.zip  # passed
.venv/bin/python -m build --no-isolation                 # passed
```

The local WSL Node launcher cannot run the frontend job in this environment: `node --version` is
not available and `npm ci` fails before dependency installation with
`Could not determine Node.js install directory`. The GitHub Actions `live-frontend` job uses
`actions/setup-node@v4` on Ubuntu and remains the CI source of truth for frontend npm checks.

GitHub Actions status could not be checked directly from this environment because the `gh` CLI is
not installed and there is no open PR returned for `ictseoyoungmin/SkillLogBoard`. The CI workflow
now includes an explicit package/CLI version sync check before lint, tests, and package build.

## Boundary

The Live Board remains a local FastAPI app for active inspection. Portable reports remain static
HTML/Markdown/YAML/table/figure assets with relative paths and offline provenance.

## Deferred To v1.5

- Full agent feedback schema for report validation beyond the lightweight v1.4 JSON fields.
- Retention/pruning, JSONL rotation, project index, and operational rule gates.
- Generated baseline-delta tables; v1.4 parses and preserves baseline/reference/delta metadata.

No TestPyPI, PyPI, GitHub Release, cloud sync, or publishing action was performed.
