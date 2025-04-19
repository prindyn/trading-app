import json
import config
from pathlib import Path
from datetime import datetime


def log_model_entry(
    name: str, version: str, accuracy: float, path: str, params: dict = None
):
    entry = {
        "model": name,
        "version": version,
        "accuracy": round(accuracy, 4),
        "path": str(path),
        "timestamp": datetime.utcnow().isoformat(),
        "params": params or {},
    }

    if config.MODEL_REGISTRY_PATH.exists():
        with open(config.MODEL_REGISTRY_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(config.MODEL_REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[registry] logged model: {name}@{version} with accuracy={accuracy}")


def get_best_model_path(name: str) -> Path | None:
    if not config.MODEL_REGISTRY_PATH.exists():
        return None
    with open(config.MODEL_REGISTRY_PATH, "r") as f:
        models = [m for m in json.load(f) if m["model"] == name]
    if not models:
        return None
    best = sorted(models, key=lambda m: m["accuracy"], reverse=True)[0]
    return Path(best["path"])
