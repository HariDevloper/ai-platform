"""
PyTorch model adapter
Handles loading and inference of PyTorch models
"""
from typing import Any, Dict, Union, List
import numpy as np
from pathlib import Path
from app.adapters.base_adapter import BaseModelAdapter, PredictionOutput
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PyTorchAdapter(BaseModelAdapter):
    """Adapter for PyTorch models"""
    
    def __init__(self, model_path: str, device: str = "cpu"):
        super().__init__(model_path)
        self.device = device
        self.torch = None
        self._import_torch()
    
    def _import_torch(self) -> None:
        """Dynamically import torch"""
        try:
            import torch
            self.torch = torch
        except ImportError:
            logger.error("PyTorch not installed. Install with: pip install torch")
            raise
    
    def load_model(self) -> bool:
        """Load PyTorch model from file"""
        try:
            if not Path(self.model_path).exists():
                logger.error(f"Model file not found: {self.model_path}")
                return False
            
            # Load model
            self.model = self.torch.load(self.model_path, map_location=self.device)
            
            # Set to evaluation mode
            if hasattr(self.model, 'eval'):
                self.model.eval()
            
            self.loaded = True
            logger.info(f"PyTorch model loaded successfully: {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading PyTorch model: {str(e)}")
            self.loaded = False
            return False
    
    def predict(self, data: Union[np.ndarray, List]) -> PredictionOutput:
        """
        Make predictions using PyTorch model
        
        Args:
            data: Input data as numpy array or list
        
        Returns:
            PredictionOutput: Standardized predictions
        """
        if not self.loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            # Convert to tensor
            if isinstance(data, list):
                data = np.array(data)
            
            if isinstance(data, np.ndarray):
                tensor = self.torch.from_numpy(data).float().to(self.device)
            else:
                tensor = data.to(self.device)
            
            # Inference
            with self.torch.no_grad():
                outputs = self.model(tensor)
            
            # Convert outputs to numpy
            if hasattr(outputs, 'cpu'):
                predictions = outputs.cpu().numpy()
            else:
                predictions = outputs.numpy() if isinstance(outputs, self.torch.Tensor) else outputs
            
            # Handle different output types
            if len(predictions.shape) > 1 and predictions.shape[1] > 1:
                # Multi-class: compute probabilities via softmax
                probabilities = self._softmax(predictions)
                class_predictions = np.argmax(predictions, axis=1)
                confidence = np.max(probabilities, axis=1)
                
                return PredictionOutput(
                    predictions=class_predictions,
                    probabilities=probabilities,
                    confidence=confidence,
                )
            else:
                # Regression or binary
                return PredictionOutput(
                    predictions=predictions.flatten(),
                    confidence=np.abs(predictions.flatten()),
                )
            
        except Exception as e:
            logger.error(f"Error during PyTorch prediction: {str(e)}")
            raise
    
    @staticmethod
    def _softmax(x: np.ndarray) -> np.ndarray:
        """Compute softmax"""
        e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return e_x / e_x.sum(axis=1, keepdims=True)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        info = super().get_model_info()
        info.update({
            "device": self.device,
            "model_type": "PyTorch",
        })
        
        if self.model:
            info["model_class"] = self.model.__class__.__name__
        
        return info
