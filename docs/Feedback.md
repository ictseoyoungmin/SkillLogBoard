# SkillLogBoard Feedback Policy

## 0. Purpose

This document defines the policy for collecting, structuring, reviewing, and converting SkillLogBoard alpha/beta feedback into product decisions and development backlog items.

SkillLogBoard feedback must not remain a free-form opinion log. It should become a reproducible product-learning loop:

```text
real workflow usage
→ observed friction
→ evidence path
→ product interpretation
→ deduplicated backlog
→ implementation slice
→ verification result
```

The policy is designed for:

- human maintainers
- coding agents
- future contributors
- release planning
- regression testing
- product positioning

---

## 1. Feedback Scope

SkillLogBoard feedback should be categorized by product surface.

| Product Area | Feedback Target |
|---|---|
| Core Logging | `RunLogger`, metrics, configs, notes, artifacts |
| Artifact Semantics | artifact roles, provenance, storage, prediction bundles |
| Report Artifact Layer | `report.html`, `report.md`, manifest, figures, tables, findings |
| Static Dashboard | `dashboard.html`, portable evidence, offline rendering |
| Live Board | Overview, Runs, Compare, Metric Lab, Artifacts, Reports, Agent, Settings |
| CLI | `index`, `runs list`, `compare`, `report`, `prune`, `rotate`, `feedback` |
| Template Forge | scaffold generation, harness, validation, examples |
| Agent Research Layer | handoff, safety gate, feedback JSON, validation feedback |
| Operational Rules | retention, pruning, status consistency, large-project behavior |
| Documentation | README, quickstart, examples, troubleshooting |

Feedback outside these areas should be recorded as general product ideas, not immediate implementation backlog.

---

## 2. Feedback Quality Standard

### 2.1 Required Qualities

Good feedback must be:

| Quality | Meaning |
|---|---|
| Reproducible | It names the command, run, file, config, or workflow where the issue appeared. |
| Evidence-backed | It points to a file path, artifact, log, report, dashboard screen, or command output. |
| Actionable | It can be converted into a bug, helper, template, CLI change, report block, UI change, or documentation task. |
| Specific | It avoids vague statements like “the UI is bad” or “automation is needed.” |
| Prioritized | It proposes or supports a P0/P1/P2/P3 priority. |
| Product-area tagged | It indicates whether the issue belongs to core, report, live, CLI, agent, template, or docs. |
| Human- and agent-readable | It has a Markdown explanation and, where possible, a JSONL event. |

### 2.2 Bad Feedback Examples

```text
- UI is bad.
- It is inconvenient.
- More automation is needed.
- The report should be better.
- It would be nice if this worked.
```

### 2.3 Good Feedback Examples

```text
- `skilllog compare` prints the full leaderboard before the concise result, which makes agent logs too long. Add `--quiet` and `--top-k`.
- `summary.md` shows `running` while `manifest.yaml` shows `completed`. Static evidence becomes inconsistent.
- `predictions.npz` contains `oof_pred` and `test_pred`, but their roles are only understandable from runner code. Add artifact role metadata.
- Submission folder is empty when validation score is below threshold, but report does not say whether this is expected or a failure. Add submission gate evidence.
```

---

## 3. Feedback File Policy

Each alpha/beta project should keep feedback in a predictable structure.

```text
alpha-test-project/<project_name>/
  Feedback.md                         # optional project-local copy of this policy/template
  results/
    backlog/
      skilllog_alpha_feedback.md      # chronological raw run feedback
      skilllog_feature_feedback.md    # feature-area analysis
      skilllog_product_backlog.md     # deduplicated backlog items
      agent_feedback.jsonl            # machine-readable feedback events
```

### 3.1 `skilllog_alpha_feedback.md`

Purpose:

- chronological run-level feedback
- raw observations
- low friction
- duplicates allowed, but discouraged when no new signal is added

Rules:

- Keep entries short.
- Record only what was newly observed in that run.
- Do not repeat the same generic “good / bad / improvement” text for every run.
- Include score, delta, gate status, and newly observed SkillLogBoard issue when relevant.

Recommended format:

