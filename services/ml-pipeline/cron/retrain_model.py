# retrain.py
import subprocess
import datetime
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

MODEL_NAMES = ["xgboost", "randomforest", "logistic"]
DATA_PATH = Path("ml-pipeline/data/source")


def fetch_latest_data():
    # Pull last year of hourly data for BTC-USD from yfinance
    subprocess.run(
        [
            "python",
            "cli.py",
            "fetch-data",
            "--source=yfinance",
            "--symbol=BTC-USD",
            "--interval=1h",
            "--start=2023-01-01",
        ],
        check=True,
    )


def train_models():
    for model in MODEL_NAMES:
        logger.info(f"Training {model} with random search...")
        subprocess.run(
            ["python", "cli.py", "train", f"--model={model}", "--random-search"],
            check=True,
        )


def copy_best_to_predictor():
    predictor_path = Path("services/ml-predictor/app/models")
    artifact_path = Path("services/ml-pipeline/artifacts")

    for model in MODEL_NAMES:
        # Copy the symlinked latest model version
        latest_symlink = predictor_path / f"latest_model_{model}.pkl"
        if latest_symlink.exists():
            logger.info(f"Latest {model} model already deployed: {latest_symlink}")
            continue

        # Find latest artifact and deploy it
        versions = list(artifact_path.glob(f"{model}_*.pkl"))
        if not versions:
            logger.warning(f"No trained versions found for {model}")
            continue

        latest = sorted(versions)[-1]
        deployed_path = predictor_path / latest.name
        shutil.copy(latest, deployed_path)

        symlink = predictor_path / f"latest_model_{model}.pkl"
        if symlink.exists() or symlink.is_symlink():
            symlink.unlink()
        symlink.symlink_to(deployed_path.name)
        logger.info(f"Deployed {model} model: {deployed_path}")


def main():
    fetch_latest_data()
    train_models()
    copy_best_to_predictor()


if __name__ == "__main__":
    main()
