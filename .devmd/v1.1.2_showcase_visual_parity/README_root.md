# SkillLogBoard v1.1.2 Showcase, Visual Parity, and Demo Depth Slices

## Why v1.1.2

v1.1.1 made compare/overlay real and improved the interaction model. The remaining issue is perceived capability: the implementation can look less feature-rich than the mockups because many features are hidden behind drawers and because demo runs are too sparse.

## v1.1.2 Goal

```text
v1.1.1 true compare
+ richer demo/project state
+ visible capability affordances
+ mockup-informed visual parity pass
= convincing release-candidate demo/UI
```

## Included Structure

```text
SkillLogBoard_v1.1.2_Showcase_Visual_Parity_DevPlan.md

.devmd/v1.1.2_showcase_visual_parity/
  README.md
  day1/
  day2/
  day3/
  day4/
  day5/
```

## Completion Protocol

Each slice has an Agent Completion Block. After finishing a slice:

1. Tick completed checkboxes.
2. Change `**Status:** PENDING` to `**Status:** COMPLETED`.
3. Fill `Completed at`, `Completed by`, and `Verification command(s)`.
4. Replace `<!-- AGENT_STATUS: PENDING -->` with `<!-- AGENT_STATUS: COMPLETED -->`.
5. Add notes for skipped, deferred, or partial work.

## Final Verification

```bash
pip install -e ".[dev,dashboard,live]"
skilllog --help
skilllog watch --help
ruff check .
pytest -q
python examples/live_demo.py --multi-run --runs 5 --rich
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python -m build --no-isolation
```
