# SkillLogBoard Extension Roadmap

## Document Purpose

This document is the root planning note for the next phase of SkillLogBoard.

The current SkillLogBoard implementation has reached a v0.6 release-candidate level with:

- RunLogger lifecycle and local run folder schema
- metric/config/event/artifact logging
- static single-run dashboard
- Skills.md rule engine and `skill_trace.jsonl`
- multi-run compare reports
- template registry with `ir-drop` and `trajectory`
- release-hardening checklist, CI, and build verification

The next phase should not redefine the existing architecture. It should extend the current local-first experiment evidence package into a stronger research report and agent-ready research system.

---

## Product Direction

SkillLogBoard should remain:

> A local-first experiment evidence package that turns research runs into inspectable, reproducible, report-ready artifacts.

The extension direction is:

> SkillLogBoard becomes a research evidence and agent-ready experiment system, not just a logging/dashboard package.

This means the package should help both human researchers and coding/research agents:

1. run experiments,
2. verify required evidence,
3. generate report-ready tables and figures,
4. preserve provenance,
5. hand off the experiment state to another human or agent.

---

## Current Architecture Principle

The existing structure should be preserved.

Do not replace the current modules:

```text
core/
writers/
skills/
dashboards/
compare/
plugins/
integrations/
cli/
```

Instead, extend them with new layers:

```text
reports/
agent/
template_forge/
live/
```

The extension strategy is additive.

---

## Current vs Extended Structure

### Existing Core

```text
src/skilllogboard/
  core/
  writers/
  skills/
  dashboards/
  compare/
  plugins/
  integrations/
  cli/
```

### Extended Architecture

```text
src/skilllogboard/
  reports/          # report tables, figures, report spec, report manifest
  agent/            # agent handoff, action log, research checks
  template_forge/   # agent-assisted custom research template scaffold/validation
  live/             # later local-first live watch board
```

---

## Extended Run Folder Direction

Existing run folders remain valid.

The extension adds report and agent subfolders:

```text
runs/{project}/{run_id}/
  manifest.yaml
  config.yaml
  metrics.csv
  events.jsonl
  skill_trace.jsonl
  summary.md
  dashboard.html

  artifacts/
  tables/
  figures/

  report/
    report.md
    report.html
    report_manifest.yaml
    tables/
    figures/

  agent/
    handoff.md
    actions.jsonl
    decisions.md
```

No existing output should become invalid because of v0.7.

---

## Roadmap

### v0.7 — Report Artifact Layer

Goal:

> Strengthen research report outputs with structured tables, figures, report manifests, and report validation rules.

Primary additions:

- `report/tables/`
- `report/figures/`
- `report/report_manifest.yaml`
- stronger table export
- metric curve figure export
- seed errorbar figure export
- ablation bar figure export
- required table/figure rules
- report-ready Markdown/HTML output

Detailed plan:

```text
SkillLogBoard_v0.7_Report_Artifact_Layer_DevPlan.md
```

---

### v0.8 — Agent Research Layer

Goal:

> Make experiment runs handoff-ready for coding agents and future researchers.

Planned additions:

- `.skilllog/agent_skills.md`
- `.skilllog/experiment_plan.md`
- `agent/handoff.md`
- `agent/actions.jsonl`
- `skilllog agent check`
- `skilllog agent handoff`
- agent completion criteria based on rules and report artifacts

---

### v0.9 — Template Forge

Goal:

> Let users describe a research topic and data setting, then let an external coding agent generate a SkillLogBoard-compatible research template under a controlled harness.

Planned additions:

- `ResearchBrief.md`
- `.skilllog/template_harness.md`
- `.skilllog/template_spec.md`
- template scaffold command
- template validation command
- agent-safe custom template generation workflow

Important policy:

SkillLogBoard itself does not need to embed an LLM. It should provide harness documents, schema, scaffold, and validation gates so that Codex, Claude, Cursor, or other agents can safely generate template code.

---

### v1.0 — Local-first Live Board

Goal:

> Add a local watch server for real-time experiment monitoring while preserving static report compatibility.

Planned additions:

- `skilllog watch`
- `monitoring.jsonl`
- local live board
- live metric polling
- rule audit live panel
- artifact feed
- optional system/GPU monitor

Explicit non-goals:

- no TensorBoard import
- no W&B import
- no Prometheus/Grafana integration
- no cloud sync
- no multi-user auth

---

## Global Non-goals

Do not turn SkillLogBoard into:

- a cloud MLOps platform,
- a TensorBoard clone,
- a W&B clone,
- an MLflow replacement,
- a multi-user SaaS,
- a real-time observability platform,
- a model registry,
- a deployment system.

SkillLogBoard should remain a local-first research evidence and report tool.

---

## Development Policy

Every new feature must satisfy:

1. Existing run folders remain readable.
2. Core dependencies stay lightweight.
3. Heavy dependencies are optional extras.
4. All generated outputs are file-based.
5. Tables and figures include provenance.
6. Docs distinguish implemented features from planned features.
7. Agent-facing files must be explicit and safe.
8. New features must include tests.
9. CI must remain green across supported Python versions.
10. Release work should not proceed if public schemas are still changing.

---

## Recommended Immediate Next Step

Start with v0.7 Report Artifact Layer.

Reason:

The report layer is the foundation for later agent and live-board work. Agent workflows and live monitoring are more valuable when the package already knows how to produce report-ready tables, figures, and provenance manifests.

Read next:

```text
SkillLogBoard_v0.7_Report_Artifact_Layer_DevPlan.md
```
