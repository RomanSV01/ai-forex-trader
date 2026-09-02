import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Prepare data for AI model"""
    
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaler_fitted = False
    
    def add_technical_features(self, df):
        """
        Add technical indicators
        
        Returns:
            DataFrame with additional features
        """
        df = df.copy()
        
        # Returns (% change)
        df['returns'] = df['close'].pct_change()
        
        # Moving averages
        df['ma_5'] = df['close'].rolling(5).mean()
        df['ma_20'] = df['close'].rolling(20).mean()
        df['ma_50'] = df['close'].rolling(50).mean()
        
        # Exponential moving averages
        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()
        
        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['signal']
        
        # Volatility
        df['volatility'] = df['returns'].rolling(20).std()
        
        # RSI
        df['rsi'] = self.calculate_rsi(df['close'])
        
        # ATR
        df['atr'] = self.calculate_atr(df)
        
        # High/Low ratio
        df['hl_ratio'] = (df['high'] - df['low']) / df['close']
        
        # Volume change
        df['volume_change'] = df['volume'].pct_change()
        
        # Target variable: direction of next candle
        # 1 = up, 0 = down
        df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
        
        return df.dropna()
    
    @staticmethod
    def calculate_rsi(prices, period=14):
        """Calculate RSI (Relative Strength Index)"""
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100. / (1. + rs)
        
        for i in range(period, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
            
            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            
            rs = up / down
            rsi[i] = 100. - 100. / (1. + rs)
        
        return rsi
    
    @staticmethod
    def calculate_atr(df, period=14):
        """Calculate ATR (Average True Range)"""
        df = df.copy()
        df['tr1'] = df['high'] - df['low']
        df['tr2'] = abs(df['high'] - df['close'].shift())
        df['tr3'] = abs(df['low'] - df['close'].shift())
        df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
        df['atr'] = df['tr'].rolling(period).mean()
        return df['atr']
    
    def normalize_data(self, X, fit=False):
        """
        Normalize features (0-1)
        
        Args:
            X: Feature matrix
            fit: If True, fit scaler on data
        """
        if fit:
            self.scaler.fit(X)
            self.scaler_fitted = True
        
        if not self.scaler_fitted:
            raise ValueError("Scaler not fitted. Call with fit=True first")
        
        return self.scaler.transform(X)
    
    def create_sequences(self, data, lookback=50):
        """
        Create sequences for LSTM
        
        Args:
            data: Normalized data
            lookback: Number of periods per window
        
        Returns:
            (X, y) - input and target sequences
        """
        X, y = [], []
        
        for i in range(len(data) - lookback):
            X.append(data[i:i+lookback])
            # Target is direction on next candle
            y.append(data[i+lookback, -1])
        
        return np.array(X), np.array(y)
