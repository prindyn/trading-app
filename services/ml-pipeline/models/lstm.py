import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler


class PriceSequenceDataset(Dataset):
    def __init__(self, df: pd.DataFrame, seq_len=48):
        self.seq_len = seq_len
        self.X, self.y = self.make_sequences(df)

    def make_sequences(self, df):
        df = df.copy()
        df["return_1h"] = df["close"].pct_change()
        df["volatility"] = df["high"] - df["low"]
        df["momentum"] = df["close"] - df["close"].shift(3)

        df["target"] = (df["close"].shift(-3) > df["close"]).astype(int)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)

        features = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "return_1h",
            "volatility",
            "momentum",
        ]
        scaler = StandardScaler()
        df[features] = scaler.fit_transform(df[features])

        feature_array = df[features].values
        target_array = df["target"].values

        Xs, ys = [], []
        for i in range(len(df) - self.seq_len):
            Xs.append(feature_array[i : i + self.seq_len])
            ys.append(target_array[i + self.seq_len - 1])

        return np.array(Xs), np.array(ys)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return torch.tensor(self.X[idx], dtype=torch.float32), torch.tensor(
            self.y[idx], dtype=torch.float32
        )


class LSTMClassifier(nn.Module):
    def __init__(self, input_size=8, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers, batch_first=True, dropout=dropout
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        out = self.fc(hn[-1])
        return out


class LSTMTrainer:
    def __init__(self):
        self.model = LSTMClassifier()

    def train(self, data: pd.DataFrame):
        df = data.copy()
        df.dropna(inplace=True)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)

        dataset = PriceSequenceDataset(df, seq_len=48)

        temp_df = df.copy()
        temp_df["target"] = (temp_df["close"].shift(-3) > temp_df["close"]).astype(int)
        print("Target class distribution:")
        print(temp_df["target"].value_counts(normalize=True).rename("proportion"))

        train_size = int(0.8 * len(dataset))
        train_ds, test_ds = torch.utils.data.random_split(
            dataset, [train_size, len(dataset) - train_size]
        )

        # Limit workers and memory usage
        train_loader = DataLoader(
            train_ds, batch_size=32, shuffle=True, num_workers=0, pin_memory=False
        )
        test_loader = DataLoader(
            test_ds, batch_size=32, num_workers=0, pin_memory=False
        )

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.BCEWithLogitsLoss()

        self.model.train()
        for epoch in range(30):
            total_loss = 0
            for X_batch, y_batch in train_loader:
                optimizer.zero_grad()
                logits = self.model(X_batch).squeeze()
                loss = criterion(logits, y_batch)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            print(f"Epoch {epoch+1}/30, Loss: {total_loss/len(train_loader):.4f}")

        self.test_loader = test_loader

    def score(self):
        self.model.eval()
        preds, targets = [], []
        with torch.no_grad():
            for X_batch, y_batch in self.test_loader:
                logits = self.model(X_batch).squeeze()
                pred = torch.sigmoid(logits).round()
                preds.extend(pred.numpy())
                targets.extend(y_batch.numpy())

        acc = accuracy_score(targets, preds)
        f1 = f1_score(targets, preds)
        cm = confusion_matrix(targets, preds)

        print(f"LSTM Accuracy: {acc:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print("Confusion Matrix:")
        print(cm)

        return acc

    def get_params(self):
        return {
            "type": "lstm",
            "hidden_size": 64,
            "num_layers": 2,
            "dropout": 0.2,
            "seq_len": 48,
        }
