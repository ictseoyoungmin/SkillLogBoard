# SkillLogBoard v1.5 Performance, Retention, and Operational Rules Development Plan

## 1. Purpose

v1.5 defines how SkillLogBoard behaves when real research projects accumulate many runs, large artifacts, long JSONL logs, and agent-generated work.

## 2. Core Workstreams

### 2.1 Performance

- project index
- metric summary cache
- lazy full-series loading
- payload budgets
- large project smoke tests

### 2.2 Retention and Pruning

- dry-run first pruning
- keep-best/top-k policies
- tag-protected runs
- archive before delete
- checkpoint/artifact policies
- JSONL rotation and summarization

### 2.3 Operational Rules

- warning/error decision policy
- agent safety gate
- structured handoff JSON
- machine-readable validation feedback
- allowed/denied path rules

### 2.4 Compare Scalability

- tags/groups
- baseline/reference run
- query/filter interface
- baseline deltas

## 3. Completion Criteria

v1.5 is complete when:

1. Large projects remain usable with bounded state loading.
2. Pruning defaults to dry-run and protects important runs.
3. JSONL rotation/summarization policy exists and is tested.
4. Agent handoff has both Markdown and machine-readable JSON/YAML.
5. Safety gate rules prevent accidental core/manifest mutation by agents.
6. Compare supports tags/groups/baseline-friendly queries.
7. Docs clearly describe operational rules.
