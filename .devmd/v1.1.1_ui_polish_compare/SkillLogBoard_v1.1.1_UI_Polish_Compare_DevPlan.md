# SkillLogBoard v1.1.1 UI Polish, True Compare, and Interaction Hardening Development Plan

## Purpose

v1.1.1 turns the redesigned Live Board into a release-candidate-quality interface.

## Product Thesis

SkillLogBoard Live should feel like a local-first research observability workspace for people and coding agents. It is not a W&B clone, not TensorBoard, not Grafana, and not a hosted service.

## Core Workstreams

### True Compare / Overlay

- project mode exposes compare candidates
- selected metric can be overlaid across runs
- payload is bounded by max runs and max points
- baseline/best/current/latest labels are visible
- legend supports per-run visibility
- compare controls include smoothing, alignment, raw/normalized, and selected-only/top-k policy

### Minimal Interaction Model

- bottom context tray collapsed by default
- side panel compact/hide option
- right drawer opens only on intent
- Metric Lab opens only on intent
- localStorage preserves these states per run/project

### Report/Artifact Browser

- discover root-level and `report/` package artifacts
- discover tables and figures under report package
- group by type
- render compact preview metadata
- avoid inlining large files

### Visual Polish

- consistent spacing rhythm
- stable max widths
- refined chart area
- no visual overcrowding
- polished empty/loading/error states
- compare mode looks intentional

## Explicit Non-goals

- no TensorBoard import
- no W&B import
- no Prometheus/Grafana integration
- no cloud sync
- no multi-user auth
- no database
- no frontend build system
- no release publishing
