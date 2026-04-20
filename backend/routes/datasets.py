from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from backend.config import ALLOWED_DATASET_EXTENSIONS, DATASETS_UPLOAD_DIR
from backend.database import get_db
from backend.models.db_models import Dataset
from backend.utils.exceptions import AppException
from backend.utils.file_handler import build_dataset_preview, save_upload_file
from backend.utils.response import success_response

router = APIRouter(prefix="/api/datasets", tags=["datasets"])


def _estimate_rows(path: Path, data_type: str) -> int | None:
    if data_type != "tabular" or path.suffix.lower() != ".csv":
        return None
    with path.open("r", encoding="utf-8", errors="ignore") as file:
        return sum(1 for _ in file)


@router.post("/upload")
async def upload_dataset(
    name: str = Form(...),
    dataset_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    saved_file = await save_upload_file(file, DATASETS_UPLOAD_DIR, ALLOWED_DATASET_EXTENSIONS)
    path = Path(saved_file)
    dataset = Dataset(
        name=name,
        path=str(saved_file),
        data_type=dataset_type,
        size=path.stat().st_size,
        rows_samples=_estimate_rows(path, dataset_type),
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return success_response(dataset, "Dataset uploaded")


@router.get("")
def list_datasets(db: Session = Depends(get_db)):
    datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).all()
    return success_response(datasets, "Datasets retrieved")


@router.get("/{dataset_id}")
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise AppException("Dataset not found", status_code=404)
    preview = build_dataset_preview(Path(dataset.path), dataset.data_type)
    return success_response({"dataset": dataset, "preview": preview}, "Dataset retrieved")


@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise AppException("Dataset not found", status_code=404)
    path = Path(dataset.path)
    if path.exists():
        path.unlink()
    db.delete(dataset)
    db.commit()
    return success_response({}, "Dataset deleted")


@router.post("/{dataset_id}/preview")
def preview_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise AppException("Dataset not found", status_code=404)
    preview = build_dataset_preview(Path(dataset.path), dataset.data_type)
    return success_response(preview, "Dataset preview generated")
