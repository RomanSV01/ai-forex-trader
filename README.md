# AI Forex Trader

**Профессиональный AI-трейдер для торговли на Forex через MetaTrader 5 на Python**

## 🎯 Возможности

✅ Интеграция с MetaTrader 5 через Python API  
✅ LSTM нейросеть для предсказания цены  
✅ Анализ технических индикаторов (RSI, MACD, MA)  
✅ Анализ паттернов свечей (Engulfing, Hammer)  
✅ Консенсус-сигналы от AI + технических индикаторов  
✅ Управление рисками (Stop Loss, Take Profit)  
✅ Поддержка нескольких валютных пар  
✅ Полное логирование и бэктестирование  
✅ Модульная архитектура для расширения  

## 📋 Структура проекта

```
ai-forex-trader/
├── config/                    # Конфигурация
│   ├── __init__.py
│   ├── settings.py           # Основные настройки
│   ├── symbols.py            # Управление валютными парами
│   └── module_manager.py     # Менеджер модулей
├── data/                      # Работа с данными
│   ├── __init__.py
│   ├── fetcher.py            # Загрузка котировок с MT5
│   ├── preprocessor.py       # Подготовка данных
│   └── cache/                # Кэш файлов
├── models/                    # AI модели
│   ├── __init__.py
│   ├── base_model.py         # Базовый класс
│   ├── lstm_model.py         # LSTM нейросеть
│   ├── ensemble_model.py     # Комбинированная модель
│   └── checkpoints/          # Сохранённые веса
├── analysis/                  # Анализ рынка
│   ├── __init__.py
│   ├── technical_indicators.py
│   ├── candle_analyzer.py    # Анализ свечей
│   └── trend_predictor.py    # Предсказание тренда
├── trading/                   # Торговля
│   ├── __init__.py
│   ├── mt5_connector.py      # Подключение к MT5
│   ├── order_manager.py      # Управление ордерами
│   ├── risk_manager.py       # Управление рисками
│   └── backtest.py           # Бэктестирование
├── logging/                   # Логирование
│   ├── logger.py
│   └── logs/                 # Файлы логов
├── utils/                     # Утилиты
│   ├── __init__.py
│   ├── helpers.py
│   └── validators.py
├── main.py                    # Главный скрипт торговли
├── train.py                   # Обучение модели
├── requirements.txt           # Зависимости Python
├── .env.example              # Пример переменных окружения
└── .gitignore                # Git ignore
```

## 🚀 Быстрый старт

### 1. Установка

```bash
# Клонировать репозиторий
git clone https://github.com/RomanSV01/ai-forex-trader.git
cd ai-forex-trader

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Активировать (macOS/Linux)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### 2. Конфигурация

```bash
# Создать .env файл
cp .env.example .env

# Отредактировать .env с вашими данными MT5
# Откройте .env и заполните:
# MT5_LOGIN=ваш_логин
# MT5_PASSWORD=ваш_пароль  
# MT5_SERVER=ваш_сервер
```

### 3. Обучение модели

```bash
# Обучить LSTM на исторических данных
python train.py

# Это займет 5-15 минут в зависимости от объема данных
# Модель будет сохранена в models/checkpoints/
```

### 4. Запуск торговли

```bash
# Запустить торговый цикл
python main.py

# Бот начнет анализировать рынок и открывать позиции
# Все действия логируются в logging/logs/trading.log
```

## 📊 Как это работает

### Архитектура системы

```
┌─────────────────────────┐
│  MetaTrader 5 (MT5)     │  ← Терминал с котировками
└────────────┬────────────┘
             │ Python API
             ↓
┌─────────────────────────────────────┐
│  Python Скрипт                      │
│  ├─ DataFetcher: загрузка котировок │
│  ├─ Preprocessor: подготовка данных │
│  ├─ LSTM Model: предсказание цены   │
│  ├─ TrendPredictor: анализ свечей   │
│  ├─ RiskManager: контроль рисков    │
│  └─ MT5Connector: отправка ордеров  │
└──────────────┬──────────────────────┘
               │ Ордера
               ↓
┌─────────────────────────┐
│  MetaTrader 5 (MT5)     │  ← Торговля
└─────────────────────────┘
```

### Процесс принятия решения

1. **Загрузка данных** - 100+ свечей EURUSD
2. **Подготовка** - Добавление технических индикаторов (RSI, MACD, MA)
3. **Нормализация** - Масштабирование данных для ИИ
4. **Предсказание AI** - LSTM предсказывает направление (BUY/SELL)
5. **Анализ индикаторов** - RSI, MACD подтверждают сигнал
6. **Анализ свечей** - Поиск паттернов (Engulfing, Hammer)
7. **Консенсус** - Объединение всех сигналов
8. **Торговля** - Если уверенность > 65%, открывается позиция
9. **Риск-менеджмент** - Автоматический Stop Loss и Take Profit

## ⚙️ Конфигурация

Отредактируйте `config/settings.py`:

```python
# MT5 Настройки
MT5_LOGIN = 1234567
MT5_PASSWORD = "password"
MT5_SERVER = "Alpari-MT5-Demo"