```markdown
## 2026-05-17T21:43:21 / pseudo_future_residual_cap006

- score: 0.6513
- delta_vs_previous_best: +0.0438
- model_family: pseudo_future_residual
- gate_status: failed / threshold=0.7000
- newly_observed_skilllog_issue:
  - report Key Findings remained TODO even though leaderboard delta existed
  - submission gate result was not visible in report
- repeated_user_code:
  - prediction bundle convention
  - submission gate logic
- proposed_backlog:
  - [P1][report] auto findings draft
  - [P1][helper] log_submission_gate
```

### 3.2 `skilllog_feature_feedback.md`

Purpose:

- feature-area feedback
- grouped by product surface
- richer analysis than raw run feedback

Required sections:

```markdown
## RunLogger
## Project Index
## Runs List
## Compare
## Export Table
## Report Build and Validate
## Live Board
## Agent Workflow
## Template / Helper Candidates
## Reference-Guided Research Sweep <date>
```

Each section should use this structure:

```markdown
## Compare

### What worked
- ...

### Pain point
- ...

### Product interpretation
- ...

### Proposed backlog
- [P1][CLI] compare --quiet --top-k --filter

### Acceptance criteria
- `skilllog compare --top-k 5 --quiet` prints only a concise top-k summary.
- Full CSV/MD/HTML exports remain available.
```

### 3.3 `skilllog_product_backlog.md`

Purpose:

- deduplicated backlog
- ready for development slicing
- no repeated run-level boilerplate

Required backlog item format:

```markdown
## [P1][helper] Threshold-gated submission writer

### Problem
Contest-style workflows often require saving submission files only when validation score passes a threshold. Currently users implement this manually.

### Evidence
- alpha-test-project/mosquito
- repeated manual submission gate logic in runner
- feedback: submission folder can be empty without report-level explanation

### Proposed solution
Add `RunLogger.log_submission_gate(...)`.

### API sketch
```python
logger.log_submission_gate(
    metric="val/r_hit@1cm",
    value=0.6513,
    threshold=0.7000,
    mode="gte",
    path=None,
)
```

### Acceptance criteria
- Below threshold: no submission file is copied, but gate result is recorded.
- Above threshold: submission artifact is saved and indexed.
- Report shows pass/fail gate status.
- Live Board exposes gate status in run metadata.
```

### 3.4 `agent_feedback.jsonl`

Purpose:

- machine-readable feedback
- agent continuation
- automatic backlog compilation

Each line must be a valid JSON object.

Required schema:

```json
{
  "schema_version": "1.0",
  "source": "mosquito-alpha-test",
  "timestamp": "2026-05-17T21:43:21",
  "run_id": "2026-05-17_21-39-34_pseudo_future_residual_cap006",
  "product_area": "report",
  "type": "feature_request",
  "priority": "P1",
  "title": "Auto-generate report Key Findings from leaderboard and gate status",
  "evidence": "report Key Findings remained TODO while leaderboard delta existed",
  "evidence_paths": [
    "results/skilllog/.../report/report.html",
    "results/backlog/skilllog_feature_feedback.md"
  ],
  "suggested_solution": "Generate best/second/delta/submission gate findings draft",
  "acceptance": [
    "Report includes best run and delta",
    "Report states submission gate pass/fail",
    "No TODO remains when leaderboard data exists"
  ],
  "status": "proposed"
}
```

---

## 4. Priority Policy

Feedback must be converted into priority levels using the following rules.

| Priority | Definition | Examples |
|---|---|---|
| P0 | Trust, correctness, data loss, evidence inconsistency, run-breaking issue | status mismatch, wrong metric mode, broken artifact path |
| P1 | Repeated workflow boilerplate or high-impact usability problem | submission gate helper, prediction bundle, compact compare |
| P2 | Useful product polish or workflow-specific convenience | report layout, extra table columns, doctor snapshot |
| P3 | Nice-to-have or long-term exploration | advanced UI animation, optional ecosystem integrations |

### 4.1 P0 Criteria

Use P0 only when at least one is true:

```text
- Generated evidence is wrong or inconsistent.
- A run can be misinterpreted because core metadata is stale.
- Important files are missing, overwritten, or incorrectly referenced.
- A command fails in normal documented usage.
- A safety policy can be misunderstood as destructive or safe when it is not.
```

Example:

```text
[P0][bug] summary.md shows running while manifest.yaml shows completed.
```

### 4.2 P1 Criteria

Use P1 when:

```text
- The same workaround appears in multiple real workflows.
- The feature would significantly reduce repeated user code.
- It improves agent continuation or report usefulness.
- It affects core research/contest workflows.
```

