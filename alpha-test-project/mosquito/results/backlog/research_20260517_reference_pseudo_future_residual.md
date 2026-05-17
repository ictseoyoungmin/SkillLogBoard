# 2026-05-17 Reference-Guided Pseudo-Future Residual Research

## Context

- User supplied reference path: `alpha-test-project/mosquito/reference/mosquito_trajectory_prediction`.
- Reference best relevant run: `lab_codex/experiments/pseudo_future_residual_cap004_5fold/report.json`.
- Reference reported 5-fold OOF `R-Hit@1cm = 0.6518`.
- Current local framework before this session: best non-tree was `physics_finite_diff_hit_tuned = 0.6026`; best overall was tree-based `residual_extra_trees_cv_last1 = 0.6075`.
- Constraint: tree/LGBM experiments are paused; submission files may be saved only when validation `R-Hit@1cm >= 0.7000`.

## Hypothesis

The main signal is not a bigger generic model. The useful prior is a short-horizon physics anchor, while the learnable part is a small residual that is trained from train-only pseudo future tasks.

The working hypothesis is:

- `ca_last_beta_0.25` is a strong but incomplete motion prior.
- Observed timesteps can create train-only pseudo labels for +80ms prediction at current indices `[6, 7, 8]`.
- A capped MLP residual can move samples across the 1cm decision boundary without destroying too many base hits.
- The gap to 0.70 is now dominated by sample-wise mode/anchor selection, because the 66-anchor oracle reaches `0.8141`.

## Implemented Changes

- Added `physics_anchor_bank` and `ca_last_beta_0.25` support in `contest_mosquito/physics.py`.
- Added `contest_mosquito/pseudo_future.py`:
  - train-fold-only pseudo future windows;
  - capped residual MLP;
  - no-harm penalty for samples already hit by base anchor;
  - fold-wise OOF metrics and final full-data test inference.
- Added configs:
  - `configs/pseudo_future_residual_cap004.yaml`
  - `configs/pseudo_future_residual_cap006.yaml`
  - `configs/pseudo_future_residual_cap008.yaml`
  - `configs/pseudo_future_residual_cap006_noharm055.yaml`
- Updated `README.md` with the new best run and CUDA torch-first execution pattern.

## Experiment Results

| Run | Residual cap | No-harm | OOF R-Hit@1cm | Fold min | Mean dist | Median dist | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|
| `pseudo_future_residual_cap004` | 0.004 | 0.35 | 0.6506 | 0.6350 | 0.012148 | 0.007326 | 246.85s |
| `pseudo_future_residual_cap006` | 0.006 | 0.35 | 0.6513 | 0.6395 | 0.012028 | 0.007285 | 242.80s |
| `pseudo_future_residual_cap008` | 0.008 | 0.35 | 0.6497 | 0.6370 | 0.011964 | 0.007301 | 238.01s |
| `pseudo_future_residual_cap006_noharm055` | 0.006 | 0.55 | 0.6504 | 0.6400 | 0.012034 | 0.007288 | 225.23s |

Best local run:

- Run ID: `2026-05-17_21-39-34_pseudo_future_residual_cap006`
- Validation: `R-Hit@1cm = 0.6513`
- Submission: not saved, because `0.6513 < 0.7000`
- CUDA recorded: `env/torch_cuda_available = 1.0`

## Artifact Insights

For `pseudo_future_residual_cap006`:

- Base `ca_last_beta_0.25` full-train hit: `0.5993`
- Residual model hit: `0.6513`
- Net hit lift over base: `+0.0520`
- Mean distance improved from `0.012895` to `0.012028`
- Median distance improved from `0.008125` to `0.007285`
- Residual norm: mean `0.00360`, p90 `0.00768`, max `0.01039`
- Base hit to model miss: `0.0259`
- Base miss to model hit: `0.0779`
- Anchor oracle hit over 66 anchors: `0.8141`
- Anchor oracle mean best distance: `0.007318`

Interpretation:

- cap006 slightly beats cap004 because it converts more base misses into hits, even though it also harms more base hits.
- cap008 lowers mean distance but reduces hit rate. The competition metric is thresholded; optimizing average distance is not enough.
- noharm055 protects some decisions but appears too conservative or poorly balanced; it does not improve net threshold crossing.
- The 0.65 plateau is consistent with the reference. The next leap likely requires better latent state/mode inference or differentiable anchor selection, not just cap tuning.

## Next Experiments

