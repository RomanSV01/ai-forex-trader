class SymbolManager:
    """Manage trading symbols"""
    
    SYMBOLS = {
        "EURUSD": {
            "name": "EUR/USD",
            "min_volume": 0.01,
            "max_volume": 100,
            "leverage": 500,
            "commission": 0.0002
        },
    }
    
    @classmethod
    def add_symbol(cls, symbol_code, config):
        """Add new currency pair"""
        cls.SYMBOLS[symbol_code] = config
    
    @classmethod
    def get_symbol(cls, symbol_code):
        """Get symbol config"""
        return cls.SYMBOLS.get(symbol_code)
    
    @classmethod
    def get_all_symbols(cls):
        """Get all symbols"""
        return list(cls.SYMBOLS.keys())
    
    @classmethod
    def is_valid_symbol(cls, symbol_code):
        """Check if symbol is valid"""
        return symbol_code in cls.SYMBOLS
