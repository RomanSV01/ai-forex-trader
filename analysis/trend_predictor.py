import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TrendPredictor:
    """Predict trend based on candle analysis and AI"""
    
    def __init__(self, ai_model):
        self.ai_model = ai_model
    
    def predict_trend(self, df, X_normalized):
        """
        Combined trend analysis
        
        Args:
            df: DataFrame with data
            X_normalized: Normalized data for AI
        
        Returns:
            dict: Full analysis with signals
        """
        
        # 1. AI prediction
        ai_prediction = self.ai_model.predict(X_normalized)
        ai_signal = self.ai_model.get_signal_with_confidence(ai_prediction)
        
        # 2. Technical indicators analysis
        technical_signals = self._analyze_technical_indicators(df)
        
        # 3. Candle analysis
        candle_signals = self._analyze_candles(df)
        
        # 4. Consensus signal
        consensus_signal = self._get_consensus_signal(
            ai_signal, 
            technical_signals, 
            candle_signals
        )
        
        return {
            'timestamp': df.index[-1],
            'ai_signal': ai_signal,
            'ai_prediction': float(ai_prediction[0]),
            'technical_signals': technical_signals,
            'candle_signals': candle_signals,
            'consensus': consensus_signal,
            'confidence_score': self._calculate_confidence(
                ai_signal, technical_signals, candle_signals
            )
        }
    
    @staticmethod
    def _analyze_technical_indicators(df):
        """Analyze technical indicators"""
        latest = df.iloc[-1]
        
        signals = {
            'rsi': 'NEUTRAL',
            'macd': 'NEUTRAL',
            'ma_cross': 'NEUTRAL',
        }
        
        # RSI analysis
        if 'rsi' in df.columns:
            rsi = latest['rsi']
            if rsi > 70:
                signals['rsi'] = 'OVERBOUGHT'
            elif rsi < 30:
                signals['rsi'] = 'OVERSOLD'
            elif rsi > 50:
                signals['rsi'] = 'BULLISH'
            else:
                signals['rsi'] = 'BEARISH'
        
        # MACD analysis
        if 'macd' in df.columns and 'signal' in df.columns:
            if latest['macd'] > latest['signal']:
                signals['macd'] = 'BULLISH'
            else:
                signals['macd'] = 'BEARISH'
        
        # Moving average cross
        if 'ma_5' in df.columns and 'ma_20' in df.columns:
            if latest['ma_5'] > latest['ma_20']:
                signals['ma_cross'] = 'BULLISH'
            else:
                signals['ma_cross'] = 'BEARISH'
        
        return signals
    
    @staticmethod
    def _analyze_candles(df):
        """Analyze candle patterns"""
        from .candle_analyzer import CandleAnalyzer
        
        analyzer = CandleAnalyzer()
        
        current_candle = analyzer.analyze_current_candle(df)
        engulfing = analyzer.detect_engulfing(df)
        hammer = analyzer.detect_hammer(df)
        sr_levels = analyzer.calculate_support_resistance(df)
        
        return {
            'current_candle': current_candle,
            'engulfing_pattern': engulfing,
            'hammer_pattern': hammer,
            'support_resistance': sr_levels
        }
    
    @staticmethod
    def _get_consensus_signal(ai_signal, technical_signals, candle_signals):
        """Get consensus signal from all analyses"""
        votes = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
        
        # AI vote
        if ai_signal['signal'] != 'HOLD':
            votes[ai_signal['signal']] += 2
        
        # Technical indicators votes
        for indicator, signal in technical_signals.items():
            if signal == 'BULLISH':
                votes['BUY'] += 1
            elif signal == 'BEARISH':
                votes['SELL'] += 1
            elif signal == 'OVERBOUGHT':
                votes['SELL'] += 1
            elif signal == 'OVERSOLD':
                votes['BUY'] += 1
        
        # Candle pattern votes
        if candle_signals['engulfing_pattern'] == 'bullish_engulfing':
            votes['BUY'] += 1
        elif candle_signals['engulfing_pattern'] == 'bearish_engulfing':
            votes['SELL'] += 1
        
        if candle_signals['hammer_pattern'] == 'hammer':
            votes['BUY'] += 1
        elif candle_signals['hammer_pattern'] == 'hanging_man':
            votes['SELL'] += 1
        
        # Determine final signal
        if votes['BUY'] > votes['SELL']:
            return 'BUY'
        elif votes['SELL'] > votes['BUY']:
            return 'SELL'
        else:
            return 'HOLD'
    
    @staticmethod
    def _calculate_confidence(ai_signal, technical_signals, candle_signals):
        """Calculate overall confidence level"""
        confidence = ai_signal['confidence']
        
        # Bonus if patterns align
        if candle_signals['engulfing_pattern'] is not None:
            confidence += 0.1
        
        if candle_signals['hammer_pattern'] is not None:
            confidence += 0.1
        
        return min(confidence, 1.0)
