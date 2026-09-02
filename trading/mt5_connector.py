import MetaTrader5 as mt5
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MT5Connector:
    """Connect to MT5 and manage orders"""
    
    def __init__(self, login, server, password):
        self.login = login
        self.server = server
        self.password = password
        self.connected = False
        self.mt5 = mt5
    
    def connect(self):
        """Connect to MT5"""
        if not mt5.initialize(login=self.login,
                             server=self.server,
                             password=self.password):
            logger.error(f"✗ MT5 connection error: {mt5.last_error()}")
            return False
        
        self.connected = True
        logger.info("✓ Connected to MT5")
        return True
    
    def disconnect(self):
        """Disconnect from MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
    
    def get_account_info(self):
        """Get account information"""
        if not self.connected:
            return None
        
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
    
    def send_order(self, symbol, order_type, volume, price=None, 
                   sl=None, tp=None, comment=""):
        """
        Send order to MT5
        
        Args:
            symbol: Currency pair
            order_type: mt5.ORDER_TYPE_BUY or mt5.ORDER_TYPE_SELL
            volume: Position size
            price: Order price (current if None)
            sl: Stop Loss
            tp: Take Profit
            comment: Order comment
        
        Returns:
            dict: Order result
        """
        if not self.connected:
            logger.error("✗ Not connected to MT5")
            return None
        
        try:
            # Get current tick
            tick = mt5.symbol_info_tick(symbol)
            if not tick:
                logger.error(f"✗ Error getting tick for {symbol}")
                return None
            
            # Use current price if not specified
            if price is None:
                price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
            
            # Prepare order
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "deviation": 20,
                "magic": 234000,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Add Stop Loss and Take Profit
            if sl:
                request["sl"] = sl
            if tp:
                request["tp"] = tp
            
            # Send order
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"✓ Order executed: {symbol} {order_type} {volume}L @ {price}")
                return {
                    'success': True,
                    'order_id': result.order,
                    'price': result.price,
                    'volume': result.volume
                }
            else:
                logger.error(f"✗ Order rejected: {result.comment}")
                return {'success': False, 'error': result.comment}
        
        except Exception as e:
            logger.error(f"✗ Order error: {e}")
            return None
    
    def close_position(self, ticket, volume=None):
        """Close position by ticket"""
        if not self.connected:
            return None
        
        # Get position info
        position = mt5.positions_get(ticket=ticket)
        if not position:
            logger.error(f"✗ Position {ticket} not found")
            return None
        
        pos = position[0]
        symbol = pos.symbol
        
        # Opposite order type
        order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        
        # Size
        close_volume = volume if volume else pos.volume
        
        # Current tick
        tick = mt5.symbol_info_tick(symbol)
        price = tick.bid if order_type == mt5.ORDER_TYPE_SELL else tick.ask
        
        # Close order
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": close_volume,
            "type": order_type,
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": f"Close position {ticket}",
            "type_time": mt5.ORDER_TIME_GTC,
        }
        
        result = mt5.order_send(request)
        
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            logger.info(f"✓ Position closed: {ticket}")
            return True
        else:
            logger.error(f"✗ Close error: {result.comment}")
            return False
    
    def get_open_positions(self, symbol=None):
        """Get open positions"""
        if not self.connected:
            return []
        
        positions = mt5.positions_get(symbol=symbol)
        
        if positions:
            return [{
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == mt5.ORDER_TYPE_BUY else 'SELL',
                'volume': pos.volume,
                'price_open': pos.price_open,
                'price_current': pos.price_current,
                'profit': pos.profit,
                'comment': pos.comment
            } for pos in positions]
        
        return []
