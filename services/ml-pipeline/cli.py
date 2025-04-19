import typer
import json
import config
from train_model import train_one_model, train_all_models
from model_registry import get_best_model_path
from data.loader import load_and_save_data

cli = typer.Typer()


@cli.command()
def train(
    model: str = typer.Option("logistic", help="Model type"),
    version: str = None,
    random_search: bool = typer.Option(
        False, "--random-search", help="Enable RandomizedSearchCV"
    ),
):
    result = train_one_model(model, version, use_random_search=random_search)
    print(f"[{result['name']}] Model saved to: {result['local_path']}")
    print(f"[{result['name']}] Copied to predictor: {result['predictor_path']}")
    print(f"[{result['name']}] Symlinked as latest_model_{result['name']}.pkl")
    print(f"[{result['name']}] Accuracy: {result['accuracy']:.4f}")


@cli.command()
def train_all(
    random_search: bool = typer.Option(
        False, "--random-search", help="Enable RandomizedSearchCV"
    )
):
    results = train_all_models(use_random_search=random_search)
    for r in results:
        print(f"[{r['name']}] Model saved to: {r['local_path']}")
        print(f"[{r['name']}] Copied to predictor: {r['predictor_path']}")
        print(f"[{r['name']}] Symlinked as latest_model_{r['name']}.pkl")
        print(f"[{r['name']}] Accuracy: {r['accuracy']:.4f}")


@cli.command()
def list_registry():
    if not config.MODEL_REGISTRY_PATH.exists():
        print("No models registered yet.")
        return
    with open(config.MODEL_REGISTRY_PATH, "r") as f:
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


@cli.command()
def fetch_data(
    source="yfinance", symbol="BTC-USD", interval="1h", start="2023-01-01", end=None
):
    load_and_save_data(
        source=source, symbol=symbol, interval=interval, start=start, end=end
    )


if __name__ == "__main__":
    cli()
