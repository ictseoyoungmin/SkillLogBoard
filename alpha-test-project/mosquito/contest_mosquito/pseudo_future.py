"""Train-only pseudo-future residual model for the mosquito contest."""

from __future__ import annotations

import copy
import random
from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.model_selection import KFold

from contest_mosquito.metrics import metric_summary
from contest_mosquito.models import ExperimentResult
from contest_mosquito.physics import physics_anchor_bank


@dataclass(frozen=True)
class PseudoFutureConfig:
    folds: int = 5
    seed: int = 20260517
    current_indices: tuple[int, ...] = (6, 7, 8)
    horizon_steps: float = 2.0
    base_anchor: str = "ca_last_beta_0.25"
    batch_size: int = 512
    pretrain_epochs: int = 35
    finetune_epochs: int = 100
    patience: int = 35
    lr: float = 8.0e-4
    pretrain_lr: float = 1.0e-3
    weight_decay: float = 2.0e-4
    hidden_dim: int = 256
    dropout: float = 0.08
    residual_cap: float = 0.004
    noharm_weight: float = 0.35
    hit_radius: float = 0.01
    num_workers: int = 0
    device: str = "auto"
    fit_full_model: bool = True
    final_epochs: int = 0


def evaluate_pseudo_future_residual(
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    cv_splits: int,
    seed: int,
    params: dict[str, Any] | None = None,
) -> ExperimentResult:
    try:
        import torch
    except Exception as exc:  # pragma: no cover - exercised when torch is unavailable
        raise RuntimeError("torch is required for model.type=pseudo_future_residual") from exc

    cfg = _config_from_params(cv_splits=cv_splits, seed=seed, params=params or {})
    device = _get_device(torch, cfg.device)
    splitter = KFold(n_splits=cfg.folds, shuffle=True, random_state=cfg.seed)
    oof_pred = np.zeros_like(train_y, dtype=np.float32)
    fold_rows: list[dict[str, Any]] = []
    best_epochs: list[int] = []
    cuda_available = bool(torch.cuda.is_available())
    cuda_name = torch.cuda.get_device_name(0) if cuda_available else "cpu"

    for fold, (fit_idx, val_idx) in enumerate(splitter.split(train_x)):
        _set_seed(torch, cfg.seed + fold)
        pred_val, row = _fit_fold(
            torch=torch,
            cfg=cfg,
            device=device,
            fold=fold,
            x_fit=train_x[fit_idx],
            y_fit=train_y[fit_idx],
            x_val=train_x[val_idx],
            y_val=train_y[val_idx],
        )
        oof_pred[val_idx] = pred_val
        fold_rows.append(row)
        best_epochs.append(int(row["best_epoch"]))

    metrics = metric_summary(oof_pred, train_y, prefix="val")
    metrics["val/fold_min_r_hit"] = float(min(row["val/r_hit@1cm"] for row in fold_rows))
    metrics["env/torch_cuda_available"] = float(cuda_available)
    metrics["model/residual_cap"] = float(cfg.residual_cap)
    metrics["model/pseudo_windows_per_sample"] = float(len(cfg.current_indices))
    metrics["model/median_best_epoch"] = float(np.median(best_epochs))
    test_pred = (
        _fit_full_predict(torch, cfg, device, train_x, train_y, test_x, best_epochs)
        if cfg.fit_full_model
        else _base_anchor_pred(test_x, cfg)[0]
    )
    return ExperimentResult(
        oof_pred=oof_pred,
        test_pred=test_pred.astype(np.float32),
        metrics=metrics,
        fold_rows=fold_rows,
        model_label=(
            f"pseudo_future_residual:{cfg.base_anchor}:"
            f"cap{cfg.residual_cap:g}:device={cuda_name}"
        ),
    )


def _config_from_params(cv_splits: int, seed: int, params: dict[str, Any]) -> PseudoFutureConfig:
    raw_indices = params.get("current_indices", (6, 7, 8))
    current_indices = tuple(int(item) for item in raw_indices)
    return PseudoFutureConfig(
        folds=int(params.get("folds", cv_splits)),
        seed=int(params.get("seed", seed)),
        current_indices=current_indices,
        horizon_steps=float(params.get("horizon_steps", 2.0)),
        base_anchor=str(params.get("base_anchor", "ca_last_beta_0.25")),
        batch_size=int(params.get("batch_size", 512)),
        pretrain_epochs=int(params.get("pretrain_epochs", 35)),
        finetune_epochs=int(params.get("finetune_epochs", 100)),
        patience=int(params.get("patience", 35)),
        lr=float(params.get("lr", 8.0e-4)),
        pretrain_lr=float(params.get("pretrain_lr", 1.0e-3)),
        weight_decay=float(params.get("weight_decay", 2.0e-4)),
        hidden_dim=int(params.get("hidden_dim", 256)),
        dropout=float(params.get("dropout", 0.08)),
        residual_cap=float(params.get("residual_cap", 0.004)),
        noharm_weight=float(params.get("noharm_weight", 0.35)),
        hit_radius=float(params.get("hit_radius", 0.01)),
        num_workers=int(params.get("num_workers", 0)),
        device=str(params.get("device", "auto")),
        fit_full_model=bool(params.get("fit_full_model", True)),
        final_epochs=int(params.get("final_epochs", 0)),
    )


