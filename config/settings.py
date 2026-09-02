import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "cache"
MODELS_DIR = BASE_DIR / "models" / "checkpoints"
LOGS_DIR = BASE_DIR / "logging" / "logs"

# Create directories if not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# MT5 Settings
MT5_LOGIN = int(os.getenv("MT5_LOGIN", "1234567"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "password")
MT5_SERVER = os.getenv("MT5_SERVER", "Alpari-MT5-Demo")

# Trading Parameters
DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "EURUSD")
TIMEFRAME = os.getenv("TIMEFRAME", "H1")
VOLUME = float(os.getenv("VOLUME", "0.1"))
RISK_PERCENT = float(os.getenv("RISK_PERCENT", "2"))

# AI Parameters
AI_MODEL_TYPE = "LSTM"
LOOKBACK_PERIODS = int(os.getenv("LOOKBACK_PERIODS", "100"))
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.65"))
UPDATE_FREQUENCY = int(os.getenv("UPDATE_FREQUENCY", "3600"))

# Model Management
RETRAIN_INTERVAL = int(os.getenv("RETRAIN_INTERVAL", "86400"))
MIN_TRAINING_SAMPLES = int(os.getenv("MIN_TRAINING_SAMPLES", "1000"))

# Risk Management
STOP_LOSS_PIPS = int(os.getenv("STOP_LOSS_PIPS", "50"))
TAKE_PROFIT_PIPS = int(os.getenv("TAKE_PROFIT_PIPS", "100"))
MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", "3"))
MAX_DAILY_LOSS_PERCENT = float(os.getenv("MAX_DAILY_LOSS_PERCENT", "5"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "trading.log"
