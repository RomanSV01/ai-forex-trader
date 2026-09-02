import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
from .base_model import BaseAIModel

class LSTMModel(BaseAIModel):
    """LSTM neural network for price direction prediction"""
    
    def __init__(self, lookback_periods=100, min_confidence=0.65):
        super().__init__("LSTM", lookback_periods, min_confidence)
        self.history = None
    
    def build_model(self, input_shape):
        """Build LSTM architecture"""
        self.model = Sequential([
            # First LSTM layer
            LSTM(128, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            
            # Second LSTM layer
            LSTM(64, return_sequences=True),
            Dropout(0.2),
            
            # Third LSTM layer
            LSTM(32),
            Dropout(0.2),
            
            # Dense layers
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(32, activation='relu'),
            
            # Output layer (probability)
            Dense(1, activation='sigmoid')
        ])
        
        logger.info("✓ LSTM model built")
        return self.model
    
    def train(self, X_train, y_train, validation_split=0.2, epochs=50, batch_size=32):
        """
        Train LSTM model
        
        Args:
            X_train: Training data (samples, timesteps, features)
            y_train: Target values
            validation_split: Validation data fraction
            epochs: Number of epochs
            batch_size: Batch size
        """
        logger.info(f"🎓 Training LSTM model ({len(X_train)} samples)")
        
        # Build model
        self.build_model(input_shape=(X_train.shape[1], X_train.shape[2]))
        
        # Compile
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC()]
        )
        
        # Early stopping
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Train
        self.history = self.model.fit(
            X_train, y_train,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop],
            verbose=1
        )
        
        self.is_trained = True
        logger.info("✓ Training completed")
        
        # Print results
        final_acc = self.history.history['accuracy'][-1]
        val_acc = self.history.history['val_accuracy'][-1]
        logger.info(f"  Train Accuracy: {final_acc:.4f}")
        logger.info(f"  Val Accuracy: {val_acc:.4f}")
    
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X: Input data (1, lookback, features)
        
        Returns:
            np.array: Probability of price increase (0-1)
        """
        if not self.is_trained and self.model is None:
            raise ValueError("Model not trained or loaded")
        
        prediction = self.model.predict(X, verbose=0)
        return prediction
    
    def save_model(self, filepath):
        """Save model"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        self.model.save(str(filepath.with_suffix('.h5')))
        logger.info(f"✓ Model saved: {filepath}")
    
    def load_model(self, filepath):
        """Load model"""
        self.model = tf.keras.models.load_model(filepath)
        self.is_trained = True
        logger.info(f"✓ Model loaded: {filepath}")
    
    def get_model_info(self):
        """Get model information"""
        if self.model is None:
            return {"status": "not_loaded"}
        
        return {
            "name": self.model_name,
            "parameters": self.model.count_params(),
            "lookback": self.lookback_periods,
            "min_confidence": self.min_confidence,
            "trained": self.is_trained,
            "layers": len(self.model.layers)
        }
