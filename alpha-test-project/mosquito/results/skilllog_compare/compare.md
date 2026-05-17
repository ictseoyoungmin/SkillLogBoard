# SkillLogBoard Compare

## Leaderboard

| rank | run_id | run_name | status | metric_name | metric_value | best_step | created_at | warning_count | error_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-05-17_02-02-01_residual_extra_trees_cv_last1 | residual_extra_trees_cv_last1 | completed | val/r_hit@1cm | 0.6075 | 0 | 2026-05-17T02:02:01.911672+09:00 | 0 | 0 |
| 2 | 2026-05-17_02-01-33_physics_finite_diff_hit_tuned | physics_finite_diff_hit_tuned | completed | val/r_hit@1cm | 0.6026 | 0 | 2026-05-17T02:01:33.736028+09:00 | 0 | 0 |
| 3 | 2026-05-17_20-28-06_residual_knn_cv_last1 | residual_knn_cv_last1 | completed | val/r_hit@1cm | 0.5984 | 0 | 2026-05-17T20:28:07.096385+09:00 | 0 | 0 |
| 4 | 2026-05-17_01-37-02_residual_lgbm_cv_last1 | residual_lgbm_cv_last1 | completed | val/r_hit@1cm | 0.5814 | 0 | 2026-05-17T01:37:02.374685+09:00 | 0 | 0 |
| 5 | 2026-05-17_01-36-23_physics_cv_last1 | physics_cv_last1 | completed | val/r_hit@1cm | 0.5787 | 0 | 2026-05-17T01:36:23.619886+09:00 | 0 | 0 |
| 6 | 2026-05-17_20-28-06_residual_ridge_cv_last1 | residual_ridge_cv_last1 | completed | val/r_hit@1cm | 0.5486 | 0 | 2026-05-17T20:28:07.184043+09:00 | 0 | 0 |
| 7 | 2026-05-17_20-22-05_jepa_torch_residual | jepa_torch_residual | completed | val/r_hit@1cm | 0.4847 | 0 | 2026-05-17T20:22:05.950928+09:00 | 0 | 0 |

## Config Diff

| key | distinct_values | variation_count | run:2026-05-17_01-36-23_physics_cv_last1 | run:2026-05-17_01-37-02_residual_lgbm_cv_last1 | run:2026-05-17_02-01-33_physics_finite_diff_hit_tuned | run:2026-05-17_02-02-01_residual_extra_trees_cv_last1 | run:2026-05-17_20-22-05_jepa_torch_residual | run:2026-05-17_20-28-06_residual_knn_cv_last1 | run:2026-05-17_20-28-06_residual_ridge_cv_last1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| experiment.name | jepa_torch_residual, physics_cv_last1, physics_finite_diff_hit_tuned, residual_extra_trees_cv_last1, residual_knn_cv_last1, residual_lgbm_cv_last1, residual_ridge_cv_last1 | 7 | physics_cv_last1 | residual_lgbm_cv_last1 | physics_finite_diff_hit_tuned | residual_extra_trees_cv_last1 | jepa_torch_residual | residual_knn_cv_last1 | residual_ridge_cv_last1 |
| experiment.tags | ["jepa", "torch", "residual"], ["physics", "baseline"], ["physics", "finite-difference", "hit-tuned"], ["residual", "extra-trees", "candidate"], ["residual", "knn", "non-tree"], ["residual", "lightgbm", "candidate"], ["residual", "ridge", "non-tree"] | 7 | ["physics", "baseline"] | ["residual", "lightgbm", "candidate"] | ["physics", "finite-difference", "hit-tuned"] | ["residual", "extra-trees", "candidate"] | ["jepa", "torch", "residual"] | ["residual", "knn", "non-tree"] | ["residual", "ridge", "non-tree"] |
| model.base_method | , cv_last1 | 2 |  | cv_last1 |  | cv_last1 | cv_last1 | cv_last1 | cv_last1 |
| model.method | , cv_last1, finite_diff | 3 | cv_last1 |  | finite_diff |  |  |  |  |
| model.model_kind | , extra_trees, knn, lightgbm, ridge | 5 |  | lightgbm |  | extra_trees |  | knn | ridge |
| model.params.alpha | , 0.0001 | 2 |  |  |  |  |  |  | 0.0001 |
| model.params.batch_size | , 256 | 2 |  |  |  |  | 256 |  |  |
| model.params.coefficients | , [2.4906, -0.4332, -0.0291, -0.0548, 0.017] | 2 |  |  | [2.4906, -0.4332, -0.0291, -0.0548, 0.017] |  |  |  |  |
| model.params.colsample_bytree | , 0.92 | 2 |  | 0.92 |  |  |  |  |  |
| model.params.epochs | , 100 | 2 |  |  |  |  | 100 |  |  |
| model.params.hidden | , 96 | 2 |  |  |  |  | 96 |  |  |
| model.params.learning_rate | , 0.018 | 2 |  | 0.018 |  |  |  |  |  |
| model.params.lr | , 0.001 | 2 |  |  |  |  | 0.001 |  |  |
| model.params.mask_prob | , 0.35 | 2 |  |  |  |  | 0.35 |  |  |
| model.params.max_features | , 0.5 | 2 |  |  |  | 0.5 |  |  |  |
| model.params.min_samples_leaf | , 3 | 2 |  |  |  | 3 |  |  |  |
| model.params.n_estimators | , 1400, 600 | 3 |  | 1400 |  | 600 |  |  |  |
| model.params.n_neighbors | , 80 | 2 |  |  |  |  |  | 80 |  |
| model.params.num_leaves | , 31 | 2 |  | 31 |  |  |  |  |  |
| model.params.p | , 2 | 2 |  |  |  |  |  | 2 |  |
| model.params.pretrain_epochs | , 35 | 2 |  |  |  |  | 35 |  |  |
| model.params.reg_lambda | , 0.35 | 2 |  | 0.35 |  |  |  |  |  |
| model.params.subsample | , 0.92 | 2 |  | 0.92 |  |  |  |  |  |
| model.params.weight_decay | , 0.0001 | 2 |  |  |  |  | 0.0001 |  |  |
| model.params.weights | , distance | 2 |  |  |  |  |  | distance |  |
| model.type | jepa_torch, physics, residual, residual_lgbm | 4 | physics | residual_lgbm | physics | residual | jepa_torch | residual | residual |
| runtime_args.config | alpha-test-project/mosquito/configs/jepa_torch.yaml, alpha-test-project/mosquito/configs/physics.yaml, alpha-test-project/mosquito/configs/physics_finite_diff.yaml, alpha-test-project/mosquito/configs/residual_extra_trees.yaml, alpha-test-project/mosquito/configs/residual_knn.yaml, alpha-test-project/mosquito/configs/residual_lgbm.yaml, alpha-test-project/mosquito/configs/residual_ridge.yaml | 7 | alpha-test-project/mosquito/configs/physics.yaml | alpha-test-project/mosquito/configs/residual_lgbm.yaml | alpha-test-project/mosquito/configs/physics_finite_diff.yaml | alpha-test-project/mosquito/configs/residual_extra_trees.yaml | alpha-test-project/mosquito/configs/jepa_torch.yaml | alpha-test-project/mosquito/configs/residual_knn.yaml | alpha-test-project/mosquito/configs/residual_ridge.yaml |

