from __future__ import annotations

from typing import Any

import numpy as np

from app.adapters.base_adapter import BaseModelAdapter


class PyTorchModelAdapter(BaseModelAdapter):
    def __init__(self) -> None:
        self.model: Any | None = None
        self.torch: Any | None = None

    def load_model(self, model_path: str) -> None:
        try:
            import torch  # type: ignore
        except Exception as exc:
            raise RuntimeError("PyTorch is not installed") from exc

        self.torch = torch
        self.model = torch.load(model_path, map_location="cpu")
        self.model.eval()

    def predict(self, data: Any) -> dict[str, list[Any]]:
        if self.model is None or self.torch is None:
            raise RuntimeError("Model not loaded")

        tensor = self.torch.tensor(np.asarray(data), dtype=self.torch.float32)
        with self.torch.no_grad():
            outputs = self.model(tensor)
            probs = self.torch.softmax(outputs, dim=-1).cpu().numpy().tolist()
            preds = self.torch.argmax(outputs, dim=-1).cpu().numpy().tolist()
        return self.normalize_output(predictions=preds, probabilities=probs)
