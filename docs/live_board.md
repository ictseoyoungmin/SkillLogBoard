# Live Board

The Live Board is an optional local server for watching SkillLogBoard run folders while files are
being written. It reads the same local artifacts used by the static dashboard and report layer:
`manifest.yaml`, `metrics.csv`, `events.jsonl`, `skill_trace.jsonl`, `artifact_index.json`,
`monitoring.jsonl`, and an optional log file.

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
skilllog watch runs/demo --project --latest --no-open
```

Useful options:

```bash
skilllog watch RUN_DIR --host 127.0.0.1 --port 8765
skilllog watch RUN_DIR --poll-interval 2 --monitor-system --monitor-gpu
skilllog watch RUN_DIR --log-file train.log
```

The server exposes `/api/health`, `/api/config`, and `/api/state`. `/api/config` includes the
effective `poll_interval`, mode, target directory, and monitor flags. `--poll-interval` controls
both browser refresh timing and active monitor sampling. The browser clamps the value to a safe
minimum so accidental very small intervals do not create excessive polling.

Project mode discovers `manifest.yaml` files with a bounded directory walk. It skips hidden/cache
folders and common non-run folders such as `.git`, `.venv`, `__pycache__`, `node_modules`,
`artifacts`, `report`, `_reports`, `build`, and `dist`. This keeps `skilllog watch ROOT --project`
usable on larger local workspaces without adding a database or persistent index.

`--monitor-system` samples optional `psutil` system and process metrics into `monitoring.jsonl`.
`--monitor-gpu` shells out to `nvidia-smi` when available. Missing `nvidia-smi`, empty output, or
malformed output records a skipped warning instead of silently returning an empty GPU list.
The core package does not require FastAPI, uvicorn, psutil, NVML, a GPU, or a browser.

The Live Board does not replace static outputs. `dashboard.html`, `summary.md`, `report.md`,
`report.html`, and compare reports remain file-based artifacts that can be opened without a server.
