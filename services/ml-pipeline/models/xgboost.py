from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


class XGBoostTrainer:
    def __init__(self):
        self.model = None

    def train(self):
        X = np.random.rand(1000, 3)
        y = (X[:, 0] + X[:, 1] > 1).astype(int)
        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test,
        ) = train_test_split(X, y, test_size=0.2)
        self.model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        self.model.fit(self.X_train, self.y_train)
        acc = accuracy_score(self.y_test, self.model.predict(self.X_test))
        print(f"XGBoost Accuracy: {acc:.2f}")

    def score(self):
        return accuracy_score(self.y_test, self.model.predict(self.X_test))

    def get_params(self):
        return {"n_estimators": 100}
