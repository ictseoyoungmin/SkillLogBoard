# Mosquito Contest Alpha Test

This folder contains the local SkillLogBoard-driven alpha-test framework for the
mosquito trajectory contest.

## Current Best

- `pseudo_future_residual_cap006`
- Validation: `R-Hit@1cm = 0.6513`
- Submission gate: no file is saved until validation reaches `0.7000`.

## Run Commands

Run from the repository root:

```bash
PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/physics.yaml
PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/physics_finite_diff.yaml
PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/residual_extra_trees.yaml
PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/jepa_torch.yaml
```

For CUDA torch runs in this WSL setup, import `torch` before inserting the project path:

```bash
.venv/bin/python -c "import torch, sys; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'); sys.path.insert(0, 'alpha-test-project/mosquito'); from contest_mosquito.runner import main; raise SystemExit(main(['--config', 'alpha-test-project/mosquito/configs/pseudo_future_residual_cap006.yaml']))"
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