## Ablation Axes

| key | distinct_values | run_count |
| --- | --- | --- |
| experiment.name | jepa_torch_residual, physics_cv_last1, physics_finite_diff_hit_tuned, residual_extra_trees_cv_last1, residual_knn_cv_last1, residual_lgbm_cv_last1, residual_ridge_cv_last1 | 7 |
| experiment.tags | ["jepa", "torch", "residual"], ["physics", "baseline"], ["physics", "finite-difference", "hit-tuned"], ["residual", "extra-trees", "candidate"], ["residual", "knn", "non-tree"], ["residual", "lightgbm", "candidate"], ["residual", "ridge", "non-tree"] | 7 |
| model.method | cv_last1, finite_diff | 2 |
| model.model_kind | extra_trees, knn, lightgbm, ridge | 4 |
| model.params.n_estimators | 1400, 600 | 2 |
| model.type | jepa_torch, physics, residual, residual_lgbm | 7 |
| runtime_args.config | alpha-test-project/mosquito/configs/jepa_torch.yaml, alpha-test-project/mosquito/configs/physics.yaml, alpha-test-project/mosquito/configs/physics_finite_diff.yaml, alpha-test-project/mosquito/configs/residual_extra_trees.yaml, alpha-test-project/mosquito/configs/residual_knn.yaml, alpha-test-project/mosquito/configs/residual_lgbm.yaml, alpha-test-project/mosquito/configs/residual_ridge.yaml | 7 |

## Seed Summary

