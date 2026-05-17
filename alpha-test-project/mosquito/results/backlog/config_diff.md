| key | distinct_values | variation_count | run:2026-05-17_01-36-23_physics_cv_last1 | run:2026-05-17_01-37-02_residual_lgbm_cv_last1 | run:2026-05-17_02-01-33_physics_finite_diff_hit_tuned | run:2026-05-17_02-02-01_residual_extra_trees_cv_last1 | run:2026-05-17_20-22-05_jepa_torch_residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| experiment.name | jepa_torch_residual, physics_cv_last1, physics_finite_diff_hit_tuned, residual_extra_trees_cv_last1, residual_lgbm_cv_last1 | 5 | physics_cv_last1 | residual_lgbm_cv_last1 | physics_finite_diff_hit_tuned | residual_extra_trees_cv_last1 | jepa_torch_residual |
| experiment.tags | ["jepa", "torch", "residual"], ["physics", "baseline"], ["physics", "finite-difference", "hit-tuned"], ["residual", "extra-trees", "candidate"], ["residual", "lightgbm", "candidate"] | 5 | ["physics", "baseline"] | ["residual", "lightgbm", "candidate"] | ["physics", "finite-difference", "hit-tuned"] | ["residual", "extra-trees", "candidate"] | ["jepa", "torch", "residual"] |
| model.base_method | , cv_last1 | 2 |  | cv_last1 |  | cv_last1 | cv_last1 |
| model.method | , cv_last1, finite_diff | 3 | cv_last1 |  | finite_diff |  |  |
| model.model_kind | , extra_trees, lightgbm | 3 |  | lightgbm |  | extra_trees |  |
| model.params.batch_size | , 256 | 2 |  |  |  |  | 256 |
| model.params.coefficients | , [2.4906, -0.4332, -0.0291, -0.0548, 0.017] | 2 |  |  | [2.4906, -0.4332, -0.0291, -0.0548, 0.017] |  |  |
| model.params.colsample_bytree | , 0.92 | 2 |  | 0.92 |  |  |  |
| model.params.epochs | , 100 | 2 |  |  |  |  | 100 |
| model.params.hidden | , 96 | 2 |  |  |  |  | 96 |
| model.params.learning_rate | , 0.018 | 2 |  | 0.018 |  |  |  |
| model.params.lr | , 0.001 | 2 |  |  |  |  | 0.001 |
| model.params.mask_prob | , 0.35 | 2 |  |  |  |  | 0.35 |
| model.params.max_features | , 0.5 | 2 |  |  |  | 0.5 |  |
| model.params.min_samples_leaf | , 3 | 2 |  |  |  | 3 |  |
| model.params.n_estimators | , 1400, 600 | 3 |  | 1400 |  | 600 |  |
| model.params.num_leaves | , 31 | 2 |  | 31 |  |  |  |
| model.params.pretrain_epochs | , 35 | 2 |  |  |  |  | 35 |
| model.params.reg_lambda | , 0.35 | 2 |  | 0.35 |  |  |  |
| model.params.subsample | , 0.92 | 2 |  | 0.92 |  |  |  |
| model.params.weight_decay | , 0.0001 | 2 |  |  |  |  | 0.0001 |
| model.type | jepa_torch, physics, residual, residual_lgbm | 4 | physics | residual_lgbm | physics | residual | jepa_torch |
| runtime_args.config | alpha-test-project/mosquito/configs/jepa_torch.yaml, alpha-test-project/mosquito/configs/physics.yaml, alpha-test-project/mosquito/configs/physics_finite_diff.yaml, alpha-test-project/mosquito/configs/residual_extra_trees.yaml, alpha-test-project/mosquito/configs/residual_lgbm.yaml | 5 | alpha-test-project/mosquito/configs/physics.yaml | alpha-test-project/mosquito/configs/residual_lgbm.yaml | alpha-test-project/mosquito/configs/physics_finite_diff.yaml | alpha-test-project/mosquito/configs/residual_extra_trees.yaml | alpha-test-project/mosquito/configs/jepa_torch.yaml |