# Торговые параметры
DEFAULT_SYMBOL = "EURUSD"
TIMEFRAME = "H1"      # H1, M15, M5, M1
VOLUME = 0.1          # Размер позиции
RISK_PERCENT = 2      # Риск 2% от депозита

# ИИ параметры
LOOKBACK_PERIODS = 100  # Свечей для анализа
MIN_CONFIDENCE = 0.65   # Минимальная уверенность
UPDATE_FREQUENCY = 3600 # Проверка каждый час

# Управление рисками
STOP_LOSS_PIPS = 50
TAKE_PROFIT_PIPS = 100
MAX_OPEN_POSITIONS = 3
MAX_DAILY_LOSS_PERCENT = 5
```

## 📈 Добавление новых валютных пар

Отредактируйте `config/symbols.py`:

```python
# Добавить новую пару
SymbolManager.add_symbol("GBPUSD", {
    "name": "GBP/USD",
    "min_volume": 0.01,
    "max_volume": 100,
    "leverage": 500,
    "commission": 0.0003
})
```

Потом в `main.py` измените:

```python
TRADING_SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY"]
```

## 🧠 Обучение модели

### Как работает обучение

1. **Загрузка данных** - 5000 исторических свечей
2. **Подготовка признаков** - 14 технических индикаторов
3. **Нормализация** - Масштабирование 0-1
4. **LSTM архитектура**:
   - 3 LSTM слоя (128 → 64 → 32 нейронов)
   - 2 Dense слоя (64 → 32 нейронов)
   - Dropout для регуляризации
5. **Обучение** - 50 эпох с ранней остановкой
6. **Оценка** - Точность на тестовых данных

### Переобучение модели

Модель автоматически переобучается каждые 24 часа.

Отредактируйте в `config/settings.py`:

```python
RETRAIN_INTERVAL = 86400  # Секунд между переобучениями
```

## 📊 Логирование и мониторинг

Все события логируются в `logging/logs/trading.log`:

```
2024-01-15 10:30:45 - INFO - ⏰ 2024-01-15 10:30:00
2024-01-15 10:30:45 - INFO - AI сигнал: BUY (уверенность: 72.34%)
2024-01-15 10:30:45 - INFO - 📊 Консенсус: BUY
2024-01-15 10:30:45 - INFO - 💪 Общая уверенность: 78.50%
2024-01-15 10:30:45 - INFO - Техн. индикаторы: RSI=BULLISH, MACD=BULLISH
2024-01-15 10:30:46 - INFO - ✓ Ордер выполнен #123456
```

## 🔧 Расширение функционала

### Добавление нового индикатора

Эдитируйте `analysis/technical_indicators.py` и добавьте расчет в `data/preprocessor.py`:

```python
# В preprocessor.py добавить
df['stochastic'] = self.calculate_stochastic(df['close'])

# В trend_predictor.py добавить анализ
if 'stochastic' in df.columns:
    signals['stochastic'] = 'BULLISH' if latest['stochastic'] > 50 else 'BEARISH'
```

### Добавление нового AI модели

Создайте файл `models/xgboost_model.py` на основе `base_model.py`:

```python
from .base_model import BaseAIModel
import xgboost as xgb

class XGBoostModel(BaseAIModel):
    def __init__(self):
        super().__init__("XGBoost")
        self.model = xgb.XGBClassifier()
    
    # Реализовать методы: train, predict, save_model, load_model
```

## 🧪 Бэктестирование

Добавляется в будущих версиях. Используйте `trading/backtest.py`

## ⚠️ Важные замечания

⚠️ **Риск**: Торговля на рынке Forex содержит риск потери капитала. Тестируйте на демо-счете!  
⚠️ **Производительность**: Требуется стабильное интернет-соединение.  
⚠️ **Требования**: Python 3.8+, MetaTrader 5 должен быть запущен  
⚠️ **API ключи**: Никогда не коммитьте .env файл!  

## 📞 Поддержка

Если у вас есть вопросы:
1. Проверьте [Issues](https://github.com/RomanSV01/ai-forex-trader/issues)
2. Смотрите логи в `logging/logs/trading.log`
3. Убедитесь что MT5 запущен и подключение работает

## 📄 Лицензия

MIT License

---

**Создано для трейдеров и разработчиков. Используйте ответственно! 🚀**