Example:

```text
[P1][helper] Add log_submission_gate for threshold-gated contest submissions.
```

---

## 5. Feedback Type Policy

Every backlog item should have exactly one primary type.

| Type | Meaning |
|---|---|
| bug | Incorrect behavior or evidence inconsistency |
| helper | Small API that removes repeated boilerplate |
| template | Reusable project scaffold or experiment harness |
| CLI | Command-line behavior, flags, output, filters |
| report | Static report/dashboard artifact improvement |
| live | Live Board UI/UX improvement |
| artifact | Artifact schema, role, storage, provenance |
| agent | Handoff, feedback JSON, safety gate, agent-readable output |
| docs | README, quickstart, examples, troubleshooting |
| ops | Retention, pruning, rotation, indexing, large-project behavior |

Examples:

```text
[P0][bug] summary status mismatch
[P1][helper] threshold-gated submission writer
[P1][artifact] OOF/test prediction role metadata
[P1][CLI] compare --quiet --top-k --filter
[P2][report] environment doctor snapshot block
```

---

## 6. Evidence Policy

Every P0/P1 item must include at least one evidence reference.

Evidence can be:

```text
- run directory path
- manifest.yaml
- summary.md
- report.html
- report_manifest.yaml
- artifact_index.json
- CLI command and output
- screenshot
- traceback
- feedback file path
- agent handoff file
```

Recommended evidence format:

```markdown
### Evidence
- Run: `results/skilllog/mosquito-contest/2026-05-17_21-39-34_pseudo_future_residual_cap006`
- File: `summary.md`
- File: `manifest.yaml`
- Feedback: `results/backlog/skilllog_feature_feedback.md`
- Command: `skilllog compare ... --metric val/r_hit@1cm`
```

If no evidence path exists, the item should be marked as P2/P3 until reproduced.

---

## 7. Product Interpretation Policy

Raw feedback must be translated into product language before becoming a backlog item.

Example:

Raw feedback:

```text
index rebuild --json output is too long.
```

Product interpretation:

```text
Agent loops need a compact run discovery mode that returns only run_id, status, selected metric, tags, and group.
```

Backlog:

```text
[P1][CLI] Add compact output mode for index/runs list.
```

Acceptance:

```text
- `skilllog runs list --compact --metric val/r_hit@1cm` prints concise rows.
- `--json --compact` returns reduced fields.
- Full JSON remains available by default.
```

---

## 8. Status Policy for Feedback Items

Each product backlog item should have one status.

| Status | Meaning |
|---|---|
| proposed | Observed, not yet accepted |
| accepted | Product owner/maintainer agrees it should be implemented |
| planned | Assigned to a milestone or dev slice |
| in_progress | Agent/human is implementing |
| implemented | Code/docs/tests merged |
| verified | Verified through alpha/beta workflow |
| deferred | Valid but intentionally postponed |
| rejected | Not aligned with product direction |

Example:

```json
{
  "title": "Add compact compare output",
  "status": "planned",
  "milestone": "v1.6"
}
```

---

## 9. Feedback Review Workflow

Feedback should be reviewed in this order.

```text
1. Read new `skilllog_alpha_feedback.md` entries.
2. Extract new, non-duplicate observations.
3. Update `skilllog_feature_feedback.md` by product area.
4. Add machine-readable entries to `agent_feedback.jsonl`.
5. Deduplicate into `skilllog_product_backlog.md`.
6. Assign priority and type.
7. Convert accepted items into `.devmd` slices.
8. Implement and verify.
9. Mark backlog items as implemented/verified.
```

For agent use:

```text
Before starting implementation:
- read skilllog_product_backlog.md
- read agent_feedback.jsonl
- read relevant evidence files
- update status to in_progress

After implementation:
- add verification commands
- update backlog status to implemented
- add follow-up feedback if behavior is still insufficient
```

---

## 10. Minimum Feedback Template

Use this when time is limited.

```markdown
## <timestamp> / <run_id or command>

- product_area:
- type:
- priority:
- observed:
- expected:
- evidence:
- suggested_solution:
- acceptance:
```

Example:

```markdown
## 2026-05-17T21:43:21 / pseudo_future_residual_cap006

- product_area: report
- type: feature_request
- priority: P1
- observed: Report Key Findings remained TODO although leaderboard delta existed.
- expected: Report should draft best run, second best, delta, and gate status.
- evidence: results/skilllog/.../report/report.html
- suggested_solution: Add deterministic report auto-findings generator.
- acceptance:
  - best run is named
  - delta is shown
  - submission gate pass/fail is shown
  - no TODO remains when leaderboard data exists
```

---

## 11. Full Feedback Template

Use this for major alpha/beta test rounds.

### 11.1 Test Context

| Field | Value |
|---|---|
| Project name |  |
| Test folder |  |
| Date / time |  |
| Tester | human / agent / mixed |
| SkillLogBoard version |  |
| Python version |  |
| OS / environment |  |
| Test type | example / contest / research / agent workflow / report workflow / live board |
| Dataset or task |  |

### 11.2 Workflow Summary

```text
Describe the actual workflow: data, training/evaluation loop, artifacts, report/dashboard usage, agent involvement.
```

### 11.3 What Worked

| Product area | What worked | Evidence |
|---|---|---|
| Core Logging |  |  |
| Artifacts |  |  |
| Report |  |  |
| Live Board |  |  |
| CLI |  |  |
| Agent |  |  |

### 11.4 Pain Points

| Product area | Pain point | Impact | Evidence |
|---|---|---|---|
|  |  |  |  |

### 11.5 Missing Semantics

| Missing semantic | Why it matters | Suggested product surface |
|---|---|---|
| submission gate | Explains why submission file is absent | helper + manifest + report |
| OOF prediction role | Agents cannot infer validation artifact safely | artifact metadata |
| fold metrics role | Fold-level weakness is hidden | table artifact + report |
| rule audit | Contest policy cannot be checked | rules/audit.json + report |

### 11.6 Backlog Candidates

| Priority | Type | Title | Product area | Evidence |
|---|---|---|---|---|
| P0 | bug |  |  |  |
| P1 | helper |  |  |  |
| P1 | CLI |  |  |  |
| P2 | report |  |  |  |

---

## 12. Agent-specific Feedback Policy

When feedback is produced by a coding agent, it must include:

```text
- task instruction
- files read
- files modified
- commands run
- tests passed/failed
- blockers
- next actions
- whether SkillLogBoard evidence was sufficient
```

Agent feedback should answer:

| Question | Required? |
|---|---|
| Could the agent identify the best run? | yes |
| Could the agent identify failed/skipped/running runs? | yes |
| Could the agent find artifact roles without reading project code? | yes |
| Could the agent determine whether submission was intentionally skipped? | yes |
| Could the agent continue from handoff.json? | yes |
| Could the agent verify report/dashboard outputs? | yes |

If the answer is `no`, create a backlog item.

---

## 13. Live Board Feedback Policy

Live Board feedback must be screen-specific.

| Screen | Required feedback |
|---|---|
| Overview | Can the user understand project state in 10 seconds? |
| Runs | Can the user find best/completed/failed/tagged runs quickly? |
| Compare | Can the user compare selected runs without noisy output? |
| Metric Lab | Can the user inspect scalar behavior clearly? |
| Artifacts | Are artifact roles and provenance visible? |
| Reports | Can the user find report package and validation status? |
| Agent | Are next actions, blockers, and handoff visible? |
| Settings | Is local-first/no-cloud behavior clear? |

Avoid:

```text
- “UI is not pretty”
```

Use:

```text
- “Compare screen does not expose exclude-tag filter, so non-tree candidate review requires CLI workaround.”
- “Artifacts screen lists `predictions.npz` but does not show OOF/test roles.”
```

---

## 14. Report Feedback Policy

Report feedback must distinguish:

```text
content
layout
portability
provenance
automation
```

Report feedback checklist:

| Question | Expected |
|---|---|
| Does report explain the run without the Live Board? | yes |
| Does report show main metric and mode? | yes |
| Does report show best/second/delta when compare data exists? | yes |
| Does report show submission gate result? | yes, when logged |
| Does report avoid TODO placeholders? | yes |
| Does report render offline? | yes |
| Does report link figures/tables/provenance? | yes |

---

## 15. CLI Feedback Policy

CLI feedback must include:

```text
command
actual output problem
desired output
automation impact
```

Example:

```markdown
## CLI Feedback

- command: `skilllog compare runs --metric val/r_hit@1cm`
- observed: full leaderboard prints before concise summary
- impact: agent logs become long and best run is hard to parse
- desired: `--quiet --top-k 5`
- priority: P1
```

---

## 16. Feedback-to-Development Slice Policy

A backlog item is ready to become a `.devmd` slice only when it has:

```text
- priority
- type
- problem
- evidence
- proposed solution
- target files
- acceptance criteria
- verification commands
```

If any of these are missing, the item remains `proposed`.

Development slice title format:

```text
.devmd/<milestone>/
  01_<short_problem_or_feature>.md
```

Example:

```text
.devmd/v1.6_contest_research_workflow_semantics/
  03_submission_gate_helper.md
```

---

## 17. Current Known Feedback Themes from Mosquito Alpha Test

These are examples of how feedback should be converted.

### [P0][bug] Status consistency

```text
Problem:
summary.md can show running while manifest.yaml shows completed.

Product interpretation:
Static evidence must be internally consistent.

Backlog:
Fix finalization order or reload final manifest during summary/report generation.
```

### [P1][helper] Submission gate

```text
Problem:
Submission threshold logic is manually implemented and invisible in report.

Product interpretation:
Contest workflows need first-class submission gate evidence.

Backlog:
Add `RunLogger.log_submission_gate(...)`.
```

### [P1][artifact] Prediction role metadata

```text
Problem:
OOF/test predictions are stored in one NPZ, but roles are only known from project code.

Product interpretation:
Artifacts need role metadata for reports, Live Board, and agents.

Backlog:
Add artifact role metadata and prediction bundle helper.
```

### [P1][CLI] Compact and filtered run discovery

```text
Problem:
`index rebuild --json`, `runs list --json`, and compare output are too verbose for agent loops.

Product interpretation:
Agents need compact, filterable command output.

Backlog:
Add `--compact`, `--quiet`, `--top-k`, `--include-tags`, `--exclude-tags`.
```

### [P1][report] Auto findings

```text
Problem:
Report Key Findings can remain TODO despite available leaderboard delta.

Product interpretation:
Report generator should draft deterministic findings from existing evidence.

Backlog:
Add report auto-findings block.
```

### [P1][rules] Rule audit

```text
Problem:
Contest policy such as test data usage, fold count, threshold, and metric mode is not explicitly audited.

Product interpretation:
Research evidence should include rule audit status.

Backlog:
Add `logger.log_rule_audit(...)`.
```

---

## 18. Governance Rules

### 18.1 Do Not Overfit to One Alpha Project

Feedback from one project can motivate a feature, but implementation should be general enough for similar workflows.

```text
Good:
submission gate helper for any threshold-based artifact decision

Bad:
mosquito-specific submission writer hardcoded to R-Hit@1cm
```

### 18.2 Do Not Add Heavy Frameworks for Small Semantics

Prefer lightweight helper APIs and metadata conventions.

```text
Good:
logger.log_fold_metrics(...)

Bad:
new full competition framework dependency
```

### 18.3 Do Not Hide Raw Evidence

Generated summaries and reports should not replace raw files.

```text
Keep:
metrics.csv
manifest.yaml
artifact_index.json
report_manifest.yaml

Add:
report findings
artifact role metadata
rule audit
```

### 18.4 Keep Feedback Traceable

Every accepted backlog item should trace back to:

```text
feedback file
run id
evidence path
acceptance criteria
verification command
```

---

## 19. Final Checklist for a Feedback Review Round

Before closing a feedback review round, confirm:

```text
[ ] New raw feedback entries were reviewed.
[ ] Duplicate comments were deduplicated.
[ ] P0/P1 items have evidence paths.
[ ] Product areas and types were assigned.
[ ] Machine-readable JSONL entries were added where useful.
[ ] `skilllog_product_backlog.md` was updated.
[ ] Accepted items were linked to dev slices.
[ ] Deferred/rejected items have reasons.
[ ] The next alpha-test run knows what to verify.
```

---

## 20. Recommended Future Commands

Future CLI commands may follow this direction:

```bash
skilllog feedback compile results/backlog \
  --input agent_feedback.jsonl \
  --output skilllog_product_backlog.md

skilllog feedback validate results/backlog/agent_feedback.jsonl

skilllog feedback summarize results/backlog \
  --by-priority \
  --by-product-area
```

These commands are optional future work, but feedback files should be structured so such commands are possible.
