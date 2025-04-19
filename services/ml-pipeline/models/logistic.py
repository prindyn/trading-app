import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    train_test_split,
    TimeSeriesSplit,
    RandomizedSearchCV,
    cross_val_score,
)
from sklearn.metrics import accuracy_score
import ta
import json
import numpy as np


class LogisticTrainer:
    def __init__(self, use_random_search=False, custom_params=None, param_dist=None):
        self.model = None
        self.use_random_search = use_random_search
        custom_params = custom_params or {}
        self.model_params = {
            "C": 1.0,
            "penalty": "l2",
            "solver": "lbfgs",
            "random_state": 42,
        }
        self.model_params.update(custom_params)
        self.param_dist = param_dist or {}

    def train(self, data: pd.DataFrame):
        df = data.copy()

        # Define target
        df["future_return"] = (df["close"].shift(-3) - df["close"]) / df["close"]
        df["target"] = (df["future_return"] > 0.002).astype(int)

        # Add technical indicators
        df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
        df["ema_10"] = ta.trend.EMAIndicator(df["close"], window=10).ema_indicator()
        df["volatility"] = df["high"] - df["low"]

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df = df.dropna()

        features = df[["open", "close", "volume", "rsi", "ema_10", "volatility"]]
        labels = df["target"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            features, labels, test_size=0.2, random_state=42
        )

        if self.use_random_search and self.param_dist:
            base_model = LogisticRegression()
            search = RandomizedSearchCV(
                base_model,
                param_distributions=self.param_dist,
                n_iter=10,
                scoring="accuracy",
                cv=TimeSeriesSplit(n_splits=3),
                random_state=42,
                n_jobs=-1,
            )
            search.fit(self.X_train, self.y_train)
            self.model = search.best_estimator_
            self.model_params = search.best_params_
        else:
            self.model = LogisticRegression(**self.model_params)
            self.model.fit(self.X_train, self.y_train)

        acc = self.score()
        print(f"LogisticRegression Accuracy: {acc:.2f}")

        tscv = TimeSeriesSplit(n_splits=5)
        cv_score = cross_val_score(self.model, features, labels, cv=tscv).mean()
        print(f"TimeSeries CV Accuracy (cv=5): {cv_score:.4f}")

        importance_data = {}
        for feat, imp in zip(self.X_train.columns, self.model.coef_[0]):
            importance_data[feat] = round(float(imp), 4)

        blended_output = {
            "cv_accuracy": round(cv_score, 4),
            "test_accuracy": round(acc, 4),
            "feature_weights": importance_data,
            "params": self.model_params,
        }

        with open("registry/logistic_summary.json", "w") as f:
            json.dump(blended_output, f, indent=2)

    def score(self):
        return accuracy_score(self.y_test, self.model.predict(self.X_test))

    def get_params(self):
        return self.model_params
