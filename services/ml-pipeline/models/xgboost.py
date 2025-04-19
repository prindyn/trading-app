import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class XGBoostTrainer:
    def __init__(self):
        self.model = None

    def train(self, data: pd.DataFrame):
        """
        Train XGBoost model using a DataFrame with columns:
        ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        """
        df = data.copy()
        df["price_change"] = df["close"] - df["open"]
        df["target"] = (df["price_change"] > 0).astype(int)

        features = df[["open", "close", "volume", "price_change"]]
        labels = df["target"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            features, labels, test_size=0.2, random_state=42
        )

        self.model = XGBClassifier(
            use_label_encoder=False,
            eval_metric="logloss",
            n_estimators=100,
        )
        self.model.fit(self.X_train, self.y_train)

        acc = self.score()
        print(f"XGBoost Accuracy: {acc:.2f}")

    def score(self):
        return accuracy_score(self.y_test, self.model.predict(self.X_test))

    def get_params(self):
        return {"n_estimators": 100}
