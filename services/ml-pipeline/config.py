from pathlib import Path

# ========== Directory Configuration ==========

# Root project path
BASE_DIR = Path(__file__).resolve().parent

# Where trained models are saved
MODEL_OUTPUT_DIR = BASE_DIR / "artifacts"
MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Directory used by predictor service to load models
PREDICTOR_MODEL_DIR = BASE_DIR.parent / "ml-predictor" / "app" / "models"
PREDICTOR_MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Directory containing input CSV training datasets
TRAINING_DATA_DIR = BASE_DIR / "data" / "source"

# File path for model registry (metadata log)
MODEL_REGISTRY_PATH = (
    BASE_DIR.parent / "ml-pipeline" / "registry" / "model_registry.json"
)

# ========== Model Configuration ==========

# Maps model name to its associated data file
MODEL_DATA_FILES = {
    "randomforest": "btcusd_1h.csv",
    "logistic": "btcusd_1h.csv",
    "xgboost": "btcusd_1h.csv",
}

# Model registry: maps model name to its training class
from models.randomforest import RandomForestTrainer
from models.logistic import LogisticTrainer
from models.xgboost import XGBoostTrainer

MODEL_CLASS_REGISTRY = {
    "randomforest": RandomForestTrainer,
    "logistic": LogisticTrainer,
    "xgboost": XGBoostTrainer,
}

# ========== Data Source Fetcher Configuration ==========

from data.binance_fetcher import prepare_fetch_args as bn_args, fetch_bn_ohlcv
from data.yfinance_fetcher import prepare_fetch_args as yf_args, fetch_yf_ohlcv
from data.coingecko_fetcher import prepare_fetch_args as cg_args, fetch_cg_ohlcv

DATA_SOURCE_FETCHERS = {
    "binance": (bn_args, fetch_bn_ohlcv),
    "yfinance": (yf_args, fetch_yf_ohlcv),
    "coingecko": (cg_args, fetch_cg_ohlcv),
}
