from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.schemas.evaluation_schema import EvaluationCreate, EvaluationRead
from app.services.evaluation_service import EvaluationService

router = APIRouter(tags=["evaluations"])


def _run_evaluation_async(evaluation_id: int) -> None:
    db = SessionLocal()
    try:
        EvaluationService(db).run_evaluation(evaluation_id)
    finally:
        db.close()


@router.post("/evaluate", response_model=EvaluationRead, status_code=status.HTTP_202_ACCEPTED)
def evaluate(
    payload: EvaluationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> EvaluationRead:
    service = EvaluationService(db)
    evaluation = service.create(model_id=payload.model_id, dataset_id=payload.dataset_id)
    background_tasks.add_task(_run_evaluation_async, evaluation.id)
    return EvaluationRead.model_validate(evaluation)


@router.get("/evaluations", response_model=list[EvaluationRead])
def list_evaluations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[EvaluationRead]:
    items = EvaluationService(db).list(skip=skip, limit=limit)
    return [EvaluationRead.model_validate(item) for item in items]


@router.get("/results/{id}", response_model=EvaluationRead)
def get_results(id: int, db: Session = Depends(get_db)) -> EvaluationRead:
    item = EvaluationService(db).get(id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found")
    return EvaluationRead.model_validate(item)
