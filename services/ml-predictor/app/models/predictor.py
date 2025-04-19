from pathlib import Path
import joblib

try:
    model_path = Path(__file__).resolve().parent / "models" / "latest_model.pkl"
    model = joblib.load(model_path)
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")
