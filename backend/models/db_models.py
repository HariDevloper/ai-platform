from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    path = Column(String(500), nullable=False, unique=True)
    framework = Column(String(100), nullable=False)
    model_type = Column(String(100), nullable=False, default="custom")
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    evaluations = relationship("Evaluation", back_populates="model", cascade="all, delete-orphan")


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    path = Column(String(500), nullable=False, unique=True)
    data_type = Column(String(100), nullable=False)
    size = Column(Integer, nullable=False)
    rows_samples = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    evaluations = relationship("Evaluation", back_populates="dataset", cascade="all, delete-orphan")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False, index=True)
    status = Column(String(50), default="pending", nullable=False, index=True)
    progress = Column(Float, default=0.0, nullable=False)
    metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    model = relationship("Model", back_populates="evaluations")
    dataset = relationship("Dataset", back_populates="evaluations")
    result = relationship("EvaluationResult", back_populates="evaluation", uselist=False, cascade="all, delete-orphan")


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), nullable=False, unique=True, index=True)
    metrics_data = Column(JSON, nullable=True)
    analysis_data = Column(JSON, nullable=True)

    evaluation = relationship("Evaluation", back_populates="result")
