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
skilllog watch RUN_DIR --monitor-system --monitor-gpu
skilllog watch RUN_DIR --log-file train.log
```

`--monitor-system` samples optional `psutil` system and process metrics into `monitoring.jsonl`.
`--monitor-gpu` shells out to `nvidia-smi` when available and records a skipped warning otherwise.
The core package does not require FastAPI, uvicorn, psutil, NVML, a GPU, or a browser.

The Live Board does not replace static outputs. `dashboard.html`, `summary.md`, `report.md`,
`report.html`, and compare reports remain file-based artifacts that can be opened without a server.
