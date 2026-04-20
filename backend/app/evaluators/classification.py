from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


def evaluate_classification(y_true: list[Any], y_pred: list[Any], probabilities: list[Any] | None = None) -> dict[str, float]:
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)

    metrics: dict[str, float] = {
        "accuracy": float(accuracy_score(y_true_arr, y_pred_arr)),
        "precision": float(precision_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0)),
        "recall": float(recall_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0)),
        "f1_score": float(f1_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0)),
    }

    if probabilities:
        try:
            prob_arr = np.asarray(probabilities)
            if prob_arr.ndim == 2 and prob_arr.shape[1] > 1:
                metrics["roc_auc"] = float(roc_auc_score(y_true_arr, prob_arr, multi_class="ovr"))
            elif prob_arr.ndim == 1:
                metrics["roc_auc"] = float(roc_auc_score(y_true_arr, prob_arr))
        except Exception:
            metrics["roc_auc"] = 0.0

    return metrics
