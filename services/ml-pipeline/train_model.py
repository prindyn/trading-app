from models.randomforest import RandomForestTrainer
from models.logistic import LogisticTrainer
from models.xgboost import XGBoostTrainer


def get_model(name: str):
    mapping = {
        "randomforest": RandomForestTrainer,
        "logistic": LogisticTrainer,
        "xgboost": XGBoostTrainer,
    }
    if name not in mapping:
        raise ValueError(f"Unknown model type: {name}")
    return mapping[name]()


def get_all_models():
    return {
        "randomforest": RandomForestTrainer(),
        "logistic": LogisticTrainer(),
        "xgboost": XGBoostTrainer(),
    }
