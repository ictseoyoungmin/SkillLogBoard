# SkillLogBoard v1.3 Commercial Live UI Development Plan

## 1. Purpose

v1.3 raises Live Board UI quality to a commercial or high-quality open-source level.

v1.2 provides the app shell and view contracts. v1.3 should implement the maintainable frontend architecture and polished UI system needed to compete visually with serious experiment tools.

## 2. Recommended Stack

```text
React + TypeScript + Vite
CSS variables / design tokens
TanStack Table or lightweight table component
uPlot / lightweight line chart / custom canvas-SVG chart
Packaged static assets served by local FastAPI
```

## 3. Architecture Boundary

Development may use Node/Vite, but end users should not need Node.

```text
source frontend:
  frontend/live-board/

build output:
  src/skilllogboard/live/static/
  src/skilllogboard/live/templates/app.html or equivalent
```

## 4. UI Views

```text
Overview
Runs
Compare
Metric Lab
Artifacts
Reports
Agent
Local Settings
Command Palette
Inspector Drawer
```

## 5. Completion Criteria

v1.3 is complete when:

1. Live Board frontend is componentized.
2. Build output is packaged in the Python wheel.
3. Overview/Runs/Compare/Metric Lab/Artifacts/Reports/Agent/Settings are polished and responsive.
4. Local API contracts from v1.2 are consumed correctly.
5. Rich demo looks convincing without fake cloud semantics.
6. Tests cover frontend build, packaged assets, and backend serving.
7. Existing static dashboard/report remains independent and portable.
