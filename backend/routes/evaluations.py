import asyncio

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.db_models import Dataset, Evaluation, EvaluationResult, Model
from backend.models.schemas import EvaluationCreate
from backend.services.evaluation_service import execute_evaluation
from backend.utils.exceptions import AppException
from backend.utils.response import success_response

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])


@router.post("/create")
async def create_evaluation(payload: EvaluationCreate, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == payload.model_id).first()
    if not model:
        raise AppException("Model not found", status_code=404)

    dataset = db.query(Dataset).filter(Dataset.id == payload.dataset_id).first()
    if not dataset:
        raise AppException("Dataset not found", status_code=404)

    evaluation = Evaluation(
        model_id=payload.model_id,
        dataset_id=payload.dataset_id,
        status="pending",
        progress=0.0,
        metrics={"requested_metrics": payload.metrics},
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    asyncio.create_task(execute_evaluation(evaluation.id))
    return success_response(evaluation, "Evaluation created")


@router.get("")
def list_evaluations(status: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Evaluation)
    if status:
        query = query.filter(Evaluation.status == status)
    evaluations = query.order_by(Evaluation.created_at.desc()).all()
    return success_response(evaluations, "Evaluations retrieved")


@router.get("/{evaluation_id}")
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise AppException("Evaluation not found", status_code=404)
    return success_response(evaluation, "Evaluation retrieved")


@router.get("/{evaluation_id}/status")
def get_evaluation_status(evaluation_id: int, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise AppException("Evaluation not found", status_code=404)
    return success_response(
        {
            "evaluation_id": evaluation.id,
            "status": evaluation.status,
            "progress": evaluation.progress,
            "started_at": evaluation.started_at,
            "completed_at": evaluation.completed_at,
        },
        "Evaluation status retrieved",
    )


@router.get("/{evaluation_id}/results")
def get_evaluation_results(evaluation_id: int, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise AppException("Evaluation not found", status_code=404)

    result = db.query(EvaluationResult).filter(EvaluationResult.evaluation_id == evaluation_id).first()
    return success_response(
        {
            "evaluation_id": evaluation.id,
            "status": evaluation.status,
            "metrics": evaluation.metrics,
            "metrics_data": result.metrics_data if result else {},
            "analysis_data": result.analysis_data if result else {},
        },
        "Evaluation results retrieved",
    )
