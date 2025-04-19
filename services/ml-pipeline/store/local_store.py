def save_model(model, version: str, model_dir):
    import joblib
    from pathlib import Path

    model_path = Path(model_dir) / f"model_{version}.pkl"
    joblib.dump(model, model_path)
    return model_path
