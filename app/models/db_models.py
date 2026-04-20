from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

class ModelStatus(Enum):
    TRAINING = 'training'
    DEPLOYED = 'deployed'
    RETIRED = 'retired'

class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, default=ModelStatus.TRAINING.name)
    datasets = relationship('Dataset', back_populates='model')

class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship('Model', back_populates='datasets')

class Evaluation(Base):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    metrics = Column(String, nullable=False)