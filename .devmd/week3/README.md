# SkillLogBoard Week 3 Development Slices

Week 3 turns the v0.1 run evidence package into a usable static dashboard and CLI workflow.

## Week 3 Goal

Implement v0.2 static dashboard and CLI usability:

- Jinja2 dashboard template skeleton
- single-run dashboard builder
- metric curves and best metric card
- config table
- artifact links
- export/file navigation links
- CLI dashboard/report/inspect refinement
- dashboard render smoke tests
- README quickstart update

## Scope Boundary

Allowed:

- Single-run `dashboard.html`
- Static HTML generated from saved run files
- Plotly/Jinja2 usage through optional `dashboard` extra
- Lightweight fallback if optional dependencies are missing
- CLI commands for existing run directories

Not allowed:

- Multi-run compare implementation
- Skills.md rule execution
- Real-time web server or websocket dashboard
- Streamlit app
- IR-drop/trajectory plugins
- Polished final product UI beyond useful v0.2 dashboard layout

## Completion Protocol

Each slice has an **Agent Completion Block**. After finishing a slice:

1. Tick all completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for any skipped, deferred, or partially implemented item.

## Recommended Execution Order

```text
.devmd/week2_cleanup/
.devmd/week3/day1/
.devmd/week3/day2/
.devmd/week3/day3/
.devmd/week3/day4/
.devmd/week3/day5/
```

Within each day, process files in numeric order.
