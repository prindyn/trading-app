# --- app/storage/local.py ---
import json
import os
import hashlib
from pathlib import Path
from typing import Any, Dict
from app.storage.base import BaseStorage
from app.core.logger import logger


class LocalStorage(BaseStorage):
    def __init__(self):
        self.directory = Path(Path.cwd() / "tmp" / "data").resolve()
        os.makedirs(self.directory, exist_ok=True)

    async def save(self, data: Any, metadata: Dict = None):
        metadata = metadata or {}
        filepath = self._build_filepath(metadata)

        try:
            with open(filepath, "w") as f:
                json.dump({"metadata": metadata, "data": data}, f, indent=2)
            logger.info(f"Saved data to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save data to {filepath}: {str(e)}")
            raise

    async def aggregate_and_save(self, new_data: Any, metadata: Dict):
        filepath = self._get_filepath(metadata)
        existing = []

        # Load old data if file exists
        if os.path.exists(filepath):
            try:
                with open(filepath) as f:
                    existing = json.load(f).get("data", [])
            except Exception as e:
                logger.warning(
                    f"Failed to load existing data from {filepath}: {str(e)}"
                )

        # Use timestamp as unique key to overwrite same timestamps only
        combined = {str(item["timestamp"]): item for item in existing}
        for item in new_data:
            combined[str(item["timestamp"])] = item  # overwrite or insert

        merged = list(combined.values())
        merged.sort(key=lambda x: x["timestamp"])

        await self.save(merged, metadata)

    def _get_filepath(self, metadata: Dict) -> str:
        """
        Public method to compute the file path based on metadata
        without writing the file.
        """
        return self._build_filepath(metadata)

    def _build_filepath(self, metadata: Dict) -> str:
        filename = self._get_filename(metadata)
        return os.path.join(self.directory, filename)

    def _get_filename(self, metadata: Dict) -> str:
        """
        Generate a filename by hashing the metadata key or pipeline name.
        """
        key = metadata.get("key") or metadata.get("pipeline", "unknown")
        hash_digest = hashlib.sha256(key.encode()).hexdigest()[:32]
        return f"{hash_digest}.json"
