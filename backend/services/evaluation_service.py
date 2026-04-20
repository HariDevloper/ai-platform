import asyncio
from datetime import datetime
from random import Random

from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.db_models import Evaluation, EvaluationResult


def _build_metrics(seed: int = 7) -> dict:
    rnd = Random(seed)
    return {
        "accuracy": round(rnd.uniform(0.85, 0.98), 4),
        "precision": round(rnd.uniform(0.8, 0.97), 4),
        "recall": round(rnd.uniform(0.8, 0.97), 4),
        "f1_score": round(rnd.uniform(0.8, 0.97), 4),
    }


async def execute_evaluation(evaluation_id: int) -> None:
    db: Session = SessionLocal()
    try:
        evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if not evaluation:
            return

        evaluation.status = "running"
        evaluation.started_at = datetime.utcnow()
        evaluation.progress = 5.0
        db.commit()

        for step in (20, 40, 60, 80, 95):
            await asyncio.sleep(0.2)
            evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
            if not evaluation:
                return
            evaluation.progress = float(step)
            db.commit()

        metrics = _build_metrics(seed=evaluation_id)
        evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if not evaluation:
            return

        evaluation.status = "completed"
        evaluation.progress = 100.0
        evaluation.metrics = metrics
        evaluation.completed_at = datetime.utcnow()

        result = db.query(EvaluationResult).filter(EvaluationResult.evaluation_id == evaluation_id).first()
        if result is None:
            result = EvaluationResult(evaluation_id=evaluation_id, metrics_data=metrics, analysis_data={})
            db.add(result)
        else:
            result.metrics_data = metrics
        db.commit()
    except Exception:
        db.rollback()
        evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if evaluation:
            evaluation.status = "failed"
            evaluation.completed_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()
