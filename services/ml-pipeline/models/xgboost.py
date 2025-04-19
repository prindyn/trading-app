import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    TimeSeriesSplit,
    RandomizedSearchCV,
)
from sklearn.metrics import accuracy_score
import ta
import json


class XGBoostTrainer:
    def __init__(self, use_random_search=True, custom_params=None, param_dist=None):
        self.model = None
        self.use_random_search = use_random_search
        custom_params = custom_params or {}
        self.model_params = {
            "n_estimators": 100,
            "max_depth": 3,
            "learning_rate": 0.01,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
        }
        self.model_params.update(custom_params)
        self.param_dist = param_dist or {}

    def train(self, data: pd.DataFrame):
        df = data.copy()

        # Define target
        df["future_return"] = (df["close"].shift(-3) - df["close"]) / df["close"]
        df["target"] = (df["future_return"] > 0.002).astype(int)

        # Technical indicators
        df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
        df["ema_10"] = ta.trend.EMAIndicator(df["close"], window=10).ema_indicator()
        df["volatility"] = df["high"] - df["low"]

        # Raw features
        df["returns_1h"] = df["close"].pct_change()
        df["volume_change"] = df["volume"].pct_change()
        df["high_close_diff"] = df["high"] - df["close"]
        df["low_open_diff"] = df["open"] - df["low"]

        # Advanced indicators
        df["macd"] = ta.trend.MACD(df["close"]).macd()
        df["macd_signal"] = ta.trend.MACD(df["close"]).macd_signal()
        df["stoch_rsi"] = ta.momentum.StochRSIIndicator(df["close"]).stochrsi()
        df["obv"] = ta.volume.OnBalanceVolumeIndicator(
            df["close"], df["volume"]
        ).on_balance_volume()
        df["atr"] = ta.volatility.AverageTrueRange(
            df["high"], df["low"], df["close"]
        ).average_true_range()

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)

        print("Target class distribution:")
        print(df["target"].value_counts(normalize=True).rename("proportion"))

        feature_cols = [
            "open",
            "close",
            "volume",
            "rsi",
            "ema_10",
            "volatility",
            "returns_1h",
            "volume_change",
            "high_close_diff",
            "low_open_diff",
            "macd",
            "macd_signal",
            "stoch_rsi",
            "obv",
            "atr",
        ]
        features = df[feature_cols]
        labels = df["target"]

        assert not features.isnull().any().any(), "NaNs still present in features"
        assert np.isfinite(features.values).all(), "Inf still present in features"

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            features, labels, test_size=0.2, random_state=42
        )

        if self.use_random_search and self.param_dist:
            base_model = XGBClassifier(
                use_label_encoder=False, eval_metric="logloss", random_state=42
            )
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
            self.model = XGBClassifier(
                use_label_encoder=False,
                eval_metric="logloss",
                random_state=42,
                **self.model_params,
            )
            self.model.fit(self.X_train, self.y_train)

        acc = self.score()
        print(f"XGBoost Accuracy: {acc:.2f}")

        tscv = TimeSeriesSplit(n_splits=5)
        cv_score = cross_val_score(self.model, features, labels, cv=tscv).mean()
        print(f"TimeSeries CV Accuracy (cv=5): {cv_score:.4f}")

        importance_data = {}
        for feat, imp in zip(self.X_train.columns, self.model.feature_importances_):
            importance_data[feat] = round(float(imp), 4)

        blended_output = {
            "cv_accuracy": round(cv_score, 4),
            "test_accuracy": round(acc, 4),
            "feature_importance": importance_data,
            "params": self.model_params,
        }

        with open("registry/xgboost_summary.json", "w") as f:
            json.dump(blended_output, f, indent=2)

    def score(self):
        return accuracy_score(self.y_test, self.model.predict(self.X_test))

    def get_params(self):
        return self.model_params
