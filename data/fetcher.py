import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DataFetcher:
    """Fetch quotes from MetaTrader 5"""
    
    def __init__(self, login, server, password):
        self.login = login
        self.server = server
        self.password = password
        self.connected = False
    
    def connect(self):
        """Connect to MT5"""
        try:
            if not mt5.initialize(login=self.login, 
                                 server=self.server, 
                                 password=self.password):
                raise Exception(f"MT5 init failed: {mt5.last_error()}")
            self.connected = True
            logger.info("✓ Connected to MetaTrader 5")
            return True
        except Exception as e:
            logger.error(f"✗ Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("✓ Disconnected from MetaTrader 5")
    
    def get_historical_data(self, symbol, timeframe, num_candles):
        """
        Get historical candle data
        
        Args:
            symbol: Currency pair (EURUSD)
            timeframe: Timeframe (H1, M15, M5)
            num_candles: Number of candles to fetch
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Convert timeframe string to MT5 constant
            tf_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1
            }
            
            tf = tf_map.get(timeframe)
            if not tf:
                raise ValueError(f"Unsupported timeframe: {timeframe}")
            
            # Fetch candles
            rates = mt5.copy_rates_from(symbol, tf, datetime.now(), num_candles)
            
            if rates is None:
                raise Exception(f"Error fetching {symbol}: {mt5.last_error()}")
            
            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df = df.set_index('time')
            df = df[['open', 'high', 'low', 'close', 'tick_volume']].copy()
            df.columns = ['open', 'high', 'low', 'close', 'volume']
            
            logger.info(f"✓ Loaded {len(df)} candles {symbol} {timeframe}")
            return df
        
        except Exception as e:
            logger.error(f"✗ Data fetch error: {e}")
            return None
    
    def get_current_tick(self, symbol):
        """Get current tick"""
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                raise Exception(f"Error getting tick for {symbol}")
            return tick
        except Exception as e:
            logger.error(f"✗ Tick error: {e}")
            return None
    
    def get_account_info(self):
        """Get account information"""
        try:
            info = mt5.account_info()
            if info:
                return {
                    'balance': info.balance,
                    'equity': info.equity,
                    'margin': info.margin,
                    'free_margin': info.free_margin,
                    'margin_level': info.margin_level
                }
            return None
        except Exception as e:
            logger.error(f"✗ Account info error: {e}")
            return None
