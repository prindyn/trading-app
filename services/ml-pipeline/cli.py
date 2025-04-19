import typer
import datetime
import json
from train_model import get_model, get_all_models
from store.model_store import save_model
from registry.model_registry import log_model_entry, get_best_model_path
from registry.model_registry import REGISTRY_PATH
import config

cli = typer.Typer()


@cli.command()
def train(
    model: str = typer.Option("randomforest", help="Model type"),
    version: str = datetime.datetime.now().strftime("%Y%m%d%H%M"),
):
    model_instance = get_model(model)
    model_instance.train()
    accuracy = model_instance.score()
    local_path, predictor_path = save_model(
        model_instance.model,
        version,
        config.MODEL_DIR,
        config.PREDICTOR_MODEL_DIR,
        name=model,
    )
    log_model_entry(
        model, version, accuracy, predictor_path, model_instance.get_params()
    )
    print(f"Model saved to: {local_path}")
    print(f"Copied to predictor service: {predictor_path}")
    print(f"Symlinked as latest_model_{model}.pkl")
    print(f"Accuracy: {accuracy:.4f}")


@cli.command()
def train_all():
    version = datetime.datetime.now().strftime("%Y%m%d%H%M")
    models = get_all_models()
    for name, instance in models.items():
        instance.train()
        accuracy = instance.score()
        local_path, predictor_path = save_model(
            instance.model,
            version,
            config.MODEL_DIR,
            config.PREDICTOR_MODEL_DIR,
            name=name,
        )
        log_model_entry(name, version, accuracy, predictor_path, instance.get_params())
        print(f"[{name}] Model saved to: {local_path}")
        print(f"[{name}] Copied to predictor: {predictor_path}")
        print(f"[{name}] Symlinked as latest_model_{name}.pkl")
        print(f"[{name}] Accuracy: {accuracy:.4f}")


@cli.command()
def list_registry():
    if not REGISTRY_PATH.exists():
        print("No models registered yet.")
        return
    with open(REGISTRY_PATH, "r") as f:
        data = json.load(f)
    print(f"\n  Registered Models ({len(data)} total):\n")
    for entry in sorted(data, key=lambda e: e["timestamp"], reverse=True):
        print(f"  {entry['model']}@{entry['version']}")
        print(f"    • Accuracy:  {entry['accuracy']}")
        print(f"    • Path:      {entry['path']}")
        print(f"    • Timestamp: {entry['timestamp']}")
        if entry.get("params"):
            print(f"    • Params:    {entry['params']}")
        print()


@cli.command()
def best_path(model: str):
    best = get_best_model_path(model)
    if best:
        print(f"Best model for '{model}': {best}")
    else:
        print(f"No models found for '{model}'")


if __name__ == "__main__":
    cli()
