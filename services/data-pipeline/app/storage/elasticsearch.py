from .base import BaseStorage


class ElasticsearchStorage(BaseStorage):
    async def save(self, data, metadata=None):
        print("[Elasticsearch] Saving data:", data, metadata)
