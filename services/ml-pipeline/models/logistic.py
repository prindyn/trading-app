import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class LogisticTrainer:
    def __init__(self):
        self.model = None

    def train(self, data: pd.DataFrame):
        """
        Train Logistic Regression model using a DataFrame with columns:
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

        self.model = LogisticRegression()
        self.model.fit(self.X_train, self.y_train)

        acc = self.score()
        print(f"LogisticRegression Accuracy: {acc:.2f}")

    def score(self):
        return accuracy_score(self.y_test, self.model.predict(self.X_test))

    def get_params(self):
        return {"solver": self.model.solver, "max_iter": self.model.max_iter}
