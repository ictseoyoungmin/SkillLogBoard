# SkillLogBoard v1.3 Commercial Live UI Slices

## Purpose

v1.3 upgrades the v1.2 app shell into a commercial / well-made open-source quality Live Board frontend.

The recommended architecture is:

```text
Frontend source:
  React + TypeScript + Vite

Packaged output:
  compiled static JS/CSS assets inside the Python wheel

Backend:
  local FastAPI optional extra
  REST-style local API
  no GraphQL
  no cloud/account system
```

## Design Goal

Blend useful patterns from TensorBoard, W&B, and MLflow while preserving SkillLogBoard's identity:

```text
TensorBoard:
  scalar exploration, smoothing, metric groups, marker overlay

W&B:
  polished project overview, run cards, compare UX, artifact browser

MLflow:
  run table, local metadata, params/metrics/artifacts separation

SkillLogBoard:
  local-first evidence package, report artifacts, agent handoff evidence
```

## Included Structure

```text
SkillLogBoard_v1.3_Commercial_Live_UI_DevPlan.md

.devmd/v1.3_commercial_live_ui/
  README.md
  day1/
  day2/
  day3/
  day4/
  day5/
  day6/
  day7/
  day8/
```

## Final Verification

```bash
pip install -e ".[dev,dashboard,live]"
ruff check .
pytest -q
python examples/live_demo.py --multi-run --runs 5 --rich
python -m build --no-isolation
```

If Node tooling is introduced:

```bash
cd frontend/live-board
npm ci
npm run lint
npm run test
npm run build
```
