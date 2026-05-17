# Next Non-Tree Experiment Backlog

## Observed

- Best overall remains `residual_extra_trees_cv_last1`: `0.6075`, but tree-based models are now paused.
- Best non-tree run is `physics_finite_diff_hit_tuned`: `0.6026`.
- `residual_knn_cv_last1` reached `0.5984`.
- `jepa_torch_residual` underperformed at `0.4847`, despite CUDA being available.
- `physics_bucketed_finite_diff` reached `0.6011`, slightly below the single global finite-difference run.

## Next Ideas

- Bucketed finite-difference did not improve enough; prefer a small differentiable coefficient model that predicts only 2-5 motion coefficients, not free 3D residuals.
- Try robust objective tuning around the 1cm boundary: maximize soft hit probability instead of MSE.
- Keep ensemble disabled until a non-tree single model reaches at least `0.6800`.

## SkillLog Notes

- Add non-tree/tree family tags consistently so future compare/report can isolate families.
- Add `submission_ready=false` metadata explicitly, not just absence of submission file.
- Feedback should follow `docs/Feedback.md`: include command/config/run id, missing evidence, suggested product area, and machine-readable block.
