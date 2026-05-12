# SkillLogBoard v0.8 Agent Research Layer

## Purpose

v0.8 adds a local-first agent research workflow layer to SkillLogBoard. It is not an LLM feature. It is a file-based harness that lets coding agents read project guidance, log their actions, validate completion, and write handoff notes.

## Development Days

```text
day1 — Agent data contract, action log, templates
day2 — `.skilllog/` init and project control plane
day3 — Agent handoff and decision documents
day4 — Agent completion checks and rules
day5 — CLI integration, docs, regression, final verification
```

## Compatibility Rule

v0.8 must be additive. It must not break:

- existing RunLogger usage
- existing run folders
- existing v0.7 report artifact layer
- existing dashboard/report/compare commands
- existing template examples
- existing CI/build workflow

## Product Rule

SkillLogBoard does not generate code by itself in v0.8. It only provides agent-readable files, local action logs, handoff documents, and validation gates.
