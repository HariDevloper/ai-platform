from __future__ import annotations

from typing import Any

import numpy as np
from sqlalchemy.orm import Session

from app.adapters.api_adapter import APIModelAdapter
from app.adapters.base_adapter import BaseModelAdapter
from app.adapters.pytorch_adapter import PyTorchModelAdapter
from app.adapters.tensorflow_adapter import TensorFlowModelAdapter
from app.datasets.loader import DatasetLoader
from app.datasets.preprocess import preprocess_features
from app.evaluators.classification import evaluate_classification
from app.evaluators.nlp import evaluate_nlp
from app.evaluators.regression import evaluate_regression
from app.evaluators.vision import evaluate_vision
from app.models.db_models import Evaluation, EvaluationStatus
from app.services.dataset_service import DatasetService
from app.services.model_service import ModelService
from app.trust.bias import compute_group_fairness
from app.trust.explainability import compute_feature_importance
from app.trust.robustness import evaluate_robustness
from app.utils.logger import get_logger

logger = get_logger(__name__)


class EvaluationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.model_service = ModelService(db)
        self.dataset_service = DatasetService(db)

    def create(self, *, model_id: int, dataset_id: int) -> Evaluation:
        evaluation = Evaluation(model_id=model_id, dataset_id=dataset_id, status=EvaluationStatus.PENDING)
        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation

    def get(self, evaluation_id: int) -> Evaluation | None:
        return self.db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

    def list(self, skip: int = 0, limit: int = 50) -> list[Evaluation]:
        return self.db.query(Evaluation).order_by(Evaluation.created_at.desc()).offset(skip).limit(limit).all()

    def _get_adapter(self, framework: str) -> BaseModelAdapter:
        normalized = framework.lower()
        if normalized == "pytorch":
            return PyTorchModelAdapter()
        if normalized == "tensorflow":
            return TensorFlowModelAdapter()
        if normalized in {"api", "custom_api"}:
            return APIModelAdapter()
        raise ValueError(f"Unsupported framework: {framework}")

    def _evaluate_metrics(
        self,
        model_type: str,
        y_true: list[Any],
        predictions: list[Any],
        probabilities: list[Any],
    ) -> dict[str, float]:
        normalized = model_type.lower()
        if normalized == "classification":
            return evaluate_classification(y_true, predictions, probabilities)
        if normalized == "regression":
            return evaluate_regression(y_true, predictions)
        if normalized == "nlp":
            return evaluate_nlp(y_true, predictions)
        if normalized in {"vision", "computer_vision"}:
            return evaluate_vision(y_true, predictions)
        raise ValueError(f"Unsupported model type: {model_type}")

    def run_evaluation(self, evaluation_id: int) -> None:
        evaluation = self.get(evaluation_id)
        if evaluation is None:
            logger.error("Evaluation %s not found", evaluation_id)
            return

        evaluation.status = EvaluationStatus.RUNNING
        self.db.commit()

        try:
            model = self.model_service.get(evaluation.model_id)
            dataset = self.dataset_service.get(evaluation.dataset_id)
            if model is None or dataset is None:
                raise ValueError("Invalid model or dataset reference")

            adapter = self._get_adapter(model.framework)
            adapter.load_model(model.file_path)

            data_bundle = DatasetLoader.load(dataset.path, dataset.type)
            features = preprocess_features(data_bundle.features)
            predictions_output = adapter.predict(features)

            predictions = predictions_output.get("predictions", [])
            probabilities = predictions_output.get("probabilities", [])
            metrics = self._evaluate_metrics(model.type, data_bundle.targets, predictions, probabilities)

            fairness = compute_group_fairness(predictions)
            explainability = compute_feature_importance(features, predictions)
            baseline = float(np.mean(predictions)) if predictions else 0.0
            robustness = evaluate_robustness(features, adapter.predict, baseline)

            trust_score = float(max(0.0, 1.0 - fairness.get("demographic_parity_gap", 0.0) - robustness.get("degradation", 0.0)))

            evaluation.metrics = {
                "performance": metrics,
                "bias": fairness,
                "explainability": explainability,
                "robustness": robustness,
            }
            evaluation.trust_score = trust_score
            evaluation.status = EvaluationStatus.COMPLETED
            self.db.commit()
        except Exception as exc:
            logger.exception("Evaluation %s failed", evaluation_id)
            evaluation.metrics = {"error": str(exc)}
            evaluation.status = EvaluationStatus.FAILED
            self.db.commit()
