# UI Design Guidelines

SkillLogBoard UI should feel like a local-first research product: quiet by default, fast to scan,
and explicit about local evidence.

## Portable Reports

Static report screenshots should show the report as an offline document, not as a Live Board view.
Capture `report.html` with local relative assets loaded, no CDN dependencies, and provenance visible
through `report_manifest.yaml`. Prefer desktop and narrow viewport captures for release notes.

## Live Board Principles

- Use the v1.2 app shell as the durable information architecture: Project contains Overview,
  Runs, and Compare; Analysis contains Metric Lab, Artifacts, and Reports; Evidence contains Agent
  and Local Settings.
- Keep project mode summary-first: Overview should show run count, health, shared metrics,
  evidence, and warnings without pulling full metric series.
- Keep single-run mode run-oriented: Metric Lab is the default landing view.
- Put advanced evidence in interactions and scoped views: side panels, bottom trays, drawers,
  full-screen lab, and metadata-first artifact/report views.
- Keep the bottom tray collapsed by default and make the side panel compactable for dense compare
  sessions.
- Keep local files visible and inspectable; do not imply cloud sync, auth, or hosted observability.
- Use deep navy surfaces, restrained cyan/blue accents, crisp system typography, and 8px-or-less
  radii.
- Avoid external fonts, CDNs, React/Vue/Svelte build tooling, or heavy frontend dependencies.
- Avoid account, team, invite, organization, avatar, cloud project, and remote sync metaphors.

## Metric Workspace

- Let users search, select, and pin multiple metrics.
- Provide chart transforms for raw/smoothed values, linear/log scale, and step/relative alignment.
- In project mode, compare overlays should use bounded local series, visible best/latest/baseline
  roles, run visibility toggles, and raw/normalized value controls.
- Correlate metric movement with events, rule outcomes, artifacts, logs, and resources.
- Keep preferences in browser `localStorage` scoped by mode and target directory; never add
  server-side user/session storage.

## Visual Parity Checklist

- Minimal overview: status, mode, poll interval, primary metric, alert count, and resource state
  are visible without crowding the chart.
- Capability hints: run, metric, shared metric, compare, artifact, warning, and agent evidence
  hints appear only when backed by local state.
- Metric Workspace: selected metric chips, group counts, latest values, ranges, and marker
  affordances remain readable with rich demo data and with sparse data.
- Compare overlay: compare mode has a visible mode chip, selected metric, selected run count,
  shared metric count, bounds, readable legend swatches, and warnings when the payload reports
  compare limitations.
- Drawers and trays: run picker, detail drawer, context tray, artifact preview, and Metric Lab are
  reachable but secondary to the primary chart.
- Artifact browser: report, table, figure, checkpoint, and other artifacts are grouped with compact
  metadata and do not inline unsafe or large file content.
- Agent workspace: action count, latest status, changed files, handoff, and decisions are shown as
  local evidence cards; missing evidence uses an actionable empty state.
- Empty states: no-metric, no-compare, no-artifact, no-agent, and no-log states point to local
  commands or local files without implying cloud import, auth, or hosted observability.
- Performance: project discovery, compare points, and rendered panel rows stay bounded so repeated
  polling feels responsive. Inactive heavy views should not refresh full series eagerly.

## Screenshot Guidance

Generate synthetic local evidence first:

```bash
python examples/live_demo.py --multi-run --runs 5 --rich
skilllog watch runs/live_demo --project --no-open
```

Recommended viewport sizes are 1440x960 for the primary desktop capture, 1280x800 for a compact
laptop pass, and 390x844 for a narrow mobile pass. The rich demo is deterministic synthetic local
evidence; it is meant to show supported Live Board states without external imports or services.

Capture these states for visual QA:

- Project overview with capability hints, metric chips, and a populated leaderboard chart.
- Compare mode with the compare banner, selected run count, shared metric count, and legend swatches.
- Metric Lab opened from the same selected metric.
- Artifact preview drawer opened from a report, table, or figure artifact card.
- Agent Workspace showing action count, latest action, changed files, handoff, and decisions.
- Empty-state pass on a sparse or new run folder to confirm guidance remains concise.

## Accessibility

- Interactive controls need accessible names.
- Tabs, drawers, and full-screen panels need roles or labels.
- Focus states must remain visible against dark surfaces.
- Text should fit in compact panels without overlapping or relying on viewport-scaled font sizes.
