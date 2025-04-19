import json
import uuid
import logging
import functools
from pathlib import Path
from typing import Union, Callable

logger = logging.getLogger(__name__)


def cache_response_async(path: str = "/app/.cache", name: Union[str, Callable] = ""):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            data = await func(self, *args, **kwargs)

            if getattr(self, "cache", False) and isinstance(data, (list, dict)):
                try:
                    file_name = name(self) if callable(name) else name
                    file_name = file_name or f"{func.__name__}_{uuid.uuid4()}"

                    file_path = Path(path) / f"{file_name}.json"
                    file_path.parent.mkdir(parents=True, exist_ok=True)

                    with file_path.open("w") as f:
                        json.dump(data, f, indent=2)

                    logger.info(
                        f"[{getattr(self, 'name', 'cache')}] Saved cache to {file_path}"
                    )
                except Exception as e:
                    logger.warning(
                        f"[{getattr(self, 'name', 'cache')}] Failed to save cache: {e}"
                    )

            return data

        return wrapper

    return decorator
