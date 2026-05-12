# SkillLogBoard v0.9 Template Forge Development Plan

## 1. Overview

The v0.9 milestone extends SkillLogBoard from an agent-ready research evidence system into a scaffold-and-validation system for custom research templates.

By v0.8, SkillLogBoard is expected to support:

- `.skilllog/agent_skills.md`
- `.skilllog/experiment_plan.md`
- run-level `agent/actions.jsonl`
- run-level `agent/handoff.md`
- agent completion checks
- agent CLI commands

v0.9 adds Template Forge so a user can describe a research topic and data setting in Markdown, then an external coding agent can use SkillLogBoard-generated harness files and scaffolds to create a SkillLogBoard-compatible research template.

SkillLogBoard itself should not embed an LLM. It should provide local schemas, scaffold files, harness documents, validation checks, and CLI commands.

## 2. v0.9 Goal

Implement Template Forge:

> A local-first scaffold and validation layer that lets external coding agents create new SkillLogBoard-compatible research templates safely.

## 3. Core Workflow

```text
ResearchBrief.md
  ↓
TemplateSpec.md
  ↓
skilllog forge scaffold --name custom-task --brief ResearchBrief.md
  ↓
scaffolded plugin/example/tests/docs/harness
  ↓
external coding agent fills implementation
  ↓
skilllog forge validate custom-task
  ↓
template becomes eligible for implemented status
```

## 4. Scope Boundary

Allowed:

- ResearchBrief contract
- TemplateSpec contract
- template harness Markdown files
- scaffold generation
- validation command
- plugin descriptor scaffold
- synthetic example scaffold
- tests/docs scaffold
- dependency boundary checks

Not allowed:

- built-in LLM calls
- automatic code generation
- cloud APIs
- live board
- W&B/TensorBoard import
- Prometheus/Grafana
- multi-user auth
- implementing all possible domain templates directly

## 5. Target Files

```text
src/skilllogboard/template_forge/
  __init__.py
  research_brief.py
  template_spec.py
  scaffold.py
  validator.py
  harness/
    template_harness.md
    agent_template_creation_guide.md
    research_brief_template.md
    template_spec_template.md
```

CLI:

```text
skilllog forge init-brief
skilllog forge plan
skilllog forge scaffold
skilllog forge validate
```

## 6. Success Criteria

v0.9 is complete when:

1. ResearchBrief contract and template exist.
2. TemplateSpec contract and parser exist.
3. Template harness files are package-accessible.
4. `skilllog forge init-brief` creates a research brief template.
5. `skilllog forge plan` creates or validates a TemplateSpec skeleton.
6. `skilllog forge scaffold` creates plugin/example/test/docs scaffolds.
7. `skilllog forge validate` checks registration, default skills, synthetic example, tests, docs, dependency policy, and status matrix.
8. External agents can fill generated scaffolds without modifying core APIs.
9. Existing v0.8/v0.7/v0.6 functionality remains green.
10. No LLM/cloud dependency is introduced.