def _fit_fold(
    *,
    torch: Any,
    cfg: PseudoFutureConfig,
    device: Any,
    fold: int,
    x_fit: np.ndarray,
    y_fit: np.ndarray,
    x_val: np.ndarray,
    y_val: np.ndarray,
) -> tuple[np.ndarray, dict[str, Any]]:
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset

    pseudo_x, pseudo_y = _make_pseudo_windows(x_fit, cfg.current_indices)
    anchors_fit, anchor_names = physics_anchor_bank(x_fit, cfg.horizon_steps)
    anchors_val, _ = physics_anchor_bank(x_val, cfg.horizon_steps)
    anchors_pseudo, _ = physics_anchor_bank(pseudo_x, cfg.horizon_steps)
    base_idx = _base_anchor_index(anchors_fit, anchor_names, y_fit, cfg)

    feat_fit_raw = _make_features_np(x_fit)
    feat_val_raw = _make_features_np(x_val)
    feat_pseudo_raw = _make_features_np(pseudo_x)
    mu, sd = _standardizer(np.concatenate([feat_fit_raw, feat_pseudo_raw], axis=0))
    feat_fit = _standardize(feat_fit_raw, mu, sd)
    feat_val = _standardize(feat_val_raw, mu, sd)
    feat_pseudo = _standardize(feat_pseudo_raw, mu, sd)

    model = _ResidualMLP(torch, feat_fit.shape[1], cfg.hidden_dim, cfg.dropout, cfg.residual_cap).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.pretrain_lr, weight_decay=cfg.weight_decay)
    pseudo_base = anchors_pseudo[:, base_idx]
    pseudo_loader = DataLoader(
        TensorDataset(
            torch.tensor(feat_pseudo),
            torch.tensor(pseudo_base),
            torch.tensor(pseudo_y),
            torch.tensor(_base_hit(pseudo_base, pseudo_y, cfg.hit_radius)),
        ),
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
    )
    pretrain_loss = 0.0
    for _ in range(cfg.pretrain_epochs):
        pretrain_loss = _train_epoch(torch, F, model, pseudo_loader, cfg, device, opt)

    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    fit_base = anchors_fit[:, base_idx]
    train_loader = DataLoader(
        TensorDataset(
            torch.tensor(feat_fit),
            torch.tensor(fit_base),
            torch.tensor(y_fit),
            torch.tensor(_base_hit(fit_base, y_fit, cfg.hit_radius)),
        ),
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
    )
    val_feat_t = torch.tensor(feat_val, device=device)
    val_base_t = torch.tensor(anchors_val[:, base_idx], device=device)
    best_score = -1.0
    best_state = None
    best_epoch = 0
    best_metrics: dict[str, float] = {}
    bad = 0
    train_loss = 0.0
    for epoch in range(1, cfg.finetune_epochs + 1):
        train_loss = _train_epoch(torch, F, model, train_loader, cfg, device, opt)
        model.eval()
        with torch.no_grad():
            pred = model(val_feat_t, val_base_t).detach().cpu().numpy()
        row_metrics = metric_summary(pred, y_val, prefix="val")
        score = row_metrics["val/r_hit@1cm"]
        if score > best_score:
            best_score = score
            best_state = copy.deepcopy(model.state_dict())
            best_epoch = epoch
            best_metrics = row_metrics
            bad = 0
        else:
            bad += 1
        if bad >= cfg.patience:
            break
    if best_state is None:
        raise RuntimeError("pseudo future residual fold produced no checkpoint")
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        pred_val = model(val_feat_t, val_base_t).detach().cpu().numpy()
    base_metrics = metric_summary(anchors_val[:, base_idx], y_val, prefix="base")
    row: dict[str, Any] = {
        "fold": fold,
        "base_anchor_idx": int(base_idx),
        "base_anchor": anchor_names[base_idx],
        "base/r_hit@1cm": base_metrics["base/r_hit@1cm"],
        "best_epoch": int(best_epoch),
        "pretrain_loss": float(pretrain_loss),
        "train_loss": float(train_loss),
        "pseudo_samples": int(len(pseudo_x)),
        **best_metrics,
    }
    return pred_val.astype(np.float32), row


