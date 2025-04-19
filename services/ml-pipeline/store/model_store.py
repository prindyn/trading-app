import joblib
from pathlib import Path
import shutil


def save_model(model, version: str, model_dir, predictor_dir, name: str):
    model_path = Path(model_dir) / f"{name}_{version}.pkl"
    joblib.dump(model, model_path)

    # Also copy to predictor folder
    target_path = Path(predictor_dir) / f"{name}_{version}.pkl"
    shutil.copy(model_path, target_path)

    # Optionally update a symlink to always point to latest
    symlink = Path(predictor_dir) / f"latest_model_{name}.pkl"
    if symlink.exists() or symlink.is_symlink():
        symlink.unlink()
    symlink.symlink_to(target_path.name)

    return model_path, target_path
