# UI Design Guidelines

SkillLogBoard UI should feel like a local-first research product: quiet by default, fast to scan,
and explicit about local evidence.

## Live Board Principles

- Keep the first screen minimal: status, primary metric, alerts, resources, and one dominant
  Metric Workspace.
- Put advanced evidence in interactions: side panels, bottom trays, drawers, and full-screen lab.
- Keep the bottom tray collapsed by default and make the side panel compactable for dense compare
  sessions.
- Keep local files visible and inspectable; do not imply cloud sync, auth, or hosted observability.
- Use deep navy surfaces, restrained cyan/blue accents, crisp system typography, and 8px-or-less
  radii.
- Avoid external fonts, CDNs, React/Vue/Svelte build tooling, or heavy frontend dependencies.

## Metric Workspace

- Let users search, select, and pin multiple metrics.
- Provide chart transforms for raw/smoothed values, linear/log scale, and step/relative alignment.
- In project mode, compare overlays should use bounded local series, visible best/latest/baseline
  roles, run visibility toggles, and raw/normalized value controls.
- Correlate metric movement with events, rule outcomes, artifacts, logs, and resources.
- Keep preferences in browser `localStorage` scoped by mode and target directory; never add
  server-side user/session storage.

## Accessibility

- Interactive controls need accessible names.
- Tabs, drawers, and full-screen panels need roles or labels.
- Focus states must remain visible against dark surfaces.
- Text should fit in compact panels without overlapping or relying on viewport-scaled font sizes.
