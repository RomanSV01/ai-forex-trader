from abc import ABC, abstractmethod
import numpy as np
import logging

logger = logging.getLogger(__name__)

class BaseAIModel(ABC):
    """Base class for all AI models"""
    
    def __init__(self, model_name, lookback_periods=100, min_confidence=0.65):
        self.model_name = model_name
        self.lookback_periods = lookback_periods
        self.min_confidence = min_confidence
        self.model = None
        self.is_trained = False
    
    @abstractmethod
    def train(self, X_train, y_train, validation_split=0.2, epochs=50):
        """Train model"""
        pass
    
    @abstractmethod
    def predict(self, X):
        """Make prediction"""
        pass
    
    @abstractmethod
    def save_model(self, filepath):
        """Save model weights"""
        pass
    
    @abstractmethod
    def load_model(self, filepath):
        """Load model weights"""
        pass
    
    def get_signal_with_confidence(self, prediction):
        """
        Get trading signal with confidence
        
        Args:
            prediction: Model prediction (probability)
        
        Returns:
            dict: {'signal': 'BUY'|'SELL'|'HOLD', 'confidence': float}
        """
        if isinstance(prediction, np.ndarray):
            prob = prediction[0]
        else:
            prob = prediction
        
        confidence = max(prob, 1 - prob)
        
        if confidence < self.min_confidence:
            return {'signal': 'HOLD', 'confidence': confidence}
        
        signal = 'BUY' if prob > 0.5 else 'SELL'
        return {'signal': signal, 'confidence': confidence}
    
    @abstractmethod
    def get_model_info(self):
        """Get model information"""
        pass
