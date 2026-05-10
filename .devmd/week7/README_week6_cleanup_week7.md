# SkillLogBoard Week 6 Cleanup + Week 7 Development Slices

Week 6 completed v0.5 research templates and optional examples. This package contains the small Week 6 cleanup plus Week 7 release-hardening slices.

## Overall Goal

Prepare SkillLogBoard for a v0.6 release-hardening candidate:

- fix remaining docs/status inconsistencies from Week 6
- verify packaging metadata
- harden optional extras and package data inclusion
- improve CI/build/release verification
- consolidate smoke scripts
- create release checklist, release notes, and release decision record

## Included Folders

```text
.devmd/week6_cleanup/
.devmd/week7/day1/
.devmd/week7/day2/
.devmd/week7/day3/
.devmd/week7/day4/
.devmd/week7/day5/
```

## Global Scope Boundary

Allowed:

- documentation/status cleanup
- packaging metadata cleanup
- CI matrix and build verification
- fresh environment install verification
- release notes and release checklist
- smoke scripts
- optional Docker verification notes

Not allowed:

- new dashboard features
- new Skills.md rule types
- new research templates
- W&B/TensorBoard import
- database backend
- real-time dashboard server
- PyPI publishing or GitHub release creation without explicit user approval

## Required Execution Order

```text
.devmd/week6_cleanup/
.devmd/week7/day1/
.devmd/week7/day2/
.devmd/week7/day3/
.devmd/week7/day4/
.devmd/week7/day5/
```

Within each day, process files in numeric order.
