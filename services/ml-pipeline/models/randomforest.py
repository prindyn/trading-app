import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class RandomForestTrainer:
    def __init__(self):
        self.model = None

    def train(self, data: pd.DataFrame):
        """
        Train the model using a pandas DataFrame with columns:
        ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        """
        # Example feature engineering: use close, volume, price change, etc.
        df = data.copy()
        df["price_change"] = df["close"] - df["open"]
        df["target"] = (df["price_change"] > 0).astype(int)

        features = df[["open", "close", "volume", "price_change"]]
        labels = df["target"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            features, labels, test_size=0.2, random_state=42
        )

        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(self.X_train, self.y_train)

        acc = self.score()
        print(f"RandomForest Accuracy: {acc:.2f}")

    def score(self):
        return accuracy_score(self.y_test, self.model.predict(self.X_test))

    def get_params(self):
        return {"n_estimators": 100}