1. Hard-slice specialist for fold-3-like cases:
   - Train a detector for high-risk samples using speed, curvature, last acceleration, and base-anchor margin.
   - Apply a specialist residual only when the detector predicts base failure.

2. Soft anchor mixture with entropy control:
   - Use the 66-anchor bank as candidates.
   - Predict a sparse soft distribution over anchors plus a small residual.
   - Add oracle-distance pseudo targets from train folds only.

3. Boundary-aware objective:
   - Keep SmoothL1, but increase loss weight in the 8-12mm band.
   - Track hit-to-miss and miss-to-hit transitions as first-class metrics.

4. Train-only temporal consistency:
   - Extend pseudo tasks with `[5, 6, 7, 8]`, but downweight earlier windows to avoid distribution shift.

5. Submission policy:
   - Continue to block submissions until 5-fold OOF `R-Hit@1cm >= 0.7000`.
   - Do not use test data for pretraining or tuning.

## SkillLog Good Points

- `RunLogger` gave each experiment a reproducible evidence bundle: config, metrics, OOF/test predictions, fold table, manifest, dashboard, summary, and backlog artifact.
- `log_table("fold_metrics", ...)` was especially useful because fold 3 remained the weak fold across pseudo-residual variants.
- `index rebuild` made the new best immediately visible after the four-run sweep.
- `compare` and `export-table leaderboard` were fast enough to use after every mini sweep.
- `report build --render-mode package` produced an offline report that can be reviewed without opening the live server.
- `report validate --json` was useful as an automated proof that report artifacts exist and are portable.

## SkillLog Pain Points

- The summary generated by `RunLogger.finish(build_report=True)` briefly showed `Status: running` while `manifest.yaml` already said `completed`; rebuilding/reporting later showed the correct state. This is a trust issue for evidence review.
- The project index JSON is too verbose for routine agent loops; it prints every metric summary for every run.
- Submission gate status is only implicit through a note and the absence of a file. A dashboard/report reader cannot immediately tell whether a run was below threshold or whether submission writing failed.
- Artifact metadata does not say which arrays inside `predictions.npz` are OOF, test, train IDs, or test IDs.
- Report `Key Findings` remains TODO even though the leaderboard and comparison data are present.
- `report build` emitted a matplotlib cache permission warning because `/home/ymin/.config/matplotlib` is not writable in this environment.
- Running CUDA experiments had an environment quirk: importing torch after putting `alpha-test-project/mosquito` on `PYTHONPATH` made `torch.cuda.is_available()` false, while torch-first import preserved CUDA. This should be captured by environment diagnostics.
- Rule audit is structurally present but empty; for contest work, rules like "no submission below threshold" and "test is inference-only" should be auditable.

## SkillLog Improvement Candidates

| Proposed improvement | Type | Priority | Product area |
|---|---|---:|---|
| Add first-class `submission_gate` metadata with threshold, actual score, passed flag, and output path | helper/report/UI | P0 | core/report/live |
| Add `log_predictions(oof=..., test=..., ids=...)` with role metadata | helper | P1 | core/artifact |
| Add fold-aware contest template with OOF, fold table, and gated submission writer | template | P1 | templates |
| Add compact index/runs output: top-k, metric, tags, status only | CLI | P1 | CLI |
| Add tag include/exclude filters to compare/report/export-table | CLI/UI | P1 | CLI/live/report |
| Rebuild run summary after final manifest status write, or make summary derive status from manifest | bug | P1 | core/report |
| Add report finding scaffolder that turns leaderboard deltas into editable findings | report | P2 | report |
| Add environment doctor artifact for CUDA, package versions, writable cache dirs, and import-path quirks | helper/report | P2 | core/report |
| Add contest rule audit hooks for threshold gate and test-data policy | rule/report | P1 | report |

## Machine-Readable Summary

```json
{
  "date": "2026-05-17",
  "best_run_id": "2026-05-17_21-39-34_pseudo_future_residual_cap006",
  "best_score": 0.6513,
  "submission_saved": false,
  "submission_threshold": 0.7,
  "reference_score": 0.6518,
  "base_anchor": "ca_last_beta_0.25",
  "base_score": 0.5993,
  "anchor_oracle_score": 0.8141,
  "main_bottleneck": "learnable sample-wise anchor/mode selection",
  "skilllog_feedback_priorities": [
    "submission_gate_metadata",
    "prediction_artifact_roles",
    "compact_project_index",
    "tag_exclude_filters",
    "summary_manifest_status_consistency",
    "contest_rule_audit"
  ]
}
```
