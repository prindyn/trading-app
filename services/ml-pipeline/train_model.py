import logging
import config
import datetime
from data.loader import load_training_data
from store.model_store import save_model
from model_registry import log_model_entry

logger = logging.getLogger(__name__)


def get_model(name: str, use_random_search: bool = False):
    if name not in config.MODEL_CLASS_REGISTRY:
        logger.error(f"Unknown model type: {name}")
        raise ValueError(f"Unknown model type: {name}")

    param_dist = config.MODEL_PARAM_DISTS.get(name, {})
    if use_random_search and not param_dist:
        logger.warning(f"No param_dist found for model: {name}. Skipping search.")

    model_use_search = bool(use_random_search and param_dist)
    return config.MODEL_CLASS_REGISTRY[name](
        use_random_search=model_use_search, param_dist=param_dist or {}
    )


def get_all_models(use_random_search: bool = False):
    models = {}
    for name, cls in config.MODEL_CLASS_REGISTRY.items():
        if name not in config.MODEL_CLASS_REGISTRY:
            logger.error(f"Unknown model type: {name}")
            continue
        param_dist = config.MODEL_PARAM_DISTS.get(name, {})
        if use_random_search and not param_dist:
            logger.warning(f"No param_dist found for model: {name}. Skipping search.")
        model_use_search = bool(use_random_search and param_dist)
        models[name] = cls(
            use_random_search=model_use_search, param_dist=param_dist or {}
        )
    return models


def train_one_model(
    name: str, version: str | None = None, use_random_search: bool = False
):
    version = version or datetime.datetime.now().strftime("%Y%m%d%H%M")
    data = load_training_data(name)
    instance = get_model(name, use_random_search=use_random_search)
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


def train_all_models(version: str | None = None, use_random_search: bool = False):
    version = version or datetime.datetime.now().strftime("%Y%m%d%H%M")
    results = []

    for name, instance in get_all_models(use_random_search=use_random_search).items():
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
