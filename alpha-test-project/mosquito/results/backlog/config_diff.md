| key | distinct_values | variation_count | run:2026-05-17_01-36-23_physics_cv_last1 | run:2026-05-17_01-37-02_residual_lgbm_cv_last1 | run:2026-05-17_02-01-33_physics_finite_diff_hit_tuned | run:2026-05-17_02-02-01_residual_extra_trees_cv_last1 | run:2026-05-17_20-22-05_jepa_torch_residual | run:2026-05-17_20-28-06_residual_knn_cv_last1 | run:2026-05-17_20-28-06_residual_ridge_cv_last1 | run:2026-05-17_20-54-48_physics_bucketed_finite_diff | run:2026-05-17_21-31-47_pseudo_future_residual_cap004 | run:2026-05-17_21-39-34_pseudo_future_residual_cap006 | run:2026-05-17_21-45-18_pseudo_future_residual_cap008 | run:2026-05-17_21-50-23_pseudo_future_residual_cap006_noharm055 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| experiment.name | jepa_torch_residual, physics_bucketed_finite_diff, physics_cv_last1, physics_finite_diff_hit_tuned, pseudo_future_residual_cap004, pseudo_future_residual_cap006, pseudo_future_residual_cap006_noharm055, pseudo_future_residual_cap008, residual_extra_trees_cv_last1, residual_knn_cv_last1, residual_lgbm_cv_last1, residual_ridge_cv_last1 | 12 | physics_cv_last1 | residual_lgbm_cv_last1 | physics_finite_diff_hit_tuned | residual_extra_trees_cv_last1 | jepa_torch_residual | residual_knn_cv_last1 | residual_ridge_cv_last1 | physics_bucketed_finite_diff | pseudo_future_residual_cap004 | pseudo_future_residual_cap006 | pseudo_future_residual_cap008 | pseudo_future_residual_cap006_noharm055 |
| experiment.tags | ["jepa", "torch", "residual"], ["physics", "baseline"], ["physics", "finite-difference", "bucketed", "non-tree"], ["physics", "finite-difference", "hit-tuned"], ["residual", "extra-trees", "candidate"], ["residual", "knn", "non-tree"], ["residual", "lightgbm", "candidate"], ["residual", "ridge", "non-tree"], ["torch", "pseudo-future", "residual", "non-tree", "cap-sweep"], ["torch", "pseudo-future", "residual", "non-tree", "noharm-sweep"], ["torch", "pseudo-future", "residual", "non-tree", "reference-inspired"] | 11 | ["physics", "baseline"] | ["residual", "lightgbm", "candidate"] | ["physics", "finite-difference", "hit-tuned"] | ["residual", "extra-trees", "candidate"] | ["jepa", "torch", "residual"] | ["residual", "knn", "non-tree"] | ["residual", "ridge", "non-tree"] | ["physics", "finite-difference", "bucketed", "non-tree"] | ["torch", "pseudo-future", "residual", "non-tree", "reference-inspired"] | ["torch", "pseudo-future", "residual", "non-tree", "cap-sweep"] | ["torch", "pseudo-future", "residual", "non-tree", "cap-sweep"] | ["torch", "pseudo-future", "residual", "non-tree", "noharm-sweep"] |
| model.base_method | , cv_last1 | 2 |  | cv_last1 |  | cv_last1 | cv_last1 | cv_last1 | cv_last1 |  |  |  |  |  |
| model.method | , cv_last1, finite_diff | 3 | cv_last1 |  | finite_diff |  |  |  |  |  |  |  |  |  |
| model.model_kind | , extra_trees, knn, lightgbm, ridge | 5 |  | lightgbm |  | extra_trees |  | knn | ridge |  |  |  |  |  |
| model.params.alpha | , 0.0001 | 2 |  |  |  |  |  |  | 0.0001 |  |  |  |  |  |
| model.params.base_anchor | , ca_last_beta_0.25 | 2 |  |  |  |  |  |  |  |  | ca_last_beta_0.25 | ca_last_beta_0.25 | ca_last_beta_0.25 | ca_last_beta_0.25 |
| model.params.batch_size | , 256, 512 | 3 |  |  |  |  | 256 |  |  |  | 512 | 512 | 512 | 512 |
| model.params.coefficient_count | , 3 | 2 |  |  |  |  |  |  |  | 3 |  |  |  |  |
| model.params.coefficients | , [2.4906, -0.4332, -0.0291, -0.0548, 0.017] | 2 |  |  | [2.4906, -0.4332, -0.0291, -0.0548, 0.017] |  |  |  |  |  |  |  |  |  |
| model.params.colsample_bytree | , 0.92 | 2 |  | 0.92 |  |  |  |  |  |  |  |  |  |  |
| model.params.current_indices | , [6, 7, 8] | 2 |  |  |  |  |  |  |  |  | [6, 7, 8] | [6, 7, 8] | [6, 7, 8] | [6, 7, 8] |
| model.params.device | , auto | 2 |  |  |  |  |  |  |  |  | auto | auto | auto | auto |
| model.params.dropout | , 0.08 | 2 |  |  |  |  |  |  |  |  | 0.08 | 0.08 | 0.08 | 0.08 |
| model.params.epochs | , 100 | 2 |  |  |  |  | 100 |  |  |  |  |  |  |  |
| model.params.finetune_epochs | , 100 | 2 |  |  |  |  |  |  |  |  | 100 | 100 | 100 | 100 |
| model.params.fit_full_model | , True | 2 |  |  |  |  |  |  |  |  | True | True | True | True |
| model.params.hidden | , 96 | 2 |  |  |  |  | 96 |  |  |  |  |  |  |  |
| model.params.hidden_dim | , 256 | 2 |  |  |  |  |  |  |  |  | 256 | 256 | 256 | 256 |
| model.params.horizon_steps | , 2.0 | 2 |  |  |  |  |  |  |  |  | 2.0 | 2.0 | 2.0 | 2.0 |
| model.params.learning_rate | , 0.018 | 2 |  | 0.018 |  |  |  |  |  |  |  |  |  |  |
| model.params.lr | , 0.0008, 0.001 | 3 |  |  |  |  | 0.001 |  |  |  | 0.0008 | 0.0008 | 0.0008 | 0.0008 |
| model.params.mask_prob | , 0.35 | 2 |  |  |  |  | 0.35 |  |  |  |  |  |  |  |
| model.params.max_features | , 0.5 | 2 |  |  |  | 0.5 |  |  |  |  |  |  |  |  |
| model.params.maxiter | , 35 | 2 |  |  |  |  |  |  |  | 35 |  |  |  |  |
| model.params.min_samples_leaf | , 3 | 2 |  |  |  | 3 |  |  |  |  |  |  |  |  |
| model.params.n_curvature_bins | , 1 | 2 |  |  |  |  |  |  |  | 1 |  |  |  |  |
| model.params.n_estimators | , 1400, 600 | 3 |  | 1400 |  | 600 |  |  |  |  |  |  |  |  |
| model.params.n_neighbors | , 80 | 2 |  |  |  |  |  | 80 |  |  |  |  |  |  |
| model.params.n_speed_bins | , 3 | 2 |  |  |  |  |  |  |  | 3 |  |  |  |  |
| model.params.noharm_weight | , 0.35, 0.55 | 3 |  |  |  |  |  |  |  |  | 0.35 | 0.35 | 0.35 | 0.55 |
| model.params.num_leaves | , 31 | 2 |  | 31 |  |  |  |  |  |  |  |  |  |  |
| model.params.num_workers | , 0 | 2 |  |  |  |  |  |  |  |  | 0 | 0 | 0 | 0 |
| model.params.p | , 2 | 2 |  |  |  |  |  | 2 |  |  |  |  |  |  |
| model.params.patience | , 35 | 2 |  |  |  |  |  |  |  |  | 35 | 35 | 35 | 35 |
| model.params.pretrain_epochs | , 35 | 2 |  |  |  |  | 35 |  |  |  | 35 | 35 | 35 | 35 |
| model.params.pretrain_lr | , 0.001 | 2 |  |  |  |  |  |  |  |  | 0.001 | 0.001 | 0.001 | 0.001 |
| model.params.reg_lambda | , 0.35 | 2 |  | 0.35 |  |  |  |  |  |  |  |  |  |  |
| model.params.residual_cap | , 0.004, 0.006, 0.008 | 4 |  |  |  |  |  |  |  |  | 0.004 | 0.006 | 0.008 | 0.006 |
| model.params.subsample | , 0.92 | 2 |  | 0.92 |  |  |  |  |  |  |  |  |  |  |
| model.params.weight_decay | , 0.0001, 0.0002 | 3 |  |  |  |  | 0.0001 |  |  |  | 0.0002 | 0.0002 | 0.0002 | 0.0002 |
| model.params.weights | , distance | 2 |  |  |  |  |  | distance |  |  |  |  |  |  |
| model.type | bucketed_finite_diff, jepa_torch, physics, pseudo_future_residual, residual, residual_lgbm | 6 | physics | residual_lgbm | physics | residual | jepa_torch | residual | residual | bucketed_finite_diff | pseudo_future_residual | pseudo_future_residual | pseudo_future_residual | pseudo_future_residual |
| runtime_args.config | alpha-test-project/mosquito/configs/jepa_torch.yaml, alpha-test-project/mosquito/configs/physics.yaml, alpha-test-project/mosquito/configs/physics_bucketed_finite_diff.yaml, alpha-test-project/mosquito/configs/physics_finite_diff.yaml, alpha-test-project/mosquito/configs/pseudo_future_residual_cap004.yaml, alpha-test-project/mosquito/configs/pseudo_future_residual_cap006.yaml, alpha-test-project/mosquito/configs/pseudo_future_residual_cap006_noharm055.yaml, alpha-test-project/mosquito/configs/pseudo_future_residual_cap008.yaml, alpha-test-project/mosquito/configs/residual_extra_trees.yaml, alpha-test-project/mosquito/configs/residual_knn.yaml, alpha-test-project/mosquito/configs/residual_lgbm.yaml, alpha-test-project/mosquito/configs/residual_ridge.yaml | 12 | alpha-test-project/mosquito/configs/physics.yaml | alpha-test-project/mosquito/configs/residual_lgbm.yaml | alpha-test-project/mosquito/configs/physics_finite_diff.yaml | alpha-test-project/mosquito/configs/residual_extra_trees.yaml | alpha-test-project/mosquito/configs/jepa_torch.yaml | alpha-test-project/mosquito/configs/residual_knn.yaml | alpha-test-project/mosquito/configs/residual_ridge.yaml | alpha-test-project/mosquito/configs/physics_bucketed_finite_diff.yaml | alpha-test-project/mosquito/configs/pseudo_future_residual_cap004.yaml | alpha-test-project/mosquito/configs/pseudo_future_residual_cap006.yaml | alpha-test-project/mosquito/configs/pseudo_future_residual_cap008.yaml | alpha-test-project/mosquito/configs/pseudo_future_residual_cap006_noharm055.yaml |
