"""Small JEPA-inspired torch model for coordinate trajectories."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.model_selection import KFold

from contest_mosquito.metrics import metric_summary
from contest_mosquito.physics import predict_physics


@dataclass
class JepaResult:
    oof_pred: np.ndarray
    test_pred: np.ndarray
    metrics: dict[str, float]
    fold_rows: list[dict[str, float | int]]
    model_label: str


def evaluate_jepa_torch(
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_x: np.ndarray,
    base_method: str,
    cv_splits: int,
    seed: int,
    params: dict[str, Any] | None = None,
) -> JepaResult:
    try:
        import torch
        from torch.utils.data import DataLoader, TensorDataset
    except Exception as exc:  # pragma: no cover - exercised when torch is unavailable
        raise RuntimeError("torch is required for model.type=jepa_torch") from exc

    params = params or {}
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    epochs = int(params.get("epochs", 120))
    pretrain_epochs = int(params.get("pretrain_epochs", 40))
    batch_size = int(params.get("batch_size", 256))
    lr = float(params.get("lr", 1e-3))
    hidden = int(params.get("hidden", 96))
    mask_prob = float(params.get("mask_prob", 0.35))
    base_train = predict_physics(train_x, base_method)
    base_test = predict_physics(test_x, base_method)
    target_residual = train_y - base_train
    oof_pred = np.zeros_like(train_y, dtype=np.float32)
    fold_rows: list[dict[str, float | int]] = []
    splitter = KFold(n_splits=cv_splits, shuffle=True, random_state=seed)

    for fold, (train_idx, val_idx) in enumerate(splitter.split(train_x)):
        torch.manual_seed(seed + fold)
        model = _TrajectoryJepa(hidden=hidden).to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=float(params.get("weight_decay", 1e-4)))
        train_ds = TensorDataset(
            torch.tensor(_normalize_context(train_x[train_idx]), dtype=torch.float32),
            torch.tensor(target_residual[train_idx], dtype=torch.float32),
        )
        loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        for _ in range(pretrain_epochs):
            model.train()
            for xb, _ in loader:
                xb = xb.to(device)
                mask = torch.rand(xb.shape[:2], device=device) < mask_prob
                pred_latent, target_latent = model.pretrain_forward(xb, mask)
                loss = ((pred_latent[mask] - target_latent[mask].detach()) ** 2).mean()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        for _ in range(epochs):
            model.train()
            for xb, yb in loader:
                xb = xb.to(device)
                yb = yb.to(device)
                pred = model(xb)
                loss = ((pred - yb) ** 2).mean()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        with torch.no_grad():
            val_x = torch.tensor(_normalize_context(train_x[val_idx]), dtype=torch.float32, device=device)
            val_residual = model(val_x).cpu().numpy()
        fold_pred = base_train[val_idx] + val_residual
        oof_pred[val_idx] = fold_pred.astype(np.float32)
        fold_rows.append({"fold": fold, **metric_summary(fold_pred, train_y[val_idx], prefix="val")})

    torch.manual_seed(seed + 10_000)
    model = _TrajectoryJepa(hidden=hidden).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=float(params.get("weight_decay", 1e-4)))
    full_ds = TensorDataset(
        torch.tensor(_normalize_context(train_x), dtype=torch.float32),
        torch.tensor(target_residual, dtype=torch.float32),
    )
    loader = DataLoader(full_ds, batch_size=batch_size, shuffle=True)
    for _ in range(max(1, epochs + pretrain_epochs // 2)):
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            pred = model(xb)
            loss = ((pred - yb) ** 2).mean()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    with torch.no_grad():
        test_residual = model(torch.tensor(_normalize_context(test_x), dtype=torch.float32, device=device)).cpu().numpy()
    metrics = metric_summary(oof_pred, train_y, prefix="val")
    metrics["val/fold_min_r_hit"] = float(min(row["val/r_hit@1cm"] for row in fold_rows))
    metrics["env/torch_cuda_available"] = float(torch.cuda.is_available())
    return JepaResult(
        oof_pred=oof_pred,
        test_pred=(base_test + test_residual).astype(np.float32),
        metrics=metrics,
        fold_rows=fold_rows,
        model_label=f"jepa_torch:{base_method}",
    )


def _normalize_context(x: np.ndarray) -> np.ndarray:
    last = x[:, -1:, :]
    scale = np.maximum(np.std(x - last, axis=(1, 2), keepdims=True), 1e-3)
    return (x - last) / scale


class _TrajectoryJepa:
    def __new__(cls, hidden: int):
        import torch
        from torch import nn

        class Module(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.mask_token = nn.Parameter(torch.zeros(1, 1, 3))
                self.context = nn.Sequential(nn.Linear(3, hidden), nn.GELU(), nn.Linear(hidden, hidden))
                self.target = nn.Sequential(nn.Linear(3, hidden), nn.GELU(), nn.Linear(hidden, hidden))
                self.predictor = nn.Sequential(nn.Linear(hidden, hidden), nn.GELU(), nn.Linear(hidden, hidden))
                self.head = nn.Sequential(
                    nn.LayerNorm(hidden),
                    nn.Linear(hidden, hidden),
                    nn.GELU(),
                    nn.Linear(hidden, 3),
                )

            def pretrain_forward(self, x, mask):
                masked = torch.where(mask[..., None], self.mask_token.expand_as(x), x)
                return self.predictor(self.context(masked)), self.target(x)

            def forward(self, x):
                h = self.context(x).mean(dim=1)
                return self.head(h)

        return Module()
