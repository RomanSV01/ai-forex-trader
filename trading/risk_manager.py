import logging

logger = logging.getLogger(__name__)

class RiskManager:
    """Manage trading risks"""
    
    def __init__(self, max_positions, max_daily_loss, risk_percent, 
                 stop_loss_pips, take_profit_pips):
        self.max_positions = max_positions
        self.max_daily_loss = max_daily_loss
        self.risk_percent = risk_percent
        self.stop_loss_pips = stop_loss_pips
        self.take_profit_pips = take_profit_pips
        self.daily_loss = 0
        self.daily_trades = 0
    
    def can_open_position(self, open_positions_count, account_equity):
        """Check if new position can be opened"""
        
        # Check max positions
        if open_positions_count >= self.max_positions:
            logger.warning(f"✗ Max positions reached ({self.max_positions})")
            return False, "Max positions reached"
        
        # Check daily loss limit
        if self.daily_loss >= (account_equity * self.max_daily_loss / 100):
            logger.warning(f"✗ Daily loss limit reached")
            return False, "Daily loss limit reached"
        
        return True, "OK"
    
    def calculate_position_size(self, account_balance, risk_pips, pip_value=10):
        """
        Calculate position size based on risk
        
        Args:
            account_balance: Account balance
            risk_pips: Number of pips for Stop Loss
            pip_value: Value of one pip per lot
        
        Returns:
            float: Position size in lots
        """
        
        # Max risk amount
        max_risk = account_balance * (self.risk_percent / 100)
        
        # Position size calculation
        position_size = max_risk / (risk_pips * pip_value)
        
        return position_size
    
    def get_stop_loss_price(self, entry_price, order_type):
        """
        Get Stop Loss price
        
        Args:
            entry_price: Entry price
            order_type: 'BUY' or 'SELL'
        
        Returns:
            float: Stop Loss price
        """
        # 1 pip = 0.0001 for most pairs (EURUSD)
        pip = 0.0001
        sl_distance = self.stop_loss_pips * pip
        
        if order_type == 'BUY':
            return entry_price - sl_distance
        else:  # SELL
            return entry_price + sl_distance
    
    def get_take_profit_price(self, entry_price, order_type):
        """
        Get Take Profit price
        
        Args:
            entry_price: Entry price
            order_type: 'BUY' or 'SELL'
        
        Returns:
            float: Take Profit price
        """
        pip = 0.0001
        tp_distance = self.take_profit_pips * pip
        
        if order_type == 'BUY':
            return entry_price + tp_distance
        else:  # SELL
            return entry_price - tp_distance
    
    def register_trade_result(self, profit_loss):
        """Register trade result"""
        if profit_loss < 0:
            self.daily_loss += abs(profit_loss)
        self.daily_trades += 1
        logger.info(f"Trade #{self.daily_trades}: P/L = {profit_loss:.2f}")
    
    def reset_daily_stats(self):
        """Reset daily statistics"""
        self.daily_loss = 0
        self.daily_trades = 0
        logger.info("✓ Daily statistics reset")
