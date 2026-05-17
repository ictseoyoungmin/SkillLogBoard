# Next Non-Tree Experiment Backlog

## Observed

- Best overall is now non-tree: `pseudo_future_residual_cap006`: `0.6513`.
- Tree-based models remain paused. The old best tree candidate was `residual_extra_trees_cv_last1`: `0.6075`.
- Reference folder reported `pseudo_future_residual_cap004_5fold`: about `0.6518`; the local SkillLog framework reproduced the same performance band.
- `residual_knn_cv_last1` reached `0.5984`.
- `jepa_torch_residual` underperformed at `0.4847`, despite CUDA being available.
- `physics_bucketed_finite_diff` reached `0.6011`, slightly below the single global finite-difference run.
- `ca_last_beta_0.25` base anchor is about `0.5993`, but the 66-anchor oracle reaches `0.8141`, so model capacity is not the main bottleneck.

## Next Ideas

- Build a hard-slice specialist for high-risk/fold-3-like rows where base anchor margin and curvature indicate likely failure.
- Try a sparse differentiable anchor mixture over the 66-anchor bank, with entropy control and small residuals.
- Add explicit hit-to-miss and miss-to-hit transition metrics to the runner so threshold movement is optimized, not just mean distance.
- Try train-only pseudo temporal consistency with `[5, 6, 7, 8]`, but downweight early windows to avoid distribution shift.
- Explore boundary-aware loss around 8-12mm; cap008 lowered mean distance but reduced hit rate, so average distance is a misleading target.
- Keep ensemble disabled until a non-tree single model reaches at least `0.6800`.

## SkillLog Notes

- Add non-tree/tree family tags consistently so future compare/report can isolate families.
- Add `submission_ready=false` metadata explicitly, not just absence of submission file.
- Feedback should follow `docs/Feedback.md`: include command/config/run id, missing evidence, suggested product area, and machine-readable block.
- Add prediction artifact roles and contest rule audit hooks for threshold gate/test-data policy.
