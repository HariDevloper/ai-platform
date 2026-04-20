from __future__ import annotations

from typing import Any

import numpy as np

from app.adapters.base_adapter import BaseModelAdapter


class TensorFlowModelAdapter(BaseModelAdapter):
    def __init__(self) -> None:
        self.model: Any | None = None

    def load_model(self, model_path: str) -> None:
        try:
            import tensorflow as tf  # type: ignore
        except Exception as exc:
            raise RuntimeError("TensorFlow is not installed") from exc

        self.model = tf.keras.models.load_model(model_path)

    def predict(self, data: Any) -> dict[str, list[Any]]:
        if self.model is None:
            raise RuntimeError("Model not loaded")

        outputs = self.model.predict(np.asarray(data), verbose=0)
        outputs = np.asarray(outputs)
        if outputs.ndim == 1:
            probs = outputs.tolist()
            preds = [float(v) for v in outputs]
            return self.normalize_output(predictions=preds, probabilities=probs)

        probs = outputs.tolist()
        preds = np.argmax(outputs, axis=1).tolist()
        return self.normalize_output(predictions=preds, probabilities=probs)
