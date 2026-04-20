from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseModelAdapter(ABC):
    @abstractmethod
    def load_model(self, model_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def predict(self, data: Any) -> dict[str, list[Any]]:
        raise NotImplementedError

    @staticmethod
    def normalize_output(predictions: list[Any], probabilities: list[Any] | None = None) -> dict[str, list[Any]]:
        return {"predictions": predictions, "probabilities": probabilities or []}
