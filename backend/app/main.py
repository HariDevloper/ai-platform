from __future__ import annotations

from fastapi import FastAPI

from app.api.routes_datasets import router as datasets_router
from app.api.routes_evaluation import router as evaluation_router
from app.api.routes_models import router as models_router
from app.core.config import settings
from app.core.database import Base, engine


app = FastAPI(title=settings.app_name, version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    settings.ensure_storage_dirs()
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(models_router)
app.include_router(datasets_router)
app.include_router(evaluation_router)
