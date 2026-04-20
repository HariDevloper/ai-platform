from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = BASE_DIR / "uploads"
MODELS_UPLOAD_DIR = UPLOADS_DIR / "models"
DATASETS_UPLOAD_DIR = UPLOADS_DIR / "datasets"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{(STORAGE_DIR / 'database.db').as_posix()}")
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",") if origin.strip()]

ALLOWED_MODEL_EXTENSIONS = {".pt", ".pth", ".onnx", ".h5", ".pkl"}
ALLOWED_DATASET_EXTENSIONS = {".csv", ".txt", ".json", ".jpg", ".jpeg", ".png", ".bmp", ".gif"}

for directory in [STORAGE_DIR, UPLOADS_DIR, MODELS_UPLOAD_DIR, DATASETS_UPLOAD_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
