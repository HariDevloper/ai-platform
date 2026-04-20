from __future__ import annotations

from typing import Any

import requests

from app.adapters.base_adapter import BaseModelAdapter


class APIModelAdapter(BaseModelAdapter):
    def __init__(self) -> None:
        self.endpoint: str | None = None

    def load_model(self, model_path: str) -> None:
        self.endpoint = model_path

    def predict(self, data: Any) -> dict[str, list[Any]]:
        if not self.endpoint:
            raise RuntimeError("API endpoint not configured")

        response = requests.post(self.endpoint, json={"inputs": data}, timeout=30)
        response.raise_for_status()
        payload = response.json()

        predictions = payload.get("predictions", [])
        probabilities = payload.get("probabilities", [])
        return self.normalize_output(predictions=predictions, probabilities=probabilities)
