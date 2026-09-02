import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class CandleAnalyzer:
    """Analyze candle patterns"""
    
    BULLISH_PATTERNS = ['hammer', 'engulfing_bullish', 'morning_star']
    BEARISH_PATTERNS = ['hanging_man', 'engulfing_bearish', 'evening_star']
    
    @staticmethod
    def analyze_current_candle(df):
        """
        Analyze current (last) candle
        
        Args:
            df: DataFrame with OHLC data
        
        Returns:
            dict: Candle information
        """
        if df.empty:
            return None
        
        latest = df.iloc[-1]
        
        body = latest['close'] - latest['open']
        range_hl = latest['high'] - latest['low']
        
        # Classify candle
        if abs(body) < range_hl * 0.1:  # Doji
            candle_type = 'doji'
        elif body > 0:
            candle_type = 'bullish'
        elif body < 0:
            candle_type = 'bearish'
        else:
            candle_type = 'neutral'
        
        # Wick sizes
        upper_wick = latest['high'] - max(latest['open'], latest['close'])
        lower_wick = min(latest['open'], latest['close']) - latest['low']
        
        return {
            'time': df.index[-1],
            'open': latest['open'],
            'high': latest['high'],
            'low': latest['low'],
            'close': latest['close'],
            'type': candle_type,
            'body_size': abs(body),
            'range': range_hl,
            'upper_wick': upper_wick,
            'lower_wick': lower_wick,
            'volume': latest['volume'],
            'body_to_range_ratio': abs(body) / range_hl if range_hl > 0 else 0
        }
    
    @staticmethod
    def detect_engulfing(df):
        """
        Detect Engulfing pattern
        
        Returns:
            'bullish_engulfing' | 'bearish_engulfing' | None
        """
        if len(df) < 2:
            return None
        
        prev = df.iloc[-2]
        curr = df.iloc[-1]
        
        prev_body = prev['close'] - prev['open']
        curr_body = curr['close'] - curr['open']
        
        # Bullish Engulfing
        if prev_body < 0 and curr_body > 0:
            if curr['open'] < prev['close'] and curr['close'] > prev['open']:
                return 'bullish_engulfing'
        
        # Bearish Engulfing
        if prev_body > 0 and curr_body < 0:
            if curr['open'] > prev['close'] and curr['close'] < prev['open']:
                return 'bearish_engulfing'
        
        return None
    
    @staticmethod
    def detect_hammer(df):
        """
        Detect Hammer pattern
        
        Returns:
            'hammer' | 'hanging_man' | None
        """
        if len(df) < 1:
            return None
        
        candle = df.iloc[-1]
        body = candle['close'] - candle['open']
        lower_wick = min(candle['open'], candle['close']) - candle['low']
        upper_wick = candle['high'] - max(candle['open'], candle['close'])
        range_hl = candle['high'] - candle['low']
        
        # Hammer: small body, long lower wick
        if (lower_wick > 2 * abs(body) and 
            upper_wick < abs(body) and 
            abs(body) < 0.3 * range_hl):
            
            # Hammer (bullish)
            if body > 0:
                return 'hammer'
            # Hanging man (bearish)
            elif body < 0:
                return 'hanging_man'
        
        return None
    
    @staticmethod
    def calculate_support_resistance(df, lookback=50):
        """
        Calculate support and resistance levels
        
        Args:
            df: DataFrame
            lookback: Number of candles to analyze
        
        Returns:
            dict: {'support': float, 'resistance': float}
        """
        recent = df[-lookback:]
        
        support = recent['low'].min()
        resistance = recent['high'].max()
        
        return {
            'support': support,
            'resistance': resistance,
            'range': resistance - support
        }
