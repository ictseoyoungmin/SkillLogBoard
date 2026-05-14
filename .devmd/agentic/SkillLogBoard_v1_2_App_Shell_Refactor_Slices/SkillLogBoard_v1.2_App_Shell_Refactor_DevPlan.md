# SkillLogBoard v1.2 App Shell Refactor Development Plan

## 1. Purpose

v1.2 restructures Live Board into a screen-based local app.

The current UI has strong components, but many features are hidden or layered into one workspace. v1.2 separates concerns through a lightweight app shell and lazy state loading.

## 2. Target Views

```text
Project
  Overview
  Runs
  Compare

Analysis
  Metric Lab
  Artifacts
  Reports

Evidence
  Agent
  Local Settings
```

## 3. Key Requirements

### 3.1 Project mode default

When the user runs:

```bash
skilllog watch runs/live_demo --project
```

the default screen must be **Overview**.

### 3.2 Single-run mode default

When the user runs:

```bash
skilllog watch runs/live_demo/r_0001
```

the default screen should be a run-oriented dashboard or Metric Lab, not Project Overview.

### 3.3 Summary-first performance

Overview must not eagerly load full metric series from every run.

```text
Overview: manifest + metric summary only
Compare: selected metric + selected runs only
Metric Lab: selected run/metric only
Artifacts: artifact metadata only
Agent: agent metadata only
```

### 3.4 Local-first language

No account, team, invite, organization, avatar, cloud project, or remote sync metaphors.

## 4. Completion Criteria

v1.2 is complete when:

1. Sidebar navigation maps to real view state.
2. Project mode opens Overview by default.
3. Compare, Metric Lab, Artifacts, Reports, Agent, Settings render as distinct views.
4. Overview uses summary data and avoids full-series loading.
5. Compare and Metric Lab load series lazily.
6. UI copy preserves local-first positioning.
7. Existing v1.1.2 functionality remains usable.
8. Tests cover view state, routing, API contracts, and performance guards.
