from .base import BaseStorage


class PostgresStorage(BaseStorage):
    async def save(self, data, metadata=None):
        print("[Postgres] Saving data:", data, metadata)
