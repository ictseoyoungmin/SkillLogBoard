# SkillLogBoard v1.1 UI/UX Redesign and Metric Workspace Development Plan

## Design Thesis

The Live Board should feel like a polished local-first research product, not a crowded generated dashboard.

```text
card-heavy dashboard
→ minimal command center
→ chart-first Metric Workspace
→ details through drawers, trays, and compare mode
```

## Design Principles

1. **Minimal by default**  
   Show status, primary metric, alert count, resource health, and one focused metric workspace. Hide deep details until requested.

2. **Metric Workspace, not one chart**  
   Support many metrics through selector/search, groups, pins, smoothing, scale controls, x-axis alignment, and full-screen metric lab.

3. **Compare/overlay as a first-class mode**  
   Support current run vs baseline, best run, selected runs, seed group, and failed/successful run comparison.

4. **Context correlation**  
   Let events, rule warnings/errors, checkpoints, eval boundaries, logs, and resources explain metric changes.

5. **Local-first product identity**  
   Make local files, inspectability, no cloud, and no auth feel like intentional strengths.

## Scope

Included:

- live.html redesign
- local CSS/vanilla JS only
- metric catalog state extension
- compare/overlay UI
- drawer/tray interaction model
- artifact/report preview UI
- agent workspace polish
- UI snapshot tests and docs

Excluded:

- cloud sync
- W&B/TensorBoard import
- Prometheus/Grafana
- multi-user auth
- database
- heavy frontend build system
