from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.db_models import Evaluation, EvaluationResult
from backend.models.schemas import RobustnessRequest
from backend.services.robustness_analyzer import run_adversarial_analysis, run_perturbation_analysis
from backend.utils.exceptions import AppException
from backend.utils.response import success_response

router = APIRouter(prefix="/api/robustness", tags=["robustness"])


def _upsert_analysis(db: Session, evaluation_id: int, key: str, value: dict) -> dict:
    result = db.query(EvaluationResult).filter(EvaluationResult.evaluation_id == evaluation_id).first()
    if not result:
        result = EvaluationResult(evaluation_id=evaluation_id, metrics_data={}, analysis_data={key: value})
        db.add(result)
    else:
        analysis_data = result.analysis_data or {}
        analysis_data[key] = value
        result.analysis_data = analysis_data
    db.commit()
    db.refresh(result)
    return result.analysis_data or {}


@router.post("/adversarial")
def adversarial_analysis(payload: RobustnessRequest, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == payload.evaluation_id).first()
    if not evaluation:
        raise AppException("Evaluation not found", status_code=404)

    data = run_adversarial_analysis(payload.strength, payload.attack_type or "fgsm")
    analysis_data = _upsert_analysis(db, payload.evaluation_id, "adversarial", data)
    return success_response(analysis_data, "Adversarial analysis completed")


@router.post("/perturbation")
def perturbation_analysis(payload: RobustnessRequest, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == payload.evaluation_id).first()
    if not evaluation:
        raise AppException("Evaluation not found", status_code=404)

    data = run_perturbation_analysis(payload.strength)
    analysis_data = _upsert_analysis(db, payload.evaluation_id, "perturbation", data)
    return success_response(analysis_data, "Perturbation analysis completed")


@router.get("/{evaluation_id}/analysis")
def get_robustness_analysis(evaluation_id: int, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise AppException("Evaluation not found", status_code=404)

    result = db.query(EvaluationResult).filter(EvaluationResult.evaluation_id == evaluation_id).first()
    return success_response(result.analysis_data if result and result.analysis_data else {}, "Robustness analysis retrieved")
