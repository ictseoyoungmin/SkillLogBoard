# SkillLogBoard v0.9 Template Forge

## Purpose

v0.9 adds a controlled scaffold and validation layer that helps external coding agents create new SkillLogBoard-compatible research templates from user-provided research descriptions.

## Development Days

```text
day1 — ResearchBrief and TemplateSpec contracts
day2 — Harness documents and package templates
day3 — Scaffold generator
day4 — Template validator and safety gates
day5 — CLI, docs, regression, final verification
```

## Compatibility Rule

v0.9 must be additive. It must not break:

- existing RunLogger usage
- existing run folders
- existing v0.7 report artifact layer
- existing v0.8 agent research layer
- existing dashboard/report/compare commands
- existing template examples
- existing CI/build workflow

## Product Rule

SkillLogBoard does not call LLMs, does not generate final domain-specific research code automatically, and does not contact cloud services.

It creates local harnesses and scaffolds that an external agent can fill.
