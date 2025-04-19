from .base import BaseStorage


class S3Storage(BaseStorage):
    async def save(self, data, metadata=None):
        print("[S3] Saving data:", data, metadata)
