# Live Board

The Live Board is an optional local server for watching SkillLogBoard run folders while files are
being written. It reads the same local artifacts used by the static dashboard and report layer:
`manifest.yaml`, `metrics.csv`, `events.jsonl`, `skill_trace.jsonl`, `artifact_index.json`,
`monitoring.jsonl`, and an optional log file.

The v1.1.2 interface is intentionally quiet on first load. It shows a compact overview, then makes
the Metric Workspace the primary surface. Deeper evidence stays available through a compactable
side panel, collapsed bottom context tray, run detail drawer, artifact/report preview drawer,
agent workspace summary, run picker, compare legend, and full-screen Metric Lab. Compact capability
hints are derived from local state only: run counts, metric counts, shared metrics, artifacts,
warnings, compare readiness, and agent evidence.

Install the optional extra when you want the server:

```bash
pip install -e ".[dev,dashboard,live]"
```

Start a single-run board:

```bash
python examples/live_demo.py
skilllog watch runs/live_demo/{run_id} --no-open
```

Start a project-level board over multiple run folders:

```bash
python examples/live_demo.py --multi-run
skilllog watch runs/live_demo --project --latest --no-open
```

Create a richer local showcase for screenshots and visual QA:

```bash
python examples/live_demo.py --multi-run --runs 5 --rich
skilllog watch runs/live_demo --project --no-open
```

The rich fixture creates baseline, best, overfit, failed, and current runs with shared metrics such
as `train/loss`, `val/loss`, `val/acc`, `val/f1`, `lr`, `grad_norm`, `throughput`, `step_time`, and
`gpu/memory`. It also writes local events, rule traces, report/table/figure artifacts, and agent
workspace evidence so drawers and compare mode can be reviewed without external services.

For screenshots, use 1440x960 as the primary desktop viewport, 1280x800 for a compact laptop pass,
and 390x844 for a narrow viewport pass. Capture project overview, compare mode, Metric Lab, artifact
preview, Agent Workspace, and at least one sparse-run empty state. The rich demo is synthetic local
evidence and should not be presented as imported production telemetry.

If the target directory does not contain `manifest.yaml` but has run folders below it, `skilllog
watch` auto-detects project mode. For example, `skilllog watch runs/ --no-open` is treated as a
project board when `runs/` contains nested run directories.

Useful options:

```bash
skilllog watch RUN_DIR --host 127.0.0.1 --port 8765
skilllog watch RUN_DIR --poll-interval 2 --monitor-system --monitor-gpu
skilllog watch RUN_DIR --log-file train.log
```

The server exposes `/api/health`, `/api/config`, `/api/state`, and `/api/compare`. `/api/config` includes the
effective `poll_interval`, mode, target directory, and monitor flags. `--poll-interval` controls
both browser refresh timing and active monitor sampling. The browser clamps the value to a safe
minimum so accidental very small intervals do not create excessive polling.

`/api/state` includes additive UI fields for the Metric Workspace: `metric_catalog`,
`selected_metrics`, `pinned_metrics`, `context_markers`, `report_artifacts`, and
`agent_workspace`. v1.1.2 also includes `capabilities`, a compact summary derived from the same
local files. These fields do not require server-side user sessions.

Project mode discovers `manifest.yaml` files with a bounded directory walk. It skips hidden/cache
folders and common non-run folders such as `.git`, `.venv`, `__pycache__`, `node_modules`,
`artifacts`, `report`, `_reports`, `build`, and `dist`. This keeps `skilllog watch ROOT --project`
usable on larger local workspaces without adding a database or persistent index.

`/api/compare` is project-mode only. It returns bounded run candidates and metric series for a
single shared metric. The browser uses it for the run picker, overlay legend, and raw/normalized
compare chart. Supported query parameters are `metric`, comma-separated `runs`, `max_runs`,
`max_points`, `normalize`, and `align=step|relative`. The implementation reads local CSV files
directly and deliberately avoids pandas, databases, background indexes, TensorBoard, W&B,
Prometheus, cloud sync, and authentication.

The browser keeps refresh work bounded for perceived speed: compare requests cap selected runs and
points, project discovery is depth-limited, and long panel lists are clipped before rendering.

Report package discovery now includes common static artifacts plus metadata-only entries under
`report/`, `reports/`, `tables/`, and `figures/`. The Live Board preview drawer shows file type,
path, size, and preview policy; it does not inline large report or figure contents into the state
payload.

`--monitor-system` samples optional `psutil` system and process metrics into `monitoring.jsonl`.
`--monitor-gpu` shells out to `nvidia-smi` when available. Missing `nvidia-smi`, empty output, or
malformed output records a skipped warning instead of silently returning an empty GPU list.
The core package does not require FastAPI, uvicorn, psutil, NVML, a GPU, or a browser.

Metric selections, pinned metrics, selected compare runs, hidden legend entries, chart transforms,
tray state, compact-panel state, and active panel preferences are stored in browser `localStorage`
only. The key is scoped by mode and target directory so separate run and project boards do not
overwrite each other. The Live Board does not create accounts, write server-side UI preferences, or
sync state to a cloud service.

The Live Board does not replace static outputs. `dashboard.html`, `summary.md`, `report.md`,
`report.html`, and compare reports remain file-based artifacts that can be opened without a server.
