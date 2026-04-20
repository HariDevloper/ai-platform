"""
Database models for AI Model Evaluation Platform
Defines all SQLAlchemy ORM models for persistence layer
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ModelFramework(str, enum.Enum):
    """Supported model frameworks"""
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    SKLEARN = "sklearn"
    CUSTOM_API = "custom_api"
    ONNX = "onnx"


class ModelType(str, enum.Enum):
    """Supported model types"""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    NLP = "nlp"
    VISION = "vision"
    CUSTOM = "custom"


class DatasetType(str, enum.Enum):
    """Supported dataset types"""
    TABULAR = "tabular"
    IMAGE = "image"
    TEXT = "text"
    CUSTOM = "custom"


class EvaluationStatus(str, enum.Enum):
    """Evaluation status states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Model(Base):
    """Model registry - stores metadata about uploaded models"""
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    framework = Column(Enum(ModelFramework), nullable=False)
    model_type = Column(Enum(ModelType), nullable=False)
    file_path = Column(String(500), nullable=False, unique=True)
    file_hash = Column(String(64), nullable=True)
    file_size = Column(Integer, nullable=True)
    version = Column(String(50), default="1.0.0")
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="model", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Model(id={{self.id}}, name='{{self.name}}', framework={{self.framework}})>"


class Dataset(Base):
    """Dataset registry - stores metadata about datasets"""
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    dataset_type = Column(Enum(DatasetType), nullable=False)
    file_path = Column(String(500), nullable=False, unique=True)
    file_hash = Column(String(64), nullable=True)
    file_size = Column(Integer, nullable=True)
    num_samples = Column(Integer, nullable=True)
    num_features = Column(Integer, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="dataset", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Dataset(id={{self.id}}, name='{{self.name}}', type={{self.dataset_type}})>"


class Evaluation(Base):
    """Evaluation results - stores evaluation runs and their metrics"""
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False, index=True)
    status = Column(Enum(EvaluationStatus), default=EvaluationStatus.PENDING, index=True)
    
    # Metrics and results
    metrics = Column(JSON, nullable=True)  # Classification/Regression metrics
    trust_score = Column(Float, nullable=True)  # Overall trustworthiness score
    bias_metrics = Column(JSON, nullable=True)  # Bias detection results
    explainability = Column(JSON, nullable=True)  # Feature importance
    robustness_metrics = Column(JSON, nullable=True)  # Robustness test results
    
    # Execution metadata
    execution_time = Column(Float, nullable=True)  # In seconds
    error_message = Column(String(1000), nullable=True)
    result_path = Column(String(500), nullable=True)  # Path to detailed results
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    model = relationship("Model", back_populates="evaluations")
    dataset = relationship("Dataset", back_populates="evaluations")
    
    def __repr__(self) -> str:
        return f"<Evaluation(id={{self.id}}, model_id={{self.model_id}}, status={{self.status}})>"
    
def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "model_id": self.model_id,
            "dataset_id": self.dataset_id,
            "status": self.status.value if self.status else None,
            "metrics": self.metrics,
            "trust_score": self.trust_score,
            "bias_metrics": self.bias_metrics,
            "explainability": self.explainability,
            "robustness_metrics": self.robustness_metrics,
            "execution_time": self.execution_time,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }