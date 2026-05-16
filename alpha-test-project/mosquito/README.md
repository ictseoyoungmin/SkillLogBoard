# Mosquito Contest Alpha Test

This folder contains the local SkillLogBoard-driven alpha-test framework for the
mosquito trajectory contest.

## Current Best

- `residual_extra_trees_cv_last1`
- Validation: `R-Hit@1cm = 0.6075`
- Submission gate: no file is saved until validation reaches `0.7000`.

## Run Commands

Run from the repository root:

```bash
PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/physics.yaml
PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/physics_finite_diff.yaml
PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/residual_extra_trees.yaml
PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/jepa_torch.yaml
```

Watch the SkillLogBoard project:

```bash
.venv/bin/python -m skilllogboard.cli.main watch alpha-test-project/mosquito/results/skilllog/mosquito-contest --project --no-open
```

## Artifacts

- `results/skilllog/`: SkillLogBoard run folders.
- `results/backlog/`: experiment backlogs and SkillLog alpha feedback.
- `results/submissions/`: threshold-gated submissions only.
- `results/cache/`: dense numpy cache for the CSV dataset.

## Notes

- `test/` is only used for final inference.
- Self-supervised torch experiments must use train only.
- Ensemble is intentionally gated: it activates only once a single model reaches `0.6800`.