| group_key | count | mean | std | median | best | best_run_id |
| --- | --- | --- | --- | --- | --- | --- |
| {"__config_dir__": "/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/configs", "cv.n_splits": 5, "experiment.name": "jepa_torch_residual", "experiment.seed": 20260517, "experiment.tags": "[\"jepa\", \"torch\", \"residual\"]", "model.base_method": "cv_last1", "model.params.batch_size": 256, "model.params.epochs": 100, "model.params.hidden": 96, "model.params.lr": 0.001, "model.params.mask_prob": 0.35, "model.params.pretrain_epochs": 35, "model.params.weight_decay": 0.0001, "model.type": "jepa_torch", "paths.data_root": "data", "paths.results_root": "results", "runtime_args.config": "alpha-test-project/mosquito/configs/jepa_torch.yaml", "runtime_args.limit_test": null, "runtime_args.limit_train": null, "runtime_args.make_submission": false, "runtime_args.refresh_cache": false, "submission.threshold": 0.7} | 1 | 0.4847 | 0.0 | 0.4847 | 0.4847 | 2026-05-17_20-22-05_jepa_torch_residual |
| {"__config_dir__": "/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/configs", "cv.n_splits": 5, "experiment.name": "physics_cv_last1", "experiment.seed": 20260517, "experiment.tags": "[\"physics\", \"baseline\"]", "model.method": "cv_last1", "model.type": "physics", "paths.data_root": "data", "paths.results_root": "results", "runtime_args.config": "alpha-test-project/mosquito/configs/physics.yaml", "runtime_args.limit_test": null, "runtime_args.limit_train": null, "runtime_args.make_submission": false, "runtime_args.refresh_cache": false, "submission.threshold": 0.7} | 1 | 0.5787 | 0.0 | 0.5787 | 0.5787 | 2026-05-17_01-36-23_physics_cv_last1 |
| {"__config_dir__": "/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/configs", "cv.n_splits": 5, "experiment.name": "physics_finite_diff_hit_tuned", "experiment.seed": 20260517, "experiment.tags": "[\"physics\", \"finite-difference\", \"hit-tuned\"]", "model.method": "finite_diff", "model.params.coefficients": "[2.4906, -0.4332, -0.0291, -0.0548, 0.017]", "model.type": "physics", "paths.data_root": "data", "paths.results_root": "results", "runtime_args.config": "alpha-test-project/mosquito/configs/physics_finite_diff.yaml", "runtime_args.limit_test": null, "runtime_args.limit_train": null, "runtime_args.make_submission": false, "runtime_args.refresh_cache": false, "submission.threshold": 0.7} | 1 | 0.6026 | 0.0 | 0.6026 | 0.6026 | 2026-05-17_02-01-33_physics_finite_diff_hit_tuned |
| {"__config_dir__": "/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/configs", "cv.n_splits": 5, "experiment.name": "residual_extra_trees_cv_last1", "experiment.seed": 20260517, "experiment.tags": "[\"residual\", \"extra-trees\", \"candidate\"]", "model.base_method": "cv_last1", "model.model_kind": "extra_trees", "model.params.max_features": 0.5, "model.params.min_samples_leaf": 3, "model.params.n_estimators": 600, "model.type": "residual", "paths.data_root": "data", "paths.results_root": "results", "runtime_args.config": "alpha-test-project/mosquito/configs/residual_extra_trees.yaml", "runtime_args.limit_test": null, "runtime_args.limit_train": null, "runtime_args.make_submission": false, "runtime_args.refresh_cache": false, "submission.threshold": 0.7} | 1 | 0.6075 | 0.0 | 0.6075 | 0.6075 | 2026-05-17_02-02-01_residual_extra_trees_cv_last1 |
| {"__config_dir__": "/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/configs", "cv.n_splits": 5, "experiment.name": "residual_knn_cv_last1", "experiment.seed": 20260517, "experiment.tags": "[\"residual\", \"knn\", \"non-tree\"]", "model.base_method": "cv_last1", "model.model_kind": "knn", "model.params.n_neighbors": 80, "model.params.p": 2, "model.params.weights": "distance", "model.type": "residual", "paths.data_root": "data", "paths.results_root": "results", "runtime_args.config": "alpha-test-project/mosquito/configs/residual_knn.yaml", "runtime_args.limit_test": null, "runtime_args.limit_train": null, "runtime_args.make_submission": false, "runtime_args.refresh_cache": false, "submission.threshold": 0.7} | 1 | 0.5984 | 0.0 | 0.5984 | 0.5984 | 2026-05-17_20-28-06_residual_knn_cv_last1 |
| {"__config_dir__": "/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/configs", "cv.n_splits": 5, "experiment.name": "residual_lgbm_cv_last1", "experiment.seed": 20260517, "experiment.tags": "[\"residual\", \"lightgbm\", \"candidate\"]", "model.base_method": "cv_last1", "model.model_kind": "lightgbm", "model.params.colsample_bytree": 0.92, "model.params.learning_rate": 0.018, "model.params.n_estimators": 1400, "model.params.num_leaves": 31, "model.params.reg_lambda": 0.35, "model.params.subsample": 0.92, "model.type": "residual_lgbm", "paths.data_root": "data", "paths.results_root": "results", "runtime_args.config": "alpha-test-project/mosquito/configs/residual_lgbm.yaml", "runtime_args.limit_test": null, "runtime_args.limit_train": null, "runtime_args.make_submission": false, "runtime_args.refresh_cache": false, "submission.threshold": 0.7} | 1 | 0.5814 | 0.0 | 0.5814 | 0.5814 | 2026-05-17_01-37-02_residual_lgbm_cv_last1 |
| {"__config_dir__": "/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/configs", "cv.n_splits": 5, "experiment.name": "residual_ridge_cv_last1", "experiment.seed": 20260517, "experiment.tags": "[\"residual\", \"ridge\", \"non-tree\"]", "model.base_method": "cv_last1", "model.model_kind": "ridge", "model.params.alpha": 0.0001, "model.type": "residual", "paths.data_root": "data", "paths.results_root": "results", "runtime_args.config": "alpha-test-project/mosquito/configs/residual_ridge.yaml", "runtime_args.limit_test": null, "runtime_args.limit_train": null, "runtime_args.make_submission": false, "runtime_args.refresh_cache": false, "submission.threshold": 0.7} | 1 | 0.5486 | 0.0 | 0.5486 | 0.5486 | 2026-05-17_20-28-06_residual_ridge_cv_last1 |
