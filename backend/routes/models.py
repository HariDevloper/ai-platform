from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from backend.config import ALLOWED_MODEL_EXTENSIONS, MODELS_UPLOAD_DIR
from backend.database import get_db
from backend.models.db_models import Model
from backend.services.model_loader import detect_framework
from backend.utils.exceptions import AppException
from backend.utils.file_handler import save_upload_file
from backend.utils.response import success_response

router = APIRouter(prefix="/api/models", tags=["models"])


@router.post("/upload")
async def upload_model(
    name: str = Form(...),
    framework: str = Form(...),
    model_type: str = Form("custom"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    saved_file = await save_upload_file(file, MODELS_UPLOAD_DIR, ALLOWED_MODEL_EXTENSIONS)
    model = Model(
        name=name,
        path=str(saved_file),
        framework=detect_framework(str(saved_file), framework),
        model_type=model_type,
        size=Path(saved_file).stat().st_size,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return success_response(model, "Model uploaded")


@router.get("")
def list_models(db: Session = Depends(get_db)):
    models = db.query(Model).order_by(Model.created_at.desc()).all()
    return success_response(models, "Models retrieved")


@router.get("/{model_id}")
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise AppException("Model not found", status_code=404)
    return success_response(model, "Model retrieved")


@router.delete("/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise AppException("Model not found", status_code=404)
    path = Path(model.path)
    if path.exists():
        path.unlink()
    db.delete(model)
    db.commit()
    return success_response({}, "Model deleted")
