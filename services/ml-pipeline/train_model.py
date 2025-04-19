import config
import datetime
from data.loader import load_training_data
from store.model_store import save_model
from registry.model_registry import log_model_entry


def get_model(name: str):
    try:
        return config.MODEL_CLASS_REGISTRY[name]()
    except KeyError:
        raise ValueError(f"Unknown model type: {name}")


def get_all_models():
    return {name: cls() for name, cls in config.MODEL_CLASS_REGISTRY.items()}


def train_one_model(name: str, version: str | None = None):
    version = version or datetime.datetime.now().strftime("%Y%m%d%H%M")
    data = load_training_data(name)
    instance = get_model(name)
    instance.train(data)
    accuracy = instance.score()
    local_path, predictor_path = save_model(
        instance.model,
        version,
        config.MODEL_OUTPUT_DIR,
        config.PREDICTOR_MODEL_DIR,
        name=name,
    )
    log_model_entry(name, version, accuracy, predictor_path, instance.get_params())
    return {
        "name": name,
        "version": version,
        "accuracy": accuracy,
        "local_path": local_path,
        "predictor_path": predictor_path,
    }


def train_all_models(version: str | None = None):
    version = version or datetime.datetime.now().strftime("%Y%m%d%H%M")
    results = []
    for name, instance in get_all_models().items():
        data = load_training_data(name)
        instance.train(data)
        accuracy = instance.score()
        local_path, predictor_path = save_model(
            instance.model,
            version,
            config.MODEL_OUTPUT_DIR,
            config.PREDICTOR_MODEL_DIR,
            name=name,
        )
        log_model_entry(name, version, accuracy, predictor_path, instance.get_params())
        results.append(
            {
                "name": name,
                "version": version,
                "accuracy": accuracy,
                "local_path": local_path,
                "predictor_path": predictor_path,
            }
        )
    return results
