import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "artifacts"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
PREDICTOR_MODEL_DIR = BASE_DIR.parent / "ml-predictor" / "app" / "models"
PREDICTOR_MODEL_DIR.mkdir(parents=True, exist_ok=True)
