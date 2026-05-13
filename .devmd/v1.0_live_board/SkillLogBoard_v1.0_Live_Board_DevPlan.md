# SkillLogBoard v1.0 Local-first Live Board Development Plan

## Overview

v1.0 adds a local-first live board on top of the existing SkillLogBoard evidence package.

The live board observes local run folders and exposes a browser UI for:

- run status
- live metric curves
- events timeline
- rule audit status
- artifact feed
- log tail
- optional system/GPU/process monitoring
- project-level active run overview

It must preserve SkillLogBoard's static-report compatibility.

## Architecture

```text
RunLogger writes local files
  ├─ manifest.yaml
  ├─ metrics.csv
  ├─ events.jsonl
  ├─ skill_trace.jsonl
  ├─ artifact_index.json
  └─ monitoring.jsonl

skilllog watch RUN_DIR
  ├─ reads/tails files
  ├─ optionally samples system/GPU/process state
  ├─ builds live state
  ├─ serves /api/state
  └─ serves browser live board
```

## CLI

```bash
skilllog watch runs/demo/{run_id}

skilllog watch runs/demo/{run_id} \
  --host 127.0.0.1 \
  --port 8765 \
  --poll-interval 1.0 \
  --monitor-system \
  --monitor-gpu \
  --log-file train.log

skilllog watch runs/demo --project --latest
```

## Optional Dependencies

```toml
[project.optional-dependencies]
live = [
  "fastapi>=0.110",
  "uvicorn>=0.27",
  "psutil>=5.9",
]
```

GPU monitoring should not require a hard dependency. Use `nvidia-smi` subprocess detection first or implement graceful skip.

## Success Criteria

1. `skilllog watch RUN_DIR` starts a local server.
2. `/api/state` returns current run state.
3. Browser live board loads without external CDN.
4. Metrics/events/rules/artifacts are visible.
5. `monitoring.jsonl` can be written when active monitor is enabled.
6. Missing optional dependencies are handled gracefully.
7. Existing static dashboard/report/compare remain unchanged.
8. CI is green across supported Python versions.
