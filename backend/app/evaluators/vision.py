from __future__ import annotations

from typing import Any

import numpy as np


def evaluate_vision(y_true: list[Any], y_pred: list[Any]) -> dict[str, float]:
    true = np.asarray(y_true).astype(int)
    pred = np.asarray(y_pred).astype(int)

    intersection = float(np.logical_and(true == 1, pred == 1).sum())
    union = float(np.logical_or(true == 1, pred == 1).sum())
    tp = intersection
    fp = float(np.logical_and(true == 0, pred == 1).sum())
    fn = float(np.logical_and(true == 1, pred == 0).sum())

    iou = intersection / union if union else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    return {"iou": iou, "precision": precision, "recall": recall}
