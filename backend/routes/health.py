from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.utils.response import success_response

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return success_response({"status": "healthy", "timestamp": datetime.utcnow()}, "Health check successful")


@router.get("/status")
def system_status(db: Session = Depends(get_db)):
    return success_response(
        {
            "api": "online",
            "database": "connected",
            "time": datetime.utcnow(),
        },
        "System status retrieved",
    )