def _fit_full_predict(
    torch: Any,
    cfg: PseudoFutureConfig,
    device: Any,
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    best_epochs: list[int],
) -> np.ndarray:
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset

    _set_seed(torch, cfg.seed + 90_000)
    pseudo_x, pseudo_y = _make_pseudo_windows(train_x, cfg.current_indices)
    anchors_train, anchor_names = physics_anchor_bank(train_x, cfg.horizon_steps)
    anchors_test, _ = physics_anchor_bank(test_x, cfg.horizon_steps)
    anchors_pseudo, _ = physics_anchor_bank(pseudo_x, cfg.horizon_steps)
    base_idx = _base_anchor_index(anchors_train, anchor_names, train_y, cfg)
    feat_train_raw = _make_features_np(train_x)
    feat_test_raw = _make_features_np(test_x)
    feat_pseudo_raw = _make_features_np(pseudo_x)
    mu, sd = _standardizer(np.concatenate([feat_train_raw, feat_pseudo_raw], axis=0))
    feat_train = _standardize(feat_train_raw, mu, sd)
    feat_test = _standardize(feat_test_raw, mu, sd)
    feat_pseudo = _standardize(feat_pseudo_raw, mu, sd)
    model = _ResidualMLP(torch, feat_train.shape[1], cfg.hidden_dim, cfg.dropout, cfg.residual_cap).to(device)

    opt = torch.optim.AdamW(model.parameters(), lr=cfg.pretrain_lr, weight_decay=cfg.weight_decay)
    pseudo_base = anchors_pseudo[:, base_idx]
    pseudo_loader = DataLoader(
        TensorDataset(
            torch.tensor(feat_pseudo),
            torch.tensor(pseudo_base),
            torch.tensor(pseudo_y),
            torch.tensor(_base_hit(pseudo_base, pseudo_y, cfg.hit_radius)),
        ),
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
    )
    for _ in range(cfg.pretrain_epochs):
        _train_epoch(torch, F, model, pseudo_loader, cfg, device, opt)

    final_epochs = cfg.final_epochs or max(1, int(np.median(best_epochs)))
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    train_base = anchors_train[:, base_idx]
    train_loader = DataLoader(
        TensorDataset(
            torch.tensor(feat_train),
            torch.tensor(train_base),
            torch.tensor(train_y),
            torch.tensor(_base_hit(train_base, train_y, cfg.hit_radius)),
        ),
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
    )
    for _ in range(final_epochs):
        _train_epoch(torch, F, model, train_loader, cfg, device, opt)

    model.eval()
    with torch.no_grad():
        pred_test = model(
            torch.tensor(feat_test, device=device),
            torch.tensor(anchors_test[:, base_idx], device=device),
        ).detach().cpu().numpy()
    return pred_test


def _train_epoch(
    torch: Any,
    functional: Any,
    model: Any,
    loader: Any,
    cfg: PseudoFutureConfig,
    device: Any,
    opt: Any,
) -> float:
    model.train()
    losses: list[float] = []
    for feat, base, target, base_hit in loader:
        feat = feat.to(device)
        base = base.to(device)
        target = target.to(device)
        base_hit = base_hit.to(device)
        opt.zero_grad(set_to_none=True)
        pred = model(feat, base)
        loss = _residual_loss(functional, pred, target, cfg.hit_radius)
        if cfg.noharm_weight > 0:
            stay = functional.smooth_l1_loss(pred, base, beta=0.002, reduction="none").mean(dim=-1)
            loss = loss + cfg.noharm_weight * (stay * base_hit).mean()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        losses.append(float(loss.detach().cpu()))
    return float(np.mean(losses)) if losses else 0.0


def _residual_loss(functional: Any, pred: Any, true: Any, hit_radius: float) -> Any:
    import torch

    dist = torch.linalg.norm(pred - true, dim=-1)
    coord = functional.smooth_l1_loss(pred, true, beta=0.004, reduction="none").mean(dim=-1)
    band_weight = 1.0 + 2.0 * torch.exp(-((dist.detach() - hit_radius).abs() / 0.006))
    hit = functional.softplus((dist - hit_radius) / 0.002) * 0.002
    return (band_weight * coord).mean() + 0.25 * hit.mean()


def _base_anchor_index(
    anchors: np.ndarray,
    names: list[str],
    y: np.ndarray,
    cfg: PseudoFutureConfig,
) -> int:
    if cfg.base_anchor in names:
        return names.index(cfg.base_anchor)
    scores = []
    for idx in range(anchors.shape[1]):
        row = metric_summary(anchors[:, idx, :], y, prefix="base")
        scores.append((row["base/r_hit@1cm"], -row["base/mean_dist"], idx))
    return int(max(scores)[2])


