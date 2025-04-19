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
    "lstm": "btcusd_1h.csv",
    "randomforest": "btcusd_1h.csv",
    "logistic": "btcusd_1h.csv",
    "xgboost": "btcusd_1h.csv",
}

# Model registry: maps model name to its training class
from models.lstm import LSTMTrainer
from models.randomforest import RandomForestTrainer
from models.logistic import LogisticTrainer
from models.xgboost import XGBoostTrainer

MODEL_CLASS_REGISTRY = {
    # "lstm": LSTMTrainer,
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

# Maps model name to its associated param_dist for RandomizedSearchCV
MODEL_PARAM_DISTS = {
    "xgboost": {
        "n_estimators": [50, 100, 150, 200, 250],
        "max_depth": [3, 4, 5, 6, 8, 10],
        "learning_rate": [0.001, 0.01, 0.05, 0.1, 0.2],
        "subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.6, 0.7, 0.8, 0.9, 1.0],
        "gamma": [0, 0.1, 0.2, 1.0],  # regularization
        "reg_alpha": [0, 0.01, 0.1, 1],  # L1 regularization
        "reg_lambda": [0.1, 0.5, 1.0, 2.0],  # L2 regularization
    },
    "randomforest": {
        "n_estimators": [100, 150, 200, 250, 300],
        "max_depth": [3, 5, 10, 15, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
        "bootstrap": [True, False],
        "criterion": ["gini", "entropy", "log_loss"],
    },
    "logistic": {
        "C": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
        "penalty": ["l1", "l2", "elasticnet"],
        "solver": ["liblinear", "saga"],
        "l1_ratio": [0.0, 0.25, 0.5, 0.75, 1.0],  # only used if penalty='elasticnet'
        "max_iter": [100, 200, 500],
        "fit_intercept": [True, False],
    },
}