def _base_anchor_pred(x: np.ndarray, cfg: PseudoFutureConfig) -> tuple[np.ndarray, int]:
    anchors, names = physics_anchor_bank(x, cfg.horizon_steps)
    idx = names.index(cfg.base_anchor) if cfg.base_anchor in names else 0
    return anchors[:, idx, :], idx


def _base_hit(base: np.ndarray, true: np.ndarray, radius: float) -> np.ndarray:
    return (np.linalg.norm(base - true, axis=1) <= radius).astype(np.float32)


def _make_pseudo_windows(x: np.ndarray, current_indices: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray]:
    xs: list[np.ndarray] = []
    ys: list[np.ndarray] = []
    for current in current_indices:
        target = current + 2
        if target >= x.shape[1]:
            continue
        xs.append(_pad_prefix(x[:, : current + 1, :], x.shape[1]))
        ys.append(x[:, target, :])
    if not xs:
        raise ValueError("current_indices did not create any pseudo-future windows")
    return np.concatenate(xs, axis=0).astype(np.float32), np.concatenate(ys, axis=0).astype(np.float32)


def _pad_prefix(prefix: np.ndarray, length: int) -> np.ndarray:
    if prefix.shape[1] == length:
        return prefix
    pad_len = length - prefix.shape[1]
    pad = np.repeat(prefix[:, :1, :], pad_len, axis=1)
    return np.concatenate([pad, prefix], axis=1)


def _make_features_np(x: np.ndarray) -> np.ndarray:
    p0 = x[:, -1:]
    rel = x - p0
    vel = np.zeros_like(x)
    vel[:, 1:] = x[:, 1:] - x[:, :-1]
    acc = np.zeros_like(x)
    acc[:, 1:] = vel[:, 1:] - vel[:, :-1]
    speed = np.linalg.norm(vel, axis=-1, keepdims=True)
    acc_norm = np.linalg.norm(acc, axis=-1, keepdims=True)
    last_v = vel[:, -1]
    prev_v = vel[:, -2]
    last_a = acc[:, -1]
    jerk = acc[:, -1] - acc[:, -2]
    eps = 1e-6
    scalars = np.concatenate(
        [
            np.linalg.norm(last_v, axis=-1, keepdims=True),
            np.linalg.norm(prev_v, axis=-1, keepdims=True),
            np.linalg.norm(last_a, axis=-1, keepdims=True),
            np.linalg.norm(jerk, axis=-1, keepdims=True),
            np.linalg.norm(last_a, axis=-1, keepdims=True)
            / (np.linalg.norm(last_v, axis=-1, keepdims=True) + eps),
            np.linalg.norm(x[:, -1] - x[:, 0], axis=-1, keepdims=True),
            (last_v * last_a).sum(axis=-1, keepdims=True)
            / (
                (np.linalg.norm(last_v, axis=-1, keepdims=True) * np.linalg.norm(last_a, axis=-1, keepdims=True))
                + eps
            ),
            (last_a * jerk).sum(axis=-1, keepdims=True)
            / (
                (np.linalg.norm(last_a, axis=-1, keepdims=True) * np.linalg.norm(jerk, axis=-1, keepdims=True))
                + eps
            ),
        ],
        axis=1,
    )
    return np.concatenate(
        [
            rel.reshape(len(x), -1),
            vel.reshape(len(x), -1),
            acc.reshape(len(x), -1),
            speed.reshape(len(x), -1),
            acc_norm.reshape(len(x), -1),
            scalars,
        ],
        axis=1,
    ).astype(np.float32)


def _standardizer(train: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return train.mean(axis=0, keepdims=True), train.std(axis=0, keepdims=True) + 1e-6


def _standardize(x: np.ndarray, mu: np.ndarray, sd: np.ndarray) -> np.ndarray:
    return ((x - mu) / sd).astype(np.float32)


def _set_seed(torch: Any, seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def _get_device(torch: Any, name: str) -> Any:
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(name)


def _ResidualMLP(torch: Any, in_dim: int, hidden: int, dropout: float, cap: float) -> Any:
    from torch import nn

    class Module(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.cap = float(cap)
            self.net = nn.Sequential(
                nn.Linear(in_dim, hidden),
                nn.LayerNorm(hidden),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(hidden, hidden),
                nn.LayerNorm(hidden),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(hidden, max(8, hidden // 2)),
                nn.GELU(),
                nn.Linear(max(8, hidden // 2), 3),
            )

        def forward(self, feat: Any, base: Any) -> Any:
            return base + self.cap * torch.tanh(self.net(feat))

    return Module()
